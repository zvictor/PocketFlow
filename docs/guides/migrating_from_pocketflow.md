# Migrating from PocketFlow

## Overview

PocketFlow has been updated to use asynchronous programming patterns throughout the codebase. This guide will help you migrate your existing PocketFlow code to the new BrainyFlow async interface.

## Key Changes

1. **All core methods are now async**

   - `prep()`, `exec()`, `post()`, `_exec()`, `_run()`, and `run()` methods now use `async/await` syntax
   - All method calls to these functions must now be awaited

2. **Simplified class hierarchy**

   - Removed separate async classes (`AsyncNode`, `AsyncFlow`, etc.)
   - All classes now use async methods by default

3. **Batch processing changes**

   - `BatchNode` → `SequentialBatchNode` (sequential processing) or `ParallelBatchNode` (concurrent processing)

4. **Sleep operations**
   - `time.sleep()` → `await asyncio.sleep()`

## Why Async?

The move to async brings several benefits:

- **Improved performance**: Asynchronous code can handle I/O-bound operations more efficiently
- **Better concurrency**: Easier to implement parallel processing patterns
- **Simplified codebase**: No need for separate sync and async implementations
- **Modern Python**: Aligns with Python's direction for handling concurrent operations

## Migration Steps

### Step 1: Import asyncio

Add `asyncio` to your imports:

```python
import asyncio
```

### Step 2: Update Node implementations

#### Before:

```python
class MyNode(Node):
    def prep(self, shared):
        # Preparation logic
        return some_data

    def exec(self, prep_res):
        # Execution logic
        return result

    def post(self, shared, prep_res, exec_res):
        # Post-processing logic
        return action
```

#### After:

```python
class MyNode(Node):
    async def prep(self, shared):
        # Preparation logic
        return some_data

    async def exec(self, prep_res):
        # Execution logic
        return result

    async def post(self, shared, prep_res, exec_res):
        # Post-processing logic
        return action
```

### Step 3: Update Flow implementations

#### Before:

```python
class MyFlow(Flow):
    def prep(self, shared):
        # Preparation logic
        return some_data

    def post(self, shared, prep_res, exec_res):
        # Post-processing logic
        return action
```

#### After:

```python
class MyFlow(Flow):
    async def prep(self, shared):
        # Preparation logic
        return some_data

    async def post(self, shared, prep_res, exec_res):
        # Post-processing logic
        return action
```

### Step 4: Update Batch processing

#### Before:

```python
# For batch node processing
class MyBatchNode(BatchNode):
    def exec(self, item):
        # Process single item
        return processed_item

# For batch flow processing
class MyBatchFlow(BatchFlow):
    def prep(self, shared):
        # Return list of items to process
        return items_list
```

#### After:

```python
# For sequential batch processing
class MySequentialBatchNode(SequentialBatchNode):
    async def exec(self, item):
        # Process single item
        return processed_item

# For parallel batch processing
class MyParallelBatchNode(ParallelBatchNode):
    async def exec(self, item):
        # Process single item
        return processed_item

# For sequential batch flow
class MySequentialBatchFlow(SequentialBatchFlow):
    async def prep(self, shared):
        # Return list of items to process
        return items_list

# For parallel batch flow
class MyParallelBatchFlow(ParallelBatchFlow):
    async def prep(self, shared):
        # Return list of items to process
        return items_list
```

### Step 5: Update fallback handling

#### Before:

```python
class MyNode(Node):
    def exec_fallback(self, prep_res, exc):
        # Handle exception
        return fallback_result
```

#### After:

```python
class MyNode(Node):
    async def exec_fallback(self, prep_res, exc):
        # Handle exception
        return fallback_result
```

### Step 6: Update sleep operations

#### Before:

```python
import time

class MyNode(Node):
    def exec(self, prep_res):
        # Do something
        time.sleep(1)  # Wait for 1 second
        # Do something else
        return result
```

#### After:

```python
import asyncio

class MyNode(Node):
    async def exec(self, prep_res):
        # Do something
        await asyncio.sleep(1)  # Wait for 1 second
        # Do something else
        return result
```

### Step 7: Update code that runs nodes and flows

#### Before:

```python
# Running a node
result = my_node.run(shared_data)

# Running a flow
result = my_flow.run(shared_data)
```

#### After:

```python
# Running a node
result = await my_node.run(shared_data)

# Running a flow
result = await my_flow.run(shared_data)
```

## Migrating from Async Classes

If you were previously using the async versions of classes (`AsyncNode`, `AsyncFlow`, etc.), the migration is straightforward:

### Step 1: Replace class inheritance

#### Before:

```python
class MyNode(AsyncNode):
    async def prep_async(self, shared):
        # ...

    async def exec_async(self, prep_res):
        # ...

    async def post_async(self, shared, prep_res, exec_res):
        # ...
```

#### After:

```python
class MyNode(Node):
    async def prep(self, shared):
        # ...

    async def exec(self, prep_res):
        # ...

    async def post(self, shared, prep_res, exec_res):
        # ...
```

### Step 2: Rename methods

