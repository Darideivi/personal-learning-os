# Personal Learning OS — LearnHouse Master Plan

> **Project role:** This file is the single source of truth for the project.  
> Claude Code should read this file before making major product, architecture, UI, database, or AI decisions.

---

# 1. Product Vision

Build a **Personal Learning OS** on top of LearnHouse.

This is more than a traditional LMS. It should become a long-term system for capturing, organizing, reviewing, connecting, and applying everything I learn from:

- YouTube videos
- Online courses
- Certifications
- Documentation
- GitHub repositories
- Books and articles
- Cybersecurity labs
- AI experiments
- Software projects
- Home-lab work
- Work-related technical learning
- Notes and personal explanations

The core goal is simple:

> **Everything I learn should become reusable knowledge instead of disappearing after I finish a video, course, lab, or project.**

The product should combine:

```text
Learning Management System
+
Personal Knowledge Base
+
Progress Tracker
+
Project Journal
+
AI Tutor
+
Knowledge Graph
+
Technical Reference Library
```

---

# 2. Foundation

Use:

```text
LearnHouse
https://github.com/learnhouse/learnhouse
```

LearnHouse is the foundation rather than starting from an empty application.

Current architecture:

```text
Frontend
Next.js + React + Tailwind + Tiptap

Backend
Python + FastAPI + SQLModel + Alembic

Database
PostgreSQL + pgvector

Realtime
Hocuspocus + Yjs + WebSockets

Cache / State
Redis

AI
Provider-agnostic LLM layer
Pydantic AI
LlamaIndex
pgvector RAG

Infrastructure
Docker
LearnHouse CLI
```

The project is especially valuable because working on it teaches technologies I actively want to learn:

```text
Python
JavaScript / TypeScript
React
Next.js
FastAPI
PostgreSQL
APIs
Docker
Redis
RAG
Embeddings
AI Agents
CI/CD
Testing
```

---

# 3. Important Product Principle

Do **not** treat LearnHouse as something to completely rewrite.

First:

```text
Install
↓
Run
↓
Explore
↓
Understand
↓
Document
↓
Modify
```

Only replace parts of the system when there is a clear reason.

The project itself should be a learning exercise.

---

# 4. Installation

## Requirements

Recommended local environment:

```text
Docker Engine 20.10+
Docker Compose 2+
Node.js 18+
npm 8+
Git
```

For Windows, use:

```text
Windows
+
WSL2
+
Docker Desktop
```

Recommended development machine:

```text
4 GB+ RAM available to the stack
20 GB+ free disk space
```

---

# 5. Clone the Source Code

```bash
git clone https://github.com/learnhouse/learnhouse.git
cd learnhouse
```

Start the development environment:

```bash
npx learnhouse dev
```

This is the preferred setup for modifying the codebase.

It starts the local development services including:

```text
PostgreSQL
Redis
FastAPI API
Next.js Web App
Collaboration Server
```

with hot reload.

---

# 6. Self-Hosted Installation

If I only want to run LearnHouse before modifying it:

```bash
npx learnhouse@latest setup
```

Useful commands:

```bash
npx learnhouse start
npx learnhouse stop
npx learnhouse status
npx learnhouse logs
npx learnhouse doctor
npx learnhouse health
npx learnhouse backup
npx learnhouse update
```

The CLI handles:

```text
Docker Compose
Environment variables
Database configuration
Admin account
Reverse proxy
Backups
Updates
Health checks
```

---

# 7. Learn the Existing Architecture First

Before adding major features, understand these folders:

```text
learnhouse/
│
├── apps/
│   ├── web/
│   │   └── Next.js frontend
│   │
│   ├── api/
│   │   └── FastAPI backend
│   │
│   ├── collab/
│   │   └── realtime editing
│   │
│   └── cli/
│       └── LearnHouse command-line tools
│
├── docker/
│
└── Dockerfile
```

Learning goal:

```text
User
 ↓
Next.js
 ↓
FastAPI
 ↓
PostgreSQL
```

Also understand:

```text
Next.js
   ↓
API
   ↓
Redis
   ↓
PostgreSQL + pgvector
```

---

# 8. What We Keep From LearnHouse

