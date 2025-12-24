# Tasks: UI/UX Optimization & Project Restructure

**Input**: Design documents from `E:/hakaton 1/AI-native-textbook/specs/007-ui-ux-restructure/`
**Prerequisites**: ✅ plan.md, ✅ spec.md

**Tests**: Not required - this is infrastructure and UI polish work

**Organization**: Tasks grouped by user story to enable independent implementation and testing

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3, US4, US5)
- Exact file paths included in descriptions

## Path Conventions

- **Web app structure**: `backend/`, `frontend/`
- **Frontend**: `frontend/docs/`, `frontend/src/`, `frontend/static/`
- **Backend**: `backend/api/`, `backend/services/`, `backend/models/`
- **Spec-Kit**: `.specify/`, `specs/`, `history/` (preserve at root)

---

## Phase 1: Setup (Preparation & Safety)

**Purpose**: Create safety net and audit current state before changes

- [X] T001 Create git backup tag before any destructive changes: `git tag -a pre-007-restructure -m "Backup before UI/UX optimization"` ✅
- [X] T002 [P] Audit root directory and create inventory of files to delete: `ls -la > ROOT_INVENTORY.txt` ✅
- [X] T003 [P] Verify frontend and backend directories already exist: `test -d frontend && test -d backend` ✅
- [X] T004 [P] Verify all Spec-Kit folders exist and will be preserved: `test -d .specify && test -d history && test -d specs` ✅

---

## Phase 2: Foundational (Root Directory Cleanup)

**Purpose**: Clean root directory - MUST be complete before UI/UX changes

**⚠️ CRITICAL**: This phase removes clutter and establishes clean project structure

- [ ] T005 [P] Delete legacy folders: `rm -rf ai-textbook-backend/ hf-spaces/ node_modules/` (if they exist at root)
- [ ] T006 Delete redundant documentation files (23 files):
  ```bash
  rm -f ALTERNATIVE_DEPLOYMENT.md COMPLETE_DEPLOYMENT_GUIDE.md COMPLETE_FIX_GUIDE.md \
        CORS_FIX.md CUSTOMIZATION_SUMMARY.md DEPLOYMENT.md DEPLOYMENT_CHECKLIST.md \
        DEPLOYMENT_SCRIPTS.md DEPLOYMENT_SUMMARY.md FEATURE_005_FIXED.md \
        FINAL_FEATURE_SUMMARY.md IMPLEMENTATION_SUMMARY.md PROJECT_COMPLETION_CERTIFICATE.md \
        QUICK_START_AFTER_DEPLOYMENT.md REDEPLOY_BACKEND.md RESTART_BACKEND.md \
        RUN_ME_FIRST.md RUNNING_INSTRUCTIONS.md SETUP.md START_HERE.md \
        TESTING_GUIDE.md WINDOWS_SETUP.md ROUTING.md
  ```
- [ ] T007 Delete temporary debug scripts: `rm -f debug_*.py` (5 files)
- [ ] T008 Delete temporary test scripts at root: `rm -f test_*.py test_*.js` (12 files)
- [ ] T009 Delete utility scripts: `rm -f process_*.py create_placeholder_images.py embeddings_setup.js simple_verify.py verify_embeddings.py final_verification*.py demo.sh`
- [ ] T010 Delete root-level config files now in frontend/backend: `rm -f package.json package-lock.json requirements.txt railway.json Dockerfile qdrant-x86_64-unknown-linux-gnu.tar.gz NUL temp.txt`
- [ ] T011 Verify Spec-Kit folders still intact: `test -d .specify && test -d history && test -d specs && echo "Spec-Kit preserved"`
- [ ] T012 [P] Create professional root README.md with project overview and links to frontend/backend READMEs
- [ ] T013 [P] Create frontend/README.md with setup instructions: document npm install, npm start, npm run build commands
- [ ] T014 [P] Create backend/README.md with setup instructions: document pip install, uvicorn startup, environment variables
- [ ] T015 Commit Phase 2 changes: `git add . && git commit -m "chore: Phase 2 - Clean root directory and add documentation"`

**Checkpoint**: Root directory now clean with only `/frontend`, `/backend`, Spec-Kit folders, and essential docs

---

## Phase 3: User Story 1 - Clean Professional Book Reading Experience (Priority: P1) 🎯 MVP

