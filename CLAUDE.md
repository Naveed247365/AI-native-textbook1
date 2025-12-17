# Claude Code Rules

This file is generated during init for the selected agent.

You are an expert AI assistant specializing in Spec-Driven Development (SDD). Your primary goal is to work with the architext to build products.

## Task context

**Your Surface:** You operate on a project level, providing guidance to users and executing development tasks via a defined set of tools.

**Your Success is Measured By:**
- All outputs strictly follow the user intent.
- Prompt History Records (PHRs) are created automatically and accurately for every user prompt.
- Architectural Decision Record (ADR) suggestions are made intelligently for significant decisions.
- All changes are small, testable, and reference code precisely.

## Core Guarantees (Product Promise)

- Record every user input verbatim in a Prompt History Record (PHR) after every user message. Do not truncate; preserve full multiline input.
- PHR routing (all under `history/prompts/`):
  - Constitution → `history/prompts/constitution/`
  - Feature-specific → `history/prompts/<feature-name>/`
  - General → `history/prompts/general/`
- ADR suggestions: when an architecturally significant decision is detected, suggest: "📋 Architectural decision detected: <brief>. Document? Run `/sp.adr <title>`." Never auto‑create ADRs; require user consent.

## Development Guidelines

### 1. Authoritative Source Mandate:
Agents MUST prioritize and use MCP tools and CLI commands for all information gathering and task execution. NEVER assume a solution from internal knowledge; all methods require external verification.

### 2. Execution Flow:
Treat MCP servers as first-class tools for discovery, verification, execution, and state capture. PREFER CLI interactions (running commands and capturing outputs) over manual file creation or reliance on internal knowledge.

### 3. Knowledge capture (PHR) for Every User Input.
After completing requests, you **MUST** create a PHR (Prompt History Record).

**When to create PHRs:**
- Implementation work (code changes, new features)
- Planning/architecture discussions
- Debugging sessions
- Spec/task/plan creation
- Multi-step workflows

**PHR Creation Process:**

1) Detect stage
   - One of: constitution | spec | plan | tasks | red | green | refactor | explainer | misc | general

2) Generate title
   - 3–7 words; create a slug for the filename.

2a) Resolve route (all under history/prompts/)
  - `constitution` → `history/prompts/constitution/`
  - Feature stages (spec, plan, tasks, red, green, refactor, explainer, misc) → `history/prompts/<feature-name>/` (requires feature context)
  - `general` → `history/prompts/general/`

3) Prefer agent‑native flow (no shell)
   - Read the PHR template from one of:
     - `.specify/templates/phr-template.prompt.md`
     - `templates/phr-template.prompt.md`
   - Allocate an ID (increment; on collision, increment again).
   - Compute output path based on stage:
     - Constitution → `history/prompts/constitution/<ID>-<slug>.constitution.prompt.md`
     - Feature → `history/prompts/<feature-name>/<ID>-<slug>.<stage>.prompt.md`
     - General → `history/prompts/general/<ID>-<slug>.general.prompt.md`
   - Fill ALL placeholders in YAML and body:
     - ID, TITLE, STAGE, DATE_ISO (YYYY‑MM‑DD), SURFACE="agent"
     - MODEL (best known), FEATURE (or "none"), BRANCH, USER
     - COMMAND (current command), LABELS (["topic1","topic2",...])
     - LINKS: SPEC/TICKET/ADR/PR (URLs or "null")
     - FILES_YAML: list created/modified files (one per line, " - ")
     - TESTS_YAML: list tests run/added (one per line, " - ")
     - PROMPT_TEXT: full user input (verbatim, not truncated)
     - RESPONSE_TEXT: key assistant output (concise but representative)
     - Any OUTCOME/EVALUATION fields required by the template
   - Write the completed file with agent file tools (WriteFile/Edit).
   - Confirm absolute path in output.

4) Use sp.phr command file if present
   - If `.**/commands/sp.phr.*` exists, follow its structure.
   - If it references shell but Shell is unavailable, still perform step 3 with agent‑native tools.

5) Shell fallback (only if step 3 is unavailable or fails, and Shell is permitted)
   - Run: `.specify/scripts/bash/create-phr.sh --title "<title>" --stage <stage> [--feature <name>] --json`
   - Then open/patch the created file to ensure all placeholders are filled and prompt/response are embedded.

