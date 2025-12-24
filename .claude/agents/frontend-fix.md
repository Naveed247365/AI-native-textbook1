# Frontend UX Fix Specification: Selected Text Injection

## Goal
Fix the chat UI so that when a user selects text on the page, the selected text is automatically injected into the chat input field instead of only being shown above it.

This is a FRONTEND-ONLY change.
The backend and RAG service are already working correctly and must not be modified.

---

## Current Behavior (Incorrect)
- User selects text on the page
- A popup/chat widget opens
- The selected text is shown above the chat UI
- The chat input field remains empty
- User must manually type the question

---

## Required Behavior (Correct)
When the user selects text:

1. The chat popup opens
2. The chat input field is automatically pre-filled with:

Selected text:
"<SELECTED_TEXT>"

3. The input field placeholder must be:
"Ask a question about this text..."

4. The cursor must be placed at the end of the input so the user can immediately start typing

---

## UX Reference
This behavior should match modern AI readers like:
- Medium AI assistant
- Perplexity inline ask
- Notion AI selected-text ask

---

## Technical Requirements

### Frontend Responsibilities
- Capture text selection using `window.getSelection()`
- Store selected text in frontend state
- Inject the selected text into the chat input field value
- Do NOT display selected text separately above the input
- Ensure the input field is editable after injection

---

## Data Flow (Frontend → Backend)
The frontend must send the payload in this structure (already supported by backend):

{
  "message": "<user question>",
  "selected_text": "<auto-injected selected text>"
}

---

## Forbidden Changes
- DO NOT modify backend APIs
- DO NOT modify RAG logic
- DO NOT change fallback message
- DO NOT add new endpoints

---

## Expected Result
- Selecting text auto-fills the chat input
- User sees selected text inside input
- User can immediately type their question
- Backend receives selected_text correctly
- RAG works as expected

---

## Completion Criteria
This task is complete ONLY when:
- Selected text appears inside the input field
- Placeholder text is visible
- No duplicate selected text UI exists