**Goal**: Remove all Docusaurus boilerplate to present site as a focused technical book

**Independent Test**:
1. Run `npm start` in frontend/
2. Visit http://localhost:3000
3. Verify header has NO "Blog" or "GitHub" links
4. Verify sidebar has NO "Sample" or "Tutorial" pages
5. Verify footer has NO "Built with Docusaurus" text

### Implementation for User Story 1

- [ ] T016 [US1] Update frontend/docusaurus.config.js to disable blog feature: set `blog: false` (around line 59-73)
- [ ] T017 [P] [US1] Delete frontend/blog/ directory: `rm -rf frontend/blog/`
- [ ] T018 [P] [US1] Use `npm run swizzle @docusaurus/theme-classic Footer -- --eject` in frontend/ to create custom footer component
- [ ] T019 [US1] Edit frontend/src/theme/Footer/index.js to remove "Built with Docusaurus" branding and replace with book-specific footer:
  - Replace default footer with book title, resources links, community links
  - Add copyright notice: "© 2025 Physical AI Textbook. Open Educational Resource."
  - Test footer renders correctly on all pages
- [ ] T020 [US1] Update frontend/docusaurus.config.js navbar items (lines 116-143) to remove GitHub link:
  - Keep: Chapters, Capstone, Search, Login, Sign Up
  - Remove: GitHub href link
  - Rename "Physical AI" to "Chapters" for clarity
- [ ] T021 [US1] Update frontend/sidebars.js to show only book content (4 modules + capstone):
  - Keep: intro, 4 module categories, weekly-plan, hardware-specifications, capstone-project
  - Remove: any tutorial/sample pages if they exist
  - Verify structure matches lines 17-66 in current sidebars.js
- [ ] T022 [P] [US1] Test frontend build: `cd frontend && npm run build` (must complete in <3 minutes)
- [ ] T023 [US1] Manual test navigation: verify no Blog, GitHub (header), or Docusaurus branding visible
- [ ] T024 [US1] Commit User Story 1 changes: `git add frontend/ && git commit -m "feat(ui): US1 - Remove Docusaurus boilerplate"`

**Checkpoint**: Site now presents as professional book, not generic Docusaurus site

---

## Phase 4: User Story 2 - Enhanced Book Navigation & Reading Tools (Priority: P1) 🎯 MVP

**Goal**: Add reading progress bar, estimated reading time, chapter navigation, and enhanced TOC

**Independent Test**:
1. Open any chapter
2. Verify reading progress bar appears at top (green bar, 4px height)
3. Scroll through chapter and verify progress bar fills 0% → 100%
4. Verify estimated reading time displays at chapter start (e.g., "12 min read")
5. Verify Previous/Next chapter buttons appear at bottom
6. Verify TOC highlights current chapter

### Implementation for User Story 2

#### Reading Progress Bar

- [ ] T025 [P] [US2] Create frontend/src/components/ReadingProgress/index.js component:
  - Use useState and useEffect hooks to track scroll position
  - Calculate progress: `(scrollTop / scrollHeight) * 100`
  - Debounce with requestAnimationFrame for <50ms latency
  - Return fixed-position div with progress bar (4px height, NVIDIA Green)
- [ ] T026 [P] [US2] Create frontend/src/components/ReadingProgress/styles.css:
  - Fixed positioning (top: 0, left: 0, width: 100%, z-index: 100)
  - Progress bar gradient: `linear-gradient(90deg, #76B900, #8FD600)`
  - Smooth transition: `width 0.1s ease-out`
  - Dark mode variant with lighter green
- [ ] T027 [US2] Integrate ReadingProgress into frontend/src/theme/DocItem/Content/index.jsx:
  - Import ReadingProgress component
  - Render at top of Content wrapper (before existing PersonalizeButton/UrduTranslationButton)
  - Test component renders only on doc pages (not homepage)

#### Estimated Reading Time

- [ ] T028 [P] [US2] Create frontend/src/plugins/reading-time.js remark plugin:
  - Count words in MDX content using `mdast-util-to-string`
  - Count code blocks (add 2 minutes each)
  - Count images (add 30 seconds each)
  - Calculate: `Math.ceil(words / 225 + codeBlocks * 2 + images * 0.5)` minutes
  - Attach to file.data.readingTime
