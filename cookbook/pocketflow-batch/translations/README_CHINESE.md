<div align="center">
  <img src="https://github.com/The-Pocket/.github/raw/main/assets/title.png" width="600"/>
</div>


![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
[![Docs](https://img.shields.io/badge/docs-latest-blue)](https://the-pocket.github.io/PocketFlow/)
 <a href="https://discord.gg/hUHHE9Sa6T">
    <img src="https://img.shields.io/discord/1346833819172601907?logo=discord&style=flat">
</a>

Pocket Flow 是一个仅[100行代码](https://github.com/The-Pocket/PocketFlow/blob/main/pocketflow/__init__.py)的极简主义 LLM 框架

- **轻量级**：仅100行代码。零臃肿，零依赖，零供应商锁定。
  
- **表达力强**：拥有你喜爱的一切——([多](https://the-pocket.github.io/PocketFlow/design_pattern/multi_agent.html))[智能体](https://the-pocket.github.io/PocketFlow/design_pattern/agent.html)、[工作流](https://the-pocket.github.io/PocketFlow/design_pattern/workflow.html)、[RAG](https://the-pocket.github.io/PocketFlow/design_pattern/rag.html)等等。

- **[智能体编程](https://zacharyhuang.substack.com/p/agentic-coding-the-most-fun-way-to)**：让AI智能体（如Cursor AI）构建智能体—生产力提升10倍！

- 安装：```pip install pocketflow```或直接复制[源代码](https://github.com/The-Pocket/PocketFlow/blob/main/pocketflow/__init__.py)（仅100行）。
  
- 了解更多，请查看[文档](https://the-pocket.github.io/PocketFlow/)。了解动机，请阅读[故事](https://zacharyhuang.substack.com/p/i-built-an-llm-framework-in-just)。
  
- 🎉 加入我们的[Discord](https://discord.gg/hUHHE9Sa6T)！

- 🎉 感谢[@zvictor](https://www.github.com/zvictor)、[@jackylee941130](https://www.github.com/jackylee941130)和[@ZebraRoy](https://www.github.com/ZebraRoy)，我们现在有了[TypeScript版本](https://github.com/The-Pocket/PocketFlow-Typescript)！

## 为什么选择Pocket Flow？

当前的LLM框架过于臃肿...LLM框架只需要100行代码！

<div align="center">
  <img src="https://github.com/The-Pocket/.github/raw/main/assets/meme.jpg" width="400"/>


  |                | **抽象**          | **应用特定包装器**                                      | **供应商特定包装器**                                    | **代码行数**       | **大小**    |
|----------------|:-----------------------------: |:-----------------------------------------------------------:|:------------------------------------------------------------:|:---------------:|:----------------------------:|
| LangChain  | 智能体, 链               | 很多 <br><sup><sub>(例如，问答，摘要)</sub></sup>              | 很多 <br><sup><sub>(例如，OpenAI, Pinecone等)</sub></sup>                   | 405K          | +166MB                     |
| CrewAI     | 智能体, 链            | 很多 <br><sup><sub>(例如，FileReadTool, SerperDevTool)</sub></sup>         | 很多 <br><sup><sub>(例如，OpenAI, Anthropic, Pinecone等)</sub></sup>        | 18K           | +173MB                     |
| SmolAgent   | 智能体                      | 一些 <br><sup><sub>(例如，CodeAgent, VisitWebTool)</sub></sup>         | 一些 <br><sup><sub>(例如，DuckDuckGo, Hugging Face等)</sub></sup>           | 8K            | +198MB                     |
| LangGraph   | 智能体, 图           | 一些 <br><sup><sub>(例如，语义搜索)</sub></sup>                     | 一些 <br><sup><sub>(例如，PostgresStore, SqliteSaver等) </sub></sup>        | 37K           | +51MB                      |
| AutoGen    | 智能体                | 一些 <br><sup><sub>(例如，工具智能体，聊天智能体)</sub></sup>              | 很多 <sup><sub>[可选]<br> (例如，OpenAI, Pinecone等)</sub></sup>        | 7K <br><sup><sub>(仅核心)</sub></sup>    | +26MB <br><sup><sub>(仅核心)</sub></sup>          |
| **PocketFlow** | **图**                    | **无**                                                 | **无**                                                  | **100**       | **+56KB**                  |

</div>

## Pocket Flow如何工作？

这[100行代码](https://github.com/The-Pocket/PocketFlow/blob/main/pocketflow/__init__.py)捕捉了LLM框架的核心抽象：图！
<br>
<div align="center">
  <img src="https://github.com/The-Pocket/.github/raw/main/assets/abstraction.png" width="900"/>
</div>
<br>

从此出发，很容易实现流行的设计模式，如([多](https://the-pocket.github.io/PocketFlow/design_pattern/multi_agent.html))[智能体](https://the-pocket.github.io/PocketFlow/design_pattern/agent.html)、[工作流](https://the-pocket.github.io/PocketFlow/design_pattern/workflow.html)、[RAG](https://the-pocket.github.io/PocketFlow/design_pattern/rag.html)等。
<br>
<div align="center">
  <img src="https://github.com/The-Pocket/.github/raw/main/assets/design.png" width="900"/>
</div>
<br>
✨ 以下是基础教程：

<div align="center">
  
|  名称  | 难度    |  描述  |  
| :-------------:  | :-------------: | :--------------------- |  
| [聊天](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-chat) | ☆☆☆ <br> *极简*   | 具有对话历史的基础聊天机器人 |
| [结构化输出](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-structured-output) | ☆☆☆ <br> *极简* | 通过提示从简历中提取结构化数据 |
| [工作流](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-workflow) | ☆☆☆ <br> *极简*   | 一个包含大纲、内容写作和风格应用的写作工作流 |
| [智能体](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-agent) | ☆☆☆ <br> *极简*   | 一个能够搜索网络并回答问题的研究智能体 |
| [RAG](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-rag) | ☆☆☆ <br> *极简*   | 一个简单的检索增强生成过程 |
| [映射-归约](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-map-reduce) | ☆☆☆ <br> *极简* | 使用映射-归约模式进行批量评估的简历资格处理器 |
| [流式处理](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-llm-streaming) | ☆☆☆ <br> *极简*   | 具有用户中断功能的实时LLM流式演示 |
| [聊天护栏](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-chat-guardrail) | ☆☆☆ <br> *极简*  | 仅处理与旅行相关查询的旅行顾问聊天机器人 |
| [多智能体](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-multi-agent) | ★☆☆ <br> *初级* | 一个用于两个智能体之间异步通信的禁忌词游戏 |
| [监督者](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-supervisor) | ★☆☆ <br> *初级* | 研究智能体变得不可靠...让我们构建一个监督流程 |
| [并行](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-parallel-batch) | ★☆☆ <br> *初级*   | 展示3倍加速的并行执行演示 |
| [并行流](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-parallel-batch-flow) | ★☆☆ <br> *初级*   | 使用多个过滤器展示8倍加速的并行图像处理演示 |
| [多数投票](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-majority-vote) | ★☆☆ <br> *初级* | 通过聚合多个解决方案尝试提高推理准确性 |
| [思考](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-thinking) | ★☆☆ <br> *初级*   | 通过思维链解决复杂推理问题 |
| [记忆](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-chat-memory) | ★☆☆ <br> *初级* | 具有短期和长期记忆的聊天机器人 |
| [MCP](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-mcp) | ★☆☆ <br> *初级* | 使用模型上下文协议进行数值运算的智能体 |

</div>

👀 想看更多极简教程？[创建一个issue！](https://github.com/The-Pocket/PocketFlow/issues/new)

## 如何使用Pocket Flow？

🚀 通过**智能体编程**——最快的LLM应用开发范式，其中*人类设计*而*智能体编码*！

<br>
<div align="center">
  <a href="https://zacharyhuang.substack.com/p/agentic-coding-the-most-fun-way-to" target="_blank">
    <img src="https://substackcdn.com/image/fetch/f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F423a39af-49e8-483b-bc5a-88cc764350c6_1050x588.png" width="700" alt="IMAGE ALT TEXT" style="cursor: pointer;">
  </a>
</div>
<br>

✨ 以下是更复杂LLM应用的示例：

<div align="center">
  
|  应用名称     |  难度    | 主题  | 人类设计 | 智能体代码 |
| :-------------:  | :-------------: | :---------------------: |  :---: |  :---: |
| [用Cursor构建Cursor](https://github.com/The-Pocket/Tutorial-Cursor) <br> <sup><sub>我们很快就会达到奇点...</sup></sub> | ★★★ <br> *高级*   | [智能体](https://the-pocket.github.io/PocketFlow/design_pattern/agent.html) | [设计文档](https://github.com/The-Pocket/Tutorial-Cursor/blob/main/docs/design.md) | [流程代码](https://github.com/The-Pocket/Tutorial-Cursor/blob/main/flow.py)
| [咨询AI Paul Graham](https://github.com/The-Pocket/Tutorial-YC-Partner) <br> <sup><sub>咨询AI版Paul Graham，以防你未被录取</sup></sub> | ★★☆ <br> *中级*   | [RAG](https://the-pocket.github.io/PocketFlow/design_pattern/rag.html) <br> [映射-归约](https://the-pocket.github.io/PocketFlow/design_pattern/mapreduce.html) <br> [TTS](https://the-pocket.github.io/PocketFlow/utility_function/text_to_speech.html) | [设计文档](https://github.com/The-Pocket/Tutorial-AI-Paul-Graham/blob/main/docs/design.md) | [流程代码](https://github.com/The-Pocket/Tutorial-AI-Paul-Graham/blob/main/flow.py)
| [Youtube摘要器](https://github.com/The-Pocket/Tutorial-Youtube-Made-Simple)  <br> <sup><sub> 像对五岁孩子一样向你解释YouTube视频 </sup></sub> | ★☆☆ <br> *初级*   | [映射-归约](https://the-pocket.github.io/PocketFlow/design_pattern/mapreduce.html) |  [设计文档](https://github.com/The-Pocket/Tutorial-Youtube-Made-Simple/blob/main/docs/design.md) | [流程代码](https://github.com/The-Pocket/Tutorial-Youtube-Made-Simple/blob/main/flow.py)
| [冷启动生成器](https://github.com/The-Pocket/Tutorial-Cold-Email-Personalization)  <br> <sup><sub> 即时破冰器，让冷门线索变热门 </sup></sub> | ★☆☆ <br> *初级*   | [映射-归约](https://the-pocket.github.io/PocketFlow/design_pattern/mapreduce.html) <br> [网络搜索](https://the-pocket.github.io/PocketFlow/utility_function/websearch.html) |  [设计文档](https://github.com/The-Pocket/Tutorial-Cold-Email-Personalization/blob/master/docs/design.md) | [流程代码](https://github.com/The-Pocket/Tutorial-Cold-Email-Personalization/blob/master/flow.py)

</div>

- 想学习**智能体编程**？

  - 查看[我的YouTube](https://www.youtube.com/@ZacharyLLM?sub_confirmation=1)，了解上述应用如何制作的视频教程！

  - 想构建自己的LLM应用？阅读这篇[文章](https://zacharyhuang.substack.com/p/agentic-coding-the-most-fun-way-to)！从[这个模板](https://github.com/The-Pocket/PocketFlow-Template-Python)开始！

  - 想了解详细步骤？阅读这份[指南](https://the-pocket.github.io/PocketFlow/guide.html)！