Keep LearnHouse's strongest existing concepts.

## Courses

```text
Course
 ↓
Chapter
 ↓
Activity / Lesson
```

Use courses to organize major subjects.

Examples:

```text
AI Engineering
Python
JavaScript
Cybersecurity
Microsoft Entra ID
Docker & DevOps
Networking
Git & GitHub
Claude Code
Home Lab
```

---

# 9. Collections

Use collections to group related learning.

Example:

```text
AI Engineer Path
├── AI Fundamentals
├── Python
├── APIs
├── RAG
├── Agents
└── Automation
```

Another:

```text
Cybersecurity Path
├── Networking
├── IAM
├── Entra ID
├── Sentinel
├── Defender
└── Threat Hunting
```

---

# 10. Content Types

The system should support learning material from multiple sources.

Core content types:

```text
Article
Note
Video
YouTube Video
PDF
Documentation
GitHub Repository
Course
Lab
Project
Quiz
Code Exercise
Command Reference
External Resource
```

---

# 11. The Most Important New Workflow — Capture Learning

Create an easy **Add Learning** workflow.

The first interaction should be simple:

```text
+ Add Learning
```

Then choose:

```text
YouTube
Article
Course
PDF
GitHub Repo
Note
Project
Documentation
Lab
```

This is one of the highest-priority custom features.

---

# 12. YouTube Learning Workflow

YouTube is a major source of learning.

Desired flow:

```text
Paste YouTube URL
      ↓
Save video
      ↓
Fetch metadata
      ↓
Retrieve transcript
      ↓
AI creates summary
      ↓
Extract concepts
      ↓
Create notes
      ↓
Generate questions
      ↓
Connect concepts
      ↓
Add to knowledge graph
```

Store:

```text
Title
Channel
URL
Thumbnail
Transcript
Summary
Key Concepts
My Notes
Important Timestamps
Questions
Related Topics
Learning Status
```

The AI-generated content must remain editable.

---

# 13. Quick Capture Inbox

Create an Inbox.

The Inbox should allow me to save something immediately without organizing it first.

Example:

```text
YouTube URL
GitHub Repo
Article
Idea
Command
Course
PDF
```

Later:

```text
Inbox
 ↓
Review
 ↓
Summarize
 ↓
Tag
 ↓
Connect
 ↓
Move into Knowledge Base
```

This prevents useful learning material from being lost.

---

# 14. Personal Notes

Every lesson or resource should support personal notes.

Notes should support Markdown.

Example:

```markdown
## What I Learned

RAG retrieves information before sending context to the LLM.

## Important

Embeddings represent semantic meaning numerically.

## I Still Need To Learn

How chunk size affects retrieval.
```

The user's own explanation is more important than an AI-generated summary.

---

# 15. Knowledge Topics

The knowledge base should contain reusable concepts independent of courses.

Example:

```text
RAG
React
Docker
OAuth
FastAPI
Supabase
Conditional Access
Git Rebase
Vector Database
```

Each topic should contain:

```text
Definition
Why It Matters
Core Concepts
Examples
Commands
Related Topics
Resources
Projects
Lessons
My Notes
Confidence
Next Step
```

---

# 16. Knowledge Graph

A key differentiator from traditional LMS platforms.

Concepts should connect to each other.

Example:

```text
                    AI
                     │
        ┌────────────┴────────────┐
        ↓                         ↓
       RAG                      Agents
        │                         │
   Embeddings                   Tools
        │                         │
 Vector Database                MCP
        │
     pgvector
        │
   PostgreSQL
```

Software example:

```text
JavaScript
    ↓
React
    ↓
Next.js
    ↓
Frontend
    ↓
REST API
    ↓
FastAPI
    ↓
PostgreSQL
```

Security example:

```text
Identity
  ↓
Entra ID
  ↓
OAuth / OIDC
  ↓
Authentication
  ↓
Conditional Access
```

---

# 17. Graph Data Model

Start simple.

Possible relationships:

```text
Topic -> Related Topic
Topic -> Learned From -> Resource
Topic -> Used In -> Project
Topic -> Prerequisite -> Topic
Project -> Uses -> Skill
Course -> Contains -> Topic
Video -> Teaches -> Topic
Quiz -> Tests -> Topic
```