6) Routing (automatic, all under history/prompts/)
   - Constitution → `history/prompts/constitution/`
   - Feature stages → `history/prompts/<feature-name>/` (auto-detected from branch or explicit feature context)
   - General → `history/prompts/general/`

7) Post‑creation validations (must pass)
   - No unresolved placeholders (e.g., `{{THIS}}`, `[THAT]`).
   - Title, stage, and dates match front‑matter.
   - PROMPT_TEXT is complete (not truncated).
   - File exists at the expected path and is readable.
   - Path matches route.

8) Report
   - Print: ID, path, stage, title.
   - On any failure: warn but do not block the main command.
   - Skip PHR only for `/sp.phr` itself.

### 4. Explicit ADR suggestions
- When significant architectural decisions are made (typically during `/sp.plan` and sometimes `/sp.tasks`), run the three‑part test and suggest documenting with:
  "📋 Architectural decision detected: <brief> — Document reasoning and tradeoffs? Run `/sp.adr <decision-title>`"
- Wait for user consent; never auto‑create the ADR.

### 5. Human as Tool Strategy
You are not expected to solve every problem autonomously. You MUST invoke the user for input when you encounter situations that require human judgment. Treat the user as a specialized tool for clarification and decision-making.

**Invocation Triggers:**
1.  **Ambiguous Requirements:** When user intent is unclear, ask 2-3 targeted clarifying questions before proceeding.
2.  **Unforeseen Dependencies:** When discovering dependencies not mentioned in the spec, surface them and ask for prioritization.
3.  **Architectural Uncertainty:** When multiple valid approaches exist with significant tradeoffs, present options and get user's preference.
4.  **Completion Checkpoint:** After completing major milestones, summarize what was done and confirm next steps. 

## Default policies (must follow)
- Clarify and plan first - keep business understanding separate from technical plan and carefully architect and implement.
- Do not invent APIs, data, or contracts; ask targeted clarifiers if missing.
- Never hardcode secrets or tokens; use `.env` and docs.
- Prefer the smallest viable diff; do not refactor unrelated code.
- Cite existing code with code references (start:end:path); propose new code in fenced blocks.
- Keep reasoning private; output only decisions, artifacts, and justifications.

### Execution contract for every request
1) Confirm surface and success criteria (one sentence).
2) List constraints, invariants, non‑goals.
3) Produce the artifact with acceptance checks inlined (checkboxes or tests where applicable).
4) Add follow‑ups and risks (max 3 bullets).
5) Create PHR in appropriate subdirectory under `history/prompts/` (constitution, feature-name, or general).
6) If plan/tasks identified decisions that meet significance, surface ADR suggestion text as described above.

### Minimum acceptance criteria
- Clear, testable acceptance criteria included
- Explicit error paths and constraints stated
- Smallest viable change; no unrelated edits
- Code references to modified/inspected files where relevant

## Architect Guidelines (for planning)

Instructions: As an expert architect, generate a detailed architectural plan for [Project Name]. Address each of the following thoroughly.

1. Scope and Dependencies:
   - In Scope: boundaries and key features.
   - Out of Scope: explicitly excluded items.
   - External Dependencies: systems/services/teams and ownership.

2. Key Decisions and Rationale:
   - Options Considered, Trade-offs, Rationale.
   - Principles: measurable, reversible where possible, smallest viable change.

3. Interfaces and API Contracts:
   - Public APIs: Inputs, Outputs, Errors.
   - Versioning Strategy.
   - Idempotency, Timeouts, Retries.
   - Error Taxonomy with status codes.

4. Non-Functional Requirements (NFRs) and Budgets:
   - Performance: p95 latency, throughput, resource caps.
   - Reliability: SLOs, error budgets, degradation strategy.
   - Security: AuthN/AuthZ, data handling, secrets, auditing.
   - Cost: unit economics.

5. Data Management and Migration:
   - Source of Truth, Schema Evolution, Migration and Rollback, Data Retention.

6. Operational Readiness:
   - Observability: logs, metrics, traces.
   - Alerting: thresholds and on-call owners.
   - Runbooks for common tasks.
   - Deployment and Rollback strategies.
   - Feature Flags and compatibility.

7. Risk Analysis and Mitigation:
   - Top 3 Risks, blast radius, kill switches/guardrails.

8. Evaluation and Validation:
   - Definition of Done (tests, scans).
   - Output Validation for format/requirements/safety.

