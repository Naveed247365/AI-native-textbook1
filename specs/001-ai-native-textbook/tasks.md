# Implementation Tasks: AI-native Interactive Textbook Platform for Physical AI

**Feature**: AI-native Interactive Textbook Platform for Physical AI
**Branch**: `001-ai-native-textbook`
**Date**: 2025-12-10
**Input**: Feature specification from `/specs/001-ai-native-textbook/spec.md`

## Implementation Strategy

This project implements an AI-native interactive textbook platform with Docusaurus frontend, RAG chatbot backend using FastAPI, Neon Postgres, and Qdrant vector database. The platform includes selected-text-only chatbot functionality, Better-Auth with background questions, per-chapter personalization, Urdu translation, and Claude Code Subagents/Skills.

**MVP Scope**: User Story 1 (Interactive Learning with AI Assistance) - Docusaurus book with RAG chatbot that answers questions based only on selected text.

## Dependencies

- User Story 2 (Personalized Learning) depends on: User Story 1 (auth system), User Story 4 (content available)
- User Story 3 (Multilingual Support) depends on: User Story 1 (content available)
- User Story 4 (Comprehensive Content) is foundational and can be developed in parallel with other stories

## Parallel Execution Examples

- **User Story 1**: Backend (RAG server, API) and frontend (Docusaurus setup) can be developed in parallel
- **User Story 2**: Auth system and personalization service can be developed in parallel
- **User Story 3**: Translation service and UI components can be developed in parallel
- **User Story 4**: Individual chapters can be developed in parallel

---

## Phase 1: Setup & Initialization

### Goal
Initialize project structure with Docusaurus, Spec-Kit Plus, and Claude Code infrastructure.

- [ ] T001 Create project structure per implementation plan using `npm init docusaurus@latest ai-native-textbook classic`
- [ ] T002 [P] Install Spec-Kit Plus dependencies with `npm install @spec-labs/spec-kit-plus`
- [ ] T003 [P] Create project structure with `mkdir -p src/components/{chatbot,auth,personalization,translation}`
- [ ] T004 [P] Create module directories with `mkdir -p src/pages/modules/{1-ros2,2-gazebo-unity,3-nvidia-isaac,4-vla}`
- [ ] T005 [P] Create additional content directories with `mkdir -p src/pages/{weekly-plan,capstone,hardware-specs}`
- [ ] T006 [P] Create backend structure with `mkdir -p backend/{api,models,services,vector-db}`
- [ ] T007 [P] Install backend dependencies with `pip install fastapi uvicorn python-multipart psycopg2-binary qdrant-client openai python-dotenv better-auth`
- [ ] T008 [P] Initialize backend directory structure with `mkdir -p backend/{api,models,services,utils,config}`
- [ ] T009 [P] Create Claude Code directories with `mkdir -p .claude/{subagents,skills}`
- [ ] T010 [P] Update docusaurus.config.js to include Urdu language support
- [ ] T011 Deploy blank Docusaurus site to verify setup is working

---

## Phase 2: Foundational Components

### Goal
Build foundational backend services and database schema required by multiple user stories.

- [ ] T012 [P] Create `backend/main.py` with FastAPI application and route configuration
- [ ] T013 [P] Create `backend/models/user.py` with User model and authentication schema
- [ ] T014 [P] Create `backend/models/chat_session.py` with ChatSession model for storing conversation history
- [ ] T015 [P] Create `backend/models/user_profile.py` with UserProfile model for storing background information
- [ ] T016 [P] Create `backend/database/schema.sql` with database schema for Neon Postgres
- [ ] T017 [P] Create `backend/services/vector_db.py` with Qdrant integration for vector storage
- [ ] T018 [P] Create `backend/services/rag_service.py` with selected-text-only functionality
- [ ] T019 [P] Create `backend/services/translation_service.py` with Urdu translation functionality
- [ ] T020 [P] Create `backend/services/personalization_service.py` with content adaptation logic
- [ ] T021 [P] Create `backend/services/content_adaptation.py` with difficulty and example adaptation
- [ ] T022 [P] Create `backend/api/chat.py` with chat API endpoints for selected-text functionality
- [ ] T023 [P] Create `backend/api/auth.py` with Better-Auth integration and background question endpoints
- [ ] T024 [P] Create `backend/api/translation.py` with translation API endpoints
- [ ] T025 [P] Create `backend/middleware/auth_middleware.py` with authentication middleware
- [ ] T026 [P] Create Claude Code subagents directory structure with `mkdir -p .claude/subagents`
- [ ] T027 [P] Create Claude Code skills directory structure with `mkdir -p .claude/skills`

