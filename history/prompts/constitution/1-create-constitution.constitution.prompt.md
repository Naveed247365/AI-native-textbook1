---
id: 1
title: Create Constitution
stage: constitution
date: 2025-12-10
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: user
command: /sp.constitution
labels: [constitution,physical-ai,humanoid-robotics]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

Create a complete AI-native textbook titled "Physical AI & Humanoid Robotics" for Panaversity hackathon. Use Docusaurus + Spec-Kit Plus, deploy to GitHub Pages. Must include embedded RAG chatbot (OpenAI + FastAPI + Neon Postgres + Qdrant Free) that answers from full book and selected text only. Target 100 base + all 200 bonus points (Claude Subagents, Better-Auth signup with background questions, per-chapter personalization button, per-chapter Urdu translation button). Strictly follow the 9-page course document provided (modules, weekly breakdown, hardware, capstone, etc.). Deadline Nov 30 2025. Output full project constitution.

## Response snapshot

Created a comprehensive constitution for the "Physical AI & Humanoid Robotics" AI-native textbook project with 6 core principles: AI-Native Educational Content, Modular & Extensible Architecture, Test-First Development, Full Integration Testing, Performance & Accessibility, and Data Privacy & Security. Added Technology Stack Requirements, Development Workflow, and Governance sections. The constitution is version 1.0.0, ratified on 2025-12-10.

## Outcome

- ✅ Impact: Created initial project constitution with comprehensive principles and requirements
- 🧪 Tests: none
- 📁 Files: Updated .specify/memory/constitution.md with complete constitution
- 🔁 Next prompts: Proceed with project specification and planning
- 🧠 Reflection: Constitution establishes clear direction for the AI-native textbook project

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): not applicable
- Prompt variant (if applicable): not applicable
- Next experiment (smallest change to try): not applicable