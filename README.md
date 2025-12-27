# Physical AI & Humanoid Robotics Textbook

AI-native interactive textbook for embodied intelligence education.

## Project Structure

```
E:/hakaton 1/AI-native-textbook/
├── frontend/          # Docusaurus-based static site (React/Node.js)
├── backend/           # FastAPI server with RAG, auth, personalization (Python)
├── specs/             # Feature specifications (Spec-Kit Plus)
├── .specify/          # Project templates and memory
├── history/           # Prompt History Records (PHRs)
├── CLAUDE.md          # Project constitution
└── DEPLOYMENT.md      # Deployment guide (coming soon)
```

## Quick Start

### Frontend (Docusaurus)

```bash
cd frontend
npm install
npm start
```

Visit http://localhost:3000

### Backend (FastAPI)

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8001
```

Visit http://localhost:8001/docs

## Documentation

- [Frontend Setup](frontend/README.md)
- [Backend Setup](backend/README.md)
- [Project Constitution](CLAUDE.md)

## Features

- **RAG-powered chatbot** for context-aware Q&A
- **User authentication** and personalization
- **Dynamic Urdu translation**
- **Interactive book navigation** with reading progress
- **Professional Humanoid Robotics theme**

## Tech Stack

- **Frontend**: Docusaurus 3.9.2, React 19.0
- **Backend**: FastAPI, Python 3.9+
- **Database**: Neon Postgres
- **Vector DB**: Qdrant
- **LLM**: Google Gemini, OpenRouter

## License

Open Educational Resource

## Contributing

See individual README files in `/frontend` and `/backend` for development guidelines.
