from utils.match_logic import CollegePredictor

def debug_prediction():
    p = CollegePredictor()
    
    # Test parameters
    exam = 'jee'
    rank = 150000
    category = 'General'
    gender = 'All'
    quota = 'All India'
    tolerance_percent = 0.0
    states = ['Maharashtra']
    
    print(f"Testing prediction with:")
    print(f"Exam: {exam}")
    print(f"Rank: {rank}")
    print(f"Category: {category}")
    print(f"Gender: {gender}")
    print(f"Quota: {quota}")
    print(f"Tolerance: {tolerance_percent}%")
    print(f"States: {states}")
    print()
    
    # Get Maharashtra records
    maharashtra_records = [r for r in p.cutoff_data[exam] if r.get('state') == 'Maharashtra']
    print(f"Total Maharashtra records: {len(maharashtra_records)}")
    
    # Check first few records
    print("\nFirst 5 Maharashtra records:")
    for i, record in enumerate(maharashtra_records[:5]):
        print(f"{i+1}. College: {record.get('college')}")
        print(f"   Branch: {record.get('branch')}")
        print(f"   Category: {record.get('category')}")
        print(f"   Quota: {record.get('quota')}")
        print(f"   Opening Rank: {record.get('opening_rank')}")
        print(f"   Closing Rank: {record.get('closing_rank')}")
        print(f"   State: {record.get('state')}")
        print()
    
    # Test rank eligibility for first record
    if maharashtra_records:
        first_record = maharashtra_records[0]
        print("Testing rank eligibility for first record:")
        print(f"College: {first_record.get('college')}")
        print(f"Closing Rank: {first_record.get('closing_rank')}")
        
        # Test the eligibility function
        is_eligible = p._is_rank_eligible(first_record, rank, category, gender, quota, tolerance_percent)
        print(f"Is eligible: {is_eligible}")
        
        # Check each condition
        print("\nChecking each condition:")
        print(f"Category match: {category.lower() == first_record.get('category', '').strip().lower()}")
        print(f"Quota match: {quota.lower() == first_record.get('quota', '').strip().lower()}")
        print(f"Gender match: {gender.lower() == first_record.get('gender', '').strip().lower()}")
        print(f"Rank check: {rank} <= {first_record.get('closing_rank')}")

if __name__ == "__main__":
    debug_prediction()
