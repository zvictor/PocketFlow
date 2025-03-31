<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://cdn.jsdelivr.net/gh/zvictor/brainyflow@master/.github/media/logo-dark.png">
    <source media="(prefers-color-scheme: light)" srcset="https://cdn.jsdelivr.net/gh/zvictor/brainyflow@master/.github/media/logo-light.png">
    <img width="280px" alt="Brainyflow's logo" src="https://cdn.jsdelivr.net/gh/zvictor/brainyflow@master/.github/media/logo.png">
  </picture>
<p>

<p align="center">
  A <a href="https://github.com/zvictor/BrainyFlow/blob/main/python/brainyflow.py">65-line</a> minimalist AI framework 🤯
  <br />
  <sub>Let Agents build Agents with zero bloat, zero dependencies, zero vendor lock-in 😮</sub>
</p>

<p align="center">

  <a href="https://pypi.org/project/brainyflow">
   <img src="https://img.shields.io/pypi/dw/brainyflow?logo=python&label=Python&style=flat-square" alt="python version">
  </a>
  <a href="https://npm.com/packages/brainyflow">
   <img src="https://img.shields.io/npm/d18m/brainyflow?logo=typescript&label=Typescript&style=flat-square" alt="typescript version">
  </a>
  <a href="https://discord.gg/hUHHE9Sa6T">
    <img src="https://img.shields.io/discord/1346833819172601907?logo=discord&style=flat-square" alt="Discord">
  </a>
  <a href="https://github.com/zvictor/brainyflow">
    <img src="https://img.shields.io/github/stars/zvictor/BrainyFlow?logo=github&style=flat-square" alt="GitHub Repository">
  </a>
  <a href="https://github.com/sponsors/zvictor">
    <img src="https://img.shields.io/github/sponsors/zvictor?logo=github&style=flat-square" alt="GitHub Sponsors">
  </a>
</p>

## Features

- **Multi-language**: <a href="https://pypi.org/project/brainyflow">
  <img src="https://iconduck.com/vectors/vctrahatphfa/media/svg/download" width="16" height="16" alt="Python Logo" style="vertical-align: middle; margin: 0 2px;"></a> Python and <a href="https://npm.com/packages/brainyflow"><img src="https://iconduck.com/vectors/vctrk180y7wy/media/svg/download" width="16" height="16" alt="Typescript Logo" style="vertical-align: middle; margin: 0 2px;"></a> Typescript support.

- **Lightweight**: Zero bloat, zero dependencies, zero vendor lock-in.

