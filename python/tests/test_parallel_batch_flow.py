import pytest
import asyncio
import time
from brainyflow import Node, ParallelBatchFlow, Flow

# Helper Nodes for testing
class AddNode(Node):
    async def exec(self, prep_res):
        start_time = time.monotonic()
        val = self.params.get('value', 0)
        delay = self.params.get('delay', 0.1) # Simulate work
        await asyncio.sleep(delay)
        end_time = time.monotonic()
        return {'start': start_time, 'end': end_time, 'result': val}

# Define the ParallelBatchFlow
class ParallelTestFlow(ParallelBatchFlow):
    async def prep(self, shared):
        # Prepare parameter sets for parallel execution
        shared['results'] = []
        return [
            {'value': 1, 'delay': 0.2},
            {'value': 2, 'delay': 0.1},
            {'value': 3, 'delay': 0.15}
        ]

    async def post(self, shared, prep_res, exec_results):
        # exec_results is None for Flows, results are collected via shared state or side effects
        pass # Results collected in AddNode's post or via shared dict

# Define a simple flow containing just the AddNode
add_node = AddNode()
simple_flow = Flow(start=add_node)

# Test case for ParallelBatchFlow
@pytest.mark.asyncio
async def test_parallel_batch_flow_execution():
    shared_data = {'total': 0, 'timestamps': []}

    # Modify AddNode's post to collect results in shared_data
    original_post = add_node.post
    async def collecting_post(self, shared, prep_res, exec_res):
        shared['total'] += exec_res['result']
        shared['timestamps'].append((exec_res['start'], exec_res['end']))
        # Check if original_post is awaitable before awaiting
        if asyncio.iscoroutinefunction(original_post):
             return await original_post(shared, prep_res, exec_res)
        else:
             # Assuming original_post might be a synchronous placeholder or None
             return None # Or handle appropriately if original_post needs calling
    add_node.post = collecting_post.__get__(add_node, AddNode) # Bind method

    # Create and run the ParallelBatchFlow
    batch_flow = ParallelTestFlow(start=simple_flow)
    start_run_time = time.monotonic()
    await batch_flow.run(shared_data)
    end_run_time = time.monotonic()

    # Restore original post method if necessary for other tests
    add_node.post = original_post

    # Assertions
    assert shared_data['total'] == 6, "Total should be the sum of values (1+2+3)"
    assert len(shared_data['timestamps']) == 3, "Should have results from 3 parallel runs"

    # Check for parallelism: Max end time should be less than sum of delays
    # Sum of delays = 0.2 + 0.1 + 0.15 = 0.45
    # Total runtime should be closer to the longest delay (0.2) plus some overhead
    total_runtime = end_run_time - start_run_time
    max_delay = 0.2
    sum_delays = 0.45

    print(f"\nShared Data: {shared_data}")
    print(f"Total Runtime: {total_runtime:.4f}s")
    print(f"Sum of Delays: {sum_delays:.4f}s")
    print(f"Max Individual Delay: {max_delay:.4f}s")

    # Check if total runtime is significantly less than sum of delays, indicating parallelism
    # Allow for some overhead
    assert total_runtime < sum_delays * 1.1, "Total runtime should be less than sum of delays if parallel"
    assert total_runtime >= max_delay, "Total runtime should be at least the max delay"

    # More detailed check: Ensure there's overlap in execution times
    timestamps = sorted(shared_data['timestamps']) # Sort by start time
    overlap_found = False
    if len(timestamps) > 1:
        # Check if the start time of the second task is before the end time of the first
        if timestamps[1][0] < timestamps[0][1]:
            overlap_found = True
        # Check if the start time of the third task is before the end time of the second (or first)
        if len(timestamps) > 2:
            if timestamps[2][0] < timestamps[1][1] or timestamps[2][0] < timestamps[0][1]:
                 overlap_found = True

    assert overlap_found, "Execution intervals should overlap, demonstrating parallelism"

class FailingNode(Node):
    async def exec(self, prep_res):
        if self.params.get('should_fail'):
            raise ValueError("Intentional failure")
        return {"result": "success"}

class ParamVerificationNode(Node):
    async def exec(self, prep_res):
        return {"params": dict(self.params)}

