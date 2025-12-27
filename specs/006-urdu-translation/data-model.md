# Feature 006: Urdu Translation - Data Model Documentation

**Version**: 1.0
**Database**: Neon Postgres (Serverless PostgreSQL)
**ORM**: SQLAlchemy 2.0 with async support
**Migration Tool**: Alembic

---

## Table of Contents
1. [Schema Overview](#schema-overview)
2. [Table: translations](#table-translations)
3. [Table: translation_feedback](#table-translation_feedback)
4. [Relationships](#relationships)
5. [Indexes & Constraints](#indexes--constraints)
6. [Migration History](#migration-history)
7. [Query Patterns](#query-patterns)

---

## Schema Overview

```
┌─────────────┐
│   users     │
│ (existing)  │
└──────┬──────┘
       │
       │ user_id (FK)
       │
       ├─────────────────────┬────────────────────────┐
       │                     │                        │
       ▼                     ▼                        ▼
┌──────────────────┐  ┌───────────────────┐  ┌──────────────────────┐
│  translations    │  │ personalizations  │  │ translation_feedback │
│                  │  │    (existing)     │  │                      │
└──────┬───────────┘  └───────────────────┘  └──────────────────────┘
       │
       │ translation_id (FK)
       │
       ▼
┌──────────────────────┐
│ translation_feedback │
└──────────────────────┘
```

---

## Table: translations

### Purpose
Stores translated chapter content with caching and deduplication support.

### Schema

```sql
CREATE TABLE translations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    chapter_id VARCHAR(255) NOT NULL,
    content_hash VARCHAR(64) NOT NULL,
    source_language VARCHAR(10) DEFAULT 'english',
    target_language VARCHAR(10) NOT NULL,
    original_content TEXT NOT NULL,
    translated_content TEXT NOT NULL,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    CONSTRAINT uq_chapter_hash_language UNIQUE (chapter_id, content_hash, target_language)
);

CREATE INDEX idx_translations_lookup ON translations(chapter_id, content_hash, target_language);
CREATE INDEX ix_translations_chapter_id ON translations(chapter_id);
CREATE INDEX ix_translations_content_hash ON translations(content_hash);
CREATE INDEX ix_translations_target_language ON translations(target_language);
CREATE INDEX ix_translations_user_id ON translations(user_id);
```

### SQLAlchemy Model

**File**: `backend/models/translation.py` (legacy) or `backend/database/models.py`

```python
class Translation(Base):
    __tablename__ = "translations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chapter_id = Column(String(255), nullable=False, index=True)
    content_hash = Column(String(64), nullable=False, index=True)
    source_language = Column(String(10), nullable=False, default="english")
    target_language = Column(String(10), nullable=False, index=True)
    original_content = Column(Text, nullable=False)
    translated_content = Column(Text, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint('chapter_id', 'content_hash', 'target_language', name='uq_chapter_hash_language'),
        Index('idx_translations_lookup', 'chapter_id', 'content_hash', 'target_language'),
    )
```

### Column Descriptions

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY | Unique translation record identifier |
| `chapter_id` | VARCHAR(255) | NOT NULL, INDEXED | Chapter identifier from frontmatter (e.g., `ch01-ros2-fundamentals`) |
| `content_hash` | VARCHAR(64) | NOT NULL, INDEXED | SHA-256 hash of `original_content` for cache invalidation |
| `source_language` | VARCHAR(10) | DEFAULT 'english' | Source language code (always "english" in current implementation) |
| `target_language` | VARCHAR(10) | NOT NULL, INDEXED | Target language code (e.g., "urdu") |
| `original_content` | TEXT | NOT NULL | Full English chapter content (MDX/Markdown) |
| `translated_content` | TEXT | NOT NULL | Translated content with formatting preserved |
| `user_id` | UUID | FK → users.id, NOT NULL | User who requested the translation (for billing/analytics) |
| `created_at` | TIMESTAMP TZ | DEFAULT NOW() | When translation was first created |
| `updated_at` | TIMESTAMP TZ | DEFAULT NOW() | Last update timestamp (currently unused) |

### Cache Strategy
- **Unique Constraint**: `(chapter_id, content_hash, target_language)` ensures one translation per unique content version
- **Cache Invalidation**: When chapter content changes, new `content_hash` triggers new translation
- **Shared Cache**: Multiple users benefit from same translation (first user pays API cost, others get instant cache hit)

### Example Records

```json
{
  "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "chapter_id": "ch01-ros2-fundamentals",
  "content_hash": "8f3a9d2b7c4e5f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5",
  "source_language": "english",
  "target_language": "urdu",
  "original_content": "## Introduction to ROS2\n\nROS2 is a middleware framework...",
  "translated_content": "## ROS2 کا تعارف\n\nROS2 ایک middleware فریم ورک ہے...",
  "user_id": "f1e2d3c4-b5a6-7890-abcd-ef0987654321",
  "created_at": "2024-12-24T10:30:00Z",
  "updated_at": "2024-12-24T10:30:00Z"
}
```

---

## Table: translation_feedback

### Purpose
Stores user-reported issues with translation quality for continuous improvement.

### Schema

```sql
CREATE TABLE translation_feedback (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    translation_id UUID NOT NULL REFERENCES translations(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    issue_description TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX ix_translation_feedback_translation_id ON translation_feedback(translation_id);
CREATE INDEX ix_translation_feedback_user_id ON translation_feedback(user_id);
```

### SQLAlchemy Model

**File**: `backend/models/translation_feedback.py`

```python
class TranslationFeedback(Base):
    __tablename__ = "translation_feedback"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    translation_id = Column(UUID(as_uuid=True), ForeignKey("translations.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    issue_description = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
```

### Column Descriptions

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY | Unique feedback record identifier |
| `translation_id` | UUID | FK → translations.id, NOT NULL | Translation being reported |
| `user_id` | UUID | FK → users.id, NOT NULL | User submitting feedback |
| `issue_description` | TEXT | NOT NULL | Description of translation quality issue (10-2000 chars) |
| `created_at` | TIMESTAMP TZ | DEFAULT NOW() | Feedback submission timestamp |

### Example Records

```json
{
  "id": "f1e2d3c4-b5a6-7890-abcd-ef0987654321",
  "translation_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "user_id": "f1e2d3c4-b5a6-7890-abcd-ef0987654321",
  "issue_description": "The term 'API' was incorrectly translated to Urdu, but it should remain in English as per technical guidelines.",
  "created_at": "2024-12-24T11:45:00Z"
}
```

---

## Relationships

### Entity Relationship Diagram

```
┌──────────────────┐
│     users        │
│ ──────────────── │
│ id (PK)          │
│ email            │
│ password_hash    │
│ ...              │
└────────┬─────────┘
         │
         │ 1:N
         │
         ├──────────────────────────┐
         │                          │
         ▼                          ▼
┌────────────────────┐    ┌─────────────────────────┐
│   translations     │    │  translation_feedback   │
│ ────────────────── │    │ ─────────────────────── │
│ id (PK)            │◄───│ translation_id (FK)     │
│ chapter_id         │    │ user_id (FK)            │
│ content_hash       │    │ issue_description       │
│ ...                │    │ created_at              │
│ user_id (FK) ──────┼────┤                         │
└────────────────────┘    └─────────────────────────┘
         │
         │ UNIQUE (chapter_id, content_hash, target_language)
         └─ Ensures cache deduplication
```

### Foreign Key Constraints

1. **translations.user_id → users.id**
   - ON DELETE CASCADE: Delete translations when user account deleted
   - Purpose: Track which user first requested the translation

2. **translation_feedback.translation_id → translations.id**
   - ON DELETE CASCADE: Delete feedback when translation deleted
   - Purpose: Link feedback to specific translation

3. **translation_feedback.user_id → users.id**
   - ON DELETE CASCADE: Delete feedback when user account deleted
   - Purpose: Track which user reported the issue

---

## Indexes & Constraints

### Primary Indexes (Automatic)
- `translations.id` (PRIMARY KEY)
- `translation_feedback.id` (PRIMARY KEY)

### Unique Constraints
- `uq_chapter_hash_language` on `translations(chapter_id, content_hash, target_language)`
  - **Purpose**: Prevent duplicate translations for same content
  - **Behavior**: INSERT fails with IntegrityError if duplicate detected
  - **Handling**: Backend retries query on IntegrityError (race condition)

### Composite Index (Critical Performance)
- `idx_translations_lookup` on `translations(chapter_id, content_hash, target_language)`
  - **Purpose**: Fast cache lookups (WHERE clause matches index exactly)
  - **Query Time**: <200ms on 10,000+ records
  - **Usage**: Every translation request hits this index

### Single-Column Indexes
- `ix_translations_chapter_id`: Filter by chapter for analytics
- `ix_translations_content_hash`: Debug queries by hash
- `ix_translations_target_language`: Filter by language for reporting
- `ix_translations_user_id`: User-specific translation history
- `ix_translation_feedback_translation_id`: Find feedback for a translation
- `ix_translation_feedback_user_id`: User's feedback history

---

## Migration History

### Migration 1: Initial Translations Table

**File**: `backend/database/migrations/versions/57c6b0ea13f8_add_translations_table.py`
**Date**: December 2024
**Purpose**: Create translations table with caching support

```bash
alembic revision --autogenerate -m "add translations table"
alembic upgrade head
```

**Changes**:
- Created `translations` table
- Added unique constraint `uq_chapter_hash_language`
- Created composite index `idx_translations_lookup`
- Added foreign key to `users.id`

### Migration 2: Translation Feedback Table

**File**: `backend/database/migrations/versions/809b34b1c5dc_add_translation_feedback_table.py`
**Date**: December 2024
**Purpose**: Add user feedback mechanism for translation quality

```bash
alembic revision --autogenerate -m "add translation_feedback table"
alembic upgrade head
```

**Changes**:
- Created `translation_feedback` table
- Added foreign keys to `translations.id` and `users.id`
- Created indexes on `translation_id` and `user_id`

---

## Query Patterns

### 1. Cache Lookup (Most Frequent)

**Purpose**: Check if translation already exists before calling OpenRouter API

```python
# SQLAlchemy ORM
cached_translation = db.query(Translation).filter(
    Translation.chapter_id == request.chapter_id,
    Translation.content_hash == request.content_hash,
    Translation.target_language == "urdu"
).first()

# Raw SQL (for reference)
SELECT * FROM translations
WHERE chapter_id = 'ch01-ros2-fundamentals'
  AND content_hash = '8f3a9d2b...'
  AND target_language = 'urdu'
LIMIT 1;
```

**Performance**: <200ms (uses `idx_translations_lookup`)

### 2. Insert New Translation (Cache Miss)

```python
# SQLAlchemy ORM
db_translation = Translation(
    id=uuid.uuid4(),
    chapter_id=request.chapter_id,
    content_hash=request.content_hash,
    source_language="english",
    target_language="urdu",
    original_content=request.content,
    translated_content=translated_text,
    user_id=uuid.UUID(user_id)
)
db.add(db_translation)
db.commit()
```

**Handles Duplicates**:
```python
try:
    db.commit()
except IntegrityError:
    db.rollback()
    # Race condition - another request created translation
    # Query again to get existing translation
    cached_translation = db.query(Translation).filter(...).first()
```

### 3. Submit Feedback

```python
feedback = TranslationFeedback(
    id=uuid.uuid4(),
    translation_id=uuid.UUID(request.translation_id),
    user_id=uuid.UUID(user_id),
    issue_description=request.issue_description
)
db.add(feedback)
db.commit()
```

### 4. Analytics Queries (Admin/Reporting)

**Translation volume by chapter**:
```sql
SELECT chapter_id, target_language, COUNT(*) as translation_count
FROM translations
GROUP BY chapter_id, target_language
ORDER BY translation_count DESC;
```

**Cache hit rate calculation**:
```sql
-- Requires application-level tracking (not stored in DB)
-- See backend/api/translation.py for in-memory metrics
```

**Most reported translations**:
```sql
SELECT t.chapter_id, t.id, COUNT(f.id) as feedback_count
FROM translations t
JOIN translation_feedback f ON f.translation_id = t.id
GROUP BY t.chapter_id, t.id
ORDER BY feedback_count DESC
LIMIT 10;
```

---

## Performance Considerations

### Connection Pooling
**Configuration**: `backend/database/db.py`

```python
engine = create_engine(
    NEON_POSTGRES_URL,
    poolclass=NullPool  # Serverless Neon recommended configuration
)
```

**Rationale**: Neon Postgres is serverless, so connection pooling is handled at the platform level.

### Query Optimization
1. **Composite Index First**: Always query with `(chapter_id, content_hash, target_language)` to hit composite index
2. **LIMIT 1**: Cache lookups only need first match due to unique constraint
3. **Eager Foreign Key Loading**: Not needed (translations are self-contained)

### Scaling Considerations
- **Expected Growth**: ~10,000 translations for 100-chapter book with 100 users
- **Storage**: ~100KB per translation × 10,000 = ~1GB
- **Query Performance**: Composite index remains fast up to 1M+ records

---

## Security & Data Privacy

### Data Encryption
- ✅ **At Rest**: Neon Postgres TLS encryption
- ✅ **In Transit**: HTTPS/TLS for API calls

### Data Retention
- **Translations**: Indefinite (shared cache benefit)
- **Feedback**: Indefinite (quality improvement)
- **User Deletion**: CASCADE deletes all user's translations and feedback

### PII Considerations
- **No PII in Translations**: Only chapter content (public domain)
- **User ID Foreign Key**: Links to user account but not exposed in API response
- **Feedback**: May contain user-specific observations (admin-only access)

---

**Last Updated**: December 2024
**Schema Version**: 1.0
**Status**: ✅ Production Ready
