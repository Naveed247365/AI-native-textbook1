---
id: 1
title: ai-backend-implementation-plan
stage: plan
date: 2025-12-11
surface: agent
model: claude-sonnet-4-5-20250929
feature: ai-backend
branch: 003-ai-backend
user: unknown
command: "manual creation"
labels: [architecture, planning, backend, rag, authentication]
links:
  spec: /mnt/e/hakaton 1/AI-native-textbook/specs/003-ai-backend/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - /mnt/e/hakaton 1/AI-native-textbook/specs/003-ai-backend/plan.md
 - /mnt/e/hakaton 1/AI-native-textbook/specs/003-ai-backend/tasks.md
tests:
 - null
---

## Prompt

Create an implementation plan for the AI Backend with RAG + Authentication project based on the specification at /mnt/e/hakaton 1/AI-native-textbook/specs/003-ai-backend/spec.md

The project involves:
- Better Auth integration for user authentication
- Qdrant vector database for RAG
- Neon Postgres for user data and chat history
- Gemini embeddings and chat models
- FastAPI backend
- Complete RAG pipeline

Generate a comprehensive implementation plan that includes:
- Technical architecture decisions
- Component breakdown with dependencies
- Implementation sequence
- Technology research and decisions
- Test strategy
- Integration points
- Folder structure
- Data models
- API contracts

## Response snapshot

# Implementation Plan: AI Backend with RAG + Authentication

## Executive Summary

This plan outlines the implementation of a full-stack AI backend featuring authentication, RAG capabilities, and integration with external services. The system will use Better Auth for authentication, Qdrant for vector storage, Neon Postgres for relational data, and Google's Gemini models for embeddings and chat functionality.

## Architecture Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│   Frontend      │────│   FastAPI        │────│  Better Auth     │
│   (Future)      │    │   Backend        │    │   Service        │
└─────────────────┘    └──────────────────┘    └──────────────────┘
                              │
         ┌────────────────────┼────────────────────┐
         │                    │                    │
   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
   │  Qdrant     │    │  Neon       │    │  Gemini     │
   │  Vector DB  │    │  Postgres   │    │  API        │
   └─────────────┘    └─────────────┘    └─────────────┘
