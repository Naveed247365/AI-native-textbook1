---
id: 2
title: "ai-native-textbook-7-day-plan"
stage: "plan"
date: "2025-12-10"
model: "claude-sonnet-4-5-20250929"
feature: "ai-native-textbook"
branch: "001-ai-native-textbook"
user: "user"
command: "/sp.plan"
labels: ["planning", "hackathon", "docusaurus", "rag-chatbot", "personalization"]
links:
  spec: "specs/001-ai-native-textbook/spec.md"
  ticket: null
  adr: null
  pr: null
files:
  - "specs/001-ai-native-textbook/plan.md"
tests: []
---

# Prompt History Record

## Prompt
```
Create complete 7-day execution plan to finish and win Panaversity Hackathon Project 1 before Nov 30 2025:
Day 1 → Repo setup, Spec-Kit Plus + Docusaurus + Claude Code
Day 2 → Generate all chapters using Claude (ROS2, Gazebo, Isaac, VLA, hardware, weekly)
Day 3 → FastAPI + Neon + Qdrant RAG backend + selected-text feature
Day 4 → Better-Auth + background questions + personalization logic
Day 5 → Urdu translation button + Claude Subagents/Skills
Day 6 → Embed chatbot in Docusaurus + polish UI + deploy GitHub Pages
Day 7 → Record 90-sec demo + submit form
Include exact commands and milestones for each day.
```

## Response
```
# Implementation Plan: AI-native Interactive Textbook Platform for Physical AI

**Branch**: `001-ai-native-textbook` | **Date**: 2025-12-10 | **Spec**: [specs/001-ai-native-textbook/spec.md](specs/001-ai-native-textbook/spec.md)
**Input**: Feature specification from `/specs/001-ai-native-textbook/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Create an AI-native interactive textbook platform with Docusaurus frontend, RAG chatbot backend using FastAPI, Neon Postgres, and Qdrant vector database. The platform will include selected-text-only chatbot functionality, Better-Auth with background questions, per-chapter personalization, Urdu translation, and Claude Code Subagents/Skills as required for the Panaversity Hackathon Project 1.

## Technical Context

**Language/Version**: Python 3.11 (backend), JavaScript/TypeScript (frontend), Node.js 18+
**Primary Dependencies**: Docusaurus v3+, FastAPI, Neon Postgres, Qdrant Cloud, OpenAI API, Better-Auth, React
**Storage**: Neon Serverless Postgres (user data), Qdrant Cloud Free (vector embeddings for RAG)
**Testing**: pytest (backend), Jest/Cypress (frontend), Claude Code PHRs (specification tracking)
**Target Platform**: Web application (GitHub Pages/Vercel deployment)
**Project Type**: Web (frontend + backend architecture)
**Performance Goals**: <2-second response times for user interactions, 100 concurrent users support
**Constraints**: <2-second response times (p95), WCAG 2.1 AA accessibility compliance, selected-text-only chatbot responses
**Scale/Scope**: Up to 10,000 registered users with personalization data, comprehensive Physical AI curriculum

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- ✅ AI-Native Educational Content: Content designed for AI interaction and enhancement
- ✅ Modular & Extensible Architecture: Clear separation of concerns between textbook, RAG, auth, and personalization
- ✅ Test-First Development: All features will follow TDD methodology
- ✅ Full Integration Testing: RAG, auth, personalization, and translation components will be thoroughly tested
- ✅ Performance & Accessibility: Sub-2-second response times and WCAG 2.1 AA compliance
- ✅ Data Privacy & Security: Industry-standard security practices for student data

## Project Structure

### Documentation (this feature)

```text
specs/001-ai-native-textbook/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── main.py
├── api/
│   ├── chat.py
│   ├── auth.py
│   └── translation.py
├── models/
│   ├── user.py
│   ├── chat_session.py
│   └── user_profile.py
├── services/
│   ├── rag_service.py
│   ├── personalization_service.py
│   ├── translation_service.py
│   ├── vector_db.py
│   └── content_adaptation.py
├── database/
│   └── schema.sql
├── middleware/
│   └── auth_middleware.py
└── tests/
    ├── unit/
    └── integration/

src/
├── components/
│   ├── chatbot/
│   │   ├── ChatInterface.jsx
│   │   ├── SelectedTextHandler.jsx
│   │   └── MessageDisplay.jsx
│   ├── personalization/
│   │   └── PersonalizeButton.jsx
│   ├── translation/
│   │   └── UrduTranslationButton.jsx
│   └── auth/
│       ├── LoginModal.jsx
│       └── SignupWithBackground.jsx
├── pages/
│   ├── modules/
│   │   ├── 1-ros2/
│   │   ├── 2-gazebo-unity/
│   │   ├── 3-nvidia-isaac/
│   │   └── 4-vla/
│   ├── weekly-plan/
│   ├── capstone/
│   └── hardware-specs/
├── theme/
│   └── DocPage/index.js
└── css/
    └── custom.css

.claude/
├── subagents/
│   ├── content_generation_subagent.md
│   ├── personalization_subagent.md
│   ├── translation_assistance_subagent.md
│   ├── chat_response_subagent.md
│   └── user_profiling_subagent.md
└── skills/
    ├── textbook_navigation_skill.md
    ├── content_adaptation_skill.md
    ├── translation_skill.md
    ├── chat_interface_skill.md
    └── user_management_skill.md

docs/
├── intro.md
└── ...

.babel/
├── preset.js
└── ...

.github/
└── workflows/
    └── deploy.yml

docusaurus.config.js
package.json
vercel.json
```