- **Expressive**: Everything you love—([Multi-](https://brainy.gitbook.io/flow/design_pattern/multi_agent))[Agents](https://brainy.gitbook.io/flow/design_pattern/agent), [Workflow](https://brainy.gitbook.io/flow/design_pattern/workflow), [RAG](https://brainy.gitbook.io/flow/design_pattern/rag), and more.

- **[Agentic Coding](https://zacharyhuang.substack.com/p/agentic-coding-the-most-fun-way-to)**: Let AI Agents (e.g., Cursor AI) build Agents—10x productivity boost!

![divider](https://raw.githubusercontent.com/zvictor/brainyflow/master/.github/media/divider.png)

## Getting started

- To install in Python, `pip install brainyflow` or just copy the [source code](python/brainyflow.py) (only 65 lines!).

- To install in Javascript, `npm install brainyflow` or just copy the [source code](typescript/brainyflow.ts).

- To learn more, check out the [documentation](https://brainy.gitbook.io/flow/). For an in-depth design dive, read the [essay](https://github.com/The-Pocket/.github/blob/main/profile/pocketflow.md).

- 🎉 We now have a [discord](https://discord.gg/hUHHE9Sa6T)!

![divider](https://raw.githubusercontent.com/zvictor/brainyflow/master/.github/media/divider.png)

## Why Brainy Flow?

Current LLM frameworks are bloated... You only need 65 lines for LLM Framework!

<div align="center">
  <img src="https://raw.githubusercontent.com/The-Pocket/.github/main/assets/meme.jpg" width="400"/>

|                | **Abstraction** |                     **App-Specific Wrappers**                      |                       **Vendor-Specific Wrappers**                       |                **Lines**                 |                  **Size**                   |
| -------------- | :-------------: | :----------------------------------------------------------------: | :----------------------------------------------------------------------: | :--------------------------------------: | :-----------------------------------------: |
| LangChain      |  Agent, Chain   |      Many <br><sup><sub>(e.g., QA, Summarization)</sub></sup>      |      Many <br><sup><sub>(e.g., OpenAI, Pinecone, etc.)</sub></sup>       |                   405K                   |                   +166MB                    |
| CrewAI         |  Agent, Chain   | Many <br><sup><sub>(e.g., FileReadTool, SerperDevTool)</sub></sup> | Many <br><sup><sub>(e.g., OpenAI, Anthropic, Pinecone, etc.)</sub></sup> |                   18K                    |                   +173MB                    |
| SmolAgent      |      Agent      |   Some <br><sup><sub>(e.g., CodeAgent, VisitWebTool)</sub></sup>   |  Some <br><sup><sub>(e.g., DuckDuckGo, Hugging Face, etc.)</sub></sup>   |                    8K                    |                   +198MB                    |
| LangGraph      |  Agent, Graph   |       Some <br><sup><sub>(e.g., Semantic Search)</sub></sup>       | Some <br><sup><sub>(e.g., PostgresStore, SqliteSaver, etc.) </sub></sup> |                   37K                    |                    +51MB                    |
| AutoGen        |      Agent      |   Some <br><sup><sub>(e.g., Tool Agent, Chat Agent)</sub></sup>    | Many <sup><sub>[Optional]<br> (e.g., OpenAI, Pinecone, etc.)</sub></sup> | 7K <br><sup><sub>(core-only)</sub></sup> | +26MB <br><sup><sub>(core-only)</sub></sup> |
| **BrainyFlow** |    **Graph**    |                              **None**                              |                                 **None**                                 |                  **65**                  |                 **few KB**                  |

</div>

![divider](https://raw.githubusercontent.com/zvictor/brainyflow/master/.github/media/divider.png)

## How does Brainy Flow work?

The single file in [python](python/brainyflow.py) or [typescript](python/brainyflow.ts) capture the core abstraction of LLM frameworks: Graph!
<br>

<div align="center">
  <img src="https://raw.githubusercontent.com/The-Pocket/.github/main/assets/abstraction.png" width="900"/>
</div>
<br>

From there, it's easy to implement popular design patterns like ([Multi-](https://brainy.gitbook.io/flow/design_pattern/multi_agent))[Agents](https://brainy.gitbook.io/flow/design_pattern/agent), [Workflow](https://brainy.gitbook.io/flow/design_pattern/workflow), [RAG](https://brainy.gitbook.io/flow/design_pattern/rag), etc.
<br>

<div align="center">
  <img src="https://raw.githubusercontent.com/The-Pocket/.github/main/assets/design.png" width="900"/>
</div>
<br>
✨ Below are basic tutorials:

<div align="center">
  
|  Name  | Difficulty    |  Description  |  
| :-------------:  | :-------------: | :--------------------- |  
| [Chat](https://github.com/zvictor/BrainyFlow/tree/main/examples/python-chat) | ☆☆☆ <br> *Dummy*   | A basic chat bot with conversation history |
| [RAG](https://github.com/zvictor/BrainyFlow/tree/main/examples/python-rag) | ☆☆☆ <br> *Dummy*   | A simple Retrieval-augmented Generation process |
| [Workflow](https://github.com/zvictor/BrainyFlow/tree/main/examples/python-workflow) | ☆☆☆ <br> *Dummy*   | A writing workflow that outlines, writes content, and applies styling |
| [Map-Reduce](https://github.com/zvictor/BrainyFlow/tree/main/examples/python-map-reduce) | ☆☆☆ <br> *Dummy* | A resume qualification processor using map-reduce pattern for batch evaluation |
| [Agent](https://github.com/zvictor/BrainyFlow/tree/main/examples/python-agent) | ☆☆☆ <br> *Dummy*   | A research agent that can search the web and answer questions |
| [Streaming](https://github.com/zvictor/BrainyFlow/tree/main/examples/python-llm-streaming) | ☆☆☆ <br> *Dummy*   | A real-time LLM streaming demo with user interrupt capability |
| [Multi-Agent](https://github.com/zvictor/BrainyFlow/tree/main/examples/python-multi-agent) | ★☆☆ <br> *Beginner* | A Taboo word game for asynchronous communication between two agents |
| [Supervisor](https://github.com/zvictor/BrainyFlow/tree/main/examples/python-supervisor) | ★☆☆ <br> *Beginner* | Research agent is getting unreliable... Let's build a supervision process|
| [Parallel](https://github.com/zvictor/BrainyFlow/tree/main/examples/python-parallel-batch) | ★☆☆ <br> *Beginner*   | A parallel execution demo that shows 3x speedup |
| [Thinking](https://github.com/zvictor/BrainyFlow/tree/main/examples/python-thinking) | ★☆☆ <br> *Beginner*   | Solve complex reasoning problems through Chain-of-Thought |
| [Memory](https://github.com/zvictor/BrainyFlow/tree/main/examples/python-chat-memory) | ★☆☆ <br> *Beginner* | A chat bot with short-term and long-term memory |

</div>

👀 Want to see other tutorials for dummies? [Create an issue!](https://github.com/zvictor/BrainyFlow/issues/new)

![divider](https://raw.githubusercontent.com/zvictor/brainyflow/master/.github/media/divider.png)

## How to Use Brainy Flow?

🚀 Through **Agentic Coding**—the fastest LLM App development paradigm-where _humans design_ and _agents code_!

<br />

- Want to learn **Agentic Coding**?
  - To setup, read this [post](https://zacharyhuang.substack.com/p/agentic-coding-the-most-fun-way-to)!
  - Check out [my YouTube](https://www.youtube.com/@ZacharyLLM?sub_confirmation=1)! Read this [Guide](https://brainy.gitbook.io/flow/agentic_coding)!
- Want to build your own LLM App? Start with our [Python template](https://github.com/zvictor/Brainyflow-Template-Python) or [Typescript template](https://github.com/zvictor/Brainyflow-Template-Typescript)!

![divider](https://raw.githubusercontent.com/zvictor/brainyflow/master/.github/media/divider.png)

## Acknowledgement

We would like to extend our deepest gratitude to the creators and contributors of the PocketFlow framework, from which brainyFlow originated as a fork.

## Liability Disclaimer

BrainyFlow is provided "as is" without any warranties or guarantees.  
We do not take responsibility for how the generated output is used, including but not limited to its accuracy, legality, or any potential consequences arising from its use.

## Sponsors

<p align="center">
  <a style="color: inherit" href="https://github.com/sponsors/zvictor?utm_source=brainyflow&utm_medium=sponsorship&utm_campaign=brainyflow&utm_id=brainyflow">
    <img width="150px" src="https://cdn.jsdelivr.net/gh/zvictor/brainyflow@master/.github/media/brain.png" alt="Brainyflow's logo" />
  </a><br /><br />
  BrainyFlow runs on 65 lines of code and your generosity! 💰<br />
    <a style="color: inherit" href="https://github.com/sponsors/zvictor?utm_source=brainyflow&utm_medium=sponsorship&utm_campaign=brainyflow&utm_id=brainyflow">
      Help us deliver more AI with less code (but maybe more coffee)
    </a> ☕<br /><br />
    <a style="color: inherit" href="https://github.com/sponsors/zvictor?utm_source=brainyflow&utm_medium=sponsorship&utm_campaign=brainyflow&utm_id=brainyflow">Your support</a> helps keep it minimal, powerful, and dependency-free! 🚀
  </a>
</p>

![divider](https://raw.githubusercontent.com/zvictor/brainyflow/master/.github/media/divider.png)