Do **not** introduce a graph database immediately.

Start with PostgreSQL relationship tables.

Consider Neo4j or another graph engine only if PostgreSQL becomes limiting.

---

# 18. Projects Are First-Class Learning Objects

Projects are one of the strongest indicators that a skill has actually been learned.

Example:

```text
Flask + Entra ID SSO Demo
```

Connect it to:

```text
Python
Flask
OAuth
OIDC
Microsoft Entra ID
Authentication
Sessions
Environment Variables
Git
```

Project page:

```text
What I Built
Why I Built It
Technologies
Problems Encountered
How I Fixed Them
What I Learned
Screenshots
GitHub Repo
Related Concepts
Next Improvements
```

---

# 19. Learn by Building

The app must recognize real usage.

Learning loop:

```text
Learn
 ↓
Build
 ↓
Document
 ↓
Review
 ↓
Practice
 ↓
Explain
 ↓
Improve
```

The app should reward evidence rather than only lesson completion.

---

# 20. Progress System

Avoid misleading percentages.

Use:

```text
Not Started
Learning
Practicing
Comfortable
Confident
```

Evidence can come from:

```text
Read content
Completed quiz
Completed lab
Used skill in project
Explained concept
Reviewed later
```

Projects and labs should count more heavily than simply opening a lesson.

---

# 21. Mastery

Eventually calculate topic mastery from several signals.

Example:

```text
Docker

Understanding      Strong
Commands           Strong
Volumes            Strong
Networking         Developing
Docker Compose     Comfortable
Real Project Use   Strong
```

This is more useful than:

```text
Docker — 82%
```

---

# 22. Spaced Repetition

Later add review scheduling.

Example:

```text
Today

Review:
- Docker networking
- OAuth authorization code flow
- React state
- RAG embeddings
```

The system should identify topics that have not been reviewed recently.

---

# 23. Active Recall

Allow AI-generated and manual questions.

Example:

```text
What is the difference between a Docker image and container?

Why does RAG use embeddings?

What is the difference between authentication and authorization?

What problem does React state solve?
```

The goal is understanding rather than memorization.

---

# 24. AI Tutor

LearnHouse already provides AI infrastructure.

Build a personalized tutor on top of it.

The tutor should answer questions such as:

```text
Explain RAG using concepts I already understand.

Quiz me on Docker.

What should I learn next?

Where have I used OAuth?

Explain FastAPI vs Flask.

What did I learn from the AI Agents video?

Which concepts have I not reviewed recently?
```

The tutor should use my own learning data.

---

# 25. RAG

LearnHouse already includes a RAG foundation using:

```text
LlamaIndex
+
pgvector
+
PostgreSQL
```

Use this rather than introducing another vector database initially.

Desired architecture:

```text
Notes
Videos
Transcripts
Courses
Projects
Documents
       ↓
   Chunking
       ↓
  Embeddings
       ↓
   pgvector
       ↓
 Retrieval
       ↓
   AI Tutor
```

---

# 26. AI Providers

LearnHouse's current AI layer can use multiple providers.

Examples:

```text
OpenAI
Anthropic
Google
DeepSeek
Mistral
OpenRouter
Ollama
```

Keep provider selection configurable.

Do not tightly couple custom features to one model provider.

---

# 27. Personal AI Tutor Memory

Eventually give the tutor learning context such as:

```text
Current focus
Completed courses
Projects
Known concepts
Weak concepts
Recent notes
Upcoming certification
Learning goals
```

Example:

```text
User asks:
"Explain Kubernetes."

Tutor knows:
Docker = Comfortable
Linux = Comfortable
Networking = Intermediate

Tutor explains Kubernetes using Docker concepts.
```

---

# 28. Main Learning Domains

Initial categories:

## AI

```text
LLMs
Prompting
APIs
RAG
Embeddings
Vector Databases
Agents
MCP
Tools
Memory
Skills
Automation
Evaluations
```

## Python

```text
Fundamentals
OOP
Virtual Environments
APIs
Flask
FastAPI
Django
Automation
Testing
```

## JavaScript / TypeScript

```text
JavaScript Fundamentals
DOM
Async / Await
npm
TypeScript
React
Next.js
```

## Backend

```text
Flask
FastAPI
Django
REST
Authentication
PostgreSQL
Supabase
Redis
```

## Frontend

```text
HTML
CSS
JavaScript
React
Next.js
Tailwind
UI / UX
Accessibility
```

## DevOps

```text
Linux
Bash
Docker
Docker Compose
CI/CD
GitHub Actions
Deployment
Monitoring
Grafana
```

## Cybersecurity

```text
Networking
IAM
Entra ID
OAuth
OIDC
SAML
Conditional Access
Sentinel
Defender
KQL
Threat Hunting
Vulnerability Management
```

## Home Lab

```text
Linux
Docker
Networking
Storage
Jellyfin
Grafana
n8n
Remote Access
```

---

# 29. Dashboard

The dashboard should answer:

```text
What am I learning?
What should I continue?
What have I learned recently?
What needs review?
What am I building?
```

Suggested layout:

```text
┌──────────────────────────────────────────────┐
│ Welcome Back                                │
│ Continue where you left off                 │
├──────────────────┬───────────────────────────┤
│ Current Focus    │ Continue Learning         │
│                  │                           │
│ AI Agents        │ Docker Networking         │
│ SC-300           │ React State               │
│ Python           │ RAG Embeddings            │
├──────────────────┼───────────────────────────┤
│ Review Today     │ Active Projects           │
├──────────────────┴───────────────────────────┤
│ Recent Learning                              │
├──────────────────────────────────────────────┤
│ Learning Domains                             │
└──────────────────────────────────────────────┘
```

---

# 30. Main Navigation

Keep navigation simple.

```text
Dashboard
Learn
Knowledge
Projects
Roadmaps
Inbox
Resources
Progress
```

Later:

```text
Quiz
Knowledge Graph
AI Tutor
```

---

# 31. Search

Search is critical.

One search box should eventually find:

```text
Topics
Courses
Videos
Notes
Commands
Projects
Resources
Transcripts
```

Examples:

```text
OAuth
Docker volume
KQL failed login
React state
RAG chunking
```

---

# 32. Resource Library

Resources should attach to concepts.

Resource types:

```text
YouTube
Course
Article
Documentation
GitHub
PDF
Book
Lab
Tool
```

Avoid one giant bookmark collection.

A resource should explain:

```text
What it teaches
Topics
Status
Notes
Rating / usefulness
Where I found it
```

---

# 33. Commands / Cheat Sheets

Technical topics should have command references.

Example:

## Docker

```bash
docker ps
docker images
docker compose up -d
docker compose down
```

## Git

```bash
git status
git add .
git commit -m "message"
git push
```

## Python

```bash
python -m venv .venv
pip install -r requirements.txt
```

Commands should be searchable.

---

# 34. Roadmaps

Create visual learning paths.

Example:

## AI Engineer

```text
Python
 ↓
APIs
 ↓
LLMs
 ↓
Prompting
 ↓
Structured Outputs
 ↓
Tool Calling
 ↓
RAG
 ↓
Agents
 ↓
Memory
 ↓
Evaluations
```

## Frontend

```text
HTML
 ↓
CSS
 ↓
JavaScript
 ↓
React
 ↓
TypeScript
 ↓
Next.js
```

## DevOps

```text
Linux
 ↓
Git
 ↓
Docker
 ↓
Docker Compose
 ↓
CI/CD
 ↓
GitHub Actions
 ↓
Monitoring
```

---

# 35. Learning Journal

Create a daily/weekly learning log.

Example:

```text
October 2

Learned:
- Difference between workflows and agents
- LearnHouse architecture
- RAG uses retrieval before generation

Built:
- Learning Center project plan

Questions:
- How should transcripts be chunked?
- Should knowledge graph relationships be AI-generated?
```

---

# 36. Weekly Review

Eventually generate:

```text
This Week

5 topics learned
3 videos completed
2 projects updated
4 topics need review

Strongest growth:
AI Agents

Needs practice:
JavaScript async/await

Suggested next:
RAG embeddings
```

---

# 37. UI / UX Direction

Keep LearnHouse's modern design language.

Desired feel:

```text
Linear
Vercel
GitHub
Notion
Modern developer documentation
```

Principles:

- Clean
- Professional
- Minimal
- Fast
- Strong typography
- Dark mode
- Excellent search
- Clear spacing
- Avoid excessive gradients
- Avoid excessive cards
- Avoid childish gamification
- Avoid clutter

This is a technical learning environment.

---

# 38. Mobile

Mobile does not need feature parity initially.

Mobile priority:

```text
Watch
Read
Take notes
Review
Quiz
Search
```

Desktop priority:

```text
Create
Organize
Build courses
Manage projects
Knowledge graph
Admin
```

---

# 39. MVP

Do not build the entire vision at once.

## Phase 0 — Understand LearnHouse

Goals:

```text
Install repository
Run development environment
Explore UI
Understand database
Understand API
Understand editor
Understand current AI/RAG
```

Do not make major architecture changes yet.

---

# 40. Phase 1 — Personalize the LMS

Build:

```text
Personal dashboard
Learning domains
Custom branding
Personal navigation
Projects
Resource library
Personal notes
Inbox
```

Goal:

Make LearnHouse useful as a personal learning platform before adding complex AI.

---

# 41. Phase 2 — Capture System

Build:

```text
YouTube ingestion
Transcript storage
AI summaries
Concept extraction
Resource tagging
Markdown notes
GitHub resource ingestion
```

Goal:

Make saving new knowledge extremely easy.

---

# 42. Phase 3 — Knowledge System

Build:

```text
Topic pages
Topic relationships
Knowledge graph
Projects ↔ skills
Resources ↔ topics
Learning paths
Advanced search
```

Goal:

Turn isolated learning material into connected knowledge.

---

# 43. Phase 4 — Learning Intelligence

Build:

```text
AI Tutor
RAG over personal content
Automatic quizzes
Active recall
Mastery signals
Spaced repetition
Next-topic recommendations
```

Goal:

Help me retain what I learn.

---

# 44. Phase 5 — Automation

Possible workflows:

```text
YouTube URL
→ Transcript
→ Summary
→ Concepts
→ Questions
→ Knowledge graph
```

```text
GitHub Repo
→ README
→ Architecture summary
→ Important technologies
→ Learning topics
```

```text
Completed Project
→ Extract skills
→ Update topic mastery
→ Generate reflection questions
```

---

# 45. Phase 6 — Multi-User

Only after the personal product is excellent.

Potential additions:

```text
Profiles
Public courses
Shared roadmaps
Study groups
Community content
Instructor mode
Public knowledge collections
```

Personal-first remains the design principle.

---

# 46. Data We May Add

Likely new domain objects:

```text
Topic
Resource
Project
LearningLog
Review
TopicRelationship
UserTopicProgress
CommandReference
ExternalCourse
VideoTranscript
LearningGoal
```

Do not create all models immediately.

Create them when their feature enters the roadmap.

---

# 47. API Philosophy

Prefer adding functionality through the existing FastAPI architecture.

Keep endpoints:

```text
Small
Typed
Documented
Tested
```

Use:

```text
Pydantic
SQLModel
Alembic migrations
```

Avoid creating a second backend unless technically necessary.

---

# 48. Database Philosophy

Use LearnHouse's PostgreSQL database.

Prefer:

```text
PostgreSQL
+
pgvector
```

before introducing:

```text
Supabase
Pinecone
Neo4j
MongoDB
```

Those technologies may be studied separately without adding unnecessary production dependencies.

---

# 49. Docker Learning Goal

Because LearnHouse uses Docker, the project doubles as a Docker lab.

Learn:

```text
Images
Containers
Volumes
Networks
Dockerfiles
Docker Compose
Environment Variables
Logs
Health Checks
```

When fixing infrastructure problems, add useful lessons to the learning center.

---

# 50. Git Strategy

Create my own fork.

Suggested flow:

```text
learnhouse upstream
       ↓
my fork
       ↓
feature branch
       ↓
test
       ↓
merge
```

Add upstream:

