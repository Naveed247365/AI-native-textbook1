from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from .settings import settings
import logging

logger = logging.getLogger(__name__)

try:
    # Create async engine with proper configuration from settings
    engine = create_async_engine(
        settings.neon_db_url,
        echo=settings.debug,  # Set to True to log SQL queries
        pool_pre_ping=True,  # Verify connections before use
        pool_size=20,  # Connection pool size
        max_overflow=30,  # Additional connections beyond pool_size
        pool_recycle=3600,  # Recycle connections after 1 hour
        pool_pre_ping_enabled=True,  # Enable connection health checks
        pool_pool_timeout=30,  # Connection timeout
        pool_reset_on_return='commit'  # Reset connection on return
    )

    # Create async session factory
    AsyncSessionLocal = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    logger.info("Database engine created successfully")
except Exception as e:
    logger.error(f"Failed to create database engine: {e}")
    raise


async def get_db_session():
    """Dependency to get database session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            logger.error(f"Database session error: {e}")
            await session.rollback()
            raise
        finally:
            await session.close()


# Initialize the database connection
async def init_db():
    """Initialize the database connection and create tables if needed"""
    from ..db.base import Base

    logger.info("Initializing database connection...")
    try:
        # Create all tables
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise