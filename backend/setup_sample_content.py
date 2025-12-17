import os
import sys
from qdrant_client import QdrantClient
from openai import OpenAI
import uuid
from dotenv import load_dotenv

# Load environment variables from .env file in the project root
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

# Add the backend directory to the path so we can import the RAG service
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from services.rag_service import RAGService

def setup_sample_content():
    # Get environment variables
    openrouter_api_key = os.getenv("OPENAI_API_KEY")
    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")
    collection_name = os.getenv("QDRANT_COLLECTION", "project_documents")

    # Initialize Qdrant client for cloud
    if qdrant_url and qdrant_api_key and "qdrant.io" in qdrant_url:
        qdrant_client = QdrantClient(
            url=qdrant_url.replace(":6333", ""),  # Remove port from URL for cloud (same as in chat.py)
            api_key=qdrant_api_key,
            prefer_grpc=False
        )
    else:
        # Use local Qdrant if cloud not configured
        qdrant_client = QdrantClient(
            host=os.getenv("QDRANT_HOST", "localhost"),
            port=int(os.getenv("QDRANT_PORT", 6333))
        )

    # Initialize RAG service
    rag_service = RAGService(openrouter_api_key, qdrant_client, collection_name)

    # Sample content about AI and Robotics
    import uuid

    sample_content = [
        {
            "id": str(uuid.uuid4()),
            "content": "Introduction to Physical AI & Humanoid Robotics: Embodied Intelligence represents the convergence of artificial intelligence with physical systems. It's the principle that true intelligence emerges not just from abstract computation, but from the interaction between an intelligent system and its physical environment. In the context of humanoid robotics, this means creating machines that can perceive, reason, and act in the physical world much like humans do. This textbook combines cutting-edge robotics concepts with artificial intelligence to provide a deep understanding of embodied intelligence systems.",
            "metadata": {"topic": "Introduction to Physical AI & Humanoid Robotics", "level": "beginner", "original_id": "intro_physical_ai_1"}
        },
        {
            "id": str(uuid.uuid4()),
            "content": "Artificial Intelligence (AI) is a branch of computer science that aims to create software or machines that exhibit human-like intelligence. This can include learning from experience, understanding natural language, solving problems, and recognizing patterns. AI systems can be trained using various techniques including machine learning, deep learning, and neural networks.",
            "metadata": {"topic": "AI Fundamentals", "level": "beginner", "original_id": "ai_fundamentals_1"}
        },
        {
            "id": str(uuid.uuid4()),
            "content": "Machine learning is a subset of artificial intelligence that focuses on algorithms that can learn from data. Instead of being explicitly programmed, machine learning models improve their performance through experience with data. Common types include supervised learning, unsupervised learning, and reinforcement learning.",
            "metadata": {"topic": "Machine Learning", "level": "beginner", "original_id": "machine_learning_1"}
        },
        {
            "id": str(uuid.uuid4()),
            "content": "Robotics is an interdisciplinary field that combines mechanical engineering, electrical engineering, and computer science to design, construct, and operate robots. Modern robots can perform complex tasks in manufacturing, healthcare, exploration, and service industries. They often incorporate AI to enable autonomous decision-making and adaptive behavior.",
            "metadata": {"topic": "Robotics", "level": "beginner", "original_id": "robotics_intro_1"}
        },
        {
            "id": str(uuid.uuid4()),
            "content": "Neural networks are computing systems inspired by the human brain's structure and function. They consist of interconnected nodes (neurons) organized in layers. Deep learning uses neural networks with multiple hidden layers to recognize patterns and make predictions. They are particularly effective for image recognition, natural language processing, and complex decision-making tasks.",
            "metadata": {"topic": "Neural Networks", "level": "intermediate", "original_id": "neural_networks_1"}
        },
        {
            "id": str(uuid.uuid4()),
            "content": "Natural Language Processing (NLP) is a field of AI focused on enabling computers to understand, interpret, and generate human language. NLP techniques are used in chatbots, translation services, sentiment analysis, and text summarization. Modern NLP systems often use transformer architectures and large language models.",
            "metadata": {"topic": "Natural Language Processing", "level": "intermediate", "original_id": "nlp_fundamentals_1"}
        }
    ]

    print(f"Indexing {len(sample_content)} content items into collection '{collection_name}'...")

    for item in sample_content:
        rag_service.index_content(item["id"], item["content"], item["metadata"])
        print(f"Indexed: {item['id']} - {item['metadata']['topic']}")

    print(f"\nSuccessfully indexed {len(sample_content)} items into '{collection_name}' collection!")
    print("Your RAG system is now ready to answer questions about AI, Machine Learning, Robotics, Neural Networks, and NLP.")

if __name__ == "__main__":
    setup_sample_content()