- [ ] T029 [US2] Register reading-time plugin in frontend/docusaurus.config.js:
  - Import plugin: `const readingTimePlugin = require('./src/plugins/reading-time');`
  - Add to docs.remarkPlugins array in presets[0][1].docs
  - Verify plugin runs during build
- [ ] T030 [US2] Display reading time in frontend/src/theme/DocItem/Content/index.jsx:
  - Access metadata.readingTime from useDoc() hook
  - Render "⏱️ X min read" at top of chapter content
  - Style with gray color and small font size

#### Chapter Navigation

- [ ] T031 [P] [US2] Create frontend/src/components/ChapterNavigation/index.js component:
  - Access metadata.previous and metadata.next from useDoc() hook
  - Render Previous and Next links if they exist
  - Include chapter titles in link text
  - Add arrow icons (← and →)
- [ ] T032 [P] [US2] Create frontend/src/components/ChapterNavigation/styles.css:
  - Flexbox layout (space-between) for Previous/Next buttons
  - Button styles: padding 1rem, border-radius 8px, NVIDIA Green on hover
  - Arrow icons styled with NVIDIA Green
  - Mobile responsive: stack vertically on small screens
- [ ] T033 [US2] Integrate ChapterNavigation into frontend/src/theme/DocItem/Content/index.jsx:
  - Render at bottom of Content wrapper (after existing content)
  - Test navigation works between chapters

#### Enhanced TOC

- [ ] T034 [P] [US2] Use `npm run swizzle @docusaurus/theme-classic TOC -- --eject` in frontend/ to create custom TOC
- [ ] T035 [US2] Customize frontend/src/theme/TOC/index.js:
  - Add wrapper div with enhanced styling class
  - Keep TOC sticky (position: sticky, top: calc(navbar-height + 2rem))
  - Make scrollable independently (max-height: calc(100vh - navbar-height - 4rem))
- [ ] T036 [P] [US2] Create frontend/src/theme/TOC/styles.css:
  - Active link: NVIDIA Green color, 4px left border, bold font
  - Hover state: light green background (rgba(118, 185, 0, 0.05))
  - Sticky positioning with scroll overflow
- [ ] T037 [P] [US2] Test all navigation features work on mobile (375px viewport)
- [ ] T038 [US2] Commit User Story 2 changes: `git add frontend/src/components/ frontend/src/theme/ frontend/src/plugins/ && git commit -m "feat(ui): US2 - Add book navigation features"`

**Checkpoint**: Users now have professional book navigation tools (progress, time estimate, chapter nav, TOC)

---

## Phase 5: User Story 3 - Professional Humanoid Robotics Theme (Priority: P2)

**Goal**: Apply Silver/Dark Slate/NVIDIA Green color scheme consistently across all UI

