import pytest
import asyncio
import time
from brainyflow import Node, ParallelBatchNode

# Helper classes similar to TypeScript tests

class ProcessingNode(Node):
    async def exec(self, item):
        key, value = item['key'], item['value']
        await asyncio.sleep(0.01)  # Simulate async work
        return {key: value * 2}

class ThrottledParallelNode(ParallelBatchNode):
    def __init__(self, concurrency=2, max_retries=1, wait=0):
        super().__init__(max_retries=max_retries, wait=wait)
        self.semaphore = asyncio.Semaphore(concurrency)

    async def exec(self, item):
        async with self.semaphore:
            # Note: In Python, the semaphore needs to wrap the call within the batch node's _exec loop,
            # or we apply it here if we override exec directly.
            # The base ParallelBatchNode._exec handles the gathering.
            # Let's refine this - the semaphore should ideally be used *inside* the loop
            # that ParallelBatchNode._exec implicitly creates.
            # A simpler way for testing is to override _exec itself.
            # Let's stick to overriding exec for this test class for simplicity,
            # acknowledging it's slightly different from the TS Semaphore class structure.
            processing_node = ProcessingNode()
            return await processing_node.exec(item) # Use a separate node instance for processing logic

@pytest.mark.asyncio
async def test_process_items_in_parallel():
    test_items = [
        {'key': 'a', 'value': 1},
        {'key': 'b', 'value': 2},
        {'key': 'c', 'value': 3},
    ]

    node = ParallelBatchNode(max_retries=1)
    processing_node = ProcessingNode()
    # Assign the exec method directly for testing _exec
    node.exec = processing_node.exec

    results = await node._exec(test_items) # Directly test _exec like in TS
    combined = {k: v for d in results for k, v in d.items()}
    assert combined == {'a': 2, 'b': 4, 'c': 6}

@pytest.mark.asyncio
async def test_respect_concurrency_limits():
    test_items = [
        {'key': 'a', 'value': 1},
        {'key': 'b', 'value': 2},
        {'key': 'c', 'value': 3},
        {'key': 'd', 'value': 4},
    ]

    # We need a way to apply semaphore correctly within ParallelBatchNode's logic.
    # Let's redefine how ThrottledParallelNode works for Python's asyncio.gather
    class CustomThrottledNode(ParallelBatchNode):
        def __init__(self, concurrency=2, max_retries=1, wait=0):
             super().__init__(max_retries=max_retries, wait=wait)
             self.semaphore = asyncio.Semaphore(concurrency)
             self.processing_node = ProcessingNode() # Internal node for logic

        async def _exec_single_with_semaphore(self, item):
             async with self.semaphore:
                 # Use super().exec to ensure retry logic is applied if needed
                 # We need to call the *original* exec logic here, wrapped by semaphore
                 return await self.processing_node.exec(item) # Call the actual processing

        async def _exec(self, items):
             # Override _exec to use the semaphore-wrapped single execution
             if not items: return []
             tasks = [self._exec_single_with_semaphore(i) for i in items]
             return await asyncio.gather(*tasks)

    node = CustomThrottledNode(concurrency=2, max_retries=1)
    # node.exec is implicitly handled by _exec_single_with_semaphore calling processing_node.exec

    start = time.time()
    results = await node._exec(test_items)
    duration = time.time() - start

    # 4 items, 10ms each, concurrency 2 -> ~20ms total expected
    # Allow some buffer for scheduling overhead
    print(f"Duration with concurrency 2: {duration:.4f}s")
    assert duration >= 0.015 # Should take roughly 2 * 10ms
    assert len(results) == 4

@pytest.mark.asyncio
async def test_handle_varying_task_durations():
    test_items = [
        {'key': 'fast', 'value': 1, 'delay': 0.005},
        {'key': 'medium', 'value': 2, 'delay': 0.010},
        {'key': 'slow', 'value': 3, 'delay': 0.020},
    ]

    node = ParallelBatchNode(max_retries=1)
    async def exec_with_delay(item):
        await asyncio.sleep(item['delay'])
        return {item['key']: item['value'] * 2}
    node.exec = exec_with_delay

    start = time.time()
    await node._exec(test_items)
    duration = time.time() - start

    # Should take roughly as long as the slowest task
    print(f"Duration with varying delays: {duration:.4f}s")
    assert duration >= 0.018 # Close to 20ms
    assert duration < 0.050 # Definitely less than sum of delays (35ms)

