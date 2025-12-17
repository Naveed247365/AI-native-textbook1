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