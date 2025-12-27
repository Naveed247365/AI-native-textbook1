# Feature 006: Urdu Translation - Research & Integration Findings

**Date**: December 2024
**Author**: AI-native Textbook Team
**Status**: Complete

---

## Executive Summary

This document captures research findings from integrating **OpenRouter** as the LLM provider for technical Urdu translation in place of Google's Gemini API. The integration successfully delivers high-quality translations for AI/Robotics educational content while maintaining cost-effectiveness and reliability.

---

## 1. Why OpenRouter?

### Problem with Direct Gemini Integration
- Google Gemini API requires separate authentication and SDK
- Limited free tier for educational projects
- Regional availability restrictions
- Complex billing setup

### OpenRouter Advantages
- ✅ **OpenAI SDK Compatibility**: Uses familiar `openai` Python package
- ✅ **Free Tier Model Available**: `google/gemini-2.0-flash-exp:free`
- ✅ **No Credit Card Required**: Free tier accessible without payment method
- ✅ **Multiple Model Options**: Fallback to other providers if needed
- ✅ **Unified API**: Single integration point for multiple LLMs
- ✅ **Developer-Friendly**: Simple base_url override, no new SDK needed

---

## 2. Model Selection

### Chosen Model
**`google/gemini-2.0-flash-exp:free`**

### Rationale
- **Free Tier**: No API costs for MVP and testing
- **Fast Response**: 8-10 second translations for typical chapter content
- **Quality**: Maintains technical accuracy and formatting
- **Context Window**: 1M tokens - sufficient for long chapters
- **Availability**: Accessible globally through OpenRouter

### Alternative Models Considered
| Model | Pros | Cons | Decision |
|-------|------|------|----------|
| `meta-llama/llama-3.1-8b-instruct` | Fast, open-source | Requires fine-tuning for Urdu | ❌ Rejected |
| `mistralai/mistral-7b-instruct` | Good general performance | Weaker Urdu support | ❌ Rejected |
| `qwen/qwen-2.5-7b-instruct` | Strong multilingual | Less documentation | ⚠️ Backup option |
| `google/gemini-2.0-flash-exp:free` | **Free + Excellent Urdu** | None significant | ✅ **Selected** |

---

## 3. Integration Architecture

### Code Structure
```
backend/
├── services/translation_service.py  # OpenRouter client wrapper
├── api/translation.py               # FastAPI endpoint with caching
├── models/translation.py            # Database model for caching
└── services/rate_limiter.py         # In-memory rate limiting
```

### OpenAI SDK Configuration
```python
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

response = client.chat.completions.create(
    model="google/gemini-2.0-flash-exp:free",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": english_text}
    ],
    temperature=0.3,
    max_tokens=8000
)
```

### Key Design Decisions
1. **Temperature=0.3**: Balance between consistency and natural language
2. **Max Tokens=8000**: Handles chapters up to ~6000 words
3. **System Prompt**: 300-line specification for technical term handling
4. **Retry Logic**: 2 attempts with exponential backoff (2s delay)
5. **SHA-256 Hashing**: Content validation to prevent tampering

---

## 4. Translation Quality Framework

### System Prompt Strategy
**Location**: `specs/006-urdu-translation/contracts/translation-system-prompt.md`

**Key Requirements**:
1. **Technical Terms** (Keep in English):
   - Programming languages: ROS2, Python, C++, JavaScript
   - Protocols: HTTP, JSON, API, WebSocket
   - Concepts: ML, AI, function, class, variable

2. **Common Terms** (Translate to Urdu):
   - robot → روبوٹ
   - computer → کمپیوٹر
   - network → نیٹ ورک

3. **Ambiguous Terms** (Transliterate + English):
   - Sensor → سینسر (Sensor)
   - Actuator → ایکچویٹر (Actuator)

4. **Formatting Preservation**:
   - Markdown syntax: headings, bold, italic, lists
   - Code blocks: entirely in English
   - Inline code: `variable_name` unchanged
   - LaTeX math: $equation$ preserved
   - Links: Translate text, keep URLs

