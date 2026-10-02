---
type: resource
kind: youtube
title: "AI Agents, Clearly Explained"
author: Jeff Su
url:                     # TODO: add video link
status: done
rating: 5                # loved how clearly he explains
topics: [llm, ai-workflows, ai-agents, rag, mcp, agent-skills, ai-memory]
added: 2026-10-02
transcript:              # TODO: paste transcript into resources/transcripts/
---

# AI Systems Fundamentals: LLMs, Workflows, and Agents

Source inspiration: **Jeff Su — “AI Agents, Clearly Explained”**

This note is designed to be a **master reference** for understanding the three major levels of modern AI systems:

1. Large Language Models
2. AI Workflows
3. AI Agents

The key difference between them is **who makes the decisions** and **how much freedom the system has to act**.

---

# The Big Picture

AI systems can be understood as an evolution:

```text
LLM
↓
AI Workflow
↓
AI Agent
```

Another useful way to think about it:

```text
LLM        = Answer
Workflow   = Follow Steps
Agent      = Achieve a Goal
```

The more advanced the system becomes, the more responsibility shifts from the human to the AI.

---

# Level 1 — Large Language Models

## What is an LLM?

A Large Language Model is an AI model trained on large amounts of text and other data so it can understand and generate language.

Examples include:

- GPT
- Claude
- Gemini
- Llama

At its simplest, an LLM takes an input and produces an output.

```text
Human Prompt
     ↓
    LLM
     ↓
  Response
```

## Main Characteristic

The model is mostly **passive**.

It waits for you to give it a prompt, processes that prompt, and returns an answer.

```text
Prompt → Response
Prompt → Response
Prompt → Response
```

The human remains responsible for deciding what happens next.

## Example

You ask:

```text
Write an email asking someone for a coffee chat.
```

The LLM can generate the email.

But if you ask:

```text
When is my next coffee chat?
```

a standalone LLM cannot know that unless it has access to your calendar or another external source.

## Limitation

A basic LLM does not automatically have access to:

- Your calendar
- Your email
- Your files
- Private databases
- Live websites
- Company systems
- APIs

It only knows the information available in its model context and whatever you provide to it.

---

# Level 2 — AI Workflows

## What is an AI Workflow?

An AI workflow connects an LLM to tools and places the model inside a **predefined process**.

The human designs the process.

```text
Trigger
   ↓
Step 1
   ↓
Step 2
   ↓
LLM
   ↓
Step 3
   ↓
Output
```

The AI may perform powerful tasks, but the overall path was designed ahead of time.

## Example

A newsletter automation might look like this:

```text
Every Monday at 8:00 AM
        ↓
Search for AI news
        ↓
Send articles to an LLM
        ↓
Summarize the articles
        ↓
Generate newsletter content
        ↓
Create HTML email
        ↓
Send newsletter
```

The system is automated, but it follows a path that the developer already created.

## Who Makes the Decisions?

The **human programmer**.

The human decides:

- Which tools exist
- Which tool runs first
- What happens after each step
- What conditions trigger another step
- What happens if something fails

The LLM usually performs tasks inside that structure.

---

# Tools and APIs

AI workflows become much more powerful when the LLM can access external tools.

Examples:

```text
LLM
 ├── Web Search
 ├── Google Calendar
 ├── Gmail
 ├── Database
 ├── GitHub
 ├── Weather API
 ├── Slack
 └── Local Files
```

Tools allow the model to interact with information outside of its original training data.

---

# RAG — Retrieval-Augmented Generation

## What is RAG?

RAG stands for:

```text
Retrieval-Augmented Generation
```

Instead of forcing an LLM to answer only from its internal knowledge, the system first retrieves relevant information.

```text
Question
   ↓
Search Knowledge Base
   ↓
Retrieve Relevant Information
   ↓
Give Information to LLM
   ↓
Generate Answer
```

## Example

Imagine you have 1,000 company documents.

You ask:

```text
What is our refund policy?
```

The system:

1. Searches the company knowledge base.
2. Finds the refund policy.
3. Sends the relevant section to the LLM.
4. The LLM answers using that information.

The model does not need to memorize all 1,000 documents.

## Important Idea

RAG is usually part of a workflow.

```text
Retrieve → Add Context → Generate
```

---

# Workflow Limitation

A workflow normally follows the path the developer created.

For example:

```text
If calendar question:
    search Google Calendar
```

This works for:

```text
When is my meeting?
```

But the user might ask:

```text
What will the weather be during my meeting?
```

If the workflow was only designed to search the calendar, it may fail.

The system does not automatically decide:

```text
I should check the calendar,
find the meeting location and date,
then use a weather API.
```

That leads to the next level.

---

# Level 3 — AI Agents

## What is an AI Agent?

