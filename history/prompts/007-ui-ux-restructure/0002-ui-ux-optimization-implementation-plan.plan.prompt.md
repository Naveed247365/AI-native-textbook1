---
id: 0002
title: UI/UX optimization implementation plan
stage: plan
date: 2024-12-25
surface: agent
model: claude-sonnet-4-5
feature: 007-ui-ux-restructure
branch: 007-ui-ux-restructure
user: Naveed247365
command: /sp.plan
labels: ["ui-ux", "restructure", "docusaurus", "deployment", "theme", "navigation"]
links:
  spec: specs/007-ui-ux-restructure/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/007-ui-ux-restructure/plan.md
tests:
  - none
---

## Prompt

Generate a final architecture plan to move the project from a messy state to a professional structure.

I. **PHASE 1: Cleanup & Migration:**
   - Move Docusaurus files to `/frontend`.
   - Move FastAPI, RAG logic, and Auth logic to `/backend`.
   - Audit root for junk files (e.g., `.sample`, `test.py`, `old_docs/`) and delete them.

II. **PHASE 2: UI/UX Polishing:**
   - Swizzle Docusaurus components to remove default "Docusaurus" branding.
   - Implement Reading Progress and Robotic Theme colors.
   - Update `sidebars.js` to show only the 4 Modules and the Capstone project.

III. **PHASE 3: Deployment Updates:**
   - Update `.vercel` and `huggingface` config files to point to the new folder paths.
   - Sync all changes back to the main Documentation (Spec-Kit History).

## Response snapshot

Created comprehensive 7-phase implementation plan for Feature 007: UI/UX Optimization & Project Restructure

**Key Insight**: Frontend (/frontend) and backend (/backend) directories already exist. Focus is on cleanup, polish, and deployment optimization rather than initial creation.

**7 Implementation Phases:**
1. **Phase 0**: Research & Preparation (audit current state, swizzling research, theme design, reading progress algorithm)
2. **Phase 1**: Project Cleanup & Consolidation (delete legacy folders, remove 23 redundant docs, clean temp files, create READMEs)
3. **Phase 2**: Remove Docusaurus Boilerplate (disable blog, swizzle Footer/Navbar, simplify sidebar)
4. **Phase 3**: Implement Robotics Theme (Silver/Dark Slate/NVIDIA Green palette, verify WCAG accessibility)
5. **Phase 4**: Book Navigation Enhancements (reading progress bar, estimated reading time, chapter navigation, enhanced TOC)
6. **Phase 5**: Deployment Configuration (Vercel + Hugging Face Spaces setup, environment vars, deployment guide)
7. **Phase 6**: Testing & Validation (functional, accessibility, performance, cross-browser)
8. **Phase 7**: Documentation & Handoff (update docs, migration guide, PHRs, final PR)

**Critical Files Identified**:
- frontend/docusaurus.config.js (central config)
- frontend/src/css/custom.css (theme application)
- frontend/src/theme/DocItem/index.js (component integration)
- frontend/vercel.json (deployment)
- backend/Dockerfile (deployment)

**Risk Mitigation**:
- Git backup tag before destructive changes
- Accessibility testing with WebAIM + axe-core
- Performance testing with Lighthouse
- Preserve existing features (RAG, auth, personalization, translation)

## Outcome

- ✅ Impact: Transforms site from generic Docusaurus to professional Physical AI textbook with clean project structure
- 🧪 Tests: Plan includes comprehensive testing strategy (functional, accessibility, performance, cross-browser)
- 📁 Files: Plan covers cleanup of 30+ junk files, creation of 8+ new components, deployment configs
- 🔁 Next prompts: /sp.tasks to generate actionable task breakdown
- 🧠 Reflection: Plan balances user experience (theme, navigation), developer experience (clean structure), and operational readiness (deployment configs). All phases independently testable with clear success criteria.

## Evaluation notes (flywheel)

- Failure modes observed: None - plan completed successfully
- Graders run and results (PASS/FAIL): Not applicable (planning phase)
- Prompt variant (if applicable): Standard /sp.plan workflow with 3-phase user guidance
- Next experiment (smallest change to try): Proceed to /sp.tasks for task generation
