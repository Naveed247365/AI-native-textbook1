# AI-native Physical AI & Humanoid Robotics Textbook - Routing Configuration

## Project Structure & Routing

This project has been organized with a clear separation between frontend and backend:

- **Backend**: Located in the `backend/` directory, built with FastAPI
  - Serves API endpoints under `/api` prefix
  - Runs on port 8000 by default
  - Handles authentication, chat, and translation services

- **Frontend**: Located in the `ai-native-textbook/` directory, built with Docusaurus
  - Serves static content and React components
  - Runs on port 3000 by default (during development)
  - Communicates with backend via API calls

## API Routing

The backend exposes the following API endpoints:

- `/api/chat/query` - AI chat functionality
- `/api/auth/login` - User authentication
- `/api/auth/signup` - User registration
- `/api/auth/profile` - User profile management
- `/api/translation/translate` - Text translation services
- Health check endpoints for each service

## Frontend-Backend Communication

During development, the frontend is configured with a proxy that forwards all `/api` requests to the backend server running on `http://localhost:8000`. This is configured in the `docusaurus.config.js` file using a custom plugin.

In production, you would need to:
1. Deploy the backend to a server
2. Update frontend API calls to point to the deployed backend URL
3. Configure CORS appropriately on the backend

## Running the Application

1. **Start the backend**:
   ```bash
   cd backend
   python main.py
   ```

2. **Start the frontend**:
   ```bash
   cd ai-native-textbook
   npm start
   ```

The frontend will be available at `http://localhost:3000` and will automatically proxy API requests to the backend at `http://localhost:8000`.