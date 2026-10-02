---
type: resource
kind: github
title: "Public APIs"
url: https://github.com/public-apis/public-apis
status: to-do
topics: [apis]
added: 2026-10-02
---
# Public APIs

## Why I saved it
A big curated list of free APIs by category (auth type, HTTPS, CORS listed for each).
Use it when a project needs data: practice projects, automations, n8n flows, the learning app.

## How to use it
- Browse by category in the README, or search it: `gh api repos/public-apis/public-apis/readme --jq .content | base64 -d | grep -i "<keyword>"`
- Check the **Auth** column: `No` = easiest to start, `apiKey` = put the key in `.env`, never in code.

## Worth a look for my stuff
- Learning app ideas: dictionary/definitions, books (Open Library), GitHub, YouTube-adjacent.
- Practice: any `No`-auth API is perfect for learning `fetch` (JS) and `requests`/`httpx` (Python).

## My notes
