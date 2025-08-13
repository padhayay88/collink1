import json
from pathlib import Path

def test_data_structure():
    data_path = Path("data")
    
    # Test JEE data structure
    print("=== JEE Data Structure ===")
    jee_file = data_path / "jee_massive_cutoffs.json"
    if jee_file.exists():
        with open(jee_file, 'r', encoding='utf-8') as f:
            # Read first few records
            data = json.load(f)
            print(f"Total records: {len(data)}")
            if data:
                sample = data[0]
                print("Sample record keys:", list(sample.keys()))
                print("Sample record:", sample)
                
                # Check location field
                if 'location' in sample:
                    print(f"Location format: '{sample['location']}'")
                elif 'state' in sample:
                    print(f"State format: '{sample['state']}'")
                else:
                    print("No location/state field found")
    
    print("\n=== NEET Data Structure ===")
    neet_file = data_path / "neet_massive_cutoffs.json"
    if neet_file.exists():
        with open(neet_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            print(f"Total records: {len(data)}")
            if data:
                sample = data[0]
                print("Sample record keys:", list(sample.keys()))
                print("Sample record:", sample)
                
                if 'location' in sample:
                    print(f"Location format: '{sample['location']}'")
                elif 'state' in sample:
                    print(f"State format: '{sample['state']}'")
                else:
                    print("No location/state field found")

if __name__ == "__main__":
    test_data_structure()
