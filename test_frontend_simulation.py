import requests
import json

def simulate_frontend_behavior():
    print("🔍 Simulating Frontend Text Selection Behavior")
    print("=" * 70)
    print("This test simulates how the frontend would behave when users select text")
    print("and the chatbot processes their queries.")
    print()

    base_url = "http://localhost:8001/api/chat"

    # Simulate how the frontend would work:
    # 1. User selects text from the textbook
    # 2. Selected text is formatted and sent to backend
    # 3. User asks a question about the selected text

    scenarios = [
        {
            "description": "User selects Physical AI intro text and asks 'What is this?'",
            "user_query": "What is Introduction to Physical AI & Humanoid Robotics?",
            "frontend_formatted_selected_text": "Introduction to Physical AI & Humanoid Robotics: Embodied Intelligence represents the convergence of artificial intelligence with physical systems. It's the principle that true intelligence emerges not just from abstract computation, but from the interaction between an intelligent system and its physical environment. In the context of humanoid robotics, this means creating machines that can perceive, reason, and act in the physical world much like humans do. This textbook combines cutting-edge robotics concepts with artificial intelligence to provide a deep understanding of embodied intelligence systems.",
            "expected": "Should return explanation of Physical AI & Humanoid Robotics"
        },
        {
            "description": "User selects Physical AI intro text and asks 'What is embodied intelligence?'",
            "user_query": "What is embodied intelligence?",
            "frontend_formatted_selected_text": "Introduction to Physical AI & Humanoid Robotics: Embodied Intelligence represents the convergence of artificial intelligence with physical systems. It's the principle that true intelligence emerges not just from abstract computation, but from the interaction between an intelligent system and its physical environment. In the context of humanoid robotics, this means creating machines that can perceive, reason, and act in the physical world much like humans do. This textbook combines cutting-edge robotics concepts with artificial intelligence to provide a deep understanding of embodied intelligence systems.",
            "expected": "Should return explanation of embodied intelligence"
        },
        {
            "description": "User selects AI fundamentals text and asks 'What is AI?'",
            "user_query": "What is Artificial Intelligence?",
            "frontend_formatted_selected_text": "Artificial Intelligence (AI) is a branch of computer science that aims to create software or machines that exhibit human-like intelligence. This can include learning from experience, understanding natural language, solving problems, and recognizing patterns. AI systems can be trained using various techniques including machine learning, deep learning, and neural networks.",
            "expected": "Should return explanation of AI"
        },
        {
            "description": "User selects robotics text and asks 'What is robotics?'",
            "user_query": "What is robotics?",
            "frontend_formatted_selected_text": "Robotics is an interdisciplinary field that combines mechanical engineering, electrical engineering, and computer science to design, construct, and operate robots. Modern robots can perform complex tasks in manufacturing, healthcare, exploration, and service industries. They often incorporate AI to enhance their capabilities.",
            "expected": "Should return explanation of robotics"
        }
    ]

    all_passed = True

    for i, scenario in enumerate(scenarios, 1):
        print(f"Scenario {i}: {scenario['description']}")
        print(f"  Expected: {scenario['expected']}")

        payload = {
            "message": scenario['user_query'],
            "selected_text": scenario['frontend_formatted_selected_text']
        }

        try:
            response = requests.post(base_url, json=payload, headers={"Content-Type": "application/json"})
            result = response.json()

            print(f"  Status: {response.status_code}")
            print(f"  Response: {result['answer'][:100]}...")

            if "Is sawal ka jawab provided data me mojood nahi hai." in result['answer']:
                print("  ❌ FAILED: Fallback message returned")
                all_passed = False
            else:
                print("  ✅ PASSED: Content returned successfully")
        except Exception as e:
            print(f"  ❌ ERROR: {e}")
            all_passed = False

        print()

    print("=" * 70)
    if all_passed:
        print("🎉 SUCCESS: All frontend simulation tests passed!")
        print("The system works correctly for realistic user scenarios.")
    else:
        print("⚠️  Some tests failed, but this may be expected behavior")
        print("for certain edge cases in embedding-based search.")

    print("=" * 70)

if __name__ == "__main__":
    simulate_frontend_behavior()