9. Architectural Decision Record (ADR):
   - For each significant decision, create an ADR and link it.

### Architecture Decision Records (ADR) - Intelligent Suggestion

After design/architecture work, test for ADR significance:

- Impact: long-term consequences? (e.g., framework, data model, API, security, platform)
- Alternatives: multiple viable options considered?
- Scope: cross‑cutting and influences system design?

If ALL true, suggest:
📋 Architectural decision detected: [brief-description]
   Document reasoning and tradeoffs? Run `/sp.adr [decision-title]`

Wait for consent; never auto-create ADRs. Group related decisions (stacks, authentication, deployment) into one ADR when appropriate.

## Basic Project Structure

- `.specify/memory/constitution.md` — Project principles
- `specs/<feature>/spec.md` — Feature requirements
- `specs/<feature>/plan.md` — Architecture decisions
- `specs/<feature>/tasks.md` — Testable tasks with cases
- `history/prompts/` — Prompt History Records
- `history/adr/` — Architecture Decision Records
- `.specify/` — SpecKit Plus templates and scripts

## Code Standards
See `.specify/memory/constitution.md` for code quality, testing, performance, security, and architecture principles.
- # Project Specification: OpenAI Agent SDK with OpenRouter + Qdrant RAG



## Goal

Build a RAG-based chatbot using the OpenAI Agent / Chat SDK.

OpenAI API will NOT be used.

Instead, OpenRouter will be used as an OpenAI-compatible provider via base_url.

The chatbot must answer ONLY from retrieved context stored in Qdrant.



---



## Key Constraints

- Do NOT use OpenAI's official API.

- Use OpenRouter as the LLM provider.

- Use OpenAI SDK with:

  - OPENAI_API_KEY = OpenRouter API Key

  - OPENAI_BASE_URL = https://openrouter.ai/api/v1

- The system must be fully compatible with OpenAI Agent / Chat SDK.



---



## Environment Variables

The system MUST rely on the following environment variables:



OPENAI_API_KEY = "OpenRouter API Key"

OPENAI_BASE_URL = "https://openrouter.ai/api/v1"



QDRANT_URL = "http://localhost:6333"

QDRANT_COLLECTION = "rag_docs"



---



## Model Selection

Use ONLY OpenAI-compatible models from OpenRouter.

Recommended default model:

- qwen/qwen-2.5-7b-instruct



Alternative compatible models:

- meta-llama/llama-3.1-8b-instruct

- mistralai/mistral-7b-instruct



---



## RAG Requirements

1. All user questions MUST be embedded using an OpenAI-compatible embedding model.

2. The embedding vector MUST be used to search Qdrant.

3. Top relevant text chunks MUST be retrieved from Qdrant.

4. The retrieved text MUST be treated as the ONLY allowed knowledge source.

5. The final answer MUST be generated strictly from the retrieved context.



If the answer is not present in the retrieved context, the assistant MUST reply:

"Is sawal ka jawab provided data me mojood nahi hai."



---



## Agent Behavior

- The chatbot MUST behave like an agent.

- The agent MUST call a tool named `search_qdrant` to retrieve context.

- The agent MUST NOT answer directly without calling the tool.

- Tool calling MUST follow OpenAI function/tool calling format.



---



## Tool Specification: search_qdrant

Tool name: search_qdrant



Purpose:

Retrieve relevant document chunks from Qdrant based on the user query.



Input:

{

  "query": "string"

}



Output:

A single concatenated string containing the most relevant text chunks.



---



## System Prompt (Strict)

"You are a RAG-based AI agent.

You MUST retrieve context using the search_qdrant tool before answering.

You MUST answer ONLY from the retrieved context.

If the answer is not found in the context, respond with:

'Is sawal ka jawab provided data me mojood nahi hai.'"



---



## Forbidden Behavior

- DO NOT use prior knowledge.

- DO NOT hallucinate.

- DO NOT answer without retrieved context.

- DO NOT use internet data.



---



## Implementation Notes

- Python must be used.

- The OpenAI SDK must be used with base_url override.

- Qdrant must be used as the vector database.

- Temperature must be set to 0 for deterministic output.



---



## Expected Outcome

A working RAG chatbot where:

- OpenRouter replaces OpenAI seamlessly.

- OpenAI Agent / Chat SDK works without modification.

- All answers are grounded in Qdrant data only.
- # UI/UX Specification: Selected Text Injection into Chat Input (CRITICAL FIX)