An AI agent is a system where the **LLM becomes part of the decision-making engine**.

Instead of being given every step, the agent is given a goal.

```text
Human Goal
    ↓
   Agent
    ↓
Decide What To Do
    ↓
Use Tools
    ↓
Observe Results
    ↓
Adjust Plan
    ↓
Continue Until Goal Is Reached
```

The critical shift is:

```text
Workflow:
Human decides the steps.

Agent:
AI decides the steps.
```

---

# Goal-Oriented Behavior

A workflow receives instructions like:

```text
Step 1: Search Google.
Step 2: Summarize results.
Step 3: Write a post.
Step 4: Save it.
```

An agent may simply receive:

```text
Create a high-quality LinkedIn post about today's biggest AI development.
```

The agent can decide:

1. Search for current AI news.
2. Compare several sources.
3. Select the most important story.
4. Research the topic.
5. Draft the post.
6. Review the draft.
7. Improve the writing.
8. Produce the final result.

The developer did not have to explicitly program every individual decision.

---

# ReAct — Reason + Act

A common concept behind agents is **ReAct**.

```text
Reason
+
Act
```

The agent repeatedly alternates between thinking about what to do and taking action.

```text
Reason
   ↓
Action
   ↓
Observation
   ↓
Reason
   ↓
Action
   ↓
Observation
```

This forms an agent loop.

---

# The Agent Loop

A simplified agent loop looks like this:

```text
Goal
 ↓
Plan
 ↓
Action
 ↓
Tool
 ↓
Observation
 ↓
Evaluate
 ↓
Next Action
 ↓
Repeat
```

The loop continues until the agent believes the goal has been achieved or another stopping condition is reached.

---

# Tools Make Agents Powerful

An LLM by itself mainly generates information.

An agent becomes much more capable when it can use tools.

```text
Agent
 ├── Browser
 ├── Search
 ├── Terminal
 ├── Python
 ├── APIs
 ├── Databases
 ├── Files
 ├── Email
 ├── Calendar
 └── Other Agents
```

The LLM acts as the decision-making layer.

The tools perform the actual actions.

A useful mental model is:

```text
LLM = Brain
Tools = Hands
Memory = Long-Term Context
Agent Loop = Decision Process
```

---

# Self-Correction and Critique Loops

Agents can also evaluate their own work.

For example:

```text
Generate Draft
      ↓
Critique Draft
      ↓
Identify Problems
      ↓
Improve Draft
      ↓
Critique Again
      ↓
Final Output
```

This is sometimes called:

- Reflection
- Critique
- Self-correction
- Evaluation loop

The important idea is that the system does not automatically accept its first answer.

---

# Example: Social Media Agent

Instead of building this fixed workflow:

```text
Search → Summarize → Write Post
```

you could give an agent the goal:

```text
Create a high-performing social media post about today's most important AI story.
```

The agent might decide to:

```text
Search AI news
      ↓
Compare sources
      ↓
Choose a topic
      ↓
Research the topic
      ↓
Draft post
      ↓
Critique post
      ↓
Rewrite post
      ↓
Check platform style
      ↓
Final post
```

The exact path can change depending on what the agent discovers.

---

# Example: AI Vision Agent

A more advanced agent might receive the task:

```text
Find every clip containing a skier.
```

The agent can reason about what defines a skier:

```text
Person
+
Skis
+
Snow
+
Skiing motion
```

Then it can inspect video footage, identify matching frames, index the clips, and return the relevant footage.

The important point is that the system is working toward a **goal**, not simply responding to a single text prompt.

---

# LLM vs Workflow vs Agent

| Concept | LLM | AI Workflow | AI Agent |
|---|---|---|---|
| Main purpose | Generate | Automate | Achieve goals |
| Decision maker | Human | Human | AI + human constraints |
| Path | Prompt → answer | Predetermined | Dynamic |
| Tool use | Optional | Yes | Yes |
| Can change strategy | Limited | Usually no | Yes |
| Can loop | Usually no | Only if programmed | Yes |
| Self-correction | Limited | Programmed | Can be autonomous |
| Best for | Questions and content | Repeatable processes | Complex dynamic tasks |

---

# The Simplest Mental Model

Remember this:

```text
LLM
"I can answer."

Workflow
"I can follow the process."

Agent
"I can figure out how to reach the goal."
```

---

# Automation vs Agent

This distinction is important.

## Automation

```text
When X happens:
Do A
Then B
Then C
```

The logic is predetermined.

## Agent

```text
Goal: Accomplish X

AI:
What should I do first?
Which tool should I use?
Did it work?
What should I do next?
```

The agent dynamically determines the path.

---

# Agents Still Need Constraints

Agents are not completely unrestricted.

Good agent systems usually define:

```text
Goal
Tools
Rules
Permissions
Memory
Stopping Conditions
Evaluation Criteria
```

