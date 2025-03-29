import pytest
import asyncio
import time
from brainyflow import Node, ParallelBatchNode

@pytest.mark.asyncio
async def test_throttling_with_semaphore():
    """Tests that concurrency limits are respected using asyncio.Semaphore."""
    concurrency = 2
    semaphore = asyncio.Semaphore(concurrency)
    max_concurrent = 0
    current_concurrent = 0
    processed_items = []

    class ThrottledProcessingNode(Node):
        """Helper node to simulate processing with throttling."""
        async def exec(self, item):
            nonlocal max_concurrent, current_concurrent, processed_items
            async with semaphore:
                current_concurrent += 1
                max_concurrent = max(max_concurrent, current_concurrent)
                assert current_concurrent <= concurrency, "Exceeded concurrency limit"

                # Simulate async work
                await asyncio.sleep(0.01)
                result = {item['key']: item['value'] * 2}

                current_concurrent -= 1
                processed_items.append(item['value']) # Record order of completion
                return result

    # We need the ParallelBatchNode to use our throttled exec logic.
    # Since ParallelBatchNode now correctly calls super()._exec,
    # we can assign the throttled exec method directly.
    test_items = [{'key': f'item_{i}', 'value': i} for i in range(10)]
    batch_node = ParallelBatchNode(max_retries=1)
    throttled_processor = ThrottledProcessingNode()
    batch_node.exec = throttled_processor.exec # Assign the throttled exec

    start_time = time.time()
    results = await batch_node._exec(test_items) # Use _exec to test batch logic
    duration = time.time() - start_time

    # Verification
    assert max_concurrent == concurrency, f"Expected max concurrency {concurrency}, but got {max_concurrent}"
    assert len(results) == len(test_items), "Not all items were processed"
    assert current_concurrent == 0, "Some tasks might still be holding the semaphore"

    # Check results correctness (order is preserved by asyncio.gather)
    for i, result in enumerate(results):
        expected_key = f'item_{i}'
        expected_value = i * 2
        assert result == {expected_key: expected_value}, f"Incorrect result for item {i}"

    # Optional: Check duration - 10 items, 10ms each, concurrency 2 -> ~50ms
    print(f"Throttling test duration: {duration:.4f}s")
    assert duration >= 0.045, "Execution was too fast, throttling might not have worked"
    assert duration < 0.150, "Execution took unexpectedly long"
