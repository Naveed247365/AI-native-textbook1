# Feature Specification: AI Backend with RAG + Authentication

**Feature Branch**: `003-ai-backend`
**Created**: 2025-12-11
**Status**: Draft
**Input**: User description: "PROJECT NAME:

Full AI Backend with RAG + Authentication using Qdrant, Neon, Gemini Embeddings, Gemini Chat, FastAPI, and Better Auth.

OVERALL GOAL:

Build a scalable backend that:

- Authenticates users using Better Auth (JWT + Session-based)

- Stores user + project data in Neon Postgres

- Uses Gemini "text-embedding-004" model for embeddings

- Uses Qdrant as the Vector DB for RAG search

- Uses Gemini 1.5 Flash/Pro for answer generation

- Provides endpoints for embedding, search, saving chat history, and managing users

- Works inside a clean folder structure for maintainability

- Can be extended later into dashboards or mobile apps

CORE FEATURES:

1. Better Auth Integration

   - User signup

   - User login

   - Session token generation

   - JWT + cookies support

   - Auth middleware to protect routes

   - Secure password hashing

2. Gemini Embedding Integration

   - Use model: text-embedding-004

   - Single function: generate_embedding(text)

   - Use same GEMINI_API_KEY from .env

3. Qdrant Vector DB

   - Connect using QDRANT_URL + QDRANT_API_KEY

   - Create collection: "documents"

   - Upsert embeddings

   - Similarity search

   - Filter by user_id for private RAG

4. Neon Postgres Database

   - Connect using NEON_DB_URL

   - Create tables:

     - users

     - chat_history

     - documents

   - CRUD operations

5. RAG Pipeline

   - Convert text → embedding

   - Embed via Gemini

   - Store vectors in Qdrant

   - Search via similarity

   - Generate answer using Gemini chat model

   - Return final combined result

6. FastAPI Backend

   Endpoints:

   - POST /auth/signup

   - POST /auth/login

   - GET  /auth/me

   - POST /embed

   - POST /save-document

   - POST /search

   - GET  /history

   - GET  /health

7. Scripts

   - seed_qdrant.py → upload files/documents

   - migrate_neon.py → create required tables

8. Folder Structure

   src/

     auth/

     db/

     qdrant/

     embeddings/

     rag/

     routes/

     scripts/

     utils/

     models/

     config/

9. Environment Variables

   GEMINI_API_KEY=

   QDRANT_URL=

   QDRANT_API_KEY=

   NEON_DB_URL=

   SECRET_KEY=

   JWT_EXPIRES_IN=

10. Code Quality Rules

   - Use Pydantic models

   - Async FastAPI everywhere

   - No hard-coded secrets

   - Comment every function

   - Beginner-friendly readable code

   - 0 placeholder code"

## Evals (Success Criteria)

### Measurable Outcomes

- **SC-001**: Users can successfully register and authenticate with JWT tokens generated within 500ms
- **SC-002**: Document embeddings are generated and stored in Qdrant within 3 seconds per document up to 10,000 characters
- **SC-003**: Semantic search returns relevant results with 90%+ accuracy based on vector similarity (measured as cosine similarity >0.7 between query and top 5 results when ground truth is available)
- **SC-004**: Chat history is stored and retrieved with 99.9% reliability in Neon Postgres
- **SC-005**: API endpoints respond within 2 seconds under normal load conditions (up to 100 concurrent users)
- **SC-006**: The system can handle private RAG by filtering documents by user_id with 100% accuracy
- **SC-007**: All authentication and data storage follows security best practices with no hardcoded secrets

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.
  
  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently
-->

### User Story 1 - Register and Authenticate (Priority: P1)

As a new user, I want to register for the service and authenticate so that I can access my private RAG documents and maintain secure sessions.

**Why this priority**: This is the foundational functionality that enables all other features - without authentication, users cannot securely access the RAG system.

**Independent Test**: Can be fully tested by registering a new user, logging in, and verifying JWT token generation. Delivers secure access to the system.

**Acceptance Scenarios**:

1. **Given** a user with valid credentials, **When** they call POST /auth/signup, **Then** a new account is created with secure password hashing and they receive a JWT token
2. **Given** a registered user with valid credentials, **When** they call POST /auth/login, **Then** they receive a valid JWT token and session cookie
3. **Given** a user with a valid JWT token, **When** they call GET /auth/me, **Then** their user profile is returned with appropriate permissions

---

### User Story 2 - Store and Embed Documents (Priority: P1)

As an authenticated user, I want to upload documents and have them processed for RAG so that I can later search and retrieve information from them.

**Why this priority**: This enables the core RAG functionality - without stored and embedded documents, the search feature cannot work.

**Independent Test**: Can be fully tested by uploading a document, verifying it gets embedded using Gemini, and stored in Qdrant. Delivers the foundation for search capabilities.

**Acceptance Scenarios**:

1. **Given** an authenticated user with a document, **When** they call POST /save-document, **Then** the document is embedded using Gemini text-embedding-004 and stored in Qdrant with user_id filter
2. **Given** a document text, **When** the system calls the embedding function, **Then** a vector representation is generated using Gemini text-embedding-004 within 3 seconds
3. **Given** an embedded document, **When** it's stored in Qdrant, **Then** it's indexed with user_id for private RAG access

