import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

# Test OpenRouter API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key or api_key == "your_openrouter_api_key_here":
    print("❌ OPENAI_API_KEY not set or using default value in .env file")
else:
    print("✅ OPENAI_API_KEY is set in .env file")

    # Try to make a simple API call
    try:
        client = OpenAI(
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1"
        )

        # Test with a simple completion
        response = client.chat.completions.create(
            model="openai/gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=10
        )

        print(f"✅ OpenRouter API connection successful: {response.choices[0].message.content[:50]}...")

    except Exception as e:
        print(f"❌ OpenRouter API error: {str(e)}")