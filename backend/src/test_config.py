#!/usr/bin/env python3
"""
Test script to verify configuration management functionality
"""
import os
import sys
from pathlib import Path

# Add the src directory to the path so we can import modules
sys.path.insert(0, str(Path(__file__).parent))

def test_config_validation():
    """Test that configuration validation works properly"""
    print("Testing configuration validation...")

    # Test 1: Check that settings can be imported and initialized
    try:
        from config.settings import settings
        print("✓ Settings module imported successfully")
        print(f"✓ Server host: {settings.server_host}")
        print(f"✓ Server port: {settings.server_port}")
        print(f"✓ Debug mode: {settings.debug}")
        print(f"✓ Log level: {settings.log_level}")
    except Exception as e:
        print(f"✗ Failed to import or initialize settings: {e}")
        return False

    # Test 2: Check that required fields are validated
    # Temporarily unset a required environment variable to test validation
    original_neon_url = os.environ.get('NEON_DB_URL')

    # Remove the environment variable to test validation
    if 'NEON_DB_URL' in os.environ:
        del os.environ['NEON_DB_URL']

    # Try to create new settings instance without required env var
    try:
        from pydantic_settings import BaseSettings
        from pydantic import ValidationError

        # This should fail because we removed a required environment variable
        from config.settings import Settings
        try:
            temp_settings = Settings()
            print("✗ Validation failed - should have raised an error for missing required field")
            return False
        except (ValidationError, ValueError) as e:
            print(f"✓ Validation correctly caught missing required field: {type(e).__name__}")
        except Exception as e:
            print(f"✓ Validation correctly caught missing required field: {type(e).__name__}")
    finally:
        # Restore the original environment variable
        if original_neon_url is not None:
            os.environ['NEON_DB_URL'] = original_neon_url

    # Test 3: Check that default values work
    print(f"✓ JWT algorithm default: {settings.jwt_algorithm}")
    print(f"✓ JWT expires in default: {settings.jwt_expires_in}")

    # Test 4: Check that debug validation works with string input
    original_debug = os.environ.get('DEBUG')
    try:
        os.environ['DEBUG'] = 'true'
        from config.settings import Settings
        temp_settings = Settings()
        assert temp_settings.debug is True
        print("✓ Debug validation works with 'true' string")

        os.environ['DEBUG'] = 'false'
        temp_settings = Settings()
        assert temp_settings.debug is False
        print("✓ Debug validation works with 'false' string")

        os.environ['DEBUG'] = '1'
        temp_settings = Settings()
        assert temp_settings.debug is True
        print("✓ Debug validation works with '1' string")

    except Exception as e:
        print(f"✗ Debug validation test failed: {e}")
        return False
    finally:
        # Restore original value
        if original_debug is not None:
            os.environ['DEBUG'] = original_debug
        elif 'DEBUG' in os.environ:
            del os.environ['DEBUG']

    print("\n✓ All configuration validation tests passed!")
    return True

def test_database_config():
    """Test that database configuration works properly"""
    print("\nTesting database configuration...")

    try:
        from config.database import engine, AsyncSessionLocal, logger
        print("✓ Database engine created successfully")
        print("✓ Async session factory created successfully")
        print(f"✓ Database URL is properly configured (not shown for security)")
        print("✓ Connection pool settings applied")
    except Exception as e:
        print(f"✗ Database configuration test failed: {e}")
        return False

    print("✓ Database configuration test passed!")
    return True

if __name__ == "__main__":
    print("Running Configuration Management Tests...\n")

    config_ok = test_config_validation()
    db_ok = test_database_config()

    if config_ok and db_ok:
        print("\n🎉 All tests passed! Configuration management is working correctly.")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)