```bash
git remote add upstream https://github.com/learnhouse/learnhouse.git
```

Check:

```bash
git remote -v
```

Keep custom work separated from upstream as cleanly as possible.

---

# 51. Licensing Note

LearnHouse Core is licensed under **AGPL-3.0**.

For personal development and learning, continue using the open-source project.

Before turning a modified version into a commercial hosted service, review the AGPL obligations and LearnHouse's separate Enterprise licensing carefully.

Do this **before** making commercial distribution decisions.

---

# 52. Claude Code Master Instruction

When Claude Code is working on this repository:

```text
You are helping build a Personal Learning OS on top of LearnHouse.

Before making major changes, read this master plan.

Do not rewrite existing LearnHouse functionality unless there is a clear technical reason.

First understand the existing implementation.

Prefer extending existing architecture and components.

The primary user is currently one person learning technical subjects through:
- courses
- YouTube
- projects
- documentation
- labs
- certifications
- GitHub repositories

The product must turn learning activity into durable, connected knowledge.

Every feature should improve at least one of:

1. Capture learning
2. Understand concepts
3. Connect knowledge
4. Practice knowledge
5. Track real progress
6. Apply knowledge through projects
7. Retrieve previously learned material

Keep architecture simple.

Do not introduce unnecessary frameworks or databases.

Use the existing:
- Next.js frontend
- FastAPI backend
- PostgreSQL
- pgvector
- Redis
- LearnHouse AI infrastructure

Build incrementally.

Favor maintainable code over clever code.

Preserve upstream compatibility when practical.

Treat projects, notes, topics, and resources as first-class learning objects.

The system should feel like a professional developer learning environment, not a children's education app.
```

---

# 53. Recommended Claude Code / Agent Skills

Do not install dozens of overlapping skills.

Use a small core set.

---

## Serena

**Purpose:** Semantic codebase navigation and editing.

This is particularly useful because LearnHouse is a large monorepo containing Python, TypeScript, React, APIs, and collaboration services.

Use Serena to understand:

```text
Functions
Classes
Symbols
References
Dependencies
```

before blindly searching large files.

Install:

```bash
uv tool install -p 3.13 serena-agent
serena init
```

---

## GitHub Spec Kit

**Purpose:** Structure major features before coding.

Use:

```text
Specification
↓
Plan
↓
Tasks
↓
Implementation
```

Good for features such as:

```text
YouTube ingestion
Knowledge graph
Learning mastery
AI tutor
```

Install:

```bash
uv tool install specify-cli
```

---

## Ponytail

**Purpose:** Prevent overengineering.

Ponytail pushes the agent to reuse:

```text
Existing LearnHouse code
Browser capabilities
Framework features
Standard libraries
Current dependencies
```

before creating new abstractions.

Install inside Claude Code:

```text
/plugin marketplace add DietrichGebert/ponytail
/plugin install ponytail@ponytail
```

---

## UI/UX Pro Max

**Purpose:** UI/UX design intelligence.

Use it when redesigning:

```text
Dashboard
Topic pages
Knowledge graph
Progress views
Learning paths
```

Install:

```bash
npx ui-ux-pro-max-cli init --ai claude
```

---

## Impeccable

**Purpose:** Audit and polish an existing interface.

Use after a feature works.

Example workflow:

```text
Build
↓
Test
↓
Impeccable audit
↓
Polish
```

Install:

```bash
npx impeccable install
```

Then:

```text
/impeccable init
```

---

## Playwright CLI

**Purpose:** Browser testing and QA.

Use it so Claude can actually verify:

```text
Navigation
Forms
Buttons
Mobile layout
Course creation
Video ingestion
Search
Login
```

Install:

```bash
npm install -g @playwright/cli@latest
playwright-cli install --skills -g
```

---

## Frontend Design

**Purpose:** Improve generated frontend quality.

Useful when creating new interfaces while staying consistent with LearnHouse.

Install:

```bash
npx skills add anthropics/claude-code --skill frontend-design
```

---

## Skill Creator

**Purpose:** Turn project workflows into reusable AI skills.

Potential future custom skills:

```text
/add-learning
/analyze-youtube
/create-topic
/project-reflection
/generate-quiz
/weekly-review
```

