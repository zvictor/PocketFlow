# Migrating from PocketFlow to BrainyFlow

## Overview

BrainyFlow is an asynchronous fork of PocketFlow, designed for enhanced performance and concurrency. This guide will help you migrate your existing PocketFlow code to BrainyFlow.

## Key Changes

1. **All core methods are now async**

   - `prep()`, `exec()`, `post()`, `_exec()`, `_run()`, and `run()` methods now use `async/await` syntax
   - All method calls to these functions must now be awaited

2. **Simplified class hierarchy**

   - Removed separate async classes (`AsyncNode`, `AsyncFlow`, etc.)
   - All classes now use async methods by default

3. **Batch processing changes**

   - `BatchNode` → `SequentialBatchNode` (sequential processing) or `ParallelBatchNode` (concurrent processing)
   - `BatchFlow` → `SequentialBatchFlow` (sequential processing) or `ParallelBatchFlow` (concurrent processing)

## Why Async?

The move to async brings several benefits:

- **Improved performance**: Asynchronous code can handle I/O-bound operations more efficiently
- **Better concurrency**: Easier to implement parallel processing patterns
- **Simplified codebase**: No need for separate sync and async implementations
- **Modern Python**: Aligns with Python's direction for handling concurrent operations

## Migration Steps

### Step 1: Update Imports

Replace PocketFlow imports with BrainyFlow imports:

```python
# Before
from pocketflow import Node, Flow, BatchNode, BatchFlow # ... and other classes

# After
import asyncio # BrainyFlow requires asyncio
from brainyflow import Node, Flow, SequentialBatchNode, ParallelBatchNode, SequentialBatchFlow, ParallelBatchFlow # ... and other classes
```

### Step 2: Update Method Definitions

All core methods in Nodes and Flows are now `async`. Add the `async` keyword to your method definitions and use `await` when calling them or other async functions. This includes `prep`, `exec`, `post`, and `exec_fallback`.

#### Node Example (Before):

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

    def exec_fallback(self, prep_res, exc):
        # Handle exception
        return fallback_result
```

#### Node Example (After):

```python
class MyNode(Node):
    async def prep(self, shared):
        # Preparation logic
        # If you call other async functions here, use await
        return some_data

    async def exec(self, prep_res):
    async def post(self, shared, prep_res, exec_res):
        # Post-processing logic
        # If you call other async functions here, use await
        return action

    async def exec_fallback(self, prep_res, exc):
        # Handle exception
        # If you call other async functions here, use await
        return fallback_result
```

_(Flow `prep` and `post` methods follow the same pattern)_

### Step 3: Update Batch Processing Classes

Replace `BatchNode` and `BatchFlow` with their BrainyFlow equivalents: `SequentialBatchNode`, `ParallelBatchNode`, `SequentialBatchFlow`, or `ParallelBatchFlow`. Choose based on whether you need sequential or parallel execution. Remember to make the relevant methods (`exec` for Batch Nodes, `prep`/`post` for Batch Flows) `async`.

#### Batch Example (Before):

```python
# Batch node processing
class MyBatchNode(BatchNode):
    def exec(self, item):
        # Process single item sequentially
        return processed_item

# Batch flow processing
class MyBatchFlow(BatchFlow):
    def prep(self, shared):
        # Return list of items to process sequentially
        return items_list
```

#### Batch Example (After - Parallel):

```python
# Parallel batch node processing
class MyParallelBatchNode(ParallelBatchNode):
    async def exec(self, item):
        # Process single item concurrently
        # Use await for async operations within
        return processed_item

# Parallel batch flow processing
class MyParallelBatchFlow(ParallelBatchFlow):
    async def prep(self, shared):
        # Return list of items to process concurrently
        # Use await for async operations within
        return items_list
```

_(Use `SequentialBatchNode` / `SequentialBatchFlow` for sequential processing)_

### Step 4: Update Code Execution

Calls to `run()` methods on Nodes and Flows must now be awaited. You'll also need an async context (like an `async def main()` function) to run them.

#### Execution Example (Before):

```python
# Running a node
result = my_node.run(shared_data)

# Running a flow
result = my_flow.run(shared_data)

# Main execution (if applicable)
if __name__ == "__main__":
    # setup and run flow/node
    pass
```

#### Execution Example (After):

```python
import asyncio

async def main():
    # Setup nodes and flows
    my_node = MyNode()
    my_flow = Flow(my_node) # Assuming Flow is defined
    shared_data = {}

    # Running a node
    node_result = await my_node.run(shared_data)

    # Running a flow
    flow_result = await my_flow.run(shared_data)

    print(f"Node Result: {node_result}")
    print(f"Flow Result: {flow_result}")

# Main execution
if __name__ == "__main__":
    asyncio.run(main())

```

## Migrating from PocketFlow Async Classes

If you were using PocketFlow's async classes (`AsyncNode`, `AsyncFlow`, etc.), the migration involves:

1.  **Change Base Classes:** Inherit from the standard BrainyFlow classes (`Node`, `Flow`, etc.) instead of the `Async*` versions.
2.  **Rename Methods:** Remove the `_async` suffix from your method names (e.g., `prep_async` becomes `prep`).
3.  **Update Calls:** Ensure all calls to `run` (previously `run_async`) are awaited.

## Running Your BrainyFlow Code

BrainyFlow code must be run within an async event loop. The standard way is using `asyncio.run()`:

```python
import asyncio

async def main():
    # ... your BrainyFlow setup and execution using await ...
    pass

if __name__ == "__main__":
    asyncio.run(main())
```

## Common Pitfalls

### 1. Forgetting `await`

The most common mistake is forgetting to use `await` when calling BrainyFlow's `run` methods or any other async function within your node/flow methods:

```python
# WRONG - Forgetting await
result = my_node.run(shared_data)  # Returns a coroutine, not the result!

# CORRECT
result = await my_node.run(shared_data)
```

### 2. Blocking Calls in Async Methods

Avoid long-running synchronous operations (like `time.sleep()` or blocking I/O) inside your `async` methods. Use `await asyncio.sleep()` and async libraries for I/O instead.

### 3. Choosing the Wrong Batch Class

Ensure you select the correct batch class (`Sequential*` vs. `Parallel*`) based on whether you need items processed one by one or concurrently.

## Example: Complete Migration

### Before (PocketFlow):

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
fetch_node >> process_node

# Run flow
shared_data = {'url': 'https://example.com'}
result = flow.run(shared_data)
print(result)
```

### After (BrainyFlow):

```python
import asyncio
from brainyflow import Node, Flow, ParallelBatchNode

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
    fetch_node >> process_node

    # Run flow
    shared_data = {'url': 'https://example.com'}
    result = await flow.run(shared_data)
    print(result)

# Run the async main function
if __name__ == "__main__":
    asyncio.run(main())
```

## Conclusion

Migrating from PocketFlow to BrainyFlow primarily involves:

1.  Updating imports to `brainyflow` and adding `import asyncio`.
2.  Adding `async` to your Node/Flow method definitions (`prep`, `exec`, `post`, `exec_fallback`).
3.  Using `await` when calling `run()` methods and any other asynchronous operations within your methods.
4.  Replacing `BatchNode`/`BatchFlow` with the appropriate `Sequential*` or `Parallel*` BrainyFlow classes.
5.  Running your main execution logic within an `async def main()` function called by `asyncio.run()`.

This transition enables you to leverage the performance and concurrency benefits of asynchronous programming in your workflows.
