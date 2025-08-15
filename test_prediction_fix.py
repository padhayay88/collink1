#!/usr/bin/env python3

import sys
import os
sys.path.append(os.getcwd())

from utils.match_logic import CollegePredictor

def test_predictions():
    print("Testing college prediction system...")
    
    try:
        # Initialize predictor
        predictor = CollegePredictor()
        
        # Test with different ranks
        test_cases = [
            {"exam": "jee", "rank": 5000, "category": "General"},
            {"exam": "jee", "rank": 15000, "category": "General"},
            {"exam": "jee", "rank": 50000, "category": "General"},
        ]
        
        for test_case in test_cases:
            print(f"\n--- Testing with rank {test_case['rank']} ---")
            predictions = predictor.predict_colleges(
                exam=test_case["exam"],
                rank=test_case["rank"],
                category=test_case["category"]
            )
            
            print(f"Found {len(predictions)} predictions")
            
            # Show first 5 predictions
            for i, prediction in enumerate(predictions[:5]):
                college = prediction.get("college", "N/A")
                branch = prediction.get("branch", "N/A")
                closing_rank = prediction.get("closing_rank", "N/A")
                confidence = prediction.get("confidence_level", "N/A")
                
                print(f"{i+1}. {college} - {branch}")
                print(f"   Closing Rank: {closing_rank}, Confidence: {confidence}")
        
        print("\nTesting completed successfully!")
        
    except Exception as e:
        print(f"Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_predictions()
