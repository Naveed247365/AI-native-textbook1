---
id: 0002
title: Personalized Book Experience Clarifications
stage: spec
date: 2025-12-23
surface: agent
model: claude-sonnet-4-5-20250929
feature: 005-personalized-book-experience
branch: 005-personalized-book-experience
user: Naveed247365
command: /sp.clarify
labels: ["clarification", "personalization", "frontend-integration", "llm-prompt-design"]
links:
  spec: specs/005-personalized-book-experience/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/005-personalized-book-experience/spec.md (updated with clarifications section and 4 integrated answers)
tests:
  - All 4 clarification questions answered and validated
  - Functional requirements updated (FR-013, FR-016, FR-017, FR-018a, FR-022, FR-022a)
  - Key entities updated (Chapter entity clarified with frontmatter requirement)
---

## Prompt

Clarify the following technical details regarding the "Personalize" button functionality:

1. **Content Strategy:** When the button is pressed, should the entire chapter be rewritten by AI, or should a "Personalized Insight" block be injected at the top? (Proposed: Inject a dynamic block).

2. **State Management:** Should the personalized version be saved in Neon so that it persists when the user returns to the chapter?

3. **Frontend Implementation:** How should the MDX files in `frontend/` detect the active chapter to send the correct ID to the `backend/`?

4. **Agent Skill:** How will the 'Personalization Agent' handle cases where a user has 'Expert' software but 'Novice' hardware skills?

## Response snapshot

Conducted sequential clarification session with 4 questions, all answered with recommended options:

**Q1: Content Strategy** → **A: Inject dynamic "Personalized Roadmap" block at top** (Option B)
- Preserves original chapter content for all users
- Adds personalized value without replacing educational material
- Faster LLM generation (smaller output)
- Allows users to see both original and personalized guidance

**Q2: State Management** → **A: Yes, save in Neon Postgres with (user_id, chapter_id) composite key** (Option A)
- Better UX with instant retrieval on return visits
- Reduces OpenRouter API costs (no regeneration)
- Aligns with existing spec's FR-016 and personalizations table schema

**Q3: Frontend Implementation** → **A: Use Docusaurus frontmatter with unique chapter_id field** (Option B)
- Clean and maintainable approach
- Follows Docusaurus conventions (useDocusaurusContext() hook)
- No URL parsing or external config files needed
- Each MDX file defines its own chapter_id in metadata

**Q4: Agent Skill (Mixed Proficiency)** → **A: Address both dimensions independently with bridging explanations** (Option A)
- Use advanced programming concepts for expert software dimension
- Explain hardware from basics for novice hardware dimension
- Bridge gap by showing how software expertise helps when learning hardware
- Creates most valuable personalized experience

**Spec Updates Applied:**
- Added "Clarifications" section with Session 2025-12-23 subsection
- Updated FR-013: LLM prompt must address both skill dimensions independently with bridging
- Updated FR-016: Emphasized composite unique constraint
- Updated FR-017: Clarified content is for injection as dynamic block
- Added FR-018a: MDX chapter_id frontmatter requirement
- Updated FR-022: Specified injection location (below title, above original content)
- Added FR-022a: Extract chapter_id from Docusaurus metadata using useDocusaurusContext()
- Updated Chapter entity: Clarified chapter_id comes from frontmatter, not file path

## Outcome

- ✅ Impact: All 4 critical technical ambiguities resolved, spec updated with actionable implementation details for frontend integration and LLM prompt design
- 🧪 Tests: Sequential questioning validated, all answers integrated into spec with no contradictions
- 📁 Files: Updated specs/005-personalized-book-experience/spec.md with Clarifications section and 7 functional requirement modifications
- 🔁 Next prompts: `/sp.plan` to generate architectural plan with clarified frontend/backend integration details
- 🧠 Reflection: Clarifications focused on implementation-critical decisions (content strategy, persistence, chapter ID detection, mixed proficiency handling) that directly impact architecture and task decomposition. All user-provided questions were high-value and appropriately scoped.

## Evaluation notes (flywheel)

- Failure modes observed: None - all 4 questions were clear, answerable with specific options, and had obvious recommended choices based on best practices
- Graders run and results (PASS/FAIL):
  - Question clarity: PASS (all 4 questions had clear context and mutually exclusive options)
  - Answer integration: PASS (all answers reflected in updated spec with no contradictions)
  - Terminology consistency: PASS (chapter_id, frontmatter, composite key terms used consistently)
  - Spec structure preservation: PASS (Clarifications section added after Overview, no disruption to existing sections)
- Prompt variant (if applicable): User-provided clarification questions (not agent-generated ambiguity scan)
- Next experiment (smallest change to try): Proceed to planning phase to see how clarifications impact task decomposition and component design
