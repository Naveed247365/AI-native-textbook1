# API Contract: Premium AI Chatbot UI Redesign

## Overview
This document defines the API contract between the redesigned chatbot UI and the backend API. The contract remains unchanged to ensure backward compatibility with existing backend implementation.

## Base URL
```
http://localhost:8001/api/chat
```

## Communication Protocol
- **Method**: POST
- **Content-Type**: application/json
- **Authentication**: None (uses OpenRouter API key configured in backend)
- **Timeout**: 30 seconds

## Request Format

### Request Body Schema
```json
{
  "message": {
    "type": "string",
    "description": "The user's question or message to send to the AI",
    "required": true,
    "minLength": 1,
    "maxLength": 5000
  },
  "selected_text": {
    "type": "string",
    "description": "The text selected by the user from the textbook content",
    "required": true,
    "minLength": 1,
    "maxLength": 5000
  },
  "user_id": {
    "type": "string",
    "description": "Optional user identifier for personalization",
    "required": false
  }
}
```

### Example Request
```json
{
  "message": "What is embodied intelligence?",
  "selected_text": "Embodied Intelligence represents the convergence of artificial intelligence with physical systems. It's the principle that true intelligence emerges not just from abstract computation, but from the interaction between an intelligent system and its physical environment.",
  "user_id": "user_12345"
}
```

## Response Format

### Success Response Schema
```json
{
  "answer": {
    "type": "string",
    "description": "The AI-generated response to the user's question",
    "required": true
  }
}
```

### Error Response Schema
```json
{
  "answer": {
    "type": "string",
    "description": "Fallback response when AI service is unavailable",
    "required": true,
    "enum": ["Is sawal ka jawab provided data me mojood nahi hai."]
  }
}
```

### Example Success Response
```json
{
  "answer": "Embodied Intelligence represents the convergence of artificial intelligence with physical systems. It's the principle that true intelligence emerges not just from abstract computation, but from the interaction between an intelligent system and its physical environment. In the context of humanoid robotics, this means creating machines that can perceive, reason, and act in the physical world much like humans do."
}
```

### Example Error Response
```json
{
  "answer": "Is sawal ka jawab provided data me mojood nahi hai."
}
```

## HTTP Status Codes
- **200 OK**: Request processed successfully, response contains AI answer
- **400 Bad Request**: Invalid request format or missing required fields
- **500 Internal Server Error**: Backend error during AI processing

## Rate Limits
- **Requests per minute**: 60 requests per IP address
- **Burst limit**: 10 requests within 1 second
- **Response**: HTTP 429 with retry-after header if exceeded

## Request Headers
```
Content-Type: application/json
```

## Response Headers
```
Content-Type: application/json
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: POST
Access-Control-Allow-Headers: Content-Type
```

## Timeout Behavior
- **Client timeout**: 30 seconds
- **Server timeout**: 25 seconds
- **Response**: If timeout occurs, client should display appropriate loading/error state

## Error Handling
The API contract ensures graceful degradation:
- If AI service is unavailable, returns fallback message
- If selected text is not found in knowledge base, returns fallback message
- If request is malformed, returns 400 error with validation details

## Versioning
- **Current version**: 1.0
- **Backward compatibility**: Maintained for all existing functionality
- **Breaking changes**: Would require version increment in URL path

## Security Considerations
- Input sanitization handled by backend
- No sensitive data transmitted
- Rate limiting implemented to prevent abuse
- Cross-origin requests allowed for frontend integration

## Performance Requirements
- **Response time**: <2 seconds for 95th percentile
- **Availability**: 99.9% uptime
- **Throughput**: Support 100 concurrent users

## Testing Contract
The following endpoints must maintain this contract:
- `/api/chat` - Primary chat endpoint
- Health check endpoints should continue to work as expected

## Backward Compatibility
This contract maintains full backward compatibility with existing frontend implementation. The UI redesign does not alter the API contract in any way.