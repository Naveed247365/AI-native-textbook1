---
id: 0003
title: UI/UX optimization tasks breakdown
stage: tasks
date: 2024-12-25
surface: agent
model: claude-sonnet-4-5
feature: 007-ui-ux-restructure
branch: 007-ui-ux-restructure
user: Naveed247365
command: /sp.tasks
labels: ["ui-ux", "restructure", "docusaurus", "deployment", "theme", "navigation", "cleanup"]
links:
  spec: specs/007-ui-ux-restructure/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/007-ui-ux-restructure/tasks.md
tests:
  - none
---

## Prompt

Break down the "Final Face" phase into actionable tasks:

1. [Structure]: Move all book content to `/frontend` and all API/Auth/RAG code to `/backend`.
2. [Cleanup]: Remove "Blog" and "GitHub" links from `docusaurus.config.js`. Delete all placeholder .md files.
3. [UX]: Add 'Reading Time' plugin and 'Search' bar. Update CSS for a Robotics theme.
4. [Routing]: Re-verify that the Frontend can still talk to the Backend after path changes.
5. [Deploy - Backend]: Push the `/backend` folder changes to Hugging Face and verify the API is live.
6. [Deploy - Frontend]: Update Vercel settings and deploy the `/frontend` folder.
7. [Spec Update]: Record all structural changes in `/docs/specs/history.md`.

## Response snapshot

Generated comprehensive task breakdown for Feature 007: UI/UX Optimization & Project Restructure

**76 Total Tasks** organized into 8 phases:
1. **Phase 1: Setup** (4 tasks) - Git backup, audit current state
2. **Phase 2: Foundational Cleanup** (11 tasks) - Delete 30+ junk files, create READMEs
3. **Phase 3: User Story 1** (9 tasks) - Remove Docusaurus boilerplate
4. **Phase 4: User Story 2** (14 tasks) - Add navigation features (progress bar, reading time, chapter nav, TOC)
5. **Phase 5: User Story 3** (10 tasks) - Implement Robotics theme
6. **Phase 6: User Story 4** (7 tasks) - Verify project structure
7. **Phase 7: User Story 5** (10 tasks) - Prepare deployment configs
8. **Phase 8: Polish** (11 tasks) - Testing, validation, PR

**Key Insights**:
- Frontend/backend directories already exist - focus on cleanup, not creation
- 30+ redundant files to delete (23 docs, 5 debug scripts, 12 test scripts, utility files)
- Swizzle 3 components: Footer, Navbar, TOC (DocItem already swizzled)
- Theme uses CSS custom properties for easy maintenance
- All existing features (RAG, auth, personalization, translation) preserved

**Parallel Opportunities**: 25+ tasks can run in parallel (marked with [P])

**MVP Scope**: Phases 1-4 (User Stories 1-2) = 38 tasks for core functionality

## Outcome

- ✅ Impact: Complete actionable roadmap for transforming site from generic Docusaurus to professional Physical AI textbook
- 🧪 Tests: Accessibility, performance, cross-browser, and mobile testing included in Phase 8
- 📁 Files: tasks.md created with 76 detailed tasks across 8 phases
- 🔁 Next prompts: /sp.implement to start implementation, or manually execute tasks in order
- 🧠 Reflection: Task breakdown balances cleanup (Phases 1-2), user-facing improvements (Phases 3-5), verification (Phase 6), deployment prep (Phase 7), and quality gates (Phase 8). Each user story independently testable.

## Evaluation notes (flywheel)

- Failure modes observed: None - tasks generated successfully
- Graders run and results (PASS/FAIL): Not applicable (task generation phase)
- Prompt variant (if applicable): Standard /sp.tasks workflow with user's 7-point breakdown
- Next experiment (smallest change to try): Proceed to /sp.implement or manual task execution
