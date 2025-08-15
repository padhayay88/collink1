import json

# Quick test to verify data structure and fix
data_file = "data/jee_massive_cutoffs.json"

print("Testing data access...")
try:
    with open(data_file, 'r') as f:
        data = json.load(f)
    
    print(f"Loaded {len(data)} records")
    
    # Show first few records
    for i, record in enumerate(data[:3]):
        print(f"Record {i+1}:")
        for key, value in record.items():
            print(f"  {key}: {value}")
        print()
    
    # Test filtering for rank 50000
    test_rank = 50000
    eligible = [r for r in data if r.get("rank", 0) >= test_rank]
    print(f"Colleges eligible for rank {test_rank}: {len(eligible)}")
    
except Exception as e:
    print(f"Error: {e}")
