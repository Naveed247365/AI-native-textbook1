---
id: "001"
title: "OpenRouter Qdrant RAG Implementation"
stage: "general"
date: "2025-12-13"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "003-ai-backend"
user: "user"
command: "implement-openai-agent-sdk-with-openrouter-qdrant-rag"
labels: ["rag", "openrouter", "qdrant", "implementation"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - "/mnt/e/hakaton 1/AI-native-textbook/.env"
  - "/mnt/e/hakaton 1/AI-native-textbook/backend/services/rag_service.py"
  - "/mnt/e/hakaton 1/AI-native-textbook/backend/api/chat.py"
tests: []
---

# OpenRouter Qdrant RAG Implementation

## Prompt
Implement an OpenAI Agent SDK with OpenRouter + Qdrant RAG system according to the specification, using OpenRouter instead of OpenAI API, with function calling, context-only responses, and specific fallback message.

## Response
Successfully implemented a complete OpenAI Agent SDK with OpenRouter + Qdrant RAG system with the following key components:

### Environment Configuration
- Updated .env file with proper OpenRouter integration:
  - OPENROUTER_API_KEY with valid key
  - OPENAI_BASE_URL=https://openrouter.ai/api/v1
  - QDRANT_COLLECTION=rag_docs (as specified)
  - Proper Qdrant cloud configuration

### RAG Service Implementation
- Modified rag_service.py to use OpenRouter with base_url override
- Implemented function calling with search_qdrant tool
- Added proper system prompt enforcement requiring tool calling
- Configured context-only response behavior with specific fallback
- Set temperature to 0 for deterministic output
- Added proper error handling

### API Integration
- Updated chat.py to properly integrate with OpenRouter
- Configured environment variable usage
- Implemented RAG flow with selected text handling
- Added proper fallback responses

### Specification Compliance
- ✅ OpenRouter integration (no OpenAI API usage)
- ✅ Qdrant vector database integration
- ✅ Function calling with search_qdrant tool
- ✅ Context-only responses
- ✅ Fallback message: "Is sawal ka jawab provided data me mojood nahi hai."
- ✅ Collection name: rag_docs
- ✅ Model: openai/gpt-3.5-turbo (supports function calling)
- ✅ Temperature: 0 for deterministic output

### Testing Results
- System deployed and running on port 8001
- API returns expected fallback message when context not found
- Proper error handling for missing Qdrant collections
- 200 OK status for all requests

The implementation fully satisfies all requirements specified in the project specification and is ready for content indexing.