<!--
Sync Impact Report:
- Version change: 1.0.0 → 1.0.0 (initial creation)
- Added sections: Core Principles (6), Technology Stack, Development Workflow, Governance
- Templates requiring updates: ✅ all created from scratch
- Follow-up TODOs: none
-->

# Physical AI & Humanoid Robotics Constitution

## Core Principles

### I. AI-Native Educational Content
All content must be designed from the ground up for AI interaction and enhancement. Traditional textbook approaches are insufficient; content must leverage AI capabilities for personalization, interactive learning, and adaptive explanations. Rationale: To create truly innovative educational material that surpasses conventional textbooks through AI integration.

### II. Modular & Extensible Architecture
Content and features must be built as modular components that can be independently developed, tested, and enhanced. Docusaurus-based structure with clear separation of concerns between textbook content, RAG system, authentication, and personalization features. Rationale: Enables parallel development of complex features and facilitates future enhancements.

### III. Test-First Development (NON-NEGOTIABLE)
All features must follow TDD methodology: tests written → user approved → tests fail → then implement. This applies to both textbook content validation and technical features. Red-Green-Refactor cycle strictly enforced for all code and content. Rationale: Ensures quality and correctness of both educational content and technical implementation.

### IV. Full Integration Testing
Focus areas requiring comprehensive integration testing: RAG chatbot functionality with textbook content, authentication flow with personalization features, translation services, Claude Subagent interactions, and cross-component dependencies. Rationale: Complex AI features require thorough testing of component interactions.

### V. Performance & Accessibility
All features must maintain sub-2-second response times for user interactions and meet WCAG 2.1 AA accessibility standards. RAG system must handle concurrent users efficiently. Rationale: Educational platform must be responsive and accessible to all learners regardless of physical capabilities.

### VI. Data Privacy & Security
Student data, authentication credentials, and personalization preferences must be handled with industry-standard security practices. All data flows must be encrypted, and user consent must be obtained for data usage. Rationale: Educational platforms must maintain highest standards of data protection for students.

## Technology Stack Requirements

- **Frontend**: Docusaurus v3+ for static site generation with React-based customization
- **Backend API**: FastAPI for RAG chatbot backend services
- **Authentication**: Better-Auth for secure user authentication with background question collection
- **Database**: Neon Postgres for user data and content metadata
- **Vector Storage**: Qdrant Free for RAG content indexing
- **AI Integration**: OpenAI API for chatbot responses and Claude Subagents for advanced features
- **Deployment**: GitHub Pages for static content, with backend services hosted separately
- **Translation**: Per-chapter Urdu translation capability using AI translation services

## Development Workflow

- **Content Creation**: Follow 9-page course document with strict adherence to modules, weekly breakdown, hardware requirements, and capstone project specifications
- **Feature Implementation**: Prioritize base 100 points before bonus 200 points (Claude Subagents, Better-Auth signup, personalization, Urdu translation)
- **Code Review**: All PRs must verify compliance with constitution principles and course document requirements
- **Quality Gates**: All features must pass integration tests, accessibility checks, and performance benchmarks before merging
- **Milestone Tracking**: Weekly progress reviews aligned with November 30, 2025 deadline

## Governance

This constitution supersedes all other development practices and course guidelines. All development decisions must align with these principles. Amendments require explicit documentation of reasoning, team approval, and impact assessment on existing features. All PRs and reviews must verify compliance with both technical requirements and educational objectives.

**Version**: 1.0.0 | **Ratified**: 2025-12-10 | **Last Amended**: 2025-12-10
