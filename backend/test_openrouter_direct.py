"""
Direct test of OpenRouter API to verify it's working
"""
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
print(f"API Key loaded: {api_key[:20]}..." if api_key else "No API key found!")

# Initialize OpenAI client with OpenRouter
client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)

# Test 1: Simple chat completion
print("\n=== Test 1: Simple Chat ===")
try:
    response = client.chat.completions.create(
        model="openai/gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "Say 'Hello, I am working!' in one sentence."}
        ],
        temperature=0
    )
    print(f"✅ Success: {response.choices[0].message.content}")
except Exception as e:
    print(f"❌ Error: {str(e)}")

# Test 2: RAG-style query with context
print("\n=== Test 2: RAG with Context ===")
context = """
Physical AI refers to artificial intelligence systems that interact with the physical world.
These systems use sensors to perceive their environment and actuators to take actions.
Examples include robots, self-driving cars, and drones.
"""

question = "What is Physical AI?"

try:
    response = client.chat.completions.create(
        model="openai/gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful AI assistant. Answer based on the provided context."},
            {"role": "user", "content": f"Context: {context}\n\nQuestion: {question}"}
        ],
        temperature=0.3,
        max_tokens=500
    )
    print(f"✅ Success: {response.choices[0].message.content}")
except Exception as e:
    print(f"❌ Error: {str(e)}")

# Test 3: Check if response is empty or too short
print("\n=== Test 3: Response Length Check ===")
try:
    response = client.chat.completions.create(
        model="openai/gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "Explain robotics in 50 words."}
        ],
        temperature=0.3
    )
    answer = response.choices[0].message.content
    print(f"Response length: {len(answer)} characters")
    print(f"Response: {answer}")

    if len(answer) < 20:
        print("⚠️ WARNING: Response too short!")
    else:
        print("✅ Response length is good")
except Exception as e:
    print(f"❌ Error: {str(e)}")

print("\n=== All Tests Complete ===")