- `prep_async` → `prep`
- `exec_async` → `exec`
- `post_async` → `post`
- `exec_fallback_async` → `exec_fallback`
- `run_async` → `run`

### Step 3: Update method calls

#### Before:

```python
result = await my_node.run_async(shared_data)
```

#### After:

```python
result = await my_node.run(shared_data)
```

## Migrating Batch Processing

The batch processing classes have been split into sequential and parallel versions:

### Sequential vs Parallel Batch Nodes

- Use `SequentialBatchNode` when you want to process items one after another
- Use `ParallelBatchNode` when you want to process items concurrently

### Sequential vs Parallel Batch Flows

- Use `SequentialBatchFlow` when you want to run flows for each item one after another
- Use `ParallelBatchFlow` when you want to run flows for each item concurrently

### AsyncBatchNode and AsyncParallelBatchNode

#### Before:

```python
class MyBatchNode(AsyncBatchNode):
    async def exec_async(self, item):
        # Process item
        return result

class MyParallelBatchNode(AsyncParallelBatchNode):
    async def exec_async(self, item):
        # Process item
        return result
```

#### After:

```python
class MyBatchNode(SequentialBatchNode):
    async def exec(self, item):
        # Process item
        return result

class MyParallelBatchNode(ParallelBatchNode):
    async def exec(self, item):
        # Process item
        return result
```

## Running Your Async Code

To run your async code, you'll need to use an event loop:

```python
import asyncio

async def main():
    # Create your nodes and flows
    my_node = MyNode()
    my_flow = MyFlow(my_node)

    # Run your flow
    result = await my_flow.run(shared_data)

    # Process result
    print(result)

# Run the main function
if __name__ == "__main__":
    asyncio.run(main())
```

## Common Pitfalls

### 1. Forgetting to await

The most common mistake is forgetting to await async method calls:

```python
# WRONG
result = my_node.run(shared_data)  # This returns a coroutine, not the actual result

# CORRECT
result = await my_node.run(shared_data)
```

### 2. Mixing sync and async code

Be careful when calling sync functions from async functions and vice versa:

```python
# WRONG
async def my_async_function():
    # This will block the event loop
    time.sleep(1)

# CORRECT
async def my_async_function():
    # This allows other tasks to run while waiting
    await asyncio.sleep(1)
```

### 3. Using the wrong batch class

Make sure you choose the right batch class for your needs:

- `SequentialBatchNode`/`SequentialBatchFlow`: Items are processed one after another
- `ParallelBatchNode`/`ParallelBatchFlow`: Items are processed concurrently

### 4. Not handling exceptions properly

Remember that with async code, exceptions need to be handled differently:

```python
# WRONG
try:
    my_node.run(shared_data)
except Exception as e:
    handle_exception(e)

# CORRECT
try:
    await my_node.run(shared_data)
except Exception as e:
    handle_exception(e)
```

## Example: Complete Migration

### Before:

```python
import time
from pocketflow import Node, Flow, BatchNode, BatchFlow

class DataFetchNode(Node):
    def prep(self, shared):
        return shared.get('url')

    def exec(self, url):
        # Fetch data from URL
        time.sleep(1)  # Simulate network delay
        return f"Data from {url}"

    def post(self, shared, url, data):
        shared['data'] = data
        return "default"

class ProcessNode(Node):
    def exec(self, prep_res):
        return f"Processed: {prep_res}"

class BatchProcessor(BatchNode):
    def exec(self, item):
        time.sleep(0.5)  # Simulate processing
        return f"Batch processed: {item}"

# Create flow
fetch_node = DataFetchNode()
process_node = ProcessNode()
flow = Flow(fetch_node)
fetch_node.add_successor(process_node)

# Run flow
shared_data = {'url': 'https://example.com'}
result = flow.run(shared_data)
print(result)
```

### After:

```python
import asyncio
from pocketflow import Node, Flow, SequentialBatchNode, ParallelBatchNode

class DataFetchNode(Node):
    async def prep(self, shared):
        return shared.get('url')

    async def exec(self, url):
        # Fetch data from URL
        await asyncio.sleep(1)  # Simulate network delay
        return f"Data from {url}"

    async def post(self, shared, url, data):
        shared['data'] = data
        return "default"

class ProcessNode(Node):
    async def exec(self, prep_res):
        return f"Processed: {prep_res}"

class BatchProcessor(ParallelBatchNode):
    async def exec(self, item):
        await asyncio.sleep(0.5)  # Simulate processing
        return f"Batch processed: {item}"

async def main():
    # Create flow
    fetch_node = DataFetchNode()
    process_node = ProcessNode()
    flow = Flow(fetch_node)
    fetch_node.add_successor(process_node)

    # Run flow
    shared_data = {'url': 'https://example.com'}
    result = await flow.run(shared_data)
    print(result)

# Run the async main function
if __name__ == "__main__":
    asyncio.run(main())
```

## Conclusion

Migrating to the new async interface requires adding `async`/`await` keywords to your methods and method calls, and updating your class inheritance if you were using the now-removed async classes. The benefits of this migration include improved performance, better concurrency, and a simplified codebase.

Remember to run your async code with `asyncio.run()` or another appropriate method for executing async functions.