**Structure Decision**: Web application with separate backend (FastAPI) and frontend (Docusaurus React) to maintain clear separation of concerns between RAG functionality and textbook presentation. Backend handles all AI interactions, authentication, and data management, while frontend provides the educational content and user interface.

## 7-Day Execution Plan for Panaversity Hackathon Project 1

### Overview
Complete AI-native Interactive Textbook Platform for Physical AI with Docusaurus, RAG chatbot, authentication, personalization, and Urdu translation by November 30, 2025.

---

## Day 1: Repo Setup & Foundation (December 11, 2025)

### Objectives:
- Set up complete Docusaurus book with Spec-Kit Plus
- Configure Claude Code infrastructure
- Initialize project structure

### Exact Commands:
```bash
# 1. Initialize Docusaurus project
npm init docusaurus@latest ai-native-textbook classic

# 2. Navigate to project directory
cd ai-native-textbook

# 3. Install Spec-Kit Plus dependencies
npm install @spec-labs/spec-kit-plus

# 4. Set up project structure according to constitution
mkdir -p src/components/{chatbot,auth,personalization,translation}
mkdir -p src/pages/modules/{1-ros2,2-gazebo-unity,3-nvidia-isaac,4-vla}
mkdir -p src/pages/{weekly-plan,capstone,hardware-specs}
mkdir -p backend/{api,models,services,vector-db}

# 5. Install additional dependencies for backend
npm install fastapi uvicorn python-multipart
pip install fastapi uvicorn python-multipart

# 6. Configure Docusaurus for multi-language support
# Update docusaurus.config.js to include Urdu language
```

### Milestones:
- ✅ Docusaurus site running locally
- ✅ Spec-Kit Plus integrated
- ✅ Claude Code commands working
- ✅ Project structure created with all required directories
- ✅ Basic configuration files set up

---

## Day 2: Content Generation (December 12, 2025)

### Objectives:
- Generate all textbook chapters using Claude Code
- Create comprehensive content for ROS2, Gazebo/Unity, NVIDIA Isaac, VLA, hardware specs, weekly plans, and capstone

### Exact Commands:
```bash
# 1. Generate module 1: ROS2 content
/sp.specify "Generate comprehensive ROS2 content for Physical AI textbook"
/sp.plan "Create ROS2 content structure"
/sp.tasks "Create tasks for ROS2 content implementation"
/sp.implement "Generate ROS2 chapter content"

# 2. Generate module 2: Gazebo/Unity content
/sp.specify "Generate comprehensive Gazebo and Unity content for Physical AI textbook"
/sp.plan "Create Gazebo/Unity content structure"
/sp.tasks "Create tasks for Gazebo/Unity content implementation"
/sp.implement "Generate Gazebo/Unity chapter content"

# 3. Generate module 3: NVIDIA Isaac content
/sp.specify "Generate comprehensive NVIDIA Isaac content for Physical AI textbook"
/sp.plan "Create NVIDIA Isaac content structure"
/sp.tasks "Create tasks for NVIDIA Isaac content implementation"
/sp.implement "Generate NVIDIA Isaac chapter content"

# 4. Generate module 4: VLA content
/sp.specify "Generate comprehensive VLA content for Physical AI textbook"
/sp.plan "Create VLA content structure"
/sp.tasks "Create tasks for VLA content implementation"
/sp.implement "Generate VLA chapter content"

# 5. Generate hardware specifications content
/sp.specify "Generate comprehensive hardware specifications content for Physical AI textbook"
/sp.plan "Create hardware specs content structure"
/sp.tasks "Create tasks for hardware specs content implementation"
/sp.implement "Generate hardware specs chapter content"

# 6. Generate weekly plan content
/sp.specify "Generate comprehensive weekly learning plan content for Physical AI textbook"
/sp.plan "Create weekly plan content structure"
/sp.tasks "Create tasks for weekly plan content implementation"
/sp.implement "Generate weekly plan chapter content"

# 7. Generate capstone project content
/sp.specify "Generate comprehensive capstone project content for Physical AI textbook"
/sp.plan "Create capstone content structure"
/sp.tasks "Create tasks for capstone content implementation"
/sp.implement "Generate capstone chapter content"
```

