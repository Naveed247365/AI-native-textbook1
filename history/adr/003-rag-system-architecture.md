# ADR 003: RAG System Architecture - Gemini + Qdrant Integration

## Status
Accepted

## Context
The project requires a Retrieval-Augmented Generation (RAG) system that can store document embeddings, perform similarity search, and generate contextual responses. The system needs to handle user isolation, provide relevant search results, and integrate with AI models for response generation.

## Decision
We will implement a RAG pipeline using Google Gemini for embeddings and chat responses with Qdrant for vector storage and similarity search, with user isolation through metadata filtering.

## Options Considered

### Gemini + Qdrant (Chosen)
- Pros: Advanced embedding models (text-embedding-004), powerful chat models (1.5 Flash/Pro), efficient vector database with filtering, good API reliability
- Cons: Multiple external dependencies, potential API costs

### OpenAI + Pinecone
- Pros: Mature ecosystem, good documentation, proven performance
- Cons: Vendor lock-in to OpenAI, commercial vector database costs

### Self-hosted Models (LLaMA + Custom Vector DB)
- Pros: Full control, no external dependencies, cost-effective at scale
- Cons: Complex setup, maintenance overhead, performance tuning required

### Cohere + Vector Database
- Pros: Good embedding and generation models, unified API
- Cons: Less familiar ecosystem, potential vendor lock-in

## Rationale
The Gemini + Qdrant combination was chosen for its advanced model capabilities and efficient vector operations. Gemini's text-embedding-004 provides high-quality embeddings, while the 1.5 Flash/Pro models offer excellent response generation. Qdrant provides efficient similarity search with rich filtering capabilities needed for user isolation in the private RAG system.

## Consequences
- Positive: High-quality embeddings and responses, efficient similarity search, proper user isolation through metadata filtering
- Negative: Dependency on external APIs, potential rate limits, API costs
- Neutral: Need for retry logic and caching mechanisms to handle API availability

## Implementation
- Use text-embedding-004 model for document embeddings
- Store vectors in Qdrant with user_id metadata for filtering
- Implement similarity search with user isolation
- Use Gemini 1.5 Flash/Pro for response generation
- Implement caching and retry mechanisms for API stability