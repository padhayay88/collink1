#!/usr/bin/env python3
"""
Test script for comprehensive college database
"""
import json
import random

def test_database():
    """Test the comprehensive database"""
    try:
        # Load the database
        with open('comprehensive_college_database.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        colleges = data['colleges']
        metadata = data['metadata']
        
        print(f"✅ Database loaded successfully!")
        print(f"📊 Total colleges: {len(colleges)}")
        print(f"📅 Last updated: {metadata['last_updated']}")
        print(f"🎯 Coverage: {metadata['coverage']}")
        print(f"📝 Exams: {metadata['exams']}")
        print(f"🏆 Rank coverage: {metadata['rank_coverage']}")
        
        # Test different rank ranges
        test_ranks = [1, 1000, 10000, 50000, 100000, 150000, 200000]
        test_exams = ["JEE Main", "JEE Advanced", "NEET"]
        
        print("\n🧪 Testing rank predictions:")
        
        for exam in test_exams:
            print(f"\n📚 {exam}:")
            for rank in test_ranks:
                # Filter colleges for this exam and rank
                matching_colleges = [
                    college for college in colleges 
                    if college['exam'] == exam and college['cutoff'] >= rank
                ]
                
                if matching_colleges:
                    # Sort by cutoff rank
                    matching_colleges.sort(key=lambda x: x['cutoff'])
                    best_college = matching_colleges[0]
                    worst_college = matching_colleges[-1]
                    
                    print(f"  Rank {rank:,}: {len(matching_colleges)} colleges found")
                    print(f"    Best: {best_college['name']} (Cutoff: {best_college['cutoff']:,})")
                    print(f"    Worst: {worst_college['name']} (Cutoff: {worst_college['cutoff']:,})")
                else:
                    print(f"  Rank {rank:,}: No colleges found")
        
        # Test college types distribution
        print("\n📈 College type distribution:")
        type_counts = {}
        for college in colleges:
            college_type = college['type']
            type_counts[college_type] = type_counts.get(college_type, 0) + 1
        
        for college_type, count in sorted(type_counts.items()):
            percentage = (count / len(colleges)) * 100
            print(f"  {college_type}: {count} colleges ({percentage:.1f}%)")
        
        # Test state distribution
        print("\n🗺️ Top 10 states by college count:")
        state_counts = {}
        for college in colleges:
            state = college['state']
            state_counts[state] = state_counts.get(state, 0) + 1
        
        top_states = sorted(state_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        for state, count in top_states:
            percentage = (count / len(colleges)) * 100
            print(f"  {state}: {count} colleges ({percentage:.1f}%)")
        
        # Test cutoff rank distribution
        print("\n📊 Cutoff rank distribution:")
        cutoffs = [college['cutoff'] for college in colleges]
        cutoffs.sort()
        
        print(f"  Minimum cutoff: {min(cutoffs):,}")
        print(f"  Maximum cutoff: {max(cutoffs):,}")
        print(f"  Median cutoff: {cutoffs[len(cutoffs)//2]:,}")
        print(f"  Average cutoff: {sum(cutoffs)//len(cutoffs):,}")
        
        # Test large rank scenarios
        print("\n🔍 Testing large rank scenarios:")
        large_ranks = [50000, 100000, 150000, 200000]
        
        for rank in large_ranks:
            print(f"\n  For rank {rank:,}:")
            for exam in test_exams:
                matching_colleges = [
                    college for college in colleges 
                    if college['exam'] == exam and college['cutoff'] >= rank
                ]
                print(f"    {exam}: {len(matching_colleges)} colleges")
        
        print("\n✅ All tests completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing database: {e}")
        return False

if __name__ == "__main__":
    test_database()