### Milestones:
- ✅ All 7 content modules completed
- ✅ Content matches 9-page course outline specifications
- ✅ Content passes initial quality checks
- ✅ All chapters properly integrated into Docusaurus navigation

---

## Day 3: RAG Backend Development (December 13, 2025)

### Objectives:
- Build FastAPI backend for RAG chatbot
- Integrate Neon Serverless Postgres and Qdrant Cloud Free
- Implement selected-text-only answer functionality

### Exact Commands:
```bash
# 1. Create backend structure
mkdir -p backend/{api,models,services,utils,config}

# 2. Install backend dependencies
pip install fastapi uvicorn python-multipart psycopg2-binary qdrant-client openai python-dotenv better-auth

# 3. Create main FastAPI app
touch backend/main.py

# 4. Create RAG service
touch backend/services/rag_service.py

# 5. Create database models
touch backend/models/user.py backend/models/chat_session.py

# 6. Create vector database integration
touch backend/services/vector_db.py

# 7. Create selected text validation service
touch backend/services/text_selection_validator.py

# 8. Create API endpoints
touch backend/api/chat.py backend/api/auth.py

# 9. Implement selected-text-only functionality
# Key implementation in rag_service.py to restrict responses to selected text only
```

### Key Implementation Files:

**backend/main.py**:
```python
from fastapi import FastAPI
from backend.api import chat, auth
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="AI Native Textbook RAG API", version="1.0.0")

app.include_router(chat.router, prefix="/api/v1/chat", tags=["chat"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])

@app.get("/")
def read_root():
    return {"message": "AI Native Textbook RAG Backend"}
```

**backend/services/rag_service.py**:
```python
import openai
from typing import List, Dict, Optional
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, VectorParams, Distance
import os

class RAGService:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.qdrant_client = QdrantClient(
            url=os.getenv("QDRANT_URL"),
            api_key=os.getenv("QDRANT_API_KEY")
        )

    def get_response_for_selected_text(self, selected_text: str, question: str) -> str:
        """
        Generate response based ONLY on the selected text.
        This ensures the chatbot doesn't hallucinate beyond the selected text.
        """
        # Validate that the response is based only on selected text
        prompt = f"""
        Using ONLY the following text content, answer the question. Do not use any external knowledge:

        SELECTED TEXT: {selected_text}

        QUESTION: {question}

        Answer based only on the selected text content. If the answer cannot be found in the selected text,
        clearly state that the information is not available in the selected text.
        """

        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.3
        )

        return response.choices[0].message.content
```

### Milestones:
- ✅ FastAPI backend operational
- ✅ Qdrant vector database integration complete
- ✅ Neon Postgres connection established
- ✅ Selected-text-only answer functionality working
- ✅ API endpoints tested and functional

---

## Day 4: Authentication & Personalization (December 14, 2025)

### Objectives:
- Implement Better-Auth signup/login
- Add software/hardware background questions at signup
- Create personalization logic for content adaptation

### Exact Commands:
```bash
# 1. Install Better-Auth
npm install better-auth

# 2. Set up authentication routes
touch backend/api/auth.py

# 3. Create user profile model with background info
touch backend/models/user_profile.py

# 4. Create personalization service
touch backend/services/personalization_service.py

# 5. Create content adaptation logic
touch backend/services/content_adaptation.py

# 6. Set up Neon database schema for user data
touch backend/database/schema.sql

# 7. Create middleware for authentication
touch backend/middleware/auth_middleware.py
```

### Key Implementation Files:

**backend/api/auth.py**:
```python
from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from pydantic import BaseModel
from better_auth import auth_backend
from backend.services.personalization_service import UserProfile

router = APIRouter()

class BackgroundInfo(BaseModel):
    software_experience: str  # "Beginner", "Intermediate", "Advanced", "Software Engineer"
    hardware_experience: str  # "Beginner", "Intermediate", "Advanced", "Hardware Engineer"
    background_notes: Optional[str] = None

@router.post("/signup-background")
async def add_user_background(background_info: BackgroundInfo, user=Depends(auth_backend.current_user)):
    """Add software/hardware background information to user profile"""
    profile = await UserProfile.update_background(user.id, background_info)
    return {"success": True, "profile": profile}

@router.get("/profile")
async def get_user_profile(user=Depends(auth_backend.current_user)):
    """Get user profile with background information"""
    profile = await UserProfile.get_by_user_id(user.id)
    return profile
```

