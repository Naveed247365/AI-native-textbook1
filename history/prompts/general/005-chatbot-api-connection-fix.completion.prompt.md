---
id: "005"
title: "Chatbot API Connection Fix"
stage: "general"
date: "2025-12-12"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "003-ai-backend"
user: "user"
command: "api-connection-fix"
labels: ["api", "chatbot", "cors", "proxy", "connection"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files: []
tests: []
---

# Chatbot API Connection Fix

## Prompt Text
```
Fix the chatbot API connection issue where it was getting 404 errors.
```

## Response Text
```
Successfully fixed the chatbot API connection issue with the following changes:

1. Identified that the Docusaurus proxy configuration was not properly forwarding API requests from frontend (port 3000) to backend (port 8001).

2. Updated the EnhancedChatbot component to use the direct backend URL instead of relying on the proxy:
   - Changed from `/api/chat/query` to `http://localhost:8001/api/chat/query`
   - Added comment explaining the change to avoid proxy issues

3. Enhanced CORS settings in the backend to allow cross-origin requests:
   - Updated allow_origins to include frontend origins: ["http://localhost:3000", "http://localhost:3001", "http://localhost:8000", "*"]
   - Added allow_origin_regex for localhost with any port

4. Both servers are now properly configured:
   - Frontend: Running on http://localhost:3000
   - Backend: Running on http://localhost:8001
   - API endpoints accessible and responding with proper fallback responses

5. The chatbot now connects directly to the backend API, bypassing the proxy configuration that was causing issues.

The API is working correctly and returns appropriate responses (fallback responses due to placeholder API key, which is expected behavior).
```

## Outcome
- Chatbot API connection issue resolved
- Direct API calls from frontend to backend working properly
- CORS settings configured to allow cross-origin requests
- Both servers running and communicating correctly
- Chatbot should now receive responses instead of 404 errors
```