```

## Technical Architecture Decisions

### 1. Authentication Layer
- **Better Auth**: Chosen for its simplicity and robust JWT/session management
- **Security**: Password hashing with bcrypt, JWT tokens with configurable expiration
- **Middleware**: Custom auth middleware to protect routes and validate tokens
- **Session Management**: Cookie-based sessions with secure flags

### 2. Database Layer
- **Neon Postgres**: Serverless PostgreSQL for user data and chat history
- **Connection Pooling**: Use asyncpg with connection pooling for efficiency
- **ORM**: SQLAlchemy with async support for database operations
- **Data Isolation**: User_id filtering for multi-tenancy

### 3. Vector Storage
- **Qdrant**: Vector database for RAG operations
- **Collection Strategy**: Single "documents" collection with user_id metadata
- **Indexing**: HNSW index for efficient similarity search
- **Filtering**: Payload filtering by user_id for private RAG

### 4. AI Integration
- **Gemini Embeddings**: text-embedding-004 model for document embeddings
- **Gemini Chat**: 1.5 Flash/Pro for response generation
- **Rate Limiting**: Built-in retry logic for API stability
- **Caching**: Optional caching layer for frequent queries

## Component Breakdown with Dependencies

### Core Components

#### 1. Authentication Module (`src/auth/`)
- **Dependencies**: Better Auth, bcrypt, JWT libraries
- **Responsibilities**: User registration, login, session management
- **Interfaces**: `/auth/*` endpoints
- **Data Models**: User, Session

#### 2. Database Module (`src/db/`)
- **Dependencies**: SQLAlchemy, asyncpg, Neon Postgres
- **Responsibilities**: Connection management, migrations, CRUD operations
- **Data Models**: User, ChatHistory, Document

#### 3. Qdrant Module (`src/qdrant/`)
- **Dependencies**: Qdrant client, vector operations
- **Responsibilities**: Vector storage, similarity search, indexing
- **Configuration**: Collection management, point operations

#### 4. Embeddings Module (`src/embeddings/`)
- **Dependencies**: Google Generative AI, API clients
- **Responsibilities**: Text embedding generation, vector processing
- **Integration**: Gemini API calls

#### 5. RAG Module (`src/rag/`)
- **Dependencies**: All above modules, Gemini chat API
- **Responsibilities**: Full RAG pipeline, search and retrieval
- **Processes**: Query processing, context retrieval, answer generation

#### 6. API Routes (`src/routes/`)
- **Dependencies**: All core modules
- **Responsibilities**: Endpoint definitions, request/response handling
- **Endpoints**: Auth, embed, search, history, health

### Supporting Modules

#### 7. Configuration (`src/config/`)
- **Dependencies**: Python os, dotenv
- **Responsibilities**: Environment variable management, app configuration

#### 8. Utilities (`src/utils/`)
- **Dependencies**: Standard Python libraries
- **Responsibilities**: Helper functions, validation, error handling

#### 9. Models (`src/models/`)
- **Dependencies**: Pydantic
- **Responsibilities**: Request/response schemas, data validation

#### 10. Scripts (`src/scripts/`)
- **Dependencies**: All core modules
- **Responsibilities**: Database migrations, data seeding

## Implementation Sequence

### Phase 1: Foundation Setup (Days 1-2)
1. Set up project structure and dependencies
2. Configure environment variables and settings
3. Initialize database connection and models
4. Set up basic FastAPI application structure
5. Create configuration management

### Phase 2: Authentication System (Days 2-3)
1. Implement Better Auth integration
2. Create user registration and login endpoints
3. Implement JWT token generation and validation
4. Build auth middleware for protected routes
5. Test authentication flows

### Phase 3: Database Integration (Days 3-4)
1. Define SQLAlchemy models (User, ChatHistory, Document)
2. Implement database CRUD operations
3. Create migration scripts for Neon Postgres
4. Implement connection pooling and error handling
5. Test database operations

### Phase 4: Vector Storage (Days 4-5)
1. Integrate Qdrant client
2. Create "documents" collection with proper schema
3. Implement embedding storage and retrieval
4. Build user_id filtering mechanism
5. Test vector operations

### Phase 5: AI Integration (Days 5-6)
1. Integrate Gemini API for embeddings
2. Implement text-embedding-004 functionality
3. Test embedding generation and storage
4. Implement error handling for API calls
5. Build retry mechanisms

### Phase 6: RAG Pipeline (Days 6-7)
1. Implement full RAG workflow
2. Build search functionality with similarity matching
3. Integrate Gemini chat for response generation
4. Implement context retrieval and formatting
5. Test end-to-end RAG functionality

### Phase 7: API Endpoints (Days 7-8)
1. Implement all required endpoints
2. Add request/response validation with Pydantic
3. Implement error handling and status codes
4. Add rate limiting and security measures
5. Test all API endpoints

### Phase 8: Scripts and Tools (Days 8-9)
1. Create database migration script
2. Build Qdrant seeding script
3. Implement health check functionality
4. Add comprehensive logging
5. Create documentation

### Phase 9: Testing and Optimization (Days 9-10)
1. Write unit tests for all components
2. Implement integration tests
3. Performance optimization
4. Security review
5. Final testing and validation

## Technology Research and Decisions

### Selected Technologies

#### Backend Framework
- **FastAPI**: Chosen for async support, automatic API documentation, and Pydantic integration

#### Authentication
- **Better Auth**: Modern authentication library with JWT and session support, easy integration

#### Databases
- **Neon Postgres**: Serverless PostgreSQL with branching capabilities for development
- **Qdrant**: Purpose-built vector database with rich filtering and search capabilities

#### AI Services
- **Google Gemini**: Advanced embedding and chat models with reliable APIs

#### Dependencies
- **SQLAlchemy**: ORM for database operations with async support
- **Pydantic**: Data validation and settings management
- **asyncio**: Asynchronous programming support
- **uvicorn**: ASGI server for deployment

### Alternative Considerations

#### Authentication Alternatives
- Auth0: More complex but feature-rich
- Firebase Auth: Vendor lock-in concerns
- Self-built: More control but maintenance overhead
- **Decision**: Better Auth offers the right balance of features and simplicity

#### Database Alternatives
- Supabase: Good alternative but Neon offers better pricing for this use case
- MongoDB: Good for document storage but Postgres preferred for relations
- **Decision**: Neon Postgres offers serverless scalability and familiar SQL interface

#### Vector Database Alternatives
- Pinecone: Commercial option with good performance
- Weaviate: Open-source with GraphQL interface
- **Decision**: Qdrant offers good performance and open-source flexibility

## Test Strategy

### Unit Testing
- **Coverage**: Target 80%+ code coverage
- **Framework**: pytest with async support
- **Components**: Individual functions, utility methods, model validations
- **Mocking**: External services (Gemini API, Qdrant) using pytest-mock

### Integration Testing
- **Database**: Test CRUD operations, relationships, and constraints
- **Authentication**: Test JWT generation, validation, and middleware
- **RAG Pipeline**: End-to-end tests for search and response generation
- **API**: Test all endpoints with various input scenarios

### Performance Testing
- **Load Testing**: Simulate concurrent users using tools like locust
- **Response Times**: Validate SC-001 to SC-005 success criteria
- **Stress Testing**: Test system limits and failure modes

### Security Testing
- **Input Validation**: Test for injection attacks and malformed inputs
- **Authentication**: Verify JWT protection and session management
- **Data Isolation**: Test user_id filtering and privacy controls

### Test Categories
- **Happy Path**: Normal operation scenarios
- **Edge Cases**: Boundary conditions and error scenarios
- **Security**: Authentication bypass attempts, data leakage
- **Performance**: Load and stress scenarios

## Integration Points

### External API Integrations
1. **Better Auth API**: User authentication and session management
2. **Gemini API**: Embedding generation and chat responses
3. **Qdrant API**: Vector storage and similarity search
4. **Neon Postgres**: Database connections via SQLAlchemy

### Internal Module Interactions
1. **Auth ↔ Database**: User model operations
2. **RAG ↔ Embeddings**: Vector generation and processing
3. **RAG ↔ Qdrant**: Vector storage and retrieval
4. **Routes ↔ All Modules**: API endpoint implementations

### Data Flow Patterns
1. **Registration Flow**: Input → Validation → Hash → Database → Token
2. **Embedding Flow**: Document → Gemini → Vector → Qdrant → Metadata
3. **Search Flow**: Query → Embed → Qdrant → Context → Gemini → Response
4. **History Flow**: Conversation → Validation → Database → Retrieval

## Folder Structure

```
backend/
├── src/
│   ├── __init__.py
│   ├── main.py                 # Application entry point
│   ├── config/                 # Configuration management
│   │   ├── __init__.py
│   │   ├── settings.py         # App settings and env vars
│   │   └── database.py         # Database configuration
│   ├── auth/                   # Authentication module
│   │   ├── __init__.py
│   │   ├── auth.py             # Better Auth integration
│   │   ├── middleware.py       # Auth middleware
│   │   └── schemas.py          # Auth-related schemas
│   ├── db/                     # Database module
│   │   ├── __init__.py
│   │   ├── base.py             # Base model class
│   │   ├── models/             # SQLAlchemy models
│   │   │   ├── __init__.py
│   │   │   ├── user.py         # User model
│   │   │   ├── chat_history.py # Chat history model
│   │   │   └── document.py     # Document model
│   │   ├── database.py         # Database connection
│   │   └── crud.py             # CRUD operations
│   ├── qdrant/                 # Vector database module
│   │   ├── __init__.py
│   │   ├── client.py           # Qdrant client setup
│   │   ├── collections.py      # Collection management
│   │   └── operations.py       # Vector operations
│   ├── embeddings/             # Embedding module
│   │   ├── __init__.py
│   │   ├── gemini_client.py    # Gemini API client
│   │   └── processor.py        # Embedding processing
│   ├── rag/                    # RAG pipeline module
│   │   ├── __init__.py
│   │   ├── pipeline.py         # Main RAG pipeline
│   │   ├── search.py           # Search functionality
│   │   └── generator.py        # Response generation
│   ├── routes/                 # API routes
│   │   ├── __init__.py
│   │   ├── auth.py             # Authentication routes
│   │   ├── embed.py            # Embedding routes
│   │   ├── search.py           # Search routes
│   │   ├── history.py          # Chat history routes
│   │   ├── documents.py        # Document management routes
│   │   └── health.py           # Health check routes
│   ├── models/                 # Pydantic models
│   │   ├── __init__.py
│   │   ├── auth.py             # Authentication models
│   │   ├── documents.py        # Document models
│   │   ├── search.py           # Search models
│   │   ├── chat.py             # Chat models
│   │   └── base.py             # Base models
│   ├── utils/                  # Utility functions
│   │   ├── __init__.py
│   │   ├── validators.py       # Input validators
│   │   ├── security.py         # Security utilities
│   │   └── helpers.py          # General helpers
│   └── scripts/                # Utility scripts
│       ├── __init__.py
│       ├── migrate_neon.py     # Database migration script
│       └── seed_qdrant.py      # Vector database seeding
├── tests/                      # Test suite
│   ├── __init__.py
│   ├── conftest.py             # Test configuration
│   ├── test_auth.py            # Authentication tests
│   ├── test_database.py        # Database tests
│   ├── test_embeddings.py      # Embedding tests
│   ├── test_rag.py             # RAG tests
│   ├── test_api.py             # API endpoint tests
│   └── fixtures/               # Test fixtures
├── requirements.txt            # Python dependencies
├── requirements-dev.txt        # Development dependencies
├── Dockerfile                  # Containerization
├── docker-compose.yml          # Multi-service orchestration
├── .env.example                # Environment variables template
├── .env                        # (gitignored) Actual environment variables
├── pyproject.toml              # Project configuration
└── README.md                   # Documentation
```

## Data Models

### User Model
```python
class User(Base):
    __tablename__ = "users"

    id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: str = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password: str = Column(String(255), nullable=False)
    full_name: str = Column(String(255))
    is_active: bool = Column(Boolean, default=True)
    created_at: datetime = Column(DateTime(timezone=True), server_default=func.now())
    updated_at: datetime = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    chat_histories: List[ChatHistory] = relationship("ChatHistory", back_populates="user")
    documents: List[Document] = relationship("Document", back_populates="user")
```

### ChatHistory Model
```python
class ChatHistory(Base):
    __tablename__ = "chat_history"

    id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: uuid.UUID = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    query: str = Column(Text, nullable=False)
    response: str = Column(Text, nullable=False)
    context_used: str = Column(Text)  # JSON string of context snippets used
    created_at: datetime = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship
    user: User = relationship("User", back_populates="chat_histories")
```

### Document Model
```python
class Document(Base):
    __tablename__ = "documents"

    id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: uuid.UUID = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    title: str = Column(String(255), nullable=False)
    content: str = Column(Text, nullable=False)
    content_hash: str = Column(String(255), nullable=False)  # For deduplication
    file_path: str = Column(String(500))  # Path if uploaded file
    metadata: dict = Column(JSON)  # Additional metadata as JSON
    created_at: datetime = Column(DateTime(timezone=True), server_default=func.now())
    updated_at: datetime = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationship
    user: User = relationship("User", back_populates="documents")
```

## API Contracts

### Authentication Endpoints
```
POST /auth/signup
Request: {email: str, password: str, full_name: str}
Response: {access_token: str, token_type: str, user: UserSchema}

POST /auth/login
Request: {email: str, password: str}
Response: {access_token: str, token_type: str, user: UserSchema}

GET /auth/me
Headers: Authorization: Bearer {token}
Response: UserSchema
```

### Embedding and Document Endpoints
```
POST /embed
Headers: Authorization: Bearer {token}
Request: {text: str}
Response: {embedding: List[float], success: bool}

POST /save-document
Headers: Authorization: Bearer {token}
Request: {title: str, content: str, metadata?: dict}
Response: {document_id: str, success: bool, message: str}
```

### Search and RAG Endpoints
```
POST /search
Headers: Authorization: Bearer {token}
Request: {query: str, top_k?: int = 5, filters?: dict}
Response: {results: List[SearchResult], query_embedding: List[float]}

POST /chat
Headers: Authorization: Bearer {token}
Request: {query: str, history_context?: List[Message]}
Response: {response: str, sources: List[DocumentReference], context_used: List[str]}
```

### History Endpoints
```
GET /history
Headers: Authorization: Bearer {token}
Query: page?: int, limit?: int
Response: {history: List[ChatHistoryItem], total: int, page: int, pages: int}

GET /history/{conversation_id}
Headers: Authorization: Bearer {token}
Response: ChatHistoryDetail
```

### Health Check Endpoint
```
GET /health
Response: {status: str, services: {postgres: bool, qdrant: bool, gemini: bool}}
```

## Risk Analysis and Mitigation

### Technical Risks
1. **API Rate Limits**: Gemini/Qdrant API limits could affect performance
   - *Mitigation*: Implement retry logic, caching, and request queuing

2. **Vector Database Performance**: Large datasets could slow search operations
   - *Mitigation*: Proper indexing, partitioning by user_id, and search optimization

3. **Memory Usage**: Large embeddings could cause memory issues
   - *Mitigation*: Streaming processing, memory monitoring, and garbage collection

### Security Risks
1. **Data Leakage**: Cross-user data access if filtering fails
   - *Mitigation*: Strict user_id validation, database-level row-level security

2. **Injection Attacks**: Malicious input could compromise system
   - *Mitigation*: Input validation, parameterized queries, and sanitization

3. **Token Security**: JWT token hijacking or replay attacks
   - *Mitigation*: Short-lived tokens, refresh tokens, and secure cookie settings

### Operational Risks
1. **External Service Downtime**: Dependency on Gemini, Qdrant, Neon
   - *Mitigation*: Graceful degradation, caching, and fallback mechanisms

2. **Scalability Issues**: Performance degradation with increased users
   - *Mitigation*: Load testing, horizontal scaling, and performance monitoring

## Success Criteria and Validation

### Performance Benchmarks
- Authentication endpoints respond within 500ms (SC-001)
- Document embedding completes within 3 seconds per document (SC-002)
- Search returns results with >0.7 cosine similarity (SC-003)
- Chat history operations achieve 99.9% reliability (SC-004)
- API endpoints respond within 2 seconds under normal load (SC-005)

### Quality Assurance
- 80%+ code coverage with unit tests
- Successful completion of all user scenario acceptance criteria
- Security audit passes without critical vulnerabilities
- Performance benchmarks met under load testing

### Operational Readiness
- Health check endpoints verify all service connectivity
- Logging and monitoring implemented for observability
- Error handling provides meaningful feedback to users
- Rate limiting prevents abuse and ensures fair usage

# Implementation Tasks: AI Backend with RAG + Authentication

## Sprint 1: Foundation and Authentication (Days 1-3)

### Task 1.1: Project Setup and Dependencies
- **ID**: T001
- **Priority**: P1
- **Effort**: 2 hours
- **Description**: Set up the project structure, install dependencies, configure environment variables
- **Tasks**:
  - Create project directory structure following the planned architecture
  - Initialize requirements.txt with necessary packages (fastapi, uvicorn, sqlalchemy, asyncpg, qdrant-client, google-generativeai, python-multipart, python-jose[cryptography], passlib[bcrypt], better-auth, python-dotenv)
  - Create .env.example with all required environment variables
  - Set up basic FastAPI application in src/main.py
  - Configure logging and basic error handling
- **Acceptance Criteria**:
  - [ ] Project structure matches planned architecture
  - [ ] All dependencies properly installed and documented
  - [ ] .env.example contains all required environment variables
  - [ ] Basic FastAPI app runs without errors
  - [ ] Logging configured and functional

### Task 1.2: Configuration Management
- **ID**: T002
- **Priority**: P1
- **Effort**: 1 hour
- **Description**: Implement configuration management with Pydantic settings
- **Tasks**:
  - Create src/config/settings.py with Pydantic BaseSettings
  - Define settings for database, Qdrant, Gemini API, JWT, etc.
  - Implement environment variable validation
  - Create src/config/database.py for database configuration
- **Acceptance Criteria**:
  - [ ] All environment variables properly validated
  - [ ] Settings accessible throughout the application
  - [ ] Error handling for missing environment variables
  - [ ] Database configuration properly set up

### Task 1.3: Better Auth Integration
- **ID**: T003
- **Priority**: P1
- **Effort**: 4 hours
- **Description**: Integrate Better Auth for user authentication
- **Tasks**:
  - Install and configure Better Auth in src/auth/auth.py
  - Set up JWT token generation with configurable expiration
  - Implement password hashing with bcrypt
  - Create auth middleware for protecting routes
  - Test basic registration and login functionality
- **Acceptance Criteria**:
  - [ ] User registration works with password hashing
  - [ ] User login generates valid JWT tokens
  - [ ] Auth middleware protects routes correctly
  - [ ] Session management works properly
  - [ ] Security best practices implemented

### Task 1.4: Authentication API Routes
- **ID**: T004
- **Priority**: P1
- **Effort**: 2 hours
- **Description**: Implement authentication API endpoints
- **Tasks**:
  - Create src/routes/auth.py with signup, login, and me endpoints
  - Implement Pydantic models for request/response validation
  - Add proper error handling and status codes
  - Test all authentication endpoints
- **Acceptance Criteria**:
  - [ ] POST /auth/signup creates user and returns token
  - [ ] POST /auth/login validates credentials and returns token
  - [ ] GET /auth/me returns user profile with valid token
  - [ ] Proper error responses for invalid credentials
  - [ ] All endpoints properly validated with Pydantic

## Sprint 2: Database Integration (Days 3-4)

### Task 2.1: Database Models and Setup
- **ID**: T005
- **Priority**: P1
- **Effort**: 3 hours
- **Description**: Create SQLAlchemy models and database connection
- **Tasks**:
  - Create src/db/base.py with Base class
  - Implement User model in src/db/models/user.py
  - Implement ChatHistory model in src/db/models/chat_history.py
  - Implement Document model in src/db/models/document.py
  - Create database connection in src/db/database.py
  - Set up async session management
- **Acceptance Criteria**:
  - [ ] All models properly defined with relationships
  - [ ] Database connection established successfully
  - [ ] Async session management working
  - [ ] Models include proper indexes and constraints
  - [ ] UUID primary keys implemented correctly

### Task 2.2: Database CRUD Operations
- **ID**: T006
- **Priority**: P1
- **Effort**: 2 hours
- **Description**: Implement CRUD operations for all models
- **Tasks**:
  - Create src/db/crud.py with user operations
  - Implement chat history CRUD operations
  - Implement document CRUD operations
  - Add proper error handling and validation
  - Test all database operations
- **Acceptance Criteria**:
  - [ ] User CRUD operations work correctly
  - [ ] Chat history CRUD operations work correctly
  - [ ] Document CRUD operations work correctly
  - [ ] Proper error handling implemented
  - [ ] All operations use async/await patterns

### Task 2.3: Database Migration Script
- **ID**: T007
- **Priority**: P1
- **Effort**: 1 hour
- **Description**: Create database migration script for Neon Postgres
- **Tasks**:
  - Create src/scripts/migrate_neon.py
  - Implement table creation logic
  - Add proper error handling for existing tables
  - Test migration script with fresh database
- **Acceptance Criteria**:
  - [ ] Migration script creates all required tables
  - [ ] Script handles existing tables gracefully
  - [ ] All indexes and constraints created properly
  - [ ] Migration script runs without errors

## Sprint 3: Vector Database Integration (Days 4-5)

### Task 3.1: Qdrant Client Setup
- **ID**: T008
- **Priority**: P1
- **Effort**: 2 hours
- **Description**: Set up Qdrant client and collection management
- **Tasks**:
  - Install qdrant-client package
  - Create src/qdrant/client.py with Qdrant client initialization
  - Implement collection creation for "documents" collection
  - Set up proper vector dimensions for Gemini embeddings
  - Add error handling for Qdrant connection issues
- **Acceptance Criteria**:
  - [ ] Qdrant client connects successfully
  - [ ] "documents" collection created with proper schema
  - [ ] Vector dimensions match Gemini embedding output (1536 for text-embedding-004)
  - [ ] Error handling implemented for connection failures

### Task 3.2: Vector Operations
- **ID**: T009
- **Priority**: P1
- **Effort**: 3 hours
- **Description**: Implement vector storage and retrieval operations
- **Tasks**:
  - Create src/qdrant/operations.py with upsert functionality
  - Implement similarity search with user_id filtering
  - Add vector point management (create, update, delete)
  - Implement payload structure with user_id metadata
  - Test vector operations with sample data
- **Acceptance Criteria**:
  - [ ] Documents can be stored as vectors with user_id metadata
  - [ ] Similarity search returns relevant results
  - [ ] User_id filtering works correctly in searches
  - [ ] Vector operations handle errors gracefully
  - [ ] Proper cleanup of deleted documents

## Sprint 4: AI Integration (Days 5-6)

### Task 4.1: Gemini Embedding Integration
- **ID**: T010
- **Priority**: P1
- **Effort**: 3 hours
- **Description**: Integrate Gemini API for text embeddings
- **Tasks**:
  - Install google-generativeai package
  - Create src/embeddings/gemini_client.py with API client
  - Implement generate_embedding function using text-embedding-004
  - Add proper error handling for API failures
  - Implement rate limiting and retry logic
- **Acceptance Criteria**:
  - [ ] Embedding generation works with text-embedding-004
  - [ ] Proper error handling for API failures
  - [ ] Rate limiting and retry logic implemented
  - [ ] Embeddings have correct dimensions (1536)
  - [ ] Function responds within 3 seconds per requirement

### Task 4.2: Embedding Processing
- **ID**: T011
- **Priority**: P1
- **Effort**: 2 hours
- **Description**: Process embeddings for storage and retrieval
- **Tasks**:
  - Create src/embeddings/processor.py with embedding workflow
  - Implement text preprocessing and validation
  - Add embedding caching to avoid duplicate processing
  - Implement document chunking for large texts
  - Test with various document sizes
- **Acceptance Criteria**:
  - [ ] Text preprocessing validates input properly
  - [ ] Caching prevents duplicate embedding work
  - [ ] Large documents are properly chunked
  - [ ] Embedding workflow integrates with Qdrant storage

### Task 4.3: Gemini Chat Integration
- **ID**: T012
- **Priority**: P1
- **Effort**: 2 hours
- **Description**: Integrate Gemini API for response generation
- **Tasks**:
  - Extend gemini_client.py with chat functionality
  - Implement response generation using Gemini 1.5 Flash/Pro
  - Add context formatting for RAG responses
  - Implement safety and moderation features
- **Acceptance Criteria**:
  - [ ] Chat responses generated using Gemini models
  - [ ] Context properly formatted for RAG
  - [ ] Safety features implemented
  - [ ] Responses generated within 5 seconds requirement

## Sprint 5: RAG Pipeline and API (Days 6-8)

### Task 5.1: RAG Pipeline Implementation
- **ID**: T013
- **Priority**: P1
- **Effort**: 4 hours
- **Description**: Build the complete RAG pipeline
- **Tasks**:
  - Create src/rag/pipeline.py with main RAG workflow
  - Implement query embedding and vector search
  - Add context retrieval and formatting
  - Integrate response generation
  - Implement user isolation for private RAG
- **Acceptance Criteria**:
  - [ ] Complete RAG pipeline functions end-to-end
  - [ ] Query embedding and search work correctly
  - [ ] Context retrieval filters by user_id
  - [ ] Response generation uses proper context
  - [ ] Private RAG ensures data isolation

### Task 5.2: Document Management API
- **ID**: T014
- **Priority**: P1
- **Effort**: 2 hours
- **Description**: Implement document upload and management endpoints
- **Tasks**:
  - Create src/routes/documents.py with document endpoints
  - Implement POST /save-document endpoint
  - Add document validation and security checks
  - Integrate with embedding and Qdrant storage
  - Implement proper error responses
- **Acceptance Criteria**:
  - [ ] POST /save-document stores document in database
  - [ ] Document gets embedded and stored in Qdrant
  - [ ] Proper validation and security checks implemented
  - [ ] Error handling works for various failure scenarios

### Task 5.3: Search API Implementation
- **ID**: T015
- **Priority**: P1
- **Effort**: 2 hours
- **Description**: Implement search functionality with RAG
- **Tasks**:
  - Create src/routes/search.py with search endpoints
  - Implement POST /search endpoint with similarity search
  - Add chat endpoint that combines search and response generation
  - Integrate authentication for user isolation
  - Implement proper request/response validation
- **Acceptance Criteria**:
  - [ ] POST /search returns relevant results based on similarity
  - [ ] User isolation maintained in search results
  - [ ] Chat endpoint generates contextual responses
  - [ ] All endpoints properly validated and secured

### Task 5.4: Chat History API
- **ID**: T016
- **Priority**: P2
- **Effort**: 2 hours
- **Description**: Implement chat history storage and retrieval
- **Tasks**:
  - Create src/routes/history.py with history endpoints
  - Implement GET /history for conversation history
  - Add proper pagination and filtering
  - Integrate with database CRUD operations
  - Test history functionality with RAG interactions
- **Acceptance Criteria**:
  - [ ] Chat history stored with user association
  - [ ] History retrieval works with pagination
  - [ ] Previous conversations accessible and preserved
  - [ ] History integrates with RAG responses

## Sprint 6: System Integration and Testing (Days 8-10)

### Task 6.1: Health Check Implementation
- **ID**: T017
- **Priority**: P2
- **Effort**: 1 hour
- **Description**: Implement health check endpoint for all services
- **Tasks**:
  - Create src/routes/health.py with health check endpoint
  - Test connectivity to Neon Postgres
  - Test connectivity to Qdrant
  - Test connectivity to Gemini API
  - Implement aggregated health status
- **Acceptance Criteria**:
  - [ ] GET /health tests all service connections
  - [ ] Health status reflects actual service availability
  - [ ] Individual service status reported
  - [ ] Proper error reporting for failed services

### Task 6.2: Comprehensive Testing
- **ID**: T018
- **Priority**: P1
- **Effort**: 6 hours
- **Description**: Write and run comprehensive tests for all components
- **Tasks**:
  - Create tests/test_auth.py for authentication
  - Create tests/test_database.py for database operations
  - Create tests/test_embeddings.py for embedding functions
  - Create tests/test_rag.py for RAG pipeline
  - Create tests/test_api.py for all endpoints
  - Run full test suite and achieve 80%+ coverage
- **Acceptance Criteria**:
  - [ ] Unit tests cover 80%+ of codebase
  - [ ] All authentication scenarios tested
  - [ ] Database operations fully tested
  - [ ] RAG pipeline end-to-end tested
  - [ ] All API endpoints tested with various inputs

### Task 6.3: Performance and Security Testing
- **ID**: T019
- **Priority**: P1
- **Effort**: 3 hours
- **Description**: Conduct performance and security validation
- **Tasks**:
  - Test response times for all endpoints
  - Validate user isolation in RAG searches
  - Test rate limiting functionality
  - Verify JWT token security
  - Conduct basic security scanning
- **Acceptance Criteria**:
  - [ ] All endpoints meet performance requirements (SC-001 to SC-005)
  - [ ] User data isolation verified
  - [ ] Rate limiting functions properly
  - [ ] JWT tokens secure and properly validated
  - [ ] Security vulnerabilities addressed

### Task 6.4: Documentation and Final Validation
- **ID**: T020
- **Priority**: P1
- **Effort**: 2 hours
- **Description**: Complete documentation and final validation
- **Tasks**:
  - Update README.md with setup and usage instructions
  - Document API endpoints with examples
  - Create deployment configuration
  - Validate all success criteria from spec
  - Prepare for handoff/deployment
- **Acceptance Criteria**:
  - [ ] README includes complete setup instructions
  - [ ] API documentation comprehensive and accurate
  - [ ] Deployment configuration ready
  - [ ] All spec success criteria validated
  - [ ] System ready for deployment/testing

## Outcome

- ✅ Impact: Created comprehensive implementation plan and detailed tasks for the AI Backend with RAG + Authentication project, covering architecture, components, implementation sequence, technology decisions, testing strategy, integration points, folder structure, data models, and API contracts
- 🧪 Tests: Not applicable for planning phase
- 📁 Files: Created plan.md and tasks.md files with complete architecture and implementation details
- 🔁 Next prompts: Implementation of the actual backend components based on this plan
- 🧠 Reflection: The plan provides a solid foundation for implementing the AI backend with clear separation of concerns, proper authentication, and RAG functionality

## Evaluation notes (flywheel)

- Failure modes observed: None at planning stage
- Graders run and results (PASS/FAIL): Not applicable for planning
- Prompt variant (if applicable): Not applicable
- Next experiment (smallest change to try): Begin implementation of foundation components as outlined in the tasks