**backend/services/personalization_service.py**:
```python
import asyncio
from typing import Dict, Any
from enum import Enum

class ExperienceLevel(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    SOFTWARE_ENGINEER = "software_engineer"
    HARDWARE_ENGINEER = "hardware_engineer"

class UserProfile:
    @staticmethod
    async def update_background(user_id: str, background_info: Dict[str, Any]):
        # Store background info in Neon database
        # Implementation details...
        pass

    @staticmethod
    async def get_by_user_id(user_id: str):
        # Retrieve user profile from database
        # Implementation details...
        pass

class ContentAdaptationService:
    @staticmethod
    async def adapt_content(content: str, user_profile: Dict[str, Any], chapter_topic: str) -> str:
        """
        Adapt content based on user background and experience level
        """
        software_exp = user_profile.get('software_experience', 'beginner')
        hardware_exp = user_profile.get('hardware_experience', 'beginner')

        # Adjust content complexity based on user background
        if software_exp in [ExperienceLevel.BEGINNER.value, ExperienceLevel.SOFTWARE_ENGINEER.value]:
            # Add more code examples for software-focused users
            content = ContentAdaptationService._add_software_examples(content, chapter_topic)

        if hardware_exp in [ExperienceLevel.BEGINNER.value, ExperienceLevel.HARDWARE_ENGINEER.value]:
            # Add more hardware examples for hardware-focused users
            content = ContentAdaptationService._add_hardware_examples(content, chapter_topic)

        if software_exp == ExperienceLevel.ADVANCED.value or hardware_exp == ExperienceLevel.ADVANCED.value:
            # Add more detailed explanations for advanced users
            content = ContentAdaptationService._add_advanced_details(content)
        elif software_exp == ExperienceLevel.BEGINNER.value or hardware_exp == ExperienceLevel.BEGINNER.value:
            # Simplify explanations for beginners
            content = ContentAdaptationService._simplify_content(content)

        return content

    @staticmethod
    def _add_software_examples(content: str, topic: str) -> str:
        # Implementation to add software-focused examples
        return content

    @staticmethod
    def _add_hardware_examples(content: str, topic: str) -> str:
        # Implementation to add hardware-focused examples
        return content

    @staticmethod
    def _add_advanced_details(content: str) -> str:
        # Implementation to add advanced details
        return content

    @staticmethod
    def _simplify_content(content: str) -> str:
        # Implementation to simplify content
        return content
```

### Milestones:
- ✅ Better-Auth signup/login functional
- ✅ Background information capture during signup working
- ✅ Personalization service created and tested
- ✅ Content adaptation logic implemented
- ✅ User profile storage and retrieval working

---

## Day 5: Translation & Claude Subagents (December 15, 2025)

### Objectives:
- Implement Urdu translation functionality
- Create 5 reusable Claude Code Subagents
- Create 5 Agent Skills

### Exact Commands:
```bash
# 1. Install translation dependencies
pip install googletrans==4.0.0rc1 transformers torch

# 2. Create translation service
touch backend/services/translation_service.py

# 3. Create Claude Code Subagents
mkdir -p .claude/subagents
touch .claude/subagents/content_generation_subagent.md
touch .claude/subagents/personalization_subagent.md
touch .claude/subagents/translation_assistance_subagent.md
touch .claude/subagents/chat_response_subagent.md
touch .claude/subagents/user_profiling_subagent.md

# 4. Create Claude Code Agent Skills
mkdir -p .claude/skills
touch .claude/skills/textbook_navigation_skill.md
touch .claude/skills/content_adaptation_skill.md
touch .claude/skills/translation_skill.md
touch .claude/skills/chat_interface_skill.md
touch .claude/skills/user_management_skill.md

# 5. Create Urdu translation API endpoint
touch backend/api/translation.py
```

### Key Implementation Files:

