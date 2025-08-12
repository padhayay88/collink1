#!/usr/bin/env python3
"""
Test script to verify that college rankings have been fixed
"""

import json
import sys
from pathlib import Path

def test_ranking_fix():
    """Test if the college ranking issue has been fixed"""
    
    print("Testing college ranking fix...")
    print("=" * 50)
    
    # Test both files
    files_to_test = [
        "data/college_info.json",
        "data/college_info_enhanced.json"
    ]
    
    for file_path in files_to_test:
        print(f"\nTesting {file_path}:")
        
        if not Path(file_path).exists():
            print(f"❌ File not found: {file_path}")
            continue
            
        with open(file_path, 'r', encoding='utf-8') as f:
            colleges = json.load(f)
        
        # Check IIT rankings
        iit_colleges = {}
        
        for college in colleges:
            name = college.get("name", "")
            if "IIT" in name and "NIRF" not in name:  # Skip non-IIT entries
                rank = college.get("nirf_rank")
                if rank is not None:
                    iit_colleges[name] = rank
        
        print(f"Found {len(iit_colleges)} IITs with NIRF ranks:")
        
        # Sort by rank
        sorted_iits = sorted(iit_colleges.items(), key=lambda x: x[1])
        
        for name, rank in sorted_iits:
            print(f"  {rank}. {name}")
        
        # Verify expected ranking order
        expected_order = ["IIT Madras", "IIT Bombay", "IIT Delhi"]
        actual_order = [name for name, rank in sorted_iits if name in expected_order]
        
        print(f"\nExpected top 3 order: {expected_order}")
        print(f"Actual top 3 order:   {actual_order}")
        
        if actual_order == expected_order:
            print("✅ Ranking order is CORRECT!")
        else:
            print("❌ Ranking order is INCORRECT!")
            
        # Check specific ranks
        checks = [
            ("IIT Madras", 1),
            ("IIT Bombay", 2), 
            ("IIT Delhi", 3)
        ]
        
        print("\nSpecific rank checks:")
        all_correct = True
        
        for expected_name, expected_rank in checks:
            actual_rank = iit_colleges.get(expected_name)
            if actual_rank == expected_rank:
                print(f"✅ {expected_name}: Rank {actual_rank} (correct)")
            else:
                print(f"❌ {expected_name}: Rank {actual_rank} (expected {expected_rank})")
                all_correct = False
        
        if all_correct:
            print(f"\n🎉 All rankings in {file_path} are FIXED!")
        else:
            print(f"\n❌ Some rankings in {file_path} are still incorrect!")

if __name__ == "__main__":
    test_ranking_fix()
