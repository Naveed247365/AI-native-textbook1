"""
Test the formatted message parsing
"""
import os
import sys
from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from services.rag_service import RAGService

# Initialize
api_key = os.getenv("OPENAI_API_KEY")
rag_service = RAGService(api_key, None, "project_documents")

# Test Case 1: User sends formatted message (what frontend sends)
print("=== Test 1: Formatted Message (Current Issue) ===")
selected_text = "Interactive Learning Features"
question = """Selected text:
"Interactive Learning Features"

Ask a question about this text..."""

print(f"Selected Text: {selected_text}")
print(f"Question (formatted): {question}")

# This is what's happening now - question should be extracted properly
# In the fixed version, frontend will extract it, but let's test backend fallback
answer = rag_service.query_rag(selected_text, question)
print(f"\n✅ Answer: {answer[:200]}...")
print(f"Length: {len(answer)} chars\n")

# Test Case 2: User sends just the selected text (no question)
print("=== Test 2: No Question, Just Selected Text ===")
selected_text2 = "Physical AI refers to artificial intelligence"
question2 = ""  # Empty question

answer2 = rag_service.query_rag(selected_text2, question2)
print(f"\n✅ Answer: {answer2[:200]}...")
print(f"Length: {len(answer2)} chars\n")

# Test Case 3: Normal question (should work)
print("=== Test 3: Normal Question ===")
selected_text3 = "Robots use sensors and actuators to interact with the environment"
question3 = "What are sensors and actuators?"

answer3 = rag_service.query_rag(selected_text3, question3)
print(f"\n✅ Answer: {answer3[:200]}...")
print(f"Length: {len(answer3)} chars\n")

# Test Case 4: Question same as selected text
print("=== Test 4: Question Same as Selected Text ===")
selected_text4 = "Humanoid Robotics"
question4 = "Humanoid Robotics"  # Same as selected text

answer4 = rag_service.query_rag(selected_text4, question4)
print(f"\n✅ Answer: {answer4[:200]}...")
print(f"Length: {len(answer4)} chars\n")

print("\n=== All Tests Complete ===")
