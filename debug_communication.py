#!/usr/bin/env python3
"""
Debug script to test the complete frontend-backend communication flow
This script will help identify where the communication might be failing
"""

import requests
import json
import time
from datetime import datetime

def test_complete_flow():
    print("🔍 Debugging Frontend-Backend Communication Flow")
    print("=" * 60)
    print(f"Test Run Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    base_url = "http://localhost:8001/api/chat"

    # Test 1: Verify API is accessible
    print("✅ Test 1: API Accessibility Check")
    try:
        response = requests.get("http://localhost:8001/health")
        if response.status_code == 200:
            print("   ✅ Backend health check: SUCCESS")
        else:
            print(f"   ❌ Backend health check: FAILED (Status: {response.status_code})")
    except Exception as e:
        print(f"   ❌ Backend health check: FAILED ({e})")
    print()

    # Test 2: Test RAG functionality with proper selected text
    print("✅ Test 2: RAG Functionality Test")
    payload = {
        "message": "What is Artificial Intelligence?",
        "selected_text": "Artificial Intelligence is a branch of computer science that aims to create software or machines that exhibit human-like intelligence."
    }

    try:
        response = requests.post(base_url, json=payload, headers={"Content-Type": "application/json"})
        result = response.json()

        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {result.get('answer', 'No answer field')[:100]}...")

        if response.status_code == 200 and 'answer' in result:
            print("   ✅ RAG functionality: SUCCESS")
        else:
            print("   ❌ RAG functionality: FAILED")
    except Exception as e:
        print(f"   ❌ RAG functionality: FAILED ({e})")
    print()

    # Test 3: Test fallback mechanism
    print("✅ Test 3: Fallback Mechanism Test")
    fallback_payload = {
        "message": "What is Quantum Computing?",
        "selected_text": "This is completely unrelated text that should not match anything in the database."
    }

    try:
        response = requests.post(base_url, json=fallback_payload, headers={"Content-Type": "application/json"})
        result = response.json()

        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {result.get('answer', 'No answer field')}")

        if result.get('answer') == "Is sawal ka jawab provided data me mojood nahi hai.":
            print("   ✅ Fallback mechanism: SUCCESS")
        else:
            print("   ❌ Fallback mechanism: FAILED - Wrong response")
    except Exception as e:
        print(f"   ❌ Fallback mechanism: FAILED ({e})")
    print()

    # Test 4: Test with formatted input (as frontend would send)
    print("✅ Test 4: Frontend-Style Payload Test")
    frontend_style_payload = {
        "message": 'Selected text:\n"Artificial Intelligence is a branch of computer science that aims to create software or machines that exhibit human-like intelligence."\n\nAsk a question about this text...What is AI?',
        "selected_text": "Artificial Intelligence is a branch of computer science that aims to create software or machines that exhibit human-like intelligence."
    }

    try:
        response = requests.post(base_url, json=frontend_style_payload, headers={"Content-Type": "application/json"})
        result = response.json()

        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {result.get('answer', 'No answer field')[:100]}...")

        if response.status_code == 200 and 'answer' in result:
            print("   ✅ Frontend-style payload: SUCCESS")
        else:
            print("   ❌ Frontend-style payload: FAILED")
    except Exception as e:
        print(f"   ❌ Frontend-style payload: FAILED ({e})")
    print()

    # Test 5: Check backend logs for recent activity
    print("✅ Test 5: Recent Backend Activity Check")
    print("   [Check the terminal where the backend is running for recent POST requests]")
    print("   [Look for lines like: 'INFO: 127.0.0.1:XXXXX - \"POST /api/chat HTTP/1.1\" 200 OK']")
    print()

    print("=" * 60)
    print("📋 DEBUGGING SUMMARY:")
    print("• Backend API: Should be accessible on http://localhost:8001")
    print("• RAG functionality: Should return context-based answers")
    print("• Fallback mechanism: Should return 'Is sawal ka jawab provided data me mojood nahi hai.'")
    print("• CORS: Should allow requests from frontend origins")
    print("• Environment: Should have valid OpenRouter API key configured")
    print()
    print("⚠️  If communication is still failing, check:")
    print("   1. Browser console for JavaScript errors")
    print("   2. Network tab for failed requests")
    print("   3. Backend server is running and accessible")
    print("   4. Text selection is working properly in the content area")
    print("   5. Input field is being populated correctly")
    print("=" * 60)

if __name__ == "__main__":
    test_complete_flow()