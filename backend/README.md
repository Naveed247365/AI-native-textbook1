# AI Backend with RAG + Authentication

A scalable backend featuring authentication, RAG capabilities, and integration with external services. The system uses Better Auth for authentication, Qdrant for vector storage, Neon Postgres for relational data, and Google's Gemini models for embeddings and chat functionality.

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

## Features

- **Authentication**: JWT-based authentication with Better Auth
- **RAG Pipeline**: Retrieval-Augmented Generation with Qdrant vector database
- **AI Integration**: Google Gemini for embeddings and chat responses
- **Database**: Neon Postgres for user data and chat history
- **Security**: Password hashing, JWT validation, user isolation
- **Scalability**: Async architecture with connection pooling

## Prerequisites

- Python 3.9+
- Qdrant vector database instance
- Neon Postgres database
- Google Gemini API key
- Node.js (for development tools, optional)

## Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd backend
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy the example environment file:

```bash
cp .env.example .env
```

Then edit `.env` with your actual configuration:

```env
# API Configuration
GEMINI_API_KEY=your_gemini_api_key_here
QDRANT_URL=your_qdrant_url_here
QDRANT_API_KEY=your_qdrant_api_key_here
NEON_DB_URL=your_neon_db_connection_string_here

# JWT Configuration
SECRET_KEY=your_secret_key_here  # Use a strong, random secret key
JWT_EXPIRES_IN=3600

# Application Configuration
DEBUG=false
LOG_LEVEL=info
```

### 5. Run the application

```bash
cd src
python main.py
```

Or using uvicorn directly:

```bash
cd src
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The application will be available at `http://localhost:8000`

## API Endpoints

### Authentication
- `POST /auth/signup` - User registration
- `POST /auth/login` - User login
- `GET /auth/me` - Get current user info

### RAG & Embeddings
- `POST /embed` - Generate embeddings for text
- `POST /save-document` - Save and embed a document
- `POST /search` - Semantic search in documents
- `POST /chat` - Chat with RAG context

### History
- `GET /history` - Get chat history
- `GET /history/{conversation_id}` - Get specific conversation

### Health
- `GET /health` - Health check endpoint

## Project Structure

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
│   ├── db/                     # Database module
│   │   ├── __init__.py
│   │   ├── base.py             # Base model class
│   │   ├── models/             # SQLAlchemy models
│   │   ├── database.py         # Database connection
│   │   └── crud.py             # CRUD operations
│   ├── qdrant/                 # Vector database module
│   ├── embeddings/             # Embedding module
│   ├── rag/                    # RAG pipeline module
│   ├── routes/                 # API routes
│   ├── models/                 # Pydantic models
│   ├── utils/                  # Utility functions
│   └── scripts/                # Utility scripts
├── tests/                      # Test suite
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variables template
└── README.md                   # Documentation
```

## Development

### Running tests

```bash
cd backend
python -m pytest tests/ -v
```

### Running with auto-reload during development

```bash
cd src
uvicorn main:app --reload
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| GEMINI_API_KEY | Google Gemini API key | Yes |
| QDRANT_URL | Qdrant vector database URL | Yes |
| QDRANT_API_KEY | Qdrant API key (if secured) | No |
| NEON_DB_URL | Neon Postgres connection string | Yes |
| SECRET_KEY | JWT secret key | Yes |
| JWT_EXPIRES_IN | JWT expiration time in seconds | No (default: 3600) |
| DEBUG | Enable debug mode | No (default: false) |
| LOG_LEVEL | Logging level | No (default: info) |

## Security Considerations

- Always use HTTPS in production
- Store secrets securely (not in version control)
- Validate and sanitize all user inputs
- Use parameterized queries to prevent SQL injection
- Implement rate limiting to prevent abuse
- Use strong, randomly generated secret keys

## Performance

- Async architecture for high concurrency
- Connection pooling for database operations
- Caching mechanisms for frequently accessed data
- Optimized vector search with Qdrant
- Efficient embedding processing pipeline

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests if applicable
5. Run tests (`python -m pytest`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## License

[Add your license here]