@pytest.mark.asyncio
async def test_maintain_order_of_results():
    test_items = [
        {'key': 'a', 'value': 1},
        {'key': 'b', 'value': 2},
        {'key': 'c', 'value': 3},
    ]

    node = ParallelBatchNode(max_retries=1)
    processing_node = ProcessingNode()
    # Assign exec method
    node.exec = processing_node.exec

    results = await node._exec(test_items)

    # Results should be in same order as input despite parallel execution
    result_keys = [list(r.keys())[0] for r in results]
    assert result_keys == ['a', 'b', 'c']

@pytest.mark.asyncio
async def test_handle_retries():
    attempt = 0
    class RetryNode(Node):
        async def exec(self, item):
            nonlocal attempt
            attempt += 1
            if attempt < 2:
                raise Exception('Simulated failure')
            return {item['key']: item['value'] * 2}

    test_items = [{'key': 'a', 'value': 1}]
    node = ParallelBatchNode(max_retries=3) # max_retries = 3
    retry_node_instance = RetryNode()
    node.exec = retry_node_instance.exec # Assign the method

    results = await node._exec(test_items)
    assert results == [{'a': 2}]
    assert attempt == 2

@pytest.mark.asyncio
async def test_use_fallback_when_retries_exhausted():
    class FallbackNode(Node):
        async def exec(self, item):
            raise Exception('Always fails')
        async def exec_fallback(self, item, exc):
             # Fallback needs access to the item, adjust base class if needed
             # Assuming exec_fallback gets prep_res (which is the item here)
            return {item['key']: 'fallback'}

    test_items = [{'key': 'a', 'value': 1}]
    # max_retries = 1 so exec fails once then fallback is called
    node = ParallelBatchNode(max_retries=1)
    fallback_node_instance = FallbackNode()
    node.exec = fallback_node_instance.exec
    node.exec_fallback = fallback_node_instance.exec_fallback # Assign fallback

    results = await node._exec(test_items)
    assert results == [{'a': 'fallback'}]

@pytest.mark.asyncio
async def test_handle_empty_input():
    node = ParallelBatchNode(max_retries=1)
    processing_node = ProcessingNode()
    node.exec = processing_node.exec

    results = await node._exec([])
    assert results == []

@pytest.mark.asyncio
async def test_propagate_errors():
    class ErrorNode(Node):
        async def exec(self, item):
            raise ValueError('Test error') # Use a specific error type

    test_items = [
        {'key': 'a', 'value': 1},
        {'key': 'b', 'value': 2},
    ]

    node = ParallelBatchNode(max_retries=1) # No retries on error
    error_node_instance = ErrorNode()
    node.exec = error_node_instance.exec

    with pytest.raises(ValueError, match='Test error'):
        await node._exec(test_items)

@pytest.mark.asyncio
async def test_handle_errors_with_concurrency():
    processed_count = 0
    class ErrorNode(Node):
        async def exec(self, item):
            nonlocal processed_count
            processed_count_before = processed_count
            processed_count += 1
            print(f"Processing item {item['key']}, current count: {processed_count_before + 1}")
            if item['key'] == 'b':
                await asyncio.sleep(0.005) # Ensure it might start before 'c'
                print(f"Throwing error for item {item['key']}")
                raise ValueError('Intentional error')
            await asyncio.sleep(0.01)
            print(f"Finished processing item {item['key']}")
            return {item['key']: item['value']}

    test_items = [
        {'key': 'a', 'value': 1},
        {'key': 'b', 'value': 2}, # This one will fail
        {'key': 'c', 'value': 3},
    ]

    node = ParallelBatchNode(max_retries=1)
    error_node_instance = ErrorNode()
    node.exec = error_node_instance.exec

    with pytest.raises(ValueError, match='Intentional error'):
        await node._exec(test_items)

    # Check if at least one item started processing. Due to parallel nature,
    # 'a' or 'c' might complete or start before 'b' errors out.
    # The exact number processed before error isn't strictly guaranteed,
    # but it should be > 0 if tasks actually run in parallel.
    print(f"Total items processed before/during error: {processed_count}")
    assert processed_count > 0