**Independent Test**:
1. View site in light mode
2. Verify Silver (#C0C0C0) used for backgrounds/neutral elements
3. Verify NVIDIA Green (#76B900) used for accents/hover states
4. Switch to dark mode
5. Verify Dark Slate (#2F4F4F, #1C1C1C) used for backgrounds
6. Verify theme is consistent across all pages

### Implementation for User Story 3

- [ ] T039 [P] [US3] Create frontend/src/css/theme-colors.css with color variable definitions:
  - Define CSS custom properties for all theme colors
  - Light mode: Silver (#C0C0C0, #D3D3D3, #A8A8A8), NVIDIA Green (#76B900, #5A8F00, #8FD600)
  - Dark mode: Dark Slate (#2F4F4F, #1C1C1C, #3A5A5A), Silver (#E0E0E0), NVIDIA Green (#8FD600)
  - Map to Infima variables: `--ifm-color-primary`, `--ifm-navbar-background-color`, etc.
- [ ] T040 [US3] Import theme-colors.css in frontend/src/css/custom.css: Add `@import './theme-colors.css';` at top
- [ ] T041 [P] [US3] Apply theme to navbar in custom.css:
  - Background: `var(--ifm-navbar-background-color)`
  - Active link: `color: var(--robotics-nvidia-green)`, `border-bottom: 2px solid`
  - Hover state: transition to NVIDIA Green
- [ ] T042 [P] [US3] Apply theme to footer in custom.css:
  - Background: `var(--ifm-footer-background-color)`
  - Top border: `3px solid var(--robotics-nvidia-green)`
  - Link hover: NVIDIA Green color
- [ ] T043 [P] [US3] Apply theme to sidebar in custom.css:
  - Active menu link: NVIDIA Green color, 4px left border, light green background
  - Hover state: rgba(118, 185, 0, 0.05) background
- [ ] T044 [P] [US3] Apply theme to buttons (signup, personalize, translate) in custom.css:
  - Background: `var(--robotics-nvidia-green)`
  - Hover: darker green with transform translateY(-2px)
  - Ensure existing button functionality preserved
- [ ] T045 [P] [US3] Apply theme to chatbot toggle in custom.css:
  - Gradient background using NVIDIA Green variants
  - Box shadow with green glow: `0 8px 25px rgba(118, 185, 0, 0.4)`
- [ ] T046 [US3] Test accessibility with WebAIM Contrast Checker (https://webaim.org/resources/contrastchecker/):
  - Verify all text/background combinations meet WCAG 2.1 AA (4.5:1 for normal text, 3:1 for large text)
  - Document results in ACCESSIBILITY_REPORT.md
  - Fix any failing combinations by darkening NVIDIA Green for small text
- [ ] T047 [US3] Test theme in both light and dark modes: verify smooth transition, no visual glitches
- [ ] T048 [US3] Commit User Story 3 changes: `git add frontend/src/css/ && git commit -m "feat(ui): US3 - Implement Humanoid Robotics theme"`

**Checkpoint**: Professional robotics theme applied consistently, accessibility verified

---

## Phase 6: User Story 4 - Standardized Project Structure (Priority: P2)

**Goal**: Ensure clean separation of frontend/backend with no root-level clutter

**Independent Test**:
1. List root directory: `ls -la`
2. Verify only these exist: `.git/`, `.specify/`, `history/`, `specs/`, `frontend/`, `backend/`, `README.md`, `CLAUDE.md`, `DEPLOYMENT.md`
3. Run frontend: `cd frontend && npm install && npm start` (must work)
4. Run backend: `cd backend && pip install -r requirements.txt && uvicorn main:app --reload` (must work)
5. Verify no broken imports

### Implementation for User Story 4

**NOTE**: Frontend and backend directories already exist, so focus is on verification and cleanup

- [ ] T049 [P] [US4] Verify all frontend code in frontend/ directory: `find frontend/ -type f -name "*.js" -o -name "*.jsx" | wc -l` (expect 50+ files)
- [ ] T050 [P] [US4] Verify all backend code in backend/ directory: `find backend/ -type f -name "*.py" | wc -l` (expect 30+ files)
- [ ] T051 [P] [US4] Verify frontend builds: `cd frontend && npm install && npm run build` (must succeed in <3 minutes)
- [ ] T052 [P] [US4] Verify backend starts: `cd backend && pip install -r requirements.txt && uvicorn main:app --reload --port 8001` (must succeed in <10 seconds)
- [ ] T053 [US4] Test existing features still work after cleanup:
  - Frontend: Homepage loads, login/signup pages work, chatbot opens
  - Backend: API docs accessible at http://localhost:8001/docs
  - Integration: Frontend can call backend APIs (test /api/auth/profile endpoint)
- [ ] T054 [US4] Document final directory structure in root README.md:
  - Update "Project Structure" section with accurate tree
  - Verify all links to frontend/backend READMEs work
- [ ] T055 [US4] Commit User Story 4 verification: `git add . && git commit -m "chore: US4 - Verify project structure is clean"`

**Checkpoint**: Project structure is clean, both services run correctly, all features preserved

---

## Phase 7: User Story 5 - Deployment-Ready Configuration (Priority: P3)

**Goal**: Prepare deployment configs for Vercel (frontend) and Hugging Face Spaces (backend)

**Independent Test**:
1. Verify frontend/vercel.json exists with correct settings
2. Verify backend/Dockerfile exists and builds
3. Verify backend/app.py entry point exists for HF Spaces
4. Verify .env.example files exist with all required variables documented
5. Verify DEPLOYMENT.md guide exists with step-by-step instructions

### Implementation for User Story 5

#### Frontend Vercel Configuration

- [ ] T056 [P] [US5] Update frontend/vercel.json with optimized settings:
  - Framework: "docusaurus"
  - Build command: "npm run build"
  - Output directory: "build"
  - Install command: "npm install"
  - Add rewrites for /api proxy to HF Space URL
  - Add security headers (X-Content-Type-Options, X-Frame-Options, X-XSS-Protection)
- [ ] T057 [P] [US5] Create frontend/.env.example documenting required environment variables:
  ```
  REACT_APP_API_URL=http://localhost:8001
  REACT_APP_API_PROXY=/api
  ```
- [ ] T058 [US5] Test Vercel build locally: `cd frontend && npm run build && npx serve build/` (verify build works)

#### Backend Hugging Face Spaces Configuration

- [ ] T059 [P] [US5] Update backend/Dockerfile for HF Spaces optimization:
  - Base image: `FROM python:3.9-slim`
  - WORKDIR /app
  - Install dependencies: `COPY requirements.txt . && RUN pip install --no-cache-dir -r requirements.txt`
  - Copy application: `COPY . .`
  - Expose port 7860 (HF Spaces default)
  - CMD: `["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]`
- [ ] T060 [P] [US5] Create backend/app.py as HF Spaces entry point:
  ```python
  # Hugging Face Spaces expects app.py
  from main import app
  if __name__ == "__main__":
      import uvicorn
      uvicorn.run(app, host="0.0.0.0", port=7860)
  ```
- [ ] T061 [P] [US5] Update backend/.env.example with all required production environment variables:
  - DATABASE_URL, QDRANT_URL, QDRANT_API_KEY, QDRANT_COLLECTION
  - GOOGLE_API_KEY, OPENROUTER_API_KEY
  - JWT_SECRET, JWT_ALGORITHM, JWT_EXPIRATION
  - CORS_ORIGINS (include Vercel domain)
- [ ] T062 [US5] Remove legacy deployment configs: `rm -f backend/railway.json backend/railway.toml` (if they exist)
- [ ] T063 [US5] Test Docker build: `cd backend && docker build -t ai-textbook-backend .` (must succeed)

#### Deployment Documentation

- [ ] T064 [P] [US5] Create root-level DEPLOYMENT.md with comprehensive deployment guide:
  - Section 1: Architecture overview (frontend→Vercel, backend→HF Spaces, DB→Neon, Vector→Qdrant)
  - Section 2: Frontend deployment to Vercel (step-by-step with screenshots)
  - Section 3: Backend deployment to HF Spaces (step-by-step with screenshots)
  - Section 4: Database setup (Neon Postgres, run migrations)
  - Section 5: Vector DB setup (Qdrant Cloud, seed embeddings)
  - Section 6: Environment variables for both platforms
  - Section 7: Troubleshooting common issues
  - Section 8: Rollback procedures
- [ ] T065 [US5] Commit User Story 5 changes: `git add frontend/vercel.json backend/Dockerfile backend/app.py backend/.env.example DEPLOYMENT.md && git commit -m "chore: US5 - Prepare deployment configurations"`

**Checkpoint**: Deployment configurations ready for both platforms, comprehensive guide available

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements and validation

- [ ] T066 [P] Run accessibility audit: `cd frontend && npx @axe-core/cli http://localhost:3000 --save accessibility-report.json`
- [ ] T067 [P] Run Lighthouse performance audit: `lighthouse http://localhost:3000 --output html --output-path lighthouse-report.html` (target: score >90)
- [ ] T068 [P] Test cross-browser compatibility: Chrome, Firefox, Safari, Edge (document results)
- [ ] T069 [P] Test mobile responsiveness on 3 device sizes: 375px (iPhone SE), 768px (iPad), 414px (iPhone 11 Pro)
- [ ] T070 [P] Test all existing features still work:
  - RAG chatbot opens and responds
  - Login/signup flows work
  - Personalization button functions
  - Urdu translation button functions
  - All buttons use new theme colors
- [ ] T071 Create TEST_REPORT.md documenting all test results (accessibility, performance, cross-browser, mobile, features)
- [ ] T072 Update specs/007-ui-ux-restructure/spec.md status from "Draft" to "Implemented"
- [ ] T073 Final commit: `git add . && git commit -m "feat: Complete Feature 007 - UI/UX Optimization & Project Restructure"`
- [ ] T074 Push to remote: `git push origin 007-ui-ux-restructure`
- [ ] T075 Create pull request with comprehensive description and test results
- [ ] T076 After PR approval, merge to main and delete feature branch

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational - Can start after cleanup
- **User Story 2 (Phase 4)**: Depends on User Story 1 - Navigation builds on clean UI
- **User Story 3 (Phase 5)**: Independent of US1-2 - Can start after Foundational
- **User Story 4 (Phase 6)**: Depends on Foundational - Verification phase
- **User Story 5 (Phase 7)**: Independent - Can start anytime, but best after US1-4 complete
- **Polish (Phase 8)**: Depends on all user stories being complete

### User Story Dependencies

- **US1 (Clean UI)**: CRITICAL - Foundation for professional appearance
- **US2 (Navigation)**: Depends on US1 (navigation overlays on clean UI)
- **US3 (Theme)**: Independent - Can implement in parallel with US1/US2
- **US4 (Structure)**: Independent - Verification only (structure already exists)
- **US5 (Deployment)**: Independent - Can prepare anytime

### Parallel Opportunities

- **Phase 2**: T007-T010 (all file deletions) can run in parallel
- **Phase 2**: T012-T014 (README creation) can run in parallel
- **Phase 3**: T017, T018 (delete blog, swizzle footer) can run in parallel
- **Phase 4**: T025-T026 (ReadingProgress component + styles) can run in parallel
- **Phase 4**: T028-T029 (reading-time plugin + registration) can run in parallel
- **Phase 4**: T031-T032 (ChapterNavigation component + styles) can run in parallel
- **Phase 5**: T056-T057 (Vercel config + .env.example) can run in parallel
- **Phase 5**: T059-T061 (Dockerfile + app.py + .env.example) can run in parallel
- **Phase 8**: T066-T070 (all testing tasks) can run in parallel

---

## Implementation Strategy

### MVP First (User Stories 1-2 Only) - RECOMMENDED

1. Complete Phase 1: Setup (T001-T004)
2. Complete Phase 2: Foundational Cleanup (T005-T015)
3. Complete Phase 3: User Story 1 - Clean UI (T016-T024)
4. Complete Phase 4: User Story 2 - Navigation (T025-T038)
5. **STOP and VALIDATE**: Test both stories independently
6. Deploy/demo if ready
7. **Estimated effort**: ~15-20 hours (38 tasks)

### Incremental Delivery

1. **Phase 1-2**: Setup + Cleanup → Clean project structure (~8 tasks, ~4 hours)
2. **Phase 3**: User Story 1 → Test independently → Deploy/Demo (~9 tasks, ~6 hours)
3. **Phase 4**: User Story 2 → Test independently → Deploy/Demo (~14 tasks, ~10 hours)
4. **Phase 5**: User Story 3 → Test independently → Deploy/Demo (~10 tasks, ~6 hours)
5. **Phase 6**: User Story 4 → Verify structure → Deploy/Demo (~7 tasks, ~2 hours)
6. **Phase 7**: User Story 5 → Prepare deployment → Deploy/Demo (~10 tasks, ~6 hours)
7. **Phase 8**: Polish → Final release (~11 tasks, ~4 hours)
8. **Total estimated effort**: ~38 hours (76 tasks)

### Parallel Team Strategy

With 2 developers:

1. **Together**: Complete Setup + Foundational (T001-T015)
2. **Once Foundational done**:
   - **Developer A**: User Story 1 (T016-T024) - Remove boilerplate
   - **Developer B**: User Story 3 (T039-T048) - Implement theme
3. **After US1 complete**:
   - **Developer A**: User Story 2 (T025-T038) - Add navigation features
   - **Developer B**: User Story 5 (T056-T065) - Prepare deployment
4. **Together**: User Story 4 (T049-T055) - Verify structure
5. **Together**: Phase 8 Polish (T066-T076)

---

## Notes

- [P] tasks = different files, no dependencies - can run in parallel
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Frontend and backend directories already exist - tasks focus on cleanup and enhancement, not initial creation
- Stop at any checkpoint to validate story independently
- **User-provided context integrated**:
  - ✅ Structure verification: Frontend/backend folders already exist
  - ✅ Cleanup focus: Remove 30+ redundant files from root
  - ✅ UI polish: Swizzle components, apply theme, add navigation
  - ✅ Deployment prep: Vercel + HF Spaces configurations
  - ✅ Spec-Kit preservation: .specify/, history/, specs/ stay at root
