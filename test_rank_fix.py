#!/usr/bin/env python3
"""
Test script to verify the rank eligibility fix
Tests if rank 50,000 now shows more than 5 colleges
"""

import requests
import json
import time

def test_rank_fix():
    """Test the rank eligibility fix with rank 50,000"""
    
    # Test data
    test_cases = [
        {"exam": "jee", "rank": 50000, "category": "General"},
        {"exam": "neet", "rank": 50000, "category": "General"},
        {"exam": "jee", "rank": 10000, "category": "General"},
        {"exam": "neet", "rank": 10000, "category": "General"},
    ]
    
    base_url = "http://localhost:8000"
    
    print("🧪 Testing Rank Eligibility Fix")
    print("=" * 50)
    
    for test_case in test_cases:
        print(f"\n📊 Testing {test_case['exam'].upper()} with rank {test_case['rank']}")
        
        try:
            # Make API request
            response = requests.post(
                f"{base_url}/predict",
                json={
                    "exam": test_case["exam"],
                    "rank": test_case["rank"],
                    "category": test_case["category"],
                    "limit": 1000  # Request up to 1000 results
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                predictions = data.get("predictions", [])
                
                print(f"✅ Status: Success")
                print(f"📈 Colleges found: {len(predictions)}")
                print(f"⏱️  Response time: {data.get('response_time', 0):.2f}s")
                
                if len(predictions) > 0:
                    print(f"🏫 Sample colleges:")
                    for i, pred in enumerate(predictions[:3]):  # Show first 3
                        college_name = pred.get('college', 'Unknown')
                        closing_rank = pred.get('closing_rank', 'N/A')
                        print(f"   {i+1}. {college_name} (Closing: {closing_rank})")
                
                # Check if the fix worked for rank 50,000
                if test_case["rank"] == 50000:
                    if len(predictions) > 5:
                        print(f"🎉 FIX SUCCESSFUL! Found {len(predictions)} colleges (previously only 5)")
                    else:
                        print(f"⚠️  Still showing only {len(predictions)} colleges - fix may need adjustment")
                        
            else:
                print(f"❌ Error: HTTP {response.status_code}")
                print(f"Response: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print(f"❌ Connection Error: Backend server not running on {base_url}")
        except requests.exceptions.Timeout:
            print(f"⏰ Timeout: Request took too long")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 Test completed!")

if __name__ == "__main__":
    test_rank_fix()