**backend/services/translation_service.py**:
```python
from transformers import MarianMTModel, MarianTokenizer
import asyncio
from typing import Optional
import requests

class TranslationService:
    def __init__(self):
        # Initialize Urdu translation model
        self.model_name = "Helsinki-NLP/opus-mt-en-ur"
        self.tokenizer = MarianTokenizer.from_pretrained(self.model_name)
        self.model = MarianMTModel.from_pretrained(self.model_name)

    async def translate_to_urdu(self, text: str) -> str:
        """
        Translate English text to Urdu
        """
        try:
            # Tokenize the input text
            inputs = self.tokenizer(text, return_tensors="pt", padding=True)

            # Generate translation
            translated = self.model.generate(**inputs)

            # Decode the translation
            urdu_text = self.tokenizer.decode(translated[0], skip_special_tokens=True)

            return urdu_text
        except Exception as e:
            # Fallback to alternative translation service
            return await self._fallback_translation(text)

    async def _fallback_translation(self, text: str) -> str:
        """
        Fallback translation service in case primary fails
        """
        # Implementation of fallback translation
        # Could use Google Translate API or other service
        return f"[TRANSLATION ERROR: {str(e)}]"

    async def translate_to_english(self, urdu_text: str) -> str:
        """
        Translate Urdu text back to English
        """
        # Model for Urdu to English translation
        model_name = "Helsinki-NLP/opus-mt-ur-en"
        tokenizer = MarianTokenizer.from_pretrained(model_name)
        model = MarianMTModel.from_pretrained(model_name)

        inputs = tokenizer(urdu_text, return_tensors="pt", padding=True)
        translated = model.generate(**inputs)
        english_text = tokenizer.decode(translated[0], skip_special_tokens=True)

        return english_text
```

**backend/api/translation.py**:
```python
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.services.translation_service import TranslationService

router = APIRouter()
translation_service = TranslationService()

class TranslationRequest(BaseModel):
    text: str
    target_language: str = "ur"  # Default to Urdu

@router.post("/translate")
async def translate_content(request: TranslationRequest):
    """Translate content to target language"""
    if request.target_language.lower() == "ur":
        translated_text = await translation_service.translate_to_urdu(request.text)
        return {"translated_text": translated_text, "target_language": "ur", "original_text": request.text}
    else:
        raise HTTPException(status_code=400, detail="Currently only Urdu translation is supported")
```

### Claude Code Subagents:

**.claude/subagents/content_generation_subagent.md**:
```markdown
# Content Generation Subagent

## Purpose
Automatically generates textbook content based on curriculum requirements and user feedback.

## Capabilities
- Creates new textbook chapters following pedagogical best practices
- Adapts content based on user background and learning objectives
- Validates content against curriculum standards
- Generates exercises and assessments for each chapter

## Usage
Trigger when: New content needs to be created, existing content needs updating based on user feedback, or curriculum changes require new materials.
```

**.claude/subagents/personalization_subagent.md**:
```markdown
# Personalization Subagent

## Purpose
Analyzes user background and learning patterns to customize content delivery and difficulty.

## Capabilities
- Processes user profile data (software/hardware background)
- Adapts content difficulty and examples based on user level
- Tracks learning progress and adjusts recommendations
- Modifies explanation depth based on user engagement

## Usage
Trigger when: User accesses personalized content, background information is updated, or learning analytics suggest content adjustments.
```

**.claude/subagents/translation_assistance_subagent.md**:
```markdown
# Translation Assistance Subagent

## Purpose
Provides multilingual content support with quality translation services.

## Capabilities
- Translates content between English and Urdu with cultural sensitivity
- Maintains technical accuracy in specialized terminology
- Preserves content structure and formatting during translation
- Handles translation caching for performance optimization

## Usage
Trigger when: User requests content translation, new content needs multilingual availability, or translation quality needs improvement.
```

**.claude/subagents/chat_response_subagent.md**:
```markdown
# Chat Response Subagent

## Purpose
Manages AI chatbot responses ensuring they adhere to selected-text-only constraints.

## Capabilities
- Restricts responses to information within selected text only
- Validates that answers don't contain hallucinated information
- Formats responses for optimal user experience
- Handles edge cases when selected text is insufficient

## Usage
Trigger when: User submits a question to the chatbot, selected text is processed, or response quality needs validation.
```

**.claude/subagents/user_profiling_subagent.md**:
```markdown
# User Profiling Subagent

## Purpose
Manages user data and background information for personalization purposes.

## Capabilities
- Collects and validates user background information
- Updates user profiles based on learning activity
- Maintains privacy and security of user data
- Integrates with authentication systems

## Usage
Trigger when: User registers, updates profile information, or personalization settings need adjustment.
```

### Claude Code Agent Skills:

**.claude/skills/textbook_navigation_skill.md**:
```markdown
# Textbook Navigation Skill

## Purpose
Enables intelligent navigation through the textbook content structure.

## Capabilities
- Provides chapter recommendations based on user progress
- Identifies prerequisite knowledge for advanced topics
- Guides users through logical learning sequences
- Locates specific content based on user queries

## Usage Context
Use when users need guidance on which chapters to study next, want to find specific topics, or need help navigating the content hierarchy.
```

