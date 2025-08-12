#!/usr/bin/env python3
"""
Final test to verify the college filtering fix works
Simple direct test without complex imports
"""

import json
import os
from pathlib import Path

def test_data_access():
    """Test direct data access and basic filtering"""
    
    print("🧪 Testing Final Fix - Data Access & Filtering")
    print("=" * 50)
    
    data_path = Path("data")
    
    # Test loading massive JEE data
    jee_file = data_path / "jee_massive_cutoffs.json"
    
    if not jee_file.exists():
        print(f"❌ JEE massive file not found: {jee_file}")
        return
    
    print(f"📁 Loading JEE massive data...")
    
    try:
        with open(jee_file, 'r', encoding='utf-8') as f:
            jee_data = json.load(f)
        
        print(f"✅ Loaded {len(jee_data):,} JEE records")
        
        # Test filtering for rank 50,000
        test_rank = 50000
        eligible_colleges = []
        
        print(f"\n🔍 Testing rank {test_rank:,} eligibility...")
        
        for record in jee_data[:1000]:  # Test first 1000 records for speed
            rank_value = record.get("rank", 0)
            college_name = record.get("college_name", "Unknown")
            category = record.get("category", "General")
            
            # Simple eligibility: user rank <= cutoff rank
            if rank_value > 0 and test_rank <= rank_value:
                eligible_colleges.append({
                    "college": college_name,
                    "cutoff_rank": rank_value,
                    "category": category,
                    "branch": record.get("branch", "Unknown")
                })
        
        print(f"📊 Found {len(eligible_colleges)} eligible colleges (from first 1000 records)")
        
        if len(eligible_colleges) > 0:
            print(f"🎉 SUCCESS! Fix is working - showing multiple colleges")
            print(f"\n📚 Sample eligible colleges:")
            for i, college in enumerate(eligible_colleges[:5]):
                print(f"   {i+1}. {college['college']} - {college['branch']}")
                print(f"      Category: {college['category']}, Cutoff: {college['cutoff_rank']:,}")
        else:
            print(f"❌ Still no eligible colleges found - need further debugging")
        
        # Test with lower rank
        test_rank_low = 10000
        eligible_low = []
        
        for record in jee_data[:1000]:
            rank_value = record.get("rank", 0)
            if rank_value > 0 and test_rank_low <= rank_value:
                eligible_low.append(record)
        
        print(f"\n🔍 Rank {test_rank_low:,} eligibility: {len(eligible_low)} colleges")
        
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        import traceback
        traceback.print_exc()

def test_backend_prediction():
    """Test the actual backend prediction logic"""
    
    print(f"\n🚀 Testing Backend Prediction Logic...")
    
    try:
        # Import and test the fixed logic
        import sys
        sys.path.append('.')
        
        from utils.match_logic_optimized import CollegePredictorOptimized
        
        print(f"📚 Initializing predictor...")
        predictor = CollegePredictorOptimized(load_essential_only=True)
        
        # Test with rank 50,000
        print(f"🧪 Testing JEE rank 50,000...")
        predictions = predictor.predict_colleges(
            exam="jee",
            rank=50000,
            category="General",
            limit=500
        )
        
        print(f"📊 Backend returned: {len(predictions)} colleges")
        
        if len(predictions) > 10:
            print(f"🎉 BACKEND FIX SUCCESS! Now showing {len(predictions)} colleges")
            print(f"\n📚 Sample predictions:")
            for i, pred in enumerate(predictions[:3]):
                college = pred.get('college', 'Unknown')
                closing_rank = pred.get('closing_rank', pred.get('rank', 'N/A'))
                branch = pred.get('branch', 'Unknown')
                print(f"   {i+1}. {college} - {branch} (Cutoff: {closing_rank})")
        else:
            print(f"⚠️ Still limited results: {len(predictions)} colleges")
            
    except Exception as e:
        print(f"❌ Backend test error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_data_access()
    test_backend_prediction()
