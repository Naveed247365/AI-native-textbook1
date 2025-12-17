import requests
import json

def test_comprehensive():
    print("🔍 Comprehensive End-to-End Test")
    print("=" * 70)

    base_url = "http://localhost:8001/api/chat"

    # Test cases to validate different scenarios
    test_cases = [
        {
            "name": "Physical AI Introduction - Direct Query",
            "payload": {
                "message": "Introduction to Physical AI & Humanoid Robotics",
                "selected_text": "Introduction to Physical AI & Humanoid Robotics"
            },
            "expected_behavior": "May return fallback due to short query"
        },
        {
            "name": "Physical AI with Full Context",
            "payload": {
                "message": "Introduction to Physical AI & Humanoid Robotics",
                "selected_text": "Introduction to Physical AI & Humanoid Robotics: Embodied Intelligence represents the convergence of artificial intelligence with physical systems. It's the principle that true intelligence emerges not just from abstract computation, but from the interaction between an intelligent system and its physical environment. In the context of humanoid robotics, this means creating machines that can perceive, reason, and act in the physical world much like humans do. This textbook combines cutting-edge robotics concepts with artificial intelligence to provide a deep understanding of embodied intelligence systems."
            },
            "expected_behavior": "Should work with full context"
        },
        {
            "name": "Embodied Intelligence Question",
            "payload": {
                "message": "What is embodied intelligence?",
                "selected_text": "Introduction to Physical AI & Humanoid Robotics: Embodied Intelligence represents the convergence of artificial intelligence with physical systems."
            },
            "expected_behavior": "Should return detailed explanation"
        },
        {
            "name": "AI Fundamentals Query",
            "payload": {
                "message": "What is Artificial Intelligence?",
                "selected_text": "Artificial Intelligence (AI) is a branch of computer science that aims to create software or machines that exhibit human-like intelligence. This can include learning from experience, understanding natural language, solving problems, and recognizing patterns. AI systems can be trained using various techniques including machine learning, deep learning, and neural networks."
            },
            "expected_behavior": "Should return AI explanation"
        },
        {
            "name": "Robotics Query",
            "payload": {
                "message": "What is robotics?",
                "selected_text": "Robotics is an interdisciplinary field that combines mechanical engineering, electrical engineering, and computer science to design, construct, and operate robots. Modern robots can perform complex tasks in manufacturing, healthcare, exploration, and service industries. They often incorporate AI to enhance their capabilities."
            },
            "expected_behavior": "Should return robotics explanation"
        },
        {
            "name": "Fallback Test",
            "payload": {
                "message": "What is Quantum Computing?",
                "selected_text": "This is completely unrelated text that should not match anything in the database."
            },
            "expected_behavior": "Should return fallback message"
        }
    ]

    results = []
    for i, test_case in enumerate(test_cases, 1):
        print(f"Test {i}: {test_case['name']}")
        print(f"  Expected: {test_case['expected_behavior']}")

        try:
            response = requests.post(base_url, json=test_case['payload'], headers={"Content-Type": "application/json"})
            result = response.json()

            print(f"  Status: {response.status_code}")
            print(f"  Response: {result['answer'][:100]}...")

            # Analyze result
            if "Is sawal ka jawab provided data me mojood nahi hai." in result['answer']:
                if test_case['name'] == "Fallback Test":
                    print("  ✅ Result: Expected fallback (PASS)")
                    status = "PASS"
                else:
                    print("  ❌ Result: Unexpected fallback (FAIL)")
                    status = "FAIL"
            else:
                if test_case['name'] == "Fallback Test":
                    print("  ❌ Result: Expected fallback but got content (FAIL)")
                    status = "FAIL"
                else:
                    print("  ✅ Result: Got content as expected (PASS)")
                    status = "PASS"

            results.append({
                "test": test_case['name'],
                "status": status,
                "response": result['answer']
            })

        except Exception as e:
            print(f"  ❌ Error: {e}")
            results.append({
                "test": test_case['name'],
                "status": "ERROR",
                "response": str(e)
            })

        print()

    # Summary
    print("=" * 70)
    print("📋 TEST SUMMARY:")
    passed = sum(1 for r in results if r['status'] == 'PASS')
    total = len(results)

    for result in results:
        status_emoji = "✅" if result['status'] == 'PASS' else "❌"
        print(f"  {status_emoji} {result['test']}: {result['status']}")

    print(f"\n📊 Overall: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! The system is working correctly.")
    else:
        print(f"⚠️  {total - passed} tests failed. Review the issues above.")

    print("=" * 70)

    return passed == total

if __name__ == "__main__":
    test_comprehensive()