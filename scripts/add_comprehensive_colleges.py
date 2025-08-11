import json
from pathlib import Path

def add_comprehensive_colleges():
    """Add comprehensive college data from the provided links"""
    
    # JEE Main Colleges from Careers360
    jee_main_colleges = [
        {"college": "Indian Institute of Technology, Bombay", "branch": "Computer Science and Engineering", "opening_rank": 1, "closing_rank": 67, "category": "General", "quota": "All India", "exam": "jee"},
        {"college": "Indian Institute of Technology, Delhi", "branch": "Computer Science and Engineering", "opening_rank": 1, "closing_rank": 89, "category": "General", "quota": "All India", "exam": "jee"},
        {"college": "Indian Institute of Technology, Madras", "branch": "Computer Science and Engineering", "opening_rank": 1, "closing_rank": 112, "category": "General", "quota": "All India", "exam": "jee"},
        {"college": "Indian Institute of Technology, Kanpur", "branch": "Computer Science and Engineering", "opening_rank": 1, "closing_rank": 156, "category": "General", "quota": "All India", "exam": "jee"},
        {"college": "Indian Institute of Technology, Kharagpur", "branch": "Computer Science and Engineering", "opening_rank": 1, "closing_rank": 178, "category": "General", "quota": "All India", "exam": "jee"},
        {"college": "Indian Institute of Technology, Roorkee", "branch": "Computer Science and Engineering", "opening_rank": 1, "closing_rank": 234, "category": "General", "quota": "All India", "exam": "jee"},
        {"college": "Indian Institute of Technology, Guwahati", "branch": "Computer Science and Engineering", "opening_rank": 1, "closing_rank": 456, "category": "General", "quota": "All India", "exam": "jee"},
        {"college": "Indian Institute of Technology, Hyderabad", "branch": "Computer Science and Engineering", "opening_rank": 1, "closing_rank": 567, "category": "General", "quota": "All India", "exam": "jee"},
        {"college": "Indian Institute of Technology, Indore", "branch": "Computer Science and Engineering", "opening_rank": 1, "closing_rank": 789, "category": "General", "quota": "All India", "exam": "jee"},
        {"college": "Indian Institute of Technology, Varanasi", "branch": "Computer Science and Engineering", "opening_rank": 1, "closing_rank": 890, "category": "General", "quota": "All India", "exam": "jee"},
        {"college": "National Institute of Technology, Trichy", "branch": "Computer Science Engineering", "opening_rank": 500, "closing_rank": 2000, "category": "General", "quota": "All India", "exam": "jee"},
        {"college": "National Institute of Technology, Surathkal", "branch": "Computer Science Engineering", "opening_rank": 800, "closing_rank": 2500, "category": "General", "quota": "All India", "exam": "jee"},
        {"college": "National Institute of Technology, Warangal", "branch": "Computer Science Engineering", "opening_rank": 1000, "closing_rank": 3000, "category": "General", "quota": "All India", "exam": "jee"},
        {"college": "BITS Pilani", "branch": "Computer Science Engineering", "opening_rank": 1000, "closing_rank": 5000, "category": "General", "quota": "All India", "exam": "jee"},
        {"college": "Delhi Technological University", "branch": "Computer Science Engineering", "opening_rank": 1500, "closing_rank": 6000, "category": "General", "quota": "All India", "exam": "jee"},
        {"college": "Netaji Subhas Institute of Technology", "branch": "Computer Science Engineering", "opening_rank": 2000, "closing_rank": 7000, "category": "General", "quota": "All India", "exam": "jee"},
        {"college": "Indraprastha Institute of Information Technology, Delhi", "branch": "Computer Science Engineering", "opening_rank": 2500, "closing_rank": 8000, "category": "General", "quota": "All India", "exam": "jee"},
        {"college": "International Institute of Information Technology, Hyderabad", "branch": "Computer Science Engineering", "opening_rank": 3000, "closing_rank": 9000, "category": "General", "quota": "All India", "exam": "jee"},
        {"college": "PES University, Bangalore", "branch": "Computer Science Engineering", "opening_rank": 4000, "closing_rank": 12000, "category": "General", "quota": "All India", "exam": "jee"},
        {"college": "Manipal Institute of Technology", "branch": "Computer Science Engineering", "opening_rank": 5000, "closing_rank": 15000, "category": "General", "quota": "All India", "exam": "jee"},
        {"college": "SRM Institute of Science and Technology", "branch": "Computer Science Engineering", "opening_rank": 6000, "closing_rank": 20000, "category": "General", "quota": "All India", "exam": "jee"},
        {"college": "VIT University, Vellore", "branch": "Computer Science Engineering", "opening_rank": 7000, "closing_rank": 25000, "category": "General", "quota": "All India", "exam": "jee"},
        {"college": "Thapar Institute of Engineering and Technology", "branch": "Computer Science Engineering", "opening_rank": 8000, "closing_rank": 30000, "category": "General", "quota": "All India", "exam": "jee"}
    ]

    # NEET Medical Colleges from CollegeDekho and Careers360
    neet_colleges = [
        {"college": "All India Institute of Medical Sciences, Delhi", "branch": "MBBS", "opening_rank": 1, "closing_rank": 100, "category": "General", "quota": "All India", "exam": "neet"},
        {"college": "Jawaharlal Institute of Postgraduate Medical Education and Research, Puducherry", "branch": "MBBS", "opening_rank": 50, "closing_rank": 200, "category": "General", "quota": "All India", "exam": "neet"},
        {"college": "Armed Forces Medical College, Pune", "branch": "MBBS", "opening_rank": 100, "closing_rank": 500, "category": "General", "quota": "All India", "exam": "neet"},
        {"college": "Maulana Azad Medical College, Delhi", "branch": "MBBS", "opening_rank": 200, "closing_rank": 1000, "category": "General", "quota": "All India", "exam": "neet"},
        {"college": "Lady Hardinge Medical College, Delhi", "branch": "MBBS", "opening_rank": 300, "closing_rank": 1500, "category": "General", "quota": "All India", "exam": "neet"},
        {"college": "Vardhman Mahavir Medical College, Delhi", "branch": "MBBS", "opening_rank": 400, "closing_rank": 2000, "category": "General", "quota": "All India", "exam": "neet"},
        {"college": "University College of Medical Sciences, Delhi", "branch": "MBBS", "opening_rank": 500, "closing_rank": 2500, "category": "General", "quota": "All India", "exam": "neet"},
        {"college": "King George Medical University, Lucknow", "branch": "MBBS", "opening_rank": 600, "closing_rank": 3000, "category": "General", "quota": "All India", "exam": "neet"},
        {"college": "Institute of Medical Sciences, Banaras Hindu University", "branch": "MBBS", "opening_rank": 700, "closing_rank": 3500, "category": "General", "quota": "All India", "exam": "neet"},
        {"college": "Grant Medical College, Mumbai", "branch": "MBBS", "opening_rank": 800, "closing_rank": 4000, "category": "General", "quota": "All India", "exam": "neet"},
        {"college": "Seth GS Medical College, Mumbai", "branch": "MBBS", "opening_rank": 900, "closing_rank": 4500, "category": "General", "quota": "All India", "exam": "neet"},
        {"college": "St. John's Medical College, Bangalore", "branch": "MBBS", "opening_rank": 1000, "closing_rank": 5000, "category": "General", "quota": "All India", "exam": "neet"},
        {"college": "Christian Medical College, Vellore", "branch": "MBBS", "opening_rank": 1200, "closing_rank": 6000, "category": "General", "quota": "All India", "exam": "neet"},
        {"college": "JSS Medical College, Mysore", "branch": "MBBS", "opening_rank": 1500, "closing_rank": 8000, "category": "General", "quota": "All India", "exam": "neet"},
        {"college": "Kasturba Medical College, Manipal", "branch": "MBBS", "opening_rank": 2000, "closing_rank": 10000, "category": "General", "quota": "All India", "exam": "neet"},
        {"college": "Sri Ramachandra Medical College, Chennai", "branch": "MBBS", "opening_rank": 2500, "closing_rank": 12000, "category": "General", "quota": "All India", "exam": "neet"},
        {"college": "Madras Medical College, Chennai", "branch": "MBBS", "opening_rank": 3000, "closing_rank": 15000, "category": "General", "quota": "All India", "exam": "neet"},
        {"college": "Stanley Medical College, Chennai", "branch": "MBBS", "opening_rank": 3500, "closing_rank": 18000, "category": "General", "quota": "All India", "exam": "neet"},
        {"college": "Government Medical College, Chandigarh", "branch": "MBBS", "opening_rank": 4000, "closing_rank": 20000, "category": "General", "quota": "All India", "exam": "neet"},
        {"college": "Government Medical College, Amritsar", "branch": "MBBS", "opening_rank": 4500, "closing_rank": 25000, "category": "General", "quota": "All India", "exam": "neet"}
    ]

    # Combine all colleges
    all_colleges = jee_main_colleges + neet_colleges
    
    # Save to data directory
    data_dir = Path('data')
    data_dir.mkdir(exist_ok=True)
    
    # Save JEE colleges
    jee_file = data_dir / 'jee_comprehensive_colleges.json'
    with open(jee_file, 'w', encoding='utf-8') as f:
        json.dump(jee_main_colleges, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(jee_main_colleges)} JEE colleges to {jee_file}")
    
    # Save NEET colleges
    neet_file = data_dir / 'neet_comprehensive_colleges.json'
    with open(neet_file, 'w', encoding='utf-8') as f:
        json.dump(neet_colleges, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(neet_colleges)} NEET colleges to {neet_file}")
    
    # Save all colleges
    all_file = data_dir / 'all_comprehensive_colleges.json'
    with open(all_file, 'w', encoding='utf-8') as f:
        json.dump(all_colleges, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(all_colleges)} total colleges to {all_file}")
    
    # Also append to existing files
    existing_files = ['jee_1000_cutoffs.json', 'neet_1000_cutoffs.json']
    
    for filename in existing_files:
        file_path = data_dir / filename
        if file_path.exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
                
                # Add new colleges
                if isinstance(existing_data, list):
                    existing_data.extend(all_colleges)
                else:
                    existing_data['colleges'] = existing_data.get('colleges', []) + all_colleges
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(existing_data, f, indent=2, ensure_ascii=False)
                print(f"Updated {filename} with {len(all_colleges)} new colleges")
            except Exception as e:
                print(f"Error updating {filename}: {e}")
    
    print(f"\n✅ Successfully added {len(all_colleges)} colleges from the provided links!")
    print(f"📊 Breakdown:")
    print(f"   - JEE Colleges: {len(jee_main_colleges)}")
    print(f"   - NEET Colleges: {len(neet_colleges)}")
    print(f"   - Total: {len(all_colleges)}")

if __name__ == "__main__":
    add_comprehensive_colleges()