**.claude/skills/content_adaptation_skill.md**:
```markdown
# Content Adaptation Skill

## Purpose
Dynamically adjusts content based on user background and learning preferences.

## Capabilities
- Modifies explanation complexity for different experience levels
- Changes example types based on user background (software vs hardware focus)
- Adjusts pacing and depth of content presentation
- Customizes exercises and assessments to user profile

## Usage Context
Use when presenting content to users, adapting existing material to new audiences, or personalizing learning experiences.
```

### Milestones:
- ✅ Urdu translation service implemented and tested
- ✅ 5 Claude Code Subagents created and documented
- ✅ 5 Agent Skills created and documented
- ✅ Translation API endpoints functional
- ✅ Translation quality meets requirements (≥90% accuracy)

---

## Day 6: Frontend Integration & Deployment (December 16, 2025)

### Objectives:
- Embed chatbot in Docusaurus frontend
- Polish UI/UX for all features
- Deploy to GitHub Pages

### Exact Commands:
```bash
# 1. Create React components for chatbot integration
mkdir -p src/components/chatbot
touch src/components/chatbot/ChatInterface.jsx
touch src/components/chatbot/SelectedTextHandler.jsx
touch src/components/chatbot/MessageDisplay.jsx

# 2. Create personalization button component
touch src/components/personalization/PersonalizeButton.jsx

# 3. Create translation button component
touch src/components/translation/UrduTranslationButton.jsx

# 4. Create authentication components
mkdir -p src/components/auth
touch src/components/auth/LoginModal.jsx
touch src/components/auth/SignupWithBackground.jsx

# 5. Update Docusaurus configuration for all features
touch docusaurus.config.js

# 6. Create custom MDX components for textbook features
mkdir -p src/theme
touch src/theme/DocPage/index.js

# 7. Set up GitHub Pages deployment
touch .github/workflows/deploy.yml

# 8. Create Vercel deployment configuration
touch vercel.json
```

### Key Implementation Files:

**src/components/chatbot/ChatInterface.jsx**:
```jsx
import React, { useState, useRef } from 'react';
import './ChatInterface.css';

const ChatInterface = ({ selectedText }) => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  React.useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputValue.trim()) return;

    // Add user message
    const userMessage = { role: 'user', content: inputValue, timestamp: new Date() };
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Call backend API with selected text
      const response = await fetch('/api/v1/chat/respond', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          question: inputValue,
          selected_text: selectedText || '',
          context: 'textbook_content'
        })
      });

      const data = await response.json();

      const botMessage = {
        role: 'assistant',
        content: data.response,
        timestamp: new Date(),
        source: 'selected_text_only' // Indicates response is based on selected text only
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      const errorMessage = {
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please make sure text is selected and try again.',
        timestamp: new Date(),
        isError: true
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chat-interface">
      <div className="chat-header">
        <h3>AI Learning Assistant</h3>
        <p className="chat-status">
          {selectedText ? "Responding to selected text" : "Please select text to ask questions"}
        </p>
      </div>

      <div className="chat-messages">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.role}`}>
            <div className="message-content">
              {msg.content}
              {msg.source === 'selected_text_only' && (
                <span className="source-indicator">Based on selected text</span>
              )}
              {msg.isError && (
                <span className="error-indicator">Error occurred</span>
              )}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="message assistant">
            <div className="message-content loading">
              Thinking...
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSubmit} className="chat-input-form">
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder={selectedText ? "Ask about the selected text..." : "Select text first to ask questions"}
          disabled={!selectedText || isLoading}
        />
        <button
          type="submit"
          disabled={!selectedText || !inputValue.trim() || isLoading}
        >
          Send
        </button>
      </form>
    </div>
  );
};

export default ChatInterface;
```

**src/components/personalization/PersonalizeButton.jsx**:
```jsx
import React, { useState } from 'react';

const PersonalizeButton = ({ chapterTopic, onContentUpdate }) => {
  const [isProcessing, setIsProcessing] = useState(false);
  const [personalizationApplied, setPersonalizationApplied] = useState(false);

  const handlePersonalize = async () => {
    setIsProcessing(true);

    try {
      // Call personalization API
      const response = await fetch('/api/v1/personalize/content', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          chapter_topic: chapterTopic,
          user_preferences: localStorage.getItem('userPreferences') || {}
        })
      });

      const data = await response.json();

      if (data.success) {
        // Update content based on personalization
        onContentUpdate(data.personalized_content);
        setPersonalizationApplied(true);
      }
    } catch (error) {
      console.error('Personalization failed:', error);
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <button
      onClick={handlePersonalize}
      disabled={isProcessing}
      className={`personalize-button ${personalizationApplied ? 'applied' : ''}`}
    >
      {isProcessing ? 'Applying...' : personalizationApplied ? 'Personalized ✓' : 'Personalize Content'}
    </button>
  );
};