---

## Phase 3: [US1] Interactive Learning with AI Assistance

### Goal
Implement Docusaurus-based textbook with integrated RAG chatbot that answers questions based only on selected text.

**Independent Test**: Can be fully tested by implementing the Docusaurus book with RAG chatbot that restricts responses to only the selected text, delivering contextual learning assistance.

- [ ] T028 [P] Create `src/components/chatbot/ChatInterface.jsx` with chat interface component
- [ ] T029 [P] Create `src/components/chatbot/SelectedTextHandler.jsx` with text selection functionality
- [ ] T030 [P] Create `src/components/chatbot/MessageDisplay.jsx` with message display component
- [ ] T031 [P] Create `src/components/auth/LoginModal.jsx` with login modal component
- [ ] T032 [P] Create `src/components/auth/SignupWithBackground.jsx` with signup form that captures background information
- [ ] T033 [P] Implement selected text validation service in `backend/services/text_selection_validator.py`
- [ ] T034 [P] Test RAG service to ensure responses are restricted to selected text only
- [ ] T035 [P] Integrate chatbot with Docusaurus pages to ensure proper functionality
- [ ] T036 [P] Implement frontend API calls to backend chat service with selected text context
- [ ] T037 [P] Create chatbot CSS styling in `src/components/chatbot/ChatInterface.css`
- [ ] T038 [P] Test acceptance scenario: user selects text and asks related question - chatbot responds with selected-text content only
- [ ] T039 [P] Test acceptance scenario: user selects text and asks unrelated question - chatbot indicates cannot answer based on selected text
- [ ] T040 [P] Test acceptance scenario: user asks question without selecting text - chatbot prompts to select text first
- [ ] T041 [P] Implement error handling for RAG service when selected text has no relevant information

---

## Phase 4: [US2] Personalized Learning Experience

### Goal
Implement Better-Auth signup with background questions and per-chapter personalization buttons.

**Independent Test**: Can be fully tested by implementing Better-Auth signup flow with background capture and personalization functionality, delivering customized content adaptation.

- [ ] T042 [P] Implement Better-Auth signup flow with background question collection
- [ ] T043 [P] Create `src/components/personalization/PersonalizeButton.jsx` with personalization button component
- [ ] T044 [P] Implement user profile storage and retrieval in Neon database
- [ ] T045 [P] Implement content adaptation logic based on user background (beginner/intermediate/advanced)
- [ ] T046 [P] Create different examples based on user background: software-focused users see more code examples, hardware-focused users see more hardware examples
- [ ] T047 [P] Test acceptance scenario: user completes registration and is prompted for software/hardware background
- [ ] T048 [P] Test acceptance scenario: user with background information clicks personalization button - content adapts to background level
- [ ] T049 [P] Test acceptance scenario: user returns to personalized chapter - personalization settings are preserved
- [ ] T050 [P] Implement personalization settings storage and retrieval
- [ ] T051 [P] Create user preference validation to ensure proper background information capture
- [ ] T052 [P] Implement content difficulty adaptation based on background experience level

---

## Phase 5: [US3] Multilingual Learning Support

### Goal
Implement per-chapter Urdu translation functionality.

**Independent Test**: Can be fully tested by implementing the Urdu translation button that converts chapter content to Urdu in real-time, delivering multilingual accessibility.

- [ ] T053 [P] Create `src/components/translation/UrduTranslationButton.jsx` with translation button component
- [ ] T054 [P] Implement translation service with quality assurance (BLEU score ≥ 0.7 or 4/5 stars from native speakers)
- [ ] T055 [P] Implement translation caching in `backend/services/translation_service.py` to improve performance
- [ ] T056 [P] Test acceptance scenario: chapter in English - user clicks "اردو میں دیکھیں" - content translated to Urdu in real-time
- [ ] T057 [P] Test acceptance scenario: chapter in Urdu - user clicks button again - content reverts to English
- [ ] T058 [P] Test acceptance scenario: network connectivity issues - appropriate fallback/error message provided
- [ ] T059 [P] Implement fallback translation service for when primary translation fails
- [ ] T060 [P] Test translation quality to ensure ≥90% accuracy per requirements
- [ ] T061 [P] Implement translation rate limiting (500 requests/hour during development)
- [ ] T062 [P] Add error handling for translation API failures

---