---

### User Story 3 - Search Documents with RAG (Priority: P1)

As an authenticated user, I want to search my documents using natural language so that I can quickly find relevant information.

**Why this priority**: This is the core value proposition of the RAG system - enabling semantic search across user documents.

**Independent Test**: Can be fully tested by searching for information in stored documents and receiving relevant results. Delivers the main RAG functionality.

**Acceptance Scenarios**:

1. **Given** an authenticated user with stored documents, **When** they call POST /search with a query, **Then** relevant document snippets are returned based on vector similarity
2. **Given** a search query, **When** the system processes it through the RAG pipeline, **Then** it returns results filtered by the user's documents only
3. **Given** a search query and relevant context, **When** Gemini 1.5 Flash/Pro generates an answer, **Then** a contextual response is provided within 5 seconds

---

### User Story 4 - Manage Chat History (Priority: P2)

As an authenticated user, I want to save and retrieve my chat history so that I can continue conversations and track my interactions with the system.

**Why this priority**: This enhances user experience by providing continuity and context preservation across sessions.

**Independent Test**: Can be fully tested by conducting a conversation, saving the history, and retrieving it later. Delivers conversation persistence.

**Acceptance Scenarios**:

1. **Given** an authenticated user in a conversation, **When** the system saves chat history, **Then** the conversation is stored in Neon Postgres with user_id association
2. **Given** an authenticated user, **When** they request chat history, **Then** their previous conversations are retrieved from Neon Postgres

---

### User Story 5 - System Health and Monitoring (Priority: P2)

As a system administrator, I want to monitor system health so that I can ensure the backend is running properly and identify issues.

**Why this priority**: This is essential for maintaining system reliability and operational awareness.

**Independent Test**: Can be fully tested by calling health endpoints and verifying all services (auth, database, vector store, AI) are accessible. Delivers operational visibility.

**Acceptance Scenarios**:

1. **Given** a healthy system, **When** GET /health is called, **Then** all connected services (Postgres, Qdrant, Gemini API) are confirmed as operational
2. **Given** a system component failure, **When** GET /health is called, **Then** the failure is reported with appropriate error status

---

### Edge Cases

- What happens when the Gemini API is temporarily unavailable? The system should queue requests or provide appropriate error messages to users
- How does the system handle extremely large documents that exceed Gemini's token limits? The system should chunk documents or provide size validation
- What happens when Qdrant vector database is down during document storage? The system should queue operations or return appropriate error responses
- How does the system handle concurrent users exceeding capacity? The system should implement rate limiting and graceful degradation
- What if a user tries to access another user's documents? The system must enforce strict user_id filtering in all queries

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST implement user registration with secure password hashing using industry-standard algorithms
- **FR-002**: System MUST generate JWT tokens with configurable expiration times for session management
- **FR-003**: System MUST store user credentials in Neon Postgres database with proper encryption at rest
- **FR-004**: System MUST authenticate users via JWT tokens and enforce session validation on protected routes
- **FR-005**: System MUST generate document embeddings using Gemini text-embedding-004 model
- **FR-006**: System MUST store document embeddings in Qdrant vector database with user_id metadata for private RAG
- **FR-007**: System MUST perform semantic search using vector similarity with configurable result limits
- **FR-008**: System MUST generate contextual responses using Gemini 1.5 Flash/Pro model based on search results
- **FR-009**: System MUST store chat history in Neon Postgres with user_id association for conversation persistence
- **FR-010**: System MUST filter search results by user_id to ensure private RAG access
- **FR-011**: System MUST validate all API inputs to prevent injection attacks and ensure data integrity
- **FR-012**: System MUST implement proper error handling with appropriate HTTP status codes and graceful degradation when external services (Gemini, Qdrant, Neon) are unavailable
- **FR-013**: System MUST support document uploads up to 10MB with appropriate validation
- **FR-014**: System MUST implement rate limiting to prevent abuse of API endpoints
- **FR-015**: System MUST provide health check endpoints for all connected services (Postgres, Qdrant, Gemini)

### Key Entities *(include if feature involves data)*

- **User**: Represents authenticated users with credentials, profile information, and permissions
- **Document**: Represents user-uploaded content that gets processed for RAG, including original text, embedding vectors, and metadata
- **ChatHistory**: Represents conversation records between users and the AI system, including queries and responses
- **Embedding**: Represents vector representations of documents generated by the Gemini embedding model
- **SearchResult**: Represents semantically relevant document snippets returned from vector similarity searches

## Constraints

- Maximum 10MB document size limit for supported formats (plain text, PDF, DOCX, MD) to prevent excessive resource usage
- Must use async FastAPI for all endpoints to handle concurrent requests efficiently
- All sensitive data must be stored encrypted using industry-standard encryption
- All external API calls (Gemini, Qdrant) must have timeout limits of 30 seconds
- No hardcoded secrets allowed - all configuration must come from environment variables

## Non-Goals

- Supporting file formats beyond plain text, PDF, and common document formats
- Implementing complex document parsing beyond basic text extraction
- Providing real-time collaborative features between users
- Implementing advanced analytics or usage tracking beyond basic logging
- Supporting on-premise deployment of external services (Neon, Qdrant, Gemini)