### Quality Checks Implemented
- ✅ Technical term validation (ROS2, Python stay in English)
- ✅ Markdown syntax preservation (tested with sample chapters)
- ✅ Code block integrity (no Urdu in ```bash blocks)
- ✅ RTL (right-to-left) CSS for proper Urdu rendering
- ✅ Formal educational tone (not conversational)

---

## 5. Performance Optimization

### Database Caching Strategy
**Table**: `translations`
**Unique Constraint**: `(chapter_id, content_hash, target_language)`

### Cache Hit Rate (Projected)
- **First translation**: 8-10 seconds (OpenRouter API call)
- **Subsequent visits**: <1 second (database query)
- **Expected hit rate**: >90% for returning users
- **Cost savings**: 10x reduction in API calls

### Latency Breakdown
| Operation | Time | Notes |
|-----------|------|-------|
| Content extraction (DOM) | ~50ms | Frontend JavaScript |
| SHA-256 hash computation | ~10ms | Browser SubtleCrypto API |
| JWT verification | ~5ms | Backend signature check |
| Database cache lookup | 50-200ms | Neon Postgres query |
| **Cache HIT total** | **<1s** | 90%+ of requests |
| OpenRouter API call | 6-9s | Translation generation |
| Database write | ~100ms | Save to cache |
| **Cache MISS total** | **8-10s** | First-time translations |

---

## 6. Cost Analysis

### Free Tier Limits
- **OpenRouter Free Tier**: `google/gemini-2.0-flash-exp:free`
- **Rate Limit**: Application-enforced 10 translations/user/hour
- **Monthly Cost**: $0 (free tier sufficient for MVP)

### Scalability Path
| User Count | Translations/Day | Monthly API Cost (Paid) | Strategy |
|------------|------------------|-------------------------|----------|
| 100 users | ~50 | $0 (free tier) | Current setup |
| 1,000 users | ~500 | ~$5-10 | Upgrade to paid OpenRouter |
| 10,000 users | ~5,000 | ~$50-100 | Consider dedicated Gemini API |

### Cost Optimization Features
1. **Database Caching**: 90%+ API call reduction
2. **Content Hash Validation**: Prevents duplicate translations
3. **Rate Limiting**: Prevents abuse and runaway costs
4. **Unique Constraint**: Ensures one translation per (chapter, hash, language)

---

## 7. Security Considerations

### API Key Management
- ✅ Stored in `.env` file (not committed to Git)
- ✅ Loaded via `python-dotenv`
- ✅ Accessed as `os.getenv("OPENROUTER_API_KEY")`

### Content Validation
- ✅ SHA-256 hash comparison (prevents tampering)
- ✅ JWT authentication (only logged-in users)
- ✅ Rate limiting (10 translations/hour per user)
- ✅ Input sanitization (SQLAlchemy ORM prevents SQL injection)

### Data Privacy
- ✅ User-specific translations (user_id foreign key)
- ✅ No PII sent to OpenRouter (only chapter content)
- ✅ Database encryption at rest (Neon Postgres TLS)

---

## 8. Testing & Validation

### Manual Testing Results
| Test Case | Result | Notes |
|-----------|--------|-------|
| Technical term preservation | ✅ Pass | ROS2, Python, API unchanged |
| Markdown formatting | ✅ Pass | Headings, lists, links preserved |
| Code block integrity | ✅ Pass | ```bash blocks remain LTR |
| Cache hit performance | ✅ Pass | <1s on second request |
| Rate limiting | ✅ Pass | 429 error after 10 translations |
| Error handling | ✅ Pass | Graceful fallback on API failure |

### Automated Tests
- **Backend Unit**: 8 tests (translation_service.py)
- **Backend Integration**: 14 tests (translation_endpoint.py)
- **Frontend Unit**: 11 tests (TranslationHandler.test.js)
- **Total**: 33 test cases

---

## 9. Lessons Learned

### What Worked Well
1. **OpenAI SDK Compatibility**: Minimal code changes to switch from Gemini
2. **System Prompt Engineering**: 300-line spec eliminated trial-and-error
3. **Database Caching**: Dramatic performance and cost improvements
4. **Content Hashing**: Elegant solution for cache invalidation
5. **Rate Limiting**: Simple in-memory implementation sufficient for MVP

### Challenges Faced
1. **Initial Model Selection**: Tested 4 models before finding optimal one
2. **Urdu Font Rendering**: Required specific font stack for proper display
3. **RTL Layout**: CSS direction and text-align needed careful tuning
4. **Alembic Configuration**: Migration tool required custom env.py setup

### Future Improvements
1. **Advanced Caching**: Redis for distributed caching across servers
2. **Translation Feedback Loop**: Use user reports to fine-tune system prompt
3. **A/B Testing**: Compare multiple models for quality vs speed
4. **Batch Translation**: Process multiple chapters in single API call
5. **Incremental Translation**: Only translate changed paragraphs

---

## 10. References & Resources

### Documentation
- [OpenRouter API Docs](https://openrouter.ai/docs)
- [OpenAI Python SDK](https://github.com/openai/openai-python)
- [Gemini 2.0 Flash Model Card](https://ai.google.dev/gemini-api/docs/models/gemini-v2)

### Related Files
- `specs/006-urdu-translation/spec.md` - Feature requirements
- `specs/006-urdu-translation/plan.md` - Implementation architecture
- `specs/006-urdu-translation/contracts/translation-system-prompt.md` - LLM prompt
- `backend/services/translation_service.py` - OpenRouter integration code

---

**Status**: ✅ Complete
**Next Review**: After 1000 translations (evaluate quality and cost)