Install:

```bash
npx skills add anthropics/skills --skill skill-creator
```

---

# 54. Optional Skills

Do not activate everything simultaneously.

## Trail of Bits Skills

Useful when performing security reviews.

```text
/plugin marketplace add trailofbits/skills
```

---

## Strix

Useful for deeper application-security testing later.

```bash
npx skills add usestrix/strix
```

Only test systems I am authorized to test.

---

## Superpowers

Useful for very disciplined feature development.

```text
/plugin install superpowers@claude-plugins-official
```

It overlaps with Spec Kit and other engineering workflows.

Use intentionally rather than stacking every workflow system together.

---

# 55. Skills We Do Not Need Running All the Time

Avoid simultaneously using multiple tools that try to control the entire development process.

Examples:

```text
Superpowers
GStack
Agent Skills
ECC
Spec Kit
Task Master
```

They are all useful, but too many orchestration layers can create conflicting instructions.

For this project, start with:

```text
Spec Kit
Ponytail
Serena
Playwright
UI/UX Pro Max
Impeccable
Skill Creator
```

Add others only when needed.

---

# 56. Project Documentation

Keep documentation inside the repository.

Suggested:

```text
/docs
│
├── MASTER_PLAN.md
├── ARCHITECTURE_NOTES.md
├── LEARNING_LOG.md
├── FEATURE_IDEAS.md
└── DECISIONS.md
```

This file should become:

```text
/docs/MASTER_PLAN.md
```

---

# 57. Decision Log

Whenever an important architecture decision is made, capture:

```text
Decision
Why
Alternatives
Tradeoffs
Date
```

Example:

```text
Decision:
Use pgvector instead of Pinecone.

Reason:
LearnHouse already uses PostgreSQL + pgvector.

Benefit:
Less infrastructure.

Revisit when:
Vector search becomes a proven bottleneck.
```

---

# 58. Learn the Code While Building

Whenever Claude changes something significant, ask it to explain:

```text
Which files changed?
Why?
What framework concept is involved?
What should I learn from this?
```

Then save the important explanation into the Learning Center.

This creates a feedback loop:

```text
Build Learning App
      ↓
Learn Technology
      ↓
Save Knowledge
      ↓
Improve Learning App
```

---

# 59. Definition of Success

This product succeeds when I can answer:

```text
What did I learn six months ago?

Where did I learn it?

What projects used it?

How confident am I?

What have I forgotten?

What should I review?

What should I learn next?

How does this concept connect to something else I know?
```

without searching through dozens of chats, bookmarks, videos, notebooks, and GitHub repositories.

---

# 60. Ultimate Product

The long-term product should become:

> **A personal technical learning operating system that turns everything I watch, read, study, and build into organized, connected, searchable, reviewable knowledge.**

The system should transform:

```text
Information
↓
Understanding
↓
Practice
↓
Projects
↓
Knowledge
↓
Long-Term Skill
```

---

# 61. First Actions

Start here.

```text
1. Fork LearnHouse.
2. Clone my fork.
3. Run `npx learnhouse dev`.
4. Create a local admin account.
5. Explore LearnHouse without modifying it.
6. Map the Web/API/database architecture.
7. Create `/docs/MASTER_PLAN.md` from this document.
8. Create `ARCHITECTURE_NOTES.md`.
9. Identify where courses, activities, AI, and progress live in the code.
10. Only then create the first custom feature.
```

First custom feature recommendation:

```text
Personal Learning Inbox
```

Why:

It immediately solves the real problem:

> I learn something useful every day and need one frictionless place to capture it before it gets lost.

After Inbox:

```text
YouTube Capture
↓
Topic System
↓
Projects
↓
Knowledge Relationships
↓
AI Tutor / RAG
↓
Review & Mastery
```

---

# Final Principle

Do not build features simply because AI can build them.

Build features that improve this loop:

```text
CAPTURE
   ↓
LEARN
   ↓
UNDERSTAND
   ↓
BUILD
   ↓
DOCUMENT
   ↓
CONNECT
   ↓
REVIEW
   ↓
REMEMBER
```

That is the product.
