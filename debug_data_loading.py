#!/usr/bin/env python3
"""
Debug script to check data loading and basic functionality
"""

import os
import json
from pathlib import Path

def debug_data_loading():
    """Debug data loading issues"""
    
    print("🔍 Debugging Data Loading")
    print("=" * 40)
    
    data_path = Path("data")
    
    # Check if data directory exists
    if not data_path.exists():
        print("❌ Data directory not found!")
        return
    
    print(f"✅ Data directory found: {data_path.absolute()}")
    
    # Check for massive data files
    massive_files = [
        "jee_massive_cutoffs.json",
        "neet_massive_cutoffs.json", 
        "ielts_massive_cutoffs.json",
        "jee_comprehensive_cutoffs.json",
        "neet_comprehensive_cutoffs.json",
        "jee_10000_cutoffs.json",
        "neet_10000_cutoffs.json",
        "ielts_10000_cutoffs.json"
    ]
    
    print(f"\n📁 Checking for data files:")
    
    total_records = 0
    available_files = []
    
    for filename in massive_files:
        file_path = data_path / filename
        if file_path.exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    record_count = len(data)
                    total_records += record_count
                    available_files.append(filename)
                    print(f"   ✅ {filename}: {record_count:,} records ({file_path.stat().st_size / 1024 / 1024:.1f} MB)")
            except Exception as e:
                print(f"   ❌ {filename}: Error loading - {e}")
        else:
            print(f"   ⚠️  {filename}: Not found")
    
    print(f"\n📊 Summary:")
    print(f"   Available files: {len(available_files)}")
    print(f"   Total records: {total_records:,}")
    
    if total_records == 0:
        print(f"\n❌ No data loaded! This explains why only 2-3 colleges are showing.")
        print(f"🔧 Need to check data file locations and formats.")
        
        # List all files in data directory
        print(f"\n📂 All files in data directory:")
        for file in data_path.iterdir():
            if file.is_file():
                size_mb = file.stat().st_size / 1024 / 1024
                print(f"   {file.name} ({size_mb:.1f} MB)")
    
    else:
        print(f"\n✅ Data files found! Testing basic prediction logic...")
        
        # Test basic prediction logic
        try:
            from utils.match_logic_optimized import CollegePredictorOptimized
            
            print(f"🚀 Initializing predictor...")
            predictor = CollegePredictorOptimized(load_essential_only=True)
            
            # Test with a simple case
            print(f"🧪 Testing JEE rank 10000...")
            predictions = predictor.predict_colleges(
                exam="jee",
                rank=10000,
                category="General",
                limit=100
            )
            
            print(f"📊 Result: {len(predictions)} colleges found")
            
            if len(predictions) > 0:
                print(f"✅ Prediction logic working!")
                for i, pred in enumerate(predictions[:3]):
                    college = pred.get('college', 'Unknown')
                    closing_rank = pred.get('closing_rank', 'N/A')
                    print(f"   {i+1}. {college} (Closing: {closing_rank})")
            else:
                print(f"❌ No predictions returned - logic issue!")
                
        except Exception as e:
            print(f"❌ Error testing prediction logic: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    debug_data_loading()
