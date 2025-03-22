# Article Writing Workflow

A PocketFlow example that demonstrates an article writing workflow using a sequence of LLM calls.

## Features

- Generate a simple outline with up to 3 main sections using YAML structured output
- Process each section independently using batch processing
- Write concise (100 words max) content for each section in simple terms
- Apply a conversational, engaging style to the final article

## Getting Started

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

2. Set your OpenAI API key as an environment variable:

```bash
export OPENAI_API_KEY=your_api_key_here
```

3. Run the application with a default topic ("AI Safety"):

```bash
python main.py
```

4. Or specify your own topic:

```bash
python main.py Climate Change
```

## How It Works

The workflow consists of three sequential nodes:

```mermaid
graph LR
    Outline[Generate Outline] --> Write[Batch Write Content]
    Write --> Style[Apply Style]
```

Here's what each node does:

1. **Generate Outline**: Creates a simple outline with up to 3 main sections using YAML structured output
2. **Write Simple Content**: Processes each section in parallel (as a BatchNode), writing a concise 100-word explanation for each
3. **Apply Style**: Rewrites the combined content in a conversational, engaging style

## Files

- [`main.py`](./main.py): Main entry point for running the article workflow
- [`flow.py`](./flow.py): Defines the flow that connects the nodes
- [`nodes.py`](./nodes.py): Contains the node classes for each step in the workflow
- [`utils.py`](./utils.py): Utility functions including the LLM wrapper
- [`requirements.txt`](./requirements.txt): Lists the required dependencies

## Example Output

```
=== Starting Article Workflow on Topic: AI Safety ===


===== OUTLINE (YAML) =====

sections:
- Understanding AI Safety
- Challenges in Ensuring AI Safety
- Strategies for Mitigating AI Risks


===== PARSED OUTLINE =====

1. Understanding AI Safety
2. Challenges in Ensuring AI Safety
3. Strategies for Mitigating AI Risks

=========================

Parsed 3 sections: ['Understanding AI Safety', 'Challenges in Ensuring AI Safety', 'Strategies for Mitigating AI Risks']

===== SECTION CONTENTS =====

--- Understanding AI Safety ---
Understanding AI safety is about ensuring that artificial intelligence systems work safely and as intended. Just like you wouldn't want a car to suddenly speed up on its own, we want AI to be predictable and reliable. For example, if an AI were to help cook, we need to make sure it identifies ingredients correctly and doesn't start a fire. By focusing on AI safety, we aim to prevent accidents and ensure these systems help rather than harm us.

--- Challenges in Ensuring AI Safety ---
Making sure AI is safe involves several challenges. Imagine teaching a robot to understand commands correctly; if it misinterprets instructions, things could go wrong. It's like teaching a toddler to cross the street safely—they need to understand when and where it's safe to walk. Similarly, AI must be programmed to make safe decisions. Ensuring AI doesn't act unpredictably and behaves as intended, even in new situations, is crucial. Balancing innovation and safety is key, just like making sure a car is fast but also has reliable brakes to prevent accidents.

--- Strategies for Mitigating AI Risks ---
Mitigating AI risks is about making sure AI technologies help us without causing harm. It's like having seat belts in cars: they allow us to drive safely by minimizing dangers. To manage AI risks, we can use guidelines and rules to ensure AI behaves as expected. Training AI with diverse data is crucial so it doesn't develop biases, much like teaching children to respect different cultures. Additionally, we can create "off switches" for AI systems, similar to remote controls, to turn them off if they start acting unexpectedly. These steps help us safely enjoy the benefits AI offers.

===========================


===== FINAL ARTICLE =====

Hey there! Have you ever wondered about the safety of artificial intelligence and how it fits into our world? It's a bit like making sure a pet behaves itself—you want your dog to fetch the ball, not run off with your slippers! At its heart, understanding AI safety means ensuring these high-tech systems do what they're supposed to without causing a ruckus. Just as you wouldn't want your car to suddenly speed up without warning, we hope for AI to be as reliable as your morning coffee brewing on schedule. Imagine an AI assistant in your kitchen—it should know the difference between sugar and salt, and definitely not turn your peaceful cooking session into a fire drill. So, by focusing on AI safety, we're aiming for a world where these systems help us, without creating chaos.

Now, navigating the challenges of AI safety? That's quite the adventure! Picture this: you're trying to teach a robot your way of doing things. It's like teaching a toddler to cross a busy street. The little one needs to know when to stop, when to go, and how to manage all the things happening around them. Similarly, our AI pals need to be programmed to make safe decisions, even if they're seeing the world for the first time through their digital eyes. It's this delicate dance between innovation and safety—like crafting a sports car that's both exhilaratingly fast and equipped with top-notch brakes. We don't want surprises when it comes to AI behavior, right?

So, how do we juggle these AI risks and keep things safe? Imagine AI guidelines and protocols like the seat belts in your car—designed to keep you secure while letting you enjoy the ride. By setting rules, we ensure AI behaves as expected, kind of like a teacher maintaining order in a classroom. And just like we educate kids to appreciate the diverse world around them, we train AI with a wide array of data to avoid any unfair biases. Plus, isn't it reassuring to know we can install an "off switch" on these systems? Think of it like having a remote control to power down the device if it starts acting up. These strategies are our way of making sure we can relish the wonders of AI, all while knowing we've got everything under control.

In a nutshell, AI safety is about bridging the gap between groundbreaking technology and everyday peace of mind. It's this journey of making technology a trustworthy companion rather than a wild card. After all, it's all about enjoying the benefits without the hiccups—who wouldn't want that kind of harmony in their tech-driven life?

========================


=== Workflow Completed ===

Topic: AI Safety
Outline Length: 100 characters
Draft Length: 1707 characters
Final Article Length: 2531 characters
```

## Extending the Example

You can easily extend this example by:

1. Adding more processing nodes to the workflow
2. Modifying the prompts in the node classes
3. Implementing branching logic based on the content generated
4. Adding user interaction between workflow steps
5. Using different structured output formats (JSON, XML, etc.)
