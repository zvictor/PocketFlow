# Majority Vote Reasoning

This project demonstrates a majority vote implementation that enables LLMs to solve complex reasoning problems by aggregating multiple independent attempts. It's designed to improve problem-solving accuracy through consensus-based reasoning.

## Features

- Improves model reliability on complex problems through multiple attempts
- Works with models like Claude 3.7 Sonnet
- Solves problems that single attempts often fail on
- Provides detailed reasoning traces for verification
- Uses a consensus approach to reduce the impact of occasional reasoning errors

## Getting Started

1. Install the required packages:
```bash
pip install -r requirements.txt
```

2. Set up your API key:
```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

3. Run a test problem to see majority voting in action:
```bash
python main.py
```

## How It Works

The implementation uses a MajorityVoteNode that processes multiple attempts and finds consensus:

```mermaid
flowchart LR
    mv[MajorityVoteNode] 
```

The MajorityVoteNode:
1. Makes multiple independent attempts to solve the same problem
2. Collects structured answers from each attempt
3. Determines the most frequent answer as the final solution
4. Returns the consensus answer

This approach helps overcome occasional reasoning errors that might occur in individual attempts.

## Example Output

Below is an example of how the majority vote approach uses Claude 3.7 Sonnet to solve this complex problem:

```
Translated Chinese text

Translated Spanish text
Translated Japanese text
Translated German text
Translated Russian text
Translated Portuguese text
Translated French text
Translated Korean text
Saved translation to translations/README_CHINESE.md
Saved translation to translations/README_SPANISH.md
Saved translation to translations/README_JAPANESE.md
Saved translation to translations/README_GERMAN.md
Saved translation to translations/README_RUSSIAN.md
Saved translation to translations/README_PORTUGUESE.md
Saved translation to translations/README_FRENCH.md
Saved translation to translations/README_KOREAN.md

=== Translation Complete ===
Translations saved to: translations
============================
```



## Files

- [`main.py`](./main.py): Implementation of the majority vote node and flow
- [`utils.py`](./utils.py): Simple wrapper for calling the Anthropic model