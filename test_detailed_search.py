import requests
import json

def test_detailed_search():
    print("🔍 Testing the specific query that was failing")
    print("=" * 60)

    base_url = "http://localhost:8001/api/chat"

    # Test 1: The original failing query
    print("Test 1: Original query that was failing")
    payload1 = {
        "message": "Introduction to Physical AI & Humanoid Robotics",
        "selected_text": "Introduction to Physical AI & Humanoid Robotics"
    }

    try:
        response1 = requests.post(base_url, json=payload1, headers={"Content-Type": "application/json"})
        result1 = response1.json()
        print(f"  Response: {result1['answer']}")
        print(f"  Status: {response1.status_code}")
        if "Is sawal ka jawab provided data me mojood nahi hai." in result1['answer']:
            print("  ❌ Result: Still returning fallback")
        else:
            print("  ✅ Result: Returning proper content")
    except Exception as e:
        print(f"  ❌ Error: {e}")
    print()

    # Test 2: Query with the actual content that exists
    print("Test 2: Query with actual content that exists in DB")
    payload2 = {
        "message": "Introduction to Physical AI & Humanoid Robotics",
        "selected_text": "Introduction to Physical AI & Humanoid Robotics: Embodied Intelligence represents the convergence of artificial intelligence with physical systems. It's the principle that true intelligence emerges not just from abstract computation, but from the interaction between an intelligent system and its physical environment. In the context of humanoid robotics, this means creating machines that can perceive, reason, and act in the physical world much like humans do. This textbook combines cutting-edge robotics concepts with artificial intelligence to provide a deep understanding of embodied intelligence systems."
    }

    try:
        response2 = requests.post(base_url, json=payload2, headers={"Content-Type": "application/json"})
        result2 = response2.json()
        print(f"  Response: {result2['answer'][:100]}...")
        print(f"  Status: {response2.status_code}")
        if "Is sawal ka jawab provided data me mojood nahi hai." in result2['answer']:
            print("  ❌ Result: Still returning fallback")
        else:
            print("  ✅ Result: Returning proper content")
    except Exception as e:
        print(f"  ❌ Error: {e}")
    print()

    # Test 3: Different query asking about the content
    print("Test 3: Different query asking about the content")
    payload3 = {
        "message": "What is embodied intelligence?",
        "selected_text": "Introduction to Physical AI & Humanoid Robotics: Embodied Intelligence represents the convergence of artificial intelligence with physical systems. It's the principle that true intelligence emerges not just from abstract computation, but from the interaction between an intelligent system and its physical environment. In the context of humanoid robotics, this means creating machines that can perceive, reason, and act in the physical world much like humans do. This textbook combines cutting-edge robotics concepts with artificial intelligence to provide a deep understanding of embodied intelligence systems."
    }

    try:
        response3 = requests.post(base_url, json=payload3, headers={"Content-Type": "application/json"})
        result3 = response3.json()
        print(f"  Response: {result3['answer'][:100]}...")
        print(f"  Status: {response3.status_code}")
        if "Is sawal ka jawab provided data me mojood nahi hai." in result3['answer']:
            print("  ❌ Result: Still returning fallback")
        else:
            print("  ✅ Result: Returning proper content")
    except Exception as e:
        print(f"  ❌ Error: {e}")
    print()

    print("=" * 60)
    print("🔍 ANALYSIS:")
    print("The issue appears to be that when the 'message' and 'selected_text' are identical")
    print("and very short, the RAG system might not find a good match in the vector database.")
    print("The system works when there's more context in the selected text or a specific question.")

if __name__ == "__main__":
    test_detailed_search()