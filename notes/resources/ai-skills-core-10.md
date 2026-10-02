---
type: resource
kind: github
title: "AI Skills: Core 10"
status: in-progress
topics: [agent-skills]
added: 2026-10-02
---

# AI Skills Knowledge Base — Core 10

Last reviewed: October 2, 2026

This is the short list I would keep as a personal AI/Claude Code skills database. I picked these based on usefulness for coding, automation, project memory, frontend design, and building your own reusable AI workflows. GitHub popularity is used as a signal, but usefulness matters more than stars alone.

> Note: Star counts change constantly and usually refer to the repository containing the skill, not the individual SKILL.md file.

---

## 1. Agent Skills — Addy Osmani

**Repo:** `addyosmani/agent-skills`  
**Popularity:** ~100K GitHub stars

**What it does:**  
A production-grade software engineering skill pack. It gives AI coding agents structured workflows for planning, building, testing, debugging, reviewing, simplifying, securing, and shipping software.

**Best for:**  
Serious coding projects where you want Claude to behave more like a disciplined software engineer instead of just generating code.

**Install:**
```bash
npx skills add addyosmani/agent-skills
```

**Useful commands:**  
`/spec` → `/plan` → `/build` → `/test` → `/review` → `/ship`

---

## 2. Skill Creator — Anthropic

**Repo:** `anthropics/skills`  
**Popularity:** ~179K GitHub stars for the official Anthropic skills repo

**What it does:**  
Helps you create, improve, test, and evaluate your own Agent Skills. This is one of the most important skills if you want to build your own reusable AI workflows.

**Best for:**  
Turning workflows you repeat into permanent skills, such as `/edit`, `/graphics`, cybersecurity workflows, RFP analysis, or business automations.

**Install:**
```bash
npx skills add anthropics/skills --skill skill-creator
```

---

## 3. Superpowers

**Repo:** `obra/superpowers`  
**Popularity:** ~290K GitHub stars

**What it does:**  
A complete software-development methodology for AI coding agents. It pushes the agent through brainstorming, planning, test-driven development, implementation, review, and verification.

**Best for:**  
Large features or projects where you want the AI to think carefully before touching the code.

**Claude Code install:**
```text
/plugin install superpowers@claude-plugins-official
```

**Important:**  
Superpowers overlaps with Agent Skills. I would normally choose one as the main engineering workflow instead of forcing both to control the same task.

---

## 4. Claude-Mem

**Repo:** `thedotmack/claude-mem`  
**Popularity:** ~95K GitHub stars

**What it does:**  
Creates persistent memory across coding sessions. It captures what the agent did, compresses the important context, and brings relevant information into future sessions.

**Best for:**  
Long-running projects where you do not want every new Claude Code session to start from zero.

**Install:**
```bash
npx claude-mem install
```

---

## 5. Graphify

**Repo:** `safishamsi/graphify`  
**Popularity:** Large and rapidly adopted open-source project

**What it does:**  
Turns a codebase, documents, PDFs, screenshots, diagrams, notes, and other project material into a queryable knowledge graph.

**Best for:**  
Understanding large projects and creating a persistent map of how files, concepts, components, and architecture connect.

**Install:**
```bash
pip install graphifyy
graphify install
```

**Use:**
```text
/graphify .
```

This is especially useful for your larger AI projects because Claude can inspect the graph instead of repeatedly searching the entire codebase.

---

## 6. Ponytail

**Repo:** `DietrichGebert/ponytail`  
**Popularity:** ~75K GitHub stars

**What it does:**  
Teaches the coding agent to aggressively prefer simpler solutions: built-in features, standard libraries, existing dependencies, and minimal code instead of unnecessary abstractions.

**Best for:**  
Preventing AI-generated overengineering and keeping vibe-coded projects maintainable.

**Claude Code install:**
```text
/plugin marketplace add DietrichGebert/ponytail
/plugin install ponytail@ponytail
```

**Mental model:**  
If the browser, standard library, framework, or existing dependency already solves the problem, do not build another system.

---

## 7. Frontend Design — Anthropic

**Repo:** `anthropics/claude-code`  
**Popularity:** ~149K GitHub stars for the Claude Code repo

**What it does:**  
Pushes Claude toward distinctive, intentional, production-quality frontend design instead of generic AI-generated layouts.

**Best for:**  
Landing pages, dashboards, portfolios, business websites, React components, and UI redesigns.

**Install:**
```bash
npx skills add anthropics/claude-code --skill frontend-design
```

Use this as a strong default whenever Claude is creating a UI from scratch.

---

## 8. Impeccable

**Repo:** `pbakaus/impeccable`  
**Popularity:** ~74K GitHub stars

**What it does:**  
A deeper frontend design system with commands for auditing, critiquing, polishing, simplifying, animating, refining, and improving an existing interface.

**Best for:**  
Taking a website that already works and pushing the visual quality much higher.

**Install:**
```bash
npx impeccable install
```

Then initialize it inside the project:
```text
/impeccable init
```

**Useful examples:**  
`/impeccable audit`  
`/impeccable critique`  
`/impeccable polish`

---

## 9. Taste Skill

**Repo:** `jeettrench/taste-skill` / `tasteskill/tasteskill`

**What it does:**  
An anti-slop frontend skill focused on premium layouts, stronger visual hierarchy, motion, layout variation, and avoiding repetitive AI design patterns.

**Best for:**  
Experiments where you want more aggressive visual creativity than a normal frontend skill gives you.

**Install:**
```bash
npx skills add https://github.com/jeettrench/taste-skill --skill design-taste-frontend
```

**Important:**  
This project is much smaller than Impeccable or Anthropic's Frontend Design. I would keep it in the knowledge base because its design philosophy is useful, not because of GitHub stars.

---

## 10. Find Skills — Vercel Labs

**Repo:** `vercel-labs/skills`  
**Popularity:** ~33K GitHub stars

**What it does:**  
Gives your agent a way to discover other Agent Skills when you need a capability you do not already have.

**Best for:**  
Expanding this knowledge base without randomly browsing GitHub every time you hear about a new skill.

**Install:**
```bash
npx skills add vercel-labs/skills
```

Think of this as the skill that helps you find more skills.

---

# How I Would Organize Them

### Core AI Infrastructure
- Skill Creator
- Find Skills
- Claude-Mem
- Graphify

### Software Engineering
- Agent Skills
- Superpowers
- Ponytail

### Frontend / Design
- Frontend Design
- Impeccable
- Taste Skill

# Recommended Default Stack

For most of your projects, I would start with:

```text
Claude-Mem
Skill Creator
Find Skills
Agent Skills
Ponytail
Frontend Design
```

Then add these only when the project calls for them:

```text
Graphify      -> large or complicated codebase / knowledge base
Impeccable    -> serious UI polishing and design review
Taste Skill   -> experimental or high-creativity frontend work
Superpowers   -> projects where you want a very strict development methodology
```

The goal is not to install every popular skill. The goal is to create a small set of reusable capabilities that make your AI coding environment consistently better.