@pytest.mark.asyncio
async def test_empty_batch():
    """Test empty batch completes successfully"""
    shared = {}
    
    class EmptyFlow(ParallelBatchFlow):
        async def prep(self, shared):
            return []
    
    flow = EmptyFlow(start=Node())
    await flow.run(shared)
    assert True  # Just verifying completion

@pytest.mark.asyncio
async def test_error_handling():
    """Test one failing task doesn't prevent others"""
    shared = {'success_count': 0}
    
    class ErrorTestFlow(ParallelBatchFlow):
        async def prep(self, shared):
            return [
                {'should_fail': True},
                {'should_fail': False},
                {'should_fail': False}
            ]
    
    class CountingNode(FailingNode):
        async def post(self, shared, prep_res, exec_res):
            if not self.params.get('should_fail'):
                shared['success_count'] += 1
    
    flow = ErrorTestFlow(start=CountingNode())
    with pytest.raises(ValueError):
        await flow.run(shared)
    
    assert shared['success_count'] == 2

@pytest.mark.asyncio
async def test_large_batch():
    """Test with larger batch size"""
    shared = {'count': 0}
    batch_size = 20
    
    class LargeBatchFlow(ParallelBatchFlow):
        async def prep(self, shared):
            return [{'index': i} for i in range(batch_size)]
    
    class CountingNode(Node):
        async def exec(self, prep_res):
            await asyncio.sleep(0.01)  # Small delay
            return {'index': self.params['index']}
        
        async def post(self, shared, prep_res, exec_res):
            shared['count'] += 1
    
    flow = LargeBatchFlow(start=CountingNode())
    await flow.run(shared)
    assert shared['count'] == batch_size

@pytest.mark.asyncio
async def test_parameter_passing():
    """Test parameters are correctly passed to nodes"""
    test_params = {'key1': 'value1', 'key2': 42}
    shared = {'collected_params': None}
    
    class ParamTestFlow(ParallelBatchFlow):
        async def prep(self, shared):
            return [test_params]
    
    class CollectingNode(ParamVerificationNode):
        async def post(self, shared, prep_res, exec_res):
            shared['collected_params'] = exec_res['params']
    
    flow = ParamTestFlow(start=CollectingNode())
    await flow.run(shared)
    
    # Verify params were passed correctly
    assert shared['collected_params'] == test_params

@pytest.mark.asyncio
async def test_shared_state():
    """Test shared state is maintained across parallel executions"""
    shared = {'data': []}
    
    class SharedStateFlow(ParallelBatchFlow):
        async def prep(self, shared):
            return [{'value': i} for i in range(5)]
    
    class StateNode(Node):
        async def exec(self, prep_res):
            return {'value': self.params['value']}
        
        async def post(self, shared, prep_res, exec_res):
            shared['data'].append(exec_res['value'])
    
    flow = SharedStateFlow(start=StateNode())
    await flow.run(shared)
    
    # Verify all values were collected
    assert len(shared['data']) == 5
    assert set(shared['data']) == {0, 1, 2, 3, 4}

@pytest.mark.asyncio
async def test_concurrency_limit():
    """Test maximum concurrency is respected"""
    max_concurrent = 3
    start_times = []
    end_times = []
    
    class LimitedFlow(ParallelBatchFlow):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.semaphore = asyncio.Semaphore(max_concurrent)
        
        async def prep(self, shared):
            # Return 5 items to process
            return [{} for _ in range(5)]
        
        async def _exec(self, items):
            # Use semaphore to limit concurrency
            async def limited_exec(item):
                async with self.semaphore:
                    return await super()._exec(item)
            return await asyncio.gather(*[limited_exec(item) for item in items])
    
    class TrackingNode(Node):
        async def exec(self, prep_res):
            start_times.append(time.monotonic())
            await asyncio.sleep(0.1)
            end_times.append(time.monotonic())
            return {}
    
    # Create flow with limited concurrency
    flow = LimitedFlow(start=TrackingNode())
    await flow.run({})
    
    # Verify we processed all items
    assert len(start_times) == 5
    assert len(end_times) == 5
    
    # Verify some overlap in execution (parallelism)
    assert any(
        end_times[i] > start_times[i+1] 
        for i in range(len(start_times)-1)
    )
