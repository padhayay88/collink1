import time
import requests
import json

def test_api_performance():
    """Test the API performance with various queries"""
    base_url = "http://localhost:8000"
    
    print("🚀 Testing API Performance...")
    print("=" * 50)
    
    # Test 1: Data Status
    print("\n📊 Testing Data Status...")
    start_time = time.time()
    try:
        response = requests.get(f"{base_url}/api/v1/data-status")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Data Status: {json.dumps(data, indent=2)}")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 2: JEE Prediction (Rank 100000)
    print("\n🎯 Testing JEE Prediction (Rank 100000)...")
    start_time = time.time()
    try:
        payload = {
            "exam": "jee",
            "rank": 100000,
            "category": "General",
            "load_full_data": False
        }
        response = requests.post(f"{base_url}/api/v1/predict", json=payload)
        if response.status_code == 200:
            data = response.json()
            prediction_time = data.get("response_time", 0)
            results_count = len(data.get("predictions", []))
            data_source = data.get("data_source", "unknown")
            print(f"✅ JEE Prediction: {results_count} results in {prediction_time:.3f}s")
            print(f"   Data Source: {data_source}")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 3: NEET Prediction (Rank 20000)
    print("\n🏥 Testing NEET Prediction (Rank 20000)...")
    start_time = time.time()
    try:
        payload = {
            "exam": "neet",
            "rank": 20000,
            "category": "General",
            "load_full_data": False
        }
        response = requests.post(f"{base_url}/api/v1/predict", json=payload)
        if response.status_code == 200:
            data = response.json()
            prediction_time = data.get("response_time", 0)
            results_count = len(data.get("predictions", []))
            data_source = data.get("data_source", "unknown")
            print(f"✅ NEET Prediction: {results_count} results in {prediction_time:.3f}s")
            print(f"   Data Source: {data_source}")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 4: IELTS Prediction
    print("\n🌍 Testing IELTS Prediction (Score 7.0)...")
    start_time = time.time()
    try:
        payload = {
            "exam": "ielts",
            "rank": 7,
            "category": "General",
            "load_full_data": False
        }
        response = requests.post(f"{base_url}/api/v1/predict", json=payload)
        if response.status_code == 200:
            data = response.json()
            prediction_time = data.get("response_time", 0)
            results_count = len(data.get("predictions", []))
            data_source = data.get("data_source", "unknown")
            print(f"✅ IELTS Prediction: {results_count} results in {prediction_time:.3f}s")
            print(f"   Data Source: {data_source}")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 5: Performance Test Endpoint
    print("\n⚡ Testing Performance Test Endpoint...")
    start_time = time.time()
    try:
        response = requests.get(f"{base_url}/api/v1/performance-test")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Performance Test Results:")
            for test_name, test_data in data.get("performance_test", {}).items():
                print(f"   {test_name}: {test_data['results']} results in {test_data['time']:.3f}s")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Performance Testing Complete!")

if __name__ == "__main__":
    test_api_performance()
