import json
from pathlib import Path

def test_massive_data():
    data_path = Path("data")
    
    # Test JEE massive data
    print("=== Testing JEE Massive Data ===")
    jee_file = data_path / "jee_massive_cutoffs.json"
    
    if jee_file.exists():
        with open(jee_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            print(f"Total records in file: {len(data)}")
            
            # Check first few records
            print("\nFirst 3 records:")
            for i, record in enumerate(data[:3]):
                print(f"Record {i+1}: {record}")
            
            # Check for different states
            states = set()
            for record in data[:1000]:
                if record.get('state'):
                    states.add(record['state'])
            
            print(f"\nStates found in first 1000 records: {sorted(list(states))}")
            
            # Check for Maharashtra specifically
            maharashtra_count = 0
            for record in data[:10000]:  # Check first 10k records
                if record.get('state') == 'Maharashtra':
                    maharashtra_count += 1
                    if maharashtra_count <= 3:
                        print(f"Maharashtra record {maharashtra_count}: {record}")
            
            print(f"\nTotal Maharashtra records in first 10k: {maharashtra_count}")
            
            # Check if there are any records with rank > 200000
            high_rank_count = 0
            for record in data[:10000]:
                rank = record.get('rank') or record.get('closing_rank')
                if rank and rank > 200000:
                    high_rank_count += 1
            
            print(f"Records with rank > 200000 in first 10k: {high_rank_count}")

if __name__ == "__main__":
    test_massive_data()
