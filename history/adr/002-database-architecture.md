# ADR 002: Database Architecture - Neon Postgres + Qdrant Vector Database

## Status
Accepted

## Context
The AI Backend with RAG + Authentication project requires both relational data storage (for user information, chat history) and vector storage (for RAG functionality). We need to select appropriate database technologies that can scale, integrate well, and meet performance requirements.

## Decision
We will use a hybrid database architecture with Neon Postgres for relational data and Qdrant for vector storage, instead of alternatives like a single database solution or other vector databases.

## Options Considered

### Neon Postgres + Qdrant (Chosen)
- Pros: Specialized databases for each use case, serverless scalability for Postgres, purpose-built vector operations in Qdrant, good performance for both relational and vector queries
- Cons: More complex architecture, multiple service dependencies

### Supabase + Vector Extensions
- Pros: Single service provider, good integration, familiar SQL interface
- Cons: Potential vendor lock-in, possible performance limitations for vector operations

### MongoDB with Vector Search
- Pros: Single database for both document and vector storage, flexible schema
- Cons: Less familiar for relational operations, potential performance trade-offs

### Pinecone + Traditional SQL
- Pros: Commercial vector database with good support, proven performance
- Cons: Vendor lock-in, commercial pricing, less flexibility than open-source

## Rationale
The Neon Postgres + Qdrant combination was chosen because it provides optimal performance for each specific use case. Neon offers serverless PostgreSQL with branching capabilities for development, while Qdrant is purpose-built for vector operations with advanced filtering and similarity search capabilities. This separation of concerns allows each database to excel in its domain while maintaining clear data isolation between relational and vector data.

## Consequences
- Positive: Optimal performance for both relational queries and vector similarity search, clear separation of concerns, scalability for each data type
- Negative: Increased architectural complexity, multiple service dependencies, additional operational overhead
- Neutral: Need for careful transaction management between systems

## Implementation
- Neon Postgres for user data, chat history, and document metadata
- Qdrant for vector embeddings with user_id payload filtering
- User isolation maintained through user_id metadata in vector database
- Connection pooling and async operations for both databases