## Phase 6: [US4] Comprehensive Content Access

### Goal
Create comprehensive textbook content covering ROS2, Gazebo/Unity, NVIDIA Isaac, VLA, hardware specifications, weekly plans, and capstone projects.

**Independent Test**: Can be fully tested by implementing all required content sections, delivering complete Physical AI curriculum coverage.

- [ ] T063 [P] Generate ROS2 content module following 9-page course outline specifications
- [ ] T064 [P] Generate Gazebo/Unity content module following 9-page course outline specifications
- [ ] T065 [P] Generate NVIDIA Isaac content module following 9-page course outline specifications
- [ ] T066 [P] Generate VLA content module following 9-page course outline specifications
- [ ] T067 [P] Generate hardware specifications content following 9-page course outline specifications
- [ ] T068 [P] Generate weekly learning plan content following 9-page course outline specifications
- [ ] T069 [P] Generate capstone project content following 9-page course outline specifications
- [ ] T070 [P] Test acceptance scenario: user navigates through chapters - finds comprehensive content covering all required topics
- [ ] T071 [P] Test acceptance scenario: user accesses weekly plans - finds structured learning schedules and milestones
- [ ] T072 [P] Test acceptance scenario: user accesses capstone project section - finds complete project requirements and guidelines
- [ ] T073 [P] Validate content matches 9-page course outline with modules 1-4, weekly breakdown, hardware tables, and capstone project
- [ ] T074 [P] Integrate all content modules into Docusaurus navigation system

---

## Phase 7: Claude Code Subagents & Agent Skills

### Goal
Implement 5 reusable Claude Code Subagents and 5 Agent Skills as bonus features.

- [ ] T075 [P] Create `content_generation_subagent.md` with content generation subagent
- [ ] T076 [P] Create `personalization_subagent.md` with personalization subagent
- [ ] T077 [P] Create `translation_assistance_subagent.md` with translation assistance subagent
- [ ] T078 [P] Create `chat_response_subagent.md` with chat response subagent
- [ ] T079 [P] Create `user_profiling_subagent.md` with user profiling subagent
- [ ] T080 [P] Create `textbook_navigation_skill.md` with textbook navigation skill
- [ ] T081 [P] Create `content_adaptation_skill.md` with content adaptation skill
- [ ] T082 [P] Create `translation_skill.md` with translation skill
- [ ] T083 [P] Create `chat_interface_skill.md` with chat interface skill
- [ ] T084 [P] Create `user_management_skill.md` with user management skill
- [ ] T085 [P] Test all Claude Code Subagents for proper functionality
- [ ] T086 [P] Test all Claude Code Agent Skills for proper functionality

---

## Phase 8: Integration & Polish

### Goal
Integrate all components and implement final polish for deployment.

- [ ] T087 [P] Integrate chatbot beautifully in every page as specified
- [ ] T088 [P] Ensure responsive UI/UX works across desktop and mobile devices (FR-020)
- [ ] T089 [P] Implement authentication requirements: core content available to guests, personalization/chatbot require auth (FR-021)
- [ ] T090 [P] Create GitHub Pages deployment configuration in `.github/workflows/deploy.yml`
- [ ] T091 [P] Test platform supports 100 concurrent users without performance degradation (SC-005)
- [ ] T092 [P] Verify RAG chatbot successfully restricts answers to selected text only with 95% accuracy (SC-011)
- [ ] T093 [P] Verify Better-Auth signup captures background with 100% completion rate (SC-012)
- [ ] T094 [P] Verify personalization button adapts content difficulty/examples (SC-013)
- [ ] T095 [P] Verify Urdu translation provides accurate translations (SC-014)
- [ ] T096 [P] Verify all 100 base points and 200 bonus points requirements are implemented (SC-015)
- [ ] T097 [P] Optimize performance to meet <2-second response time requirements
- [ ] T098 [P] Ensure WCAG 2.1 AA accessibility compliance
- [ ] T099 [P] Create 90-second demo video showcasing all core features (FR-011)
- [ ] T100 [P] Prepare submission materials including GitHub repository and live deployed link (FR-013)

---

## Policy Note for Lesson Authors

Within this chapter, each lesson must end with a single final section titled "Try With AI" (no "Key Takeaways" or "What's Next"). Before AI tools are taught (e.g., Part-1), use ChatGPT web in that section; after tool onboarding, instruct learners to use their preferred AI companion tool (e.g., Gemini CLI, Claude CLI), optionally providing CLI and web variants.