export default PersonalizeButton;
```

**src/components/translation/UrduTranslationButton.jsx**:
```jsx
import React, { useState } from 'react';

const UrduTranslationButton = ({ content, onContentUpdate }) => {
  const [isTranslating, setIsTranslating] = useState(false);
  const [isUrdu, setIsUrdu] = useState(false);

  const toggleTranslation = async () => {
    setIsTranslating(true);

    try {
      if (isUrdu) {
        // Switch back to English
        onContentUpdate(localStorage.getItem('originalContent') || '');
        setIsUrdu(false);
      } else {
        // Save original content for later restoration
        localStorage.setItem('originalContent', content);

        // Translate to Urdu
        const response = await fetch('/api/v1/translate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            text: content,
            target_language: 'ur'
          })
        });

        const data = await response.json();

        if (data.translated_text) {
          onContentUpdate(data.translated_text);
          setIsUrdu(true);
        }
      }
    } catch (error) {
      console.error('Translation failed:', error);
      alert('Translation service temporarily unavailable. Please try again later.');
    } finally {
      setIsTranslating(false);
    }
  };

  return (
    <button
      onClick={toggleTranslation}
      disabled={isTranslating}
      className={`translation-button ${isUrdu ? 'urdu-mode' : 'english-mode'}`}
    >
      {isTranslating ? 'Translating...' : isUrdu ? 'English' : 'اردو میں دیکھیں'}
    </button>
  );
};

export default UrduTranslationButton;
```

**docusaurus.config.js**:
```javascript
// @ts-check
// `@type` JSDoc annotations allow editor autocompletion and type checking
// (when paired with `@ts-check`).
// There are various equivalent ways to declare your Docusaurus config.
// See: https://docusaurus.io/docs/api/docusaurus-config

import {themes as prismThemes} from 'prism-react-renderer';

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'AI-native Physical AI Textbook',
  tagline: 'Interactive Learning Platform with AI Assistance',
  favicon: 'img/favicon.ico',

  // Set the production url of your site here
  url: 'https://your-username.github.io',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/ai-native-textbook',

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'your-username', // Usually your GitHub org/user name.
  projectName: 'ai-native-textbook', // Usually your repo name.

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'ur'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: './sidebars.js',
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/facebook/docusaurus/tree/main/packages/create-docusaurus/templates/shared/',
        },
        blog: {
          showReadingTime: true,
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/facebook/docusaurus/tree/main/packages/create-docusaurus/templates/shared/',
        },
        theme: {
          customCss: './src/css/custom.css',
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      // Replace with your project's social card
      image: 'img/docusaurus-social-card.jpg',
      navbar: {
        title: 'Physical AI Textbook',
        logo: {
          alt: 'Physical AI Logo',
          src: 'img/logo.svg',
        },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'tutorialSidebar',
            position: 'left',
            label: 'Textbook',
          },
          {to: '/blog', label: 'Blog', position: 'left'},
          {
            href: 'https://github.com/your-username/ai-native-textbook',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Docs',
            items: [
              {
                label: 'Tutorial',
                to: '/docs/intro',
              },
            ],
          },
          {
            title: 'Community',
            items: [
              {
                label: 'Stack Overflow',
                href: 'https://stackoverflow.com/questions/tagged/docusaurus',
              },
              {
                label: 'Discord',
                href: 'https://discordapp.com/invite/docusaurus',
              },
              {
                label: 'Twitter',
                href: 'https://twitter.com/docusaurus',
              },
            ],
          },
          {
            title: 'More',
            items: [
              {
                label: 'Blog',
                to: '/blog',
              },
              {
                label: 'GitHub',
                href: 'https://github.com/facebook/docusaurus',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} AI-native Physical AI Textbook. Built with Docusaurus.`,
      },
      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
      },
    }),
};

export default config;
```

**.github/workflows/deploy.yml**:
```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  deploy:
    name: Deploy to GitHub Pages
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: 18
          cache: yarn

      - name: Install dependencies
        run: yarn install --frozen-lockfile
      - name: Build website
        run: yarn build

      # Popular action to deploy to GitHub Pages:
      # Docs: https://github.com/peaceiris/actions-gh-pages#%EF%B8%8F-docusaurus
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          # Build output to publish to the `gh-pages` branch:
          publish_dir: ./build
          # The following lines assign commit authorship to the official
          # GH-Actions bot for deploys to `gh-pages` branch:
          # https://github.com/actions/checkout/issues/13#issuecomment-724415212
          # The GH actions bot is used by default if you didn't specify the two fields.
          # You can swap them out with your own user credentials.
          user_name: github-actions[bot]
          user_email: 41898282+github-actions[bot]@users.noreply.github.com
```

### Milestones:
- ✅ Chatbot embedded in Docusaurus frontend
- ✅ Personalization button integrated into chapters
- ✅ Urdu translation button working in all chapters
- ✅ UI/UX polished and responsive
- ✅ GitHub Pages deployment configured and tested

---

## Day 7: Final Testing & Demo (December 17, 2025)

### Objectives:
- Complete end-to-end testing of all features
- Record 90-second demo video
- Prepare submission materials

### Exact Commands:
```bash
# 1. Run comprehensive tests
npm run test
python -m pytest backend/tests/

# 2. Performance testing
npx lighthouse http://localhost:3000 --output html --output-path ./reports/lighthouse-report.html

# 3. Accessibility testing
npx pa11y http://localhost:3000 --reporter html > ./reports/accessibility-report.html

# 4. Create demo script
touch demo-script.txt

# 5. Package final deliverables
mkdir -p deliverables
cp -r README.md package.json .github docs/ backend/ src/ deliverables/
```

### Demo Script (demo-script.txt):
```
90-Second Demo Script for AI-native Physical AI Textbook

[0-10s] Introduction
"Welcome to our AI-native Physical AI Textbook. I'll show you how AI transforms learning."

[10-25s] Docusaurus Book & Content
"First, our comprehensive textbook covers ROS2, Gazebo, NVIDIA Isaac, VLA, and hardware specs with interactive content."

[25-45s] RAG Chatbot with Selected-Text Feature
"Now, watch our RAG chatbot. I'll select this text about ROS2 architecture and ask a question. Notice how the AI responds only to the selected text, preventing hallucinations."

[45-60s] Authentication & Personalization
"Sign up with your background. As a software engineer, I get code-focused examples. The personalization button adapts content difficulty to my level."

[60-75s] Urdu Translation
"For multilingual support, I can instantly translate any chapter to Urdu with the 'اردو میں دیکھیں' button."

[75-90s] Conclusion
"Our platform includes 5 Claude Subagents and 5 Agent Skills for advanced AI interactions. Fully deployed to GitHub Pages. Thank you!"

Total time: 90 seconds
```

### Test Checklist:
- ✅ All 7 content modules accessible and functional
- ✅ RAG chatbot responds only to selected text (no hallucinations)
- ✅ Better-Auth signup captures background information correctly
- ✅ Personalization button adapts content based on user profile
- ✅ Urdu translation button works in all chapters
- ✅ All 5 Claude Code Subagents operational
- ✅ All 5 Agent Skills functional
- ✅ Site deployed to GitHub Pages and accessible
- ✅ Demo video recorded and tested

### Submission Materials:
1. GitHub repository URL
2. Live deployed link
3. 90-second demo video
4. Technical documentation
5. Architecture diagrams
6. Test results and performance metrics

### Final Milestones:
- ✅ Complete end-to-end functionality verified
- ✅ All base requirements (100 points) implemented
- ✅ All bonus features (200 points) implemented
- ✅ 90-second demo video recorded and edited
- ✅ Project successfully deployed to GitHub Pages
- ✅ All deliverables prepared for hackathon submission

---

## Success Criteria Verification:

### Base Requirements (100 points):
- [x] Docusaurus book using Spec-Kit Plus + Claude Code
- [x] RAG chatbot (FastAPI backend, Neon, Qdrant, OpenAI)
- [x] Selected-text-only answers functionality
- [x] All content covering ROS2, Gazebo/Unity, NVIDIA Isaac, VLA, hardware specs, weekly plan, capstone

### Bonus Features (200 points):
- [x] Better-Auth signup/login + background questions
- [x] Per-chapter "Personalize Content" button
- [x] Per-chapter "اردو میں دیکھیں" button
- [x] 5 reusable Claude Code Subagents
- [x] 5 Agent Skills
- [x] Deploy to GitHub Pages
- [x] 90-second demo video

This comprehensive 7-day plan ensures all requirements are met with proper implementation, testing, and documentation to maximize the chances of winning the Panaversity Hackathon Project 1 competition.
```

## Outcome
The implementation plan for the AI-native Interactive Textbook Platform for Physical AI has been created. It includes a comprehensive 7-day execution plan with specific commands, milestones, and implementation details for all required features including Docusaurus book, RAG chatbot with selected-text-only functionality, Better-Auth with background questions, personalization, Urdu translation, Claude Subagents/Skills, and deployment to GitHub Pages. The plan addresses both the base 100 points and bonus 200 points requirements for the Panaversity Hackathon Project 1.