For example:

```text
Goal:
Find security vulnerabilities.

Tools:
Browser
Terminal
Code search

Rules:
Do not modify production data.

Stopping condition:
Complete the security report.
```

This structure keeps the agent useful and predictable.

---

# Memory

Memory allows an AI system to retain useful information across interactions or tasks.

Without memory:

```text
Session 1 → Knowledge lost
Session 2 → Start again
```

With memory:

```text
Session 1
   ↓
Important information saved
   ↓
Session 2
   ↓
Relevant information retrieved
```

Memory can include:

- User preferences
- Project decisions
- Previous tasks
- Code architecture
- Research
- Errors and fixes
- Long-term goals

Memory is one of the components that makes advanced agent systems much more useful.

---

# Agent Skills

Agent Skills are reusable instruction packages that teach an AI agent **how to perform a specific type of task**.

Examples:

```text
Frontend Design Skill
Security Audit Skill
Video Creation Skill
Code Review Skill
RFP Analysis Skill
Research Skill
```

Instead of rewriting the same instructions every time, the agent loads the relevant skill when needed.

A useful mental model:

```text
LLM = Brain
Tools = Hands
Skills = Expertise
Memory = Experience
Agents = Workers
Workflows = Processes
```

---

# MCP

MCP stands for:

```text
Model Context Protocol
```

MCP is a standard that allows AI systems to connect to external tools, services, and data sources.

Conceptually:

```text
Claude
   ↓
MCP
   ↓
GitHub
Database
Browser
Files
Slack
Other Systems
```

MCP does not automatically make something an agent.

It gives the AI **capabilities**.

The agent decides how and when to use those capabilities.

---

# APIs

An API lets software communicate with another service.

Example:

```text
Your AI App
    ↓
OpenAI API
    ↓
GPT Model
```

Or:

```text
Agent
   ↓
Weather API
   ↓
Weather Data
```

APIs are one of the main ways workflows and agents interact with external services.

---

# How Everything Fits Together

A modern AI system can contain all of these pieces:

```text
                USER GOAL
                    ↓
                 AGENT
                    ↓
            ┌───────┴────────┐
            ↓                ↓
        REASONING          MEMORY
            ↓
          SKILLS
            ↓
          TOOLS
            ↓
     ┌──────┼─────────┐
     ↓      ↓         ↓
    MCP    APIs       RAG
     ↓      ↓         ↓
 GitHub   Services  Knowledge
 Browser             Base
 Files
```

The LLM is at the center, but the surrounding systems make it capable of doing real work.

---

# A Practical AI System Stack

When looking at an AI project, ask these questions:

## 1. What model is being used?

Examples:

```text
GPT
Claude
Gemini
Llama
```

## 2. What is the goal?

```text
Generate content?
Research?
Code?
Analyze?
Automate?
```

## 3. What tools can the AI use?

```text
Browser
Terminal
Database
APIs
Files
Email
Calendar
```

## 4. Is the process fixed or dynamic?

```text
Fixed → Workflow
Dynamic → Agent
```

## 5. Does it have memory?

```text
Temporary context?
Persistent project memory?
User memory?
```

## 6. Does it have reusable skills?

```text
Coding
Security
Design
Research
Video
Business workflows
```

## 7. Does it evaluate its own output?

```text
Critique
Tests
Review
Verification
Reflection
```

These questions make it much easier to understand almost any modern AI system.

---

# Knowledge Base Summary

The concepts in this document form the foundation for understanding modern AI development.

```text
LLM
↓
Tools
↓
APIs / MCP
↓
RAG
↓
Workflows
↓
Agents
↓
Memory
↓
Skills
↓
Multi-Agent Systems
```

You do not need to memorize every framework.

Focus on understanding the architecture.

When you see a new AI product, ask:

```text
What is the model?

What tools does it have?

Who decides the next step?

Does it have memory?

Does it use a fixed workflow or an agent loop?

How does it evaluate whether the task succeeded?
```

If you can answer those questions, you can usually understand how the system works.

---

# One-Line Definitions

**LLM:** A model that understands and generates language.

**API:** A way for software systems to communicate.

**Tool:** An external capability an AI can use.

**RAG:** Retrieve relevant information before generating an answer.

**Workflow:** A predefined sequence of automated steps.

**Agent:** An AI system that dynamically decides how to achieve a goal.

**ReAct:** A loop where an agent reasons, acts, observes, and repeats.

**Memory:** Information retained and retrieved across interactions.

**Skill:** Reusable instructions or expertise an agent can load.

**MCP:** A standard way for AI systems to connect to tools and data.

**Critique Loop:** A process where AI evaluates and improves its own output.

**Multi-Agent System:** Multiple specialized agents working together toward a larger goal.
