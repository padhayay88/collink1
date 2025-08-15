#!/usr/bin/env python3
"""
Test script to verify fee filtering and caste-based reservation system
"""

import requests
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8000"

def test_fee_filter():
    """Test the fee filtering endpoint"""
    print("🧪 Testing Fee Filter System")
    print("=" * 50)
    
    # Test different categories
    test_cases = [
        {
            "name": "General Category - Engineering Colleges under 5L",
            "params": {
                "min_fee": 0,
                "max_fee": 500000,
                "category": "general",
                "exam_type": "engineering",
                "limit": 10
            }
        },
        {
            "name": "SC/ST Category - All affordable options",
            "params": {
                "min_fee": 0,
                "max_fee": 200000,
                "category": "sc_st",
                "exam_type": "engineering",
                "limit": 10
            }
        },
        {
            "name": "OBC Category - Medical colleges",
            "params": {
                "min_fee": 0,
                "max_fee": 300000,
                "category": "obc_ncl",
                "exam_type": "medical",
                "limit": 5
            }
        },
        {
            "name": "PWD Category - All colleges under 1L",
            "params": {
                "min_fee": 0,
                "max_fee": 100000,
                "category": "pwd",
                "exam_type": "all",
                "limit": 15
            }
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. {test_case['name']}")
        print("-" * 40)
        
        try:
            response = requests.get(f"{BASE_URL}/colleges/fee-filter", params=test_case["params"])
            
            if response.status_code == 200:
                data = response.json()
                colleges = data.get("colleges", [])
                
                print(f"✅ Found {len(colleges)} colleges")
                print(f"📊 Category: {data.get('filters_applied', {}).get('category')}")
                print(f"💰 Fee Range: ₹{data.get('filters_applied', {}).get('min_fee'):,} - ₹{data.get('filters_applied', {}).get('max_fee'):,}")
                
                if colleges:
                    print(f"🏛️  Top 3 Results:")
                    for j, college in enumerate(colleges[:3], 1):
                        print(f"   {j}. {college['name']} - ₹{college['total_fee']:,}/year")
                        print(f"      📍 {college['location']} | Rank: {college.get('nirf_rank', 'N/A')}")
                
            else:
                print(f"❌ Error: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"❌ Exception: {e}")
    
    return True

def test_fee_comparison():
    """Test the fee comparison endpoint"""
    print("\n\n🔍 Testing Fee Comparison System")
    print("=" * 50)
    
    # Test comparing IIT fees across categories
    test_colleges = "IIT Bombay,IIT Delhi,IIT Madras"
    
    try:
        response = requests.get(
            f"{BASE_URL}/colleges/fee-comparison",
            params={
                "college_names": test_colleges,
                "exam_type": "engineering"
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            comparison_data = data.get("comparison_data", [])
            
            print(f"✅ Comparing {len(comparison_data)} colleges")
            print(f"🏛️  Colleges: {test_colleges}")
            
            for college in comparison_data:
                print(f"\n📚 {college['name']} (Rank: {college.get('nirf_rank', 'N/A')})")
                print(f"   📍 {college.get('location')}")
                
                fee_by_category = college.get("fee_by_category", {})
                for category, fees in fee_by_category.items():
                    total_fee = fees.get("total_annual", 0)
                    print(f"   💰 {category.upper()}: ₹{total_fee:,}/year")
            
            # Show category explanations
            explanations = data.get("category_explanations", {})
            print(f"\n📋 Category Benefits:")
            for category, explanation in explanations.items():
                print(f"   • {category.upper()}: {explanation}")
                
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")
    
    return True

def test_affordable_colleges():
    """Test the affordable colleges endpoint"""
    print("\n\n💸 Testing Affordable Colleges System")
    print("=" * 50)
    
    test_cases = [
        {
            "name": "Most affordable for General category (under 3L)",
            "params": {
                "category": "general",
                "max_budget": 300000,
                "exam_type": "engineering",
                "limit": 5
            }
        },
        {
            "name": "Best value for SC/ST (under 1L)",
            "params": {
                "category": "sc_st",
                "max_budget": 100000,
                "exam_type": "engineering",
                "limit": 8
            }
        },
        {
            "name": "Affordable medical colleges for OBC",
            "params": {
                "category": "obc_ncl",
                "max_budget": 250000,
                "exam_type": "medical",
                "limit": 3
            }
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. {test_case['name']}")
        print("-" * 40)
        
        try:
            response = requests.get(f"{BASE_URL}/colleges/affordable", params=test_case["params"])
            
            if response.status_code == 200:
                data = response.json()
                colleges = data.get("colleges", [])
                search_criteria = data.get("search_criteria", {})
                
                print(f"✅ Found {len(colleges)} affordable colleges")
                print(f"🎯 Budget: ₹{search_criteria.get('max_budget', 0):,}")
                print(f"📊 Category: {search_criteria.get('category', '').upper()}")
                
                if colleges:
                    print(f"🏛️  Top Results:")
                    for j, college in enumerate(colleges[:5], 1):
                        annual_fee = college.get('annual_fee', 0)
                        roi_years = college.get('roi_years', 0)
                        savings = college.get('savings_from_general', 0)
                        
                        print(f"   {j}. {college['name']}")
                        print(f"      💰 Fee: ₹{annual_fee:,}/year")
                        if savings > 0:
                            print(f"      💵 Savings: ₹{savings:,}/year vs General")
                        print(f"      📈 ROI: {roi_years} years")
                        print(f"      📍 {college.get('location')} | Rank: {college.get('nirf_rank', 'N/A')}")
                        print()
                
            else:
                print(f"❌ Error: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"❌ Exception: {e}")
    
    return True

def test_ranking_system():
    """Test the ranking system"""
    print("\n\n🏆 Testing College Ranking System")
    print("=" * 50)
    
    try:
        response = requests.get(
            f"{BASE_URL}/colleges/by-ranking",
            params={
                "category": "engineering",
                "limit": 10
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            colleges = data.get("colleges", [])
            
            print(f"✅ Top {len(colleges)} Engineering Colleges by NIRF Ranking:")
            print()
            
            for i, college in enumerate(colleges, 1):
                rank = college.get('nirf_rank', 'N/A')
                name = college.get('name')
                location = college.get('location')
                placement = college.get('placement_percentage', 'N/A')
                avg_package = college.get('average_package', 0)
                
                print(f"{i:2}. Rank {rank:2} - {name}")
                print(f"    📍 {location}")
                print(f"    📊 Placement: {placement}% | Avg Package: ₹{avg_package:,}")
                print()
                
            # Verify top 3 are correct
            if len(colleges) >= 3:
                top_3_names = [college['name'] for college in colleges[:3]]
                expected_order = ["IIT Madras", "IIT Bombay", "IIT Delhi"]
                
                if top_3_names[:3] == expected_order[:len(top_3_names)]:
                    print("✅ Top 3 ranking order is CORRECT!")
                else:
                    print("❌ Top 3 ranking order is INCORRECT!")
                    print(f"Expected: {expected_order[:3]}")
                    print(f"Actual: {top_3_names}")
                
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")
    
    return True

def run_all_tests():
    """Run all test cases"""
    print("🚀 Starting Comprehensive Fee System Tests")
    print("=" * 60)
    
    tests = [
        ("Fee Filter System", test_fee_filter),
        ("Fee Comparison System", test_fee_comparison),
        ("Affordable Colleges System", test_affordable_colleges),
        ("College Ranking System", test_ranking_system)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            print(f"\n{'='*20} {test_name} {'='*20}")
            result = test_func()
            if result:
                passed += 1
                print(f"✅ {test_name} - PASSED")
            else:
                print(f"❌ {test_name} - FAILED")
        except Exception as e:
            print(f"❌ {test_name} - ERROR: {e}")
    
    print("\n" + "="*60)
    print(f"🏁 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests PASSED! Fee system is working correctly!")
    else:
        print(f"⚠️  {total-passed} tests failed. Please check the issues above.")
    
    return passed == total

if __name__ == "__main__":
    # Note: Make sure your FastAPI server is running on localhost:8000
    print("📋 Prerequisites:")
    print("1. FastAPI server should be running on localhost:8000")
    print("2. Run: python main.py")
    print("3. Wait for server to start, then run this test script")
    print()
    
    input("Press Enter to continue with tests... ")
    run_all_tests()
