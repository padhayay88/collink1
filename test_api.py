#!/usr/bin/env python3
"""
Test script for Collink API
Tests all major endpoints to ensure they work correctly
"""

import requests
import json
import time
import subprocess
import atexit

BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test health check endpoint"""
    print("🔍 Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_get_exams():
    """Test get exams endpoint"""
    print("🔍 Testing get exams...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/exams")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Get exams passed: {len(data.get('exams', []))} exams found")
            return True
        else:
            print(f"❌ Get exams failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Get exams error: {e}")
        return False

def test_predict_colleges():
    """Test college prediction endpoint"""
    print("🔍 Testing college prediction...")
    try:
        payload = {
            "exam": "jee",
            "rank": 100,
            "category": "General",
            "gender": "All",
            "quota": "All India"
        }
        response = requests.post(f"{BASE_URL}/api/v1/predict", json=payload)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Prediction passed: {data.get('total_colleges', 0)} colleges found")
            return True
        else:
            print(f"❌ Prediction failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Prediction error: {e}")
        return False

def test_search_colleges():
    """Test college search endpoint"""
    print("🔍 Testing college search...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/search?query=IIT&limit=5")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Search passed: {data.get('total_found', 0)} results found")
            return True
        else:
            print(f"❌ Search failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Search error: {e}")
        return False

def test_get_college_details():
    """Test get college details endpoint"""
    print("🔍 Testing college details...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/college/IIT%20Bombay")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ College details passed: {data.get('name', 'Unknown')}")
            return True
        else:
            print(f"❌ College details failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ College details error: {e}")
        return False

def test_get_all_colleges():
    """Test get all colleges endpoint"""
    print("🔍 Testing get all colleges...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/colleges?limit=10")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Get all colleges passed: {data.get('total', 0)} colleges found")
            return True
        else:
            print(f"❌ Get all colleges failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Get all colleges error: {e}")
        return False

def test_search_suggestions():
    """Test search suggestions endpoint"""
    print("🔍 Testing search suggestions...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/search/suggestions?query=IIT&limit=3")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Search suggestions passed: {len(data.get('suggestions', []))} suggestions")
            return True
        else:
            print(f"❌ Search suggestions failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Search suggestions error: {e}")
        return False

def test_popular_colleges():
    """Test popular colleges endpoint"""
    print("🔍 Testing popular colleges...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/search/popular?limit=5")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Popular colleges passed: {data.get('total', 0)} colleges found")
            return True
        else:
            print(f"❌ Popular colleges failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Popular colleges error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Collink API Test Suite")
    print("=" * 50)
    
    print("🚀 Starting API server...")
    server_process = subprocess.Popen(["python", "main.py"])
    atexit.register(server_process.terminate)

    # Wait for server to start
    print("⏳ Waiting for server to start...")
    time.sleep(3)
    
    tests = [
        test_health_check,
        test_get_exams,
        test_predict_colleges,
        test_search_colleges,
        test_get_college_details,
        test_get_all_colleges,
        test_search_suggestions,
        test_popular_colleges
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test error: {e}")
        print()
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! API is working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the API implementation.")
    
    print("\n📝 API Documentation available at:")
    print(f"   Swagger UI: {BASE_URL}/docs")
    print(f"   ReDoc: {BASE_URL}/redoc")

if __name__ == "__main__":
    main() 