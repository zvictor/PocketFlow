import pytest
import asyncio
from pocketflow import Node, Flow, SequentialBatchFlow

# --- Helper Nodes and Flows ---

class AddToResultsNode(Node):
    """A simple node that adds its parameter 'value' multiplied by a factor to a shared list."""
    async def prep(self, shared):
        # Default factor if not provided
        return self.params.get('factor', 1)

    async def exec(self, factor):
        value = self.params.get('value', 0)
        return value * factor

    async def post(self, shared, prep_res, exec_res):
        if 'results' not in shared:
            shared['results'] = []
        shared['results'].append(exec_res)
        # Also record the order of values processed
        if 'processed_order' not in shared:
            shared['processed_order'] = []
        shared['processed_order'].append(self.params.get('value', 0))

# Create a simple sub-flow using the node above
add_node = AddToResultsNode()
sub_flow = Flow(start=add_node)

# --- Test Cases ---

@pytest.mark.asyncio
async def test_sequential_batch_flow_basic():
    """Tests basic sequential execution and shared state accumulation."""
    class MyBatchFlow(SequentialBatchFlow):
        async def prep(self, shared):
            # Returns parameters for each sub-flow run
            return [{'value': 1}, {'value': 2}, {'value': 3}]

    batch_flow = MyBatchFlow(start=sub_flow)
    shared_state = {}
    await batch_flow.run(shared_state)

    assert 'results' in shared_state
    # Default factor is 1
    assert shared_state['results'] == [1, 2, 3]
    assert 'processed_order' in shared_state
    assert shared_state['processed_order'] == [1, 2, 3] # Verify order

@pytest.mark.asyncio
async def test_sequential_batch_flow_with_params():
    """Tests merging of batch flow params and prep params."""
    class MyBatchFlowWithParams(SequentialBatchFlow):
        async def prep(self, shared):
            return [{'value': 10}, {'value': 20}]

    # Initialize batch flow with its own parameters
    batch_flow = MyBatchFlowWithParams(start=sub_flow)
    batch_flow.set_params({'factor': 5}) # Set a factor on the batch flow itself

    shared_state = {}
    await batch_flow.run(shared_state)

    assert 'results' in shared_state
    # value * factor => 10*5, 20*5
    assert shared_state['results'] == [50, 100]
    assert 'processed_order' in shared_state
    assert shared_state['processed_order'] == [10, 20]

@pytest.mark.asyncio
async def test_sequential_batch_flow_empty_prep():
    """Tests behavior when prep returns an empty list."""
    class EmptyPrepBatchFlow(SequentialBatchFlow):
        async def prep(self, shared):
            shared['prep_called'] = True
            return [] # No items to process

        async def post(self, shared, prep_res, exec_res):
            shared['post_called'] = True
            # exec_res should be None as _orch wasn't called with items
            assert exec_res is None
            assert prep_res == [] # prep_res is the result of prep()

    batch_flow = EmptyPrepBatchFlow(start=sub_flow)
    shared_state = {}
    await batch_flow.run(shared_state)

    assert shared_state.get('prep_called', False) is True
    assert shared_state.get('post_called', False) is True
    # Ensure the sub-flow node didn't run
    assert 'results' not in shared_state
    assert 'processed_order' not in shared_state

@pytest.mark.asyncio
async def test_sequential_batch_flow_post_execution():
    """Tests that the batch flow's post method runs after all items."""
    class PostCheckBatchFlow(SequentialBatchFlow):
        async def prep(self, shared):
            return [{'value': 1}, {'value': 2}]

        async def post(self, shared, prep_res, exec_res):
            # This post runs *after* all iterations of the sub-flow
            shared['final_result_count'] = len(shared.get('results', []))
            shared['batch_post_executed'] = True
            # exec_res is None because SequentialBatchFlow._run doesn't return sub-flow results directly
            assert exec_res is None
            assert isinstance(prep_res, list)
            assert len(prep_res) == 2

    batch_flow = PostCheckBatchFlow(start=sub_flow)
    shared_state = {}
    await batch_flow.run(shared_state)

    assert shared_state.get('batch_post_executed', False) is True
    assert 'results' in shared_state
    assert len(shared_state['results']) == 2
    assert shared_state.get('final_result_count') == 2

@pytest.mark.asyncio
async def test_sequential_batch_flow_modifies_shared_sequentially():
    """Tests that shared state modifications happen in sequence."""
    class SequentialAppendNode(Node):
        async def exec(self, prep_res):
            # Simulate work based on value
            await asyncio.sleep(0.02 - self.params['value'] * 0.005)
            return self.params['value']

        async def post(self, shared, prep_res, exec_res):
            if 'log' not in shared:
                shared['log'] = []
            shared['log'].append(f"Processed {exec_res}")

    seq_node = SequentialAppendNode()
    seq_sub_flow = Flow(start=seq_node)

    class SequentialLogBatchFlow(SequentialBatchFlow):
        async def prep(self, shared):
            # Items that take different amounts of time
            return [{'value': 1}, {'value': 2}, {'value': 3}]

    batch_flow = SequentialLogBatchFlow(start=seq_sub_flow)
    shared_state = {}
    await batch_flow.run(shared_state)

    assert 'log' in shared_state
    # Check if the log reflects the sequential processing order
    assert shared_state['log'] == ["Processed 1", "Processed 2", "Processed 3"]
