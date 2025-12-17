import requests
import json

def test_specific_content():
    print("🔍 Testing Physical AI & Humanoid Robotics Content")
    print("=" * 60)

    base_url = "http://localhost:8001/api/chat"

    # Test with the exact content that we know exists
    print("Testing various queries with Physical AI content:")

    tests = [
        {
            "name": "Query: Tell me about Physical AI",
            "message": "Tell me about Physical AI",
            "selected_text": "Introduction to Physical AI & Humanoid Robotics: Embodied Intelligence represents the convergence of artificial intelligence with physical systems. It's the principle that true intelligence emerges not just from abstract computation, but from the interaction between an intelligent system and its physical environment. In the context of humanoid robotics, this means creating machines that can perceive, reason, and act in the physical world much like humans do. This textbook combines cutting-edge robotics concepts with artificial intelligence to provide a deep understanding of embodied intelligence systems."
        },
        {
            "name": "Query: Explain embodied intelligence",
            "message": "Explain embodied intelligence",
            "selected_text": "Introduction to Physical AI & Humanoid Robotics: Embodied Intelligence represents the convergence of artificial intelligence with physical systems. It's the principle that true intelligence emerges not just from abstract computation, but from the interaction between an intelligent system and its physical environment. In the context of humanoid robotics, this means creating machines that can perceive, reason, and act in the physical world much like humans do. This textbook combines cutting-edge robotics concepts with artificial intelligence to provide a deep understanding of embodied intelligence systems."
        },
        {
            "name": "Query: What is Physical AI & Humanoid Robotics?",
            "message": "What is Physical AI & Humanoid Robotics?",
            "selected_text": "Introduction to Physical AI & Humanoid Robotics: Embodied Intelligence represents the convergence of artificial intelligence with physical systems. It's the principle that true intelligence emerges not just from abstract computation, but from the interaction between an intelligent system and its physical environment. In the context of humanoid robotics, this means creating machines that can perceive, reason, and act in the physical world much like humans do. This textbook combines cutting-edge robotics concepts with artificial intelligence to provide a deep understanding of embodied intelligence systems."
        },
        {
            "name": "Query: Introduction to Physical AI (short)",
            "message": "Introduction to Physical AI",
            "selected_text": "Introduction to Physical AI & Humanoid Robotics: Embodied Intelligence represents the convergence of artificial intelligence with physical systems. It's the principle that true intelligence emerges not just from abstract computation, but from the interaction between an intelligent system and its physical environment. In the context of humanoid robotics, this means creating machines that can perceive, reason, and act in the physical world much like humans do. This textbook combines cutting-edge robotics concepts with artificial intelligence to provide a deep understanding of embodied intelligence systems."
        }
    ]

    for i, test in enumerate(tests, 1):
        print(f"\nTest {i}: {test['name']}")
        try:
            response = requests.post(base_url, json=test, headers={"Content-Type": "application/json"})
            result = response.json()

            print(f"  Status: {response.status_code}")
            print(f"  Response: {result['answer'][:150]}...")

            if "Is sawal ka jawab provided data me mojood nahi hai." in result['answer']:
                print("  ❌ Result: Fallback returned (content not found)")
            else:
                print("  ✅ Result: Content returned successfully")

        except Exception as e:
            print(f"  ❌ Error: {e}")

    print("\n" + "=" * 60)
    print("💡 The key insight: The selected_text parameter is used to find")
    print("   relevant context in Qdrant, while the message parameter is")
    print("   the actual question asked about that context.")

if __name__ == "__main__":
    test_specific_content()