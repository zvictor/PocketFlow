# Sequential vs Parallel Processing

Demonstrates how AsyncParallelBatchNode accelerates processing by 3x over AsyncBatchNode.

## Features

- Processes identical tasks with two approaches
- Compares sequential vs parallel execution time
- Shows 3x speed improvement with parallel processing

## Run It

```bash
pip install pocketflow
python main.py
```

## Output

```
=== Running Sequential (AsyncBatchNode) ===
[Sequential] Summarizing file1.txt...
[Sequential] Summarizing file2.txt...
[Sequential] Summarizing file3.txt...

=== Running Parallel (AsyncParallelBatchNode) ===
[Parallel] Summarizing file1.txt...
[Parallel] Summarizing file2.txt...
[Parallel] Summarizing file3.txt...

Sequential took: 3.00 seconds
Parallel took:   1.00 seconds
```

## Key Points

- **Sequential**: Total time = sum of all item times
  - Good for: Rate-limited APIs, maintaining order

- **Parallel**: Total time ≈ longest single item time
  - Good for: I/O-bound tasks, independent operations 