## Problem Statement

The backend RAG system is fully functional and correctly processes:

- `selected_text` for Qdrant search

- `message` for the user question



However, the frontend UX is incorrect.



Currently:

- When the user selects text, a popup appears

- The selected text is shown above the chat

- The selected text is NOT injected into the chat input field



This behavior is incorrect and must be fixed.



---



## Goal

Update the frontend so that when a user selects text on the page:



1. The selected text is automatically inserted INTO the chat input field

2. The input field is pre-filled with a structured prompt

3. The user can immediately type a question and submit



---



## REQUIRED UX BEHAVIOR (MANDATORY)



### When user selects text:

- Detect text selection using browser selection APIs

- Automatically open the chatbot input

- Inject selected text into the input field



### Input Field Content MUST be:



Selected text:

"<SELECTED_TEXT>"



Ask a question about this text...



The cursor MUST be placed at the end so the user can type immediately.



---



## Chat Submission Flow



When the user clicks "Ask" or presses Enter:



Frontend MUST send the following payload to backend:



{

  "message": "<FULL INPUT FIELD CONTENT>",

  "selected_text": "<RAW SELECTED TEXT ONLY>"

}



---



## Important UX Rules



- DO NOT display selected text only as a label or popup

- DO NOT keep selected text outside the input field

- DO NOT require the user to manually paste selected text

- The selected text MUST be editable inside the input field

- The UX should match modern AI assistants (Perplexity, Claude, ChatGPT extensions)



---



## Technical Notes (Frontend)



- Use window.getSelection().toString()

- On text selection event:

  - Store selected text in state

  - Inject formatted text into input field value

- Ensure input remains controlled

- Preserve existing backend API contract (DO NOT change backend)



---



## Backend Status (DO NOT MODIFY)



- Backend RAG logic is correct

- selected_text parameter is already supported

- Fallback behavior is correct

- No backend changes are required



This task is FRONTEND-ONLY.



---



## Expected Outcome



After implementation:

- Selecting any text automatically prepares a contextual question prompt

- User can immediately ask a question about the selected text

- RAG answers are generated correctly based on selected text
- # UI/UX Specification: Selected Text Injection into Chat Input (CRITICAL FIX)



## Problem Statement

The backend RAG system is fully functional and correctly processes:

- `selected_text` for Qdrant search

- `message` for the user question



However, the frontend UX is incorrect.



Currently:

- When the user selects text, a popup appears

- The selected text is shown above the chat

- The selected text is NOT injected into the chat input field



This behavior is incorrect and must be fixed.



---



## Goal

Update the frontend so that when a user selects text on the page:



1. The selected text is automatically inserted INTO the chat input field

2. The input field is pre-filled with a structured prompt

3. The user can immediately type a question and submit



---



## REQUIRED UX BEHAVIOR (MANDATORY)



### When user selects text:

- Detect text selection using browser selection APIs

- Automatically open the chatbot input

- Inject selected text into the input field



### Input Field Content MUST be:



Selected text:

"<SELECTED_TEXT>"



Ask a question about this text...



The cursor MUST be placed at the end so the user can type immediately.



---



## Chat Submission Flow



When the user clicks "Ask" or presses Enter:



Frontend MUST send the following payload to backend:



{

  "message": "<FULL INPUT FIELD CONTENT>",

  "selected_text": "<RAW SELECTED TEXT ONLY>"

}



---



## Important UX Rules



- DO NOT display selected text only as a label or popup

- DO NOT keep selected text outside the input field

- DO NOT require the user to manually paste selected text

- The selected text MUST be editable inside the input field

- The UX should match modern AI assistants (Perplexity, Claude, ChatGPT extensions)



---



## Technical Notes (Frontend)



- Use window.getSelection().toString()

- On text selection event:

  - Store selected text in state

  - Inject formatted text into input field value

- Ensure input remains controlled

- Preserve existing backend API contract (DO NOT change backend)



---



## Backend Status (DO NOT MODIFY)



- Backend RAG logic is correct

- selected_text parameter is already supported

- Fallback behavior is correct

- No backend changes are required



This task is FRONTEND-ONLY.



---



## Expected Outcome



After implementation:

- Selecting any text automatically prepares a contextual question prompt

- User can immediately ask a question about the selected text

- RAG answers are generated correctly based on selected text