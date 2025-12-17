#!/usr/bin/env python3
"""
Database Migration Script for AI Backend with RAG + Authentication
This script creates all required tables in the Neon Postgres database
"""
import asyncio
import sys
import logging
import os
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

# Add the src directory to the path so we can import our modules
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
src_dir = os.path.join(project_root, "src")
sys.path.insert(0, src_dir)

from db.base import Base
from config.settings import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


async def create_database_tables():
    """Create all required database tables"""
    logger.info("Starting database migration...")

    # Create async engine
    engine = create_async_engine(
        settings.neon_db_url,
        echo=True,  # Set to True to log SQL queries during migration
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10,
    )

    try:
        logger.info("Connecting to database...")

        # Create all tables
        async with engine.begin() as conn:
            logger.info("Creating tables...")
            await conn.run_sync(Base.metadata.create_all)
            logger.info("Tables created successfully")

            # Verify tables exist by checking if we can access them
            tables = Base.metadata.tables.keys()
            logger.info(f"Created {len(tables)} tables: {list(tables)}")

            # Test connection by running a simple query
            result = await conn.execute(text("SELECT 1"))
            logger.info("Database connection test successful")

        logger.info("Database migration completed successfully!")
        return True

    except Exception as e:
        logger.error(f"Database migration failed: {e}")
        return False
    finally:
        # Dispose of the engine to close all connections
        await engine.dispose()


async def check_existing_tables():
    """Check if tables already exist in the database"""
    engine = create_async_engine(
        settings.neon_db_url,
        pool_pre_ping=True,
    )

    try:
        async with engine.begin() as conn:
            # Get list of existing tables
            result = await conn.execute(text("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
            """))
            existing_tables = [row[0] for row in result]

            logger.info(f"Existing tables in database: {existing_tables}")

            # Check which of our models' tables already exist
            our_tables = [table.name for table in Base.metadata.tables.values()]
            existing_our_tables = [table for table in our_tables if table in existing_tables]

            if existing_our_tables:
                logger.warning(f"The following tables already exist: {existing_our_tables}")
                return existing_our_tables
            else:
                logger.info("No existing tables from our models found.")
                return []

    except Exception as e:
        logger.error(f"Error checking existing tables: {e}")
        return []
    finally:
        await engine.dispose()


async def run_migration():
    """Main function to run the migration"""
    logger.info("Migration script started")

    # Check for existing tables
    existing_tables = await check_existing_tables()

    if existing_tables:
        logger.info("Some tables already exist. Migration will continue and handle existing tables gracefully.")
    else:
        logger.info("No existing tables found. Proceeding with fresh migration.")

    # Create tables
    success = await create_database_tables()

    if success:
        logger.info("Migration completed successfully!")
        return True
    else:
        logger.error("Migration failed!")
        return False


if __name__ == "__main__":
    # Check if we're running in a virtual environment or have the required dependencies
    try:
        import sqlalchemy
        import asyncpg
    except ImportError as e:
        logger.error(f"Required dependencies not found: {e}")
        logger.error("Please make sure you've installed the requirements: pip install -r requirements.txt")
        sys.exit(1)

    # Run the migration
    success = asyncio.run(run_migration())

    if success:
        logger.info("Migration script completed successfully!")
        sys.exit(0)
    else:
        logger.error("Migration script failed!")
        sys.exit(1)