# Tasks: Premium AI Chatbot UI Redesign

**Feature**: Premium AI Chatbot UI Redesign
**Branch**: `004-chatbot-ui-redesign`
**Created**: 2025-12-14
**Status**: To Do

## Dependencies

- Docusaurus project with existing chatbot component
- OpenRouter API key configured for backend
- Qdrant vector database for RAG functionality

## Parallel Execution Examples

- **US1 & US2**: Can be developed in parallel - US1 focuses on text selection UX, US2 focuses on close behavior
- **US2 & US3**: Can be developed in parallel - US2 handles functionality, US3 handles visual design
- **Frontend & Styling**: Component logic and CSS can be developed separately

---

## Phase 1: Setup

- [ ] T001 Create project structure in `frontend/src/components/chatbot/`
- [ ] T002 Verify existing EnhancedChatbot.jsx component location and functionality
- [ ] T003 Set up development environment with Docusaurus
- [ ] T004 Verify backend API endpoint `/api/chat` is accessible

---

## Phase 2: Foundational Tasks

- [ ] T005 [P] Update React hooks for proper state management in EnhancedChatbot.jsx
- [ ] T006 [P] Create refs for chatbot container and input field in EnhancedChatbot.jsx
- [ ] T007 [P] Implement basic animation state tracking in EnhancedChatbot.jsx
- [ ] T008 [P] Set up event listener cleanup mechanism in EnhancedChatbot.jsx

---

## Phase 3: [US1] Text Selection with Chatbot Interaction

**Goal**: When a student selects text in the AI textbook, they want to immediately ask questions about that specific content without losing focus on their reading. The chatbot should appear smoothly, accept their question, and disappear cleanly when dismissed.

**Independent Test**: Can be fully tested by selecting text and verifying the chatbot appears, accepts input, processes requests, and closes properly - delivers immediate value for content clarification.

**Acceptance Scenarios**:
1. Given user has selected text in the textbook, When text selection is complete, Then a premium AI chatbot appears near the selection with the selected text available as context
2. Given chatbot is open with selected text, When user asks a question about the text, Then the question is processed using the selected text as context and a relevant response is provided
3. Given chatbot is open, When user clicks the close button (×), Then chatbot closes smoothly with fade/slide animation

- [ ] T009 [US1] Update EnhancedChatbot.jsx to accept selectedText prop from TextSelectionHandler
- [ ] T010 [US1] Implement proper selected text injection into input field with formatting
- [ ] T011 [US1] Create function to format selected text as "Selected text:\n"[TEXT]"\n\nAsk a question about this text..."
- [ ] T012 [US1] Position cursor at end of input field after selected text injection
- [ ] T013 [US1] Verify selected text appears in input field when text is selected
- [ ] T014 [US1] Test that API request includes both message and selected_text parameters

---

## Phase 4: [US2] Smooth Chatbot Open/Close Behavior

**Goal**: When interacting with the AI assistant, students want smooth, predictable UI behavior that doesn't interrupt their reading flow. The chatbot should open seamlessly on text selection and close reliably via multiple methods.

**Independent Test**: Can be fully tested by opening and closing the chatbot via different methods (close button, outside click, ESC key) - delivers value by ensuring smooth interaction flow.

**Acceptance Scenarios**:
1. Given user has selected text, When selection is made, Then chatbot opens with smooth fade-in/scale animation near the selection
2. Given chatbot is open, When user clicks outside the chatbot area, Then chatbot closes smoothly with fade-out/slide-down animation
3. Given chatbot is open, When user presses ESC key, Then chatbot closes with appropriate animation

- [ ] T015 [US2] Implement close button functionality with × icon in EnhancedChatbot.jsx
- [ ] T016 [US2] Add ESC key event listener to close chatbot in EnhancedChatbot.jsx
- [ ] T017 [US2] Implement outside click detection to close chatbot in EnhancedChatbot.jsx
- [ ] T018 [US2] Add animation states for opening/closing transitions in EnhancedChatbot.jsx
- [ ] T019 [US2] Reset chat state (messages, input) when chatbot closes in EnhancedChatbot.jsx
- [ ] T020 [US2] Test close functionality with × button
- [ ] T021 [US2] Test close functionality with outside click
- [ ] T022 [US2] Test close functionality with ESC key
- [ ] T023 [US2] Verify state is properly reset when chatbot closes

---

## Phase 5: [US3] Premium Visual Design Experience

**Goal**: When using the AI textbook assistant, students want to feel they're interacting with a sophisticated, modern AI system that matches the futuristic nature of the content (Physical AI & Humanoid Robotics).

**Independent Test**: Can be fully tested by evaluating the visual design elements, animations, and overall aesthetic - delivers value by creating confidence in the AI system.

**Acceptance Scenarios**:
1. Given chatbot appears, When it becomes visible, Then it displays a futuristic, robotics-inspired design with dark theme and neon accents
2. Given user interacts with chatbot, When they hover over elements, Then subtle animations and glow effects provide premium feedback
3. Given chatbot is active, When messages are exchanged, Then smooth animations and transitions enhance the premium experience

- [ ] T024 [US3] Create EnhancedChatbot.css with dark futuristic theme
- [ ] T025 [US3] Implement glassmorphism effect with backdrop-filter in EnhancedChatbot.css
- [ ] T026 [US3] Add neon blue (#00FFFF) and cyan (#00CED1) accent colors in EnhancedChatbot.css
- [ ] T027 [US3] Apply dark background (#0B0F19) and secondary background (#1A1F2E) in EnhancedChatbot.css
- [ ] T028 [US3] Implement floating card design with proper shadows in EnhancedChatbot.css
- [ ] T029 [US3] Add smooth fade-in/out animations (200ms ease-in-out) in EnhancedChatbot.css
- [ ] T030 [US3] Add scale transformations (0.9 to 1.0) for opening animation in EnhancedChatbot.css
- [ ] T031 [US3] Implement hover effects with subtle glow animations in EnhancedChatbot.css
- [ ] T032 [US3] Apply typography with Inter font family and specified sizes in EnhancedChatbot.css
- [ ] T033 [US3] Add proper spacing using 4px, 8px, 12px, 16px, 24px, 32px, 40px scale in EnhancedChatbot.css
- [ ] T034 [US3] Implement responsive design for mobile and desktop in EnhancedChatbot.css
- [ ] T035 [US3] Add WCAG 2.1 AA compliant focus indicators (2px solid #00FFFF) in EnhancedChatbot.css
- [ ] T036 [US3] Test visual design on different screen sizes
- [ ] T037 [US3] Verify neon accents and dark theme are properly applied
- [ ] T038 [US3] Test hover effects and animations

---

## Phase 6: Polish & Cross-Cutting Concerns

- [ ] T039 Verify all close methods work reliably (99% success rate)
- [ ] T040 Test API payload structure maintains compatibility (message, selected_text)
- [ ] T041 Verify animations run at 60fps with <100ms response time
- [ ] T042 Test mobile responsiveness across 320px to 1440px screen sizes
- [ ] T043 Verify keyboard navigation and accessibility features meet WCAG 2.1 AA standards
- [ ] T044 Test text selection detection works reliably across all textbook content sections
- [ ] T045 Test loading states with appropriate animations during API requests
- [ ] T046 Verify proper handling of long text selections (>5000 characters)
- [ ] T047 Test rapid successive text selections handling
- [ ] T048 Validate that deselecting text properly closes chatbot (FR-006)
- [ ] T049 Verify input area clearly indicates selected text and allows follow-up questions (FR-016)
- [ ] T050 Final integration test of complete user flow: text selection → chatbot appearance → question → response → close

---

## Implementation Strategy

**MVP Scope**: Implement US1 (Text Selection) and US2 (Close Behavior) first to deliver core functionality.

**Incremental Delivery**:
1. MVP: Text selection → Chatbot appearance → Close functionality
2. Enhancement: Visual redesign and animations
3. Polish: Accessibility and responsive features

## Policy Note for Lesson Authors

Within this chapter, each lesson must end with a single final section titled "Try With AI" (no "Key Takeaways" or "What's Next"). Before AI tools are taught (e.g., Part-1), use ChatGPT web in that section; after tool onboarding, instruct learners to use their preferred AI companion tool (e.g., Gemini CLI, Claude CLI), optionally providing CLI and web variants.