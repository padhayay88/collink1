import json
import random
import os

# Create data directory if it doesn't exist
os.makedirs('data', exist_ok=True)

# Categories with rank multipliers
categories = {
    "General": 1.0,
    "OBC": 1.8,  # 80% higher ranks allowed
    "SC": 3.5,   # 250% higher ranks allowed
    "ST": 4.5    # 350% higher ranks allowed
}

# JEE Engineering Branches
jee_branches = [
    "Computer Science and Engineering",
    "Electronics and Communication Engineering", 
    "Mechanical Engineering",
    "Civil Engineering",
    "Electrical Engineering",
    "Information Technology",
    "Chemical Engineering",
    "Aerospace Engineering",
    "Biotechnology",
    "Artificial Intelligence",
    "Data Science",
    "Robotics Engineering",
    "Automobile Engineering",
    "Mining Engineering",
    "Metallurgical Engineering"
]

# NEET Medical Branches
neet_branches = [
    "MBBS",
    "BDS",
    "BAMS",
    "BHMS",
    "BPT",
    "BSc Nursing",
    "BSc Medical Technology",
    "BSc Radiology",
    "BSc Optometry",
    "BSc Physiotherapy"
]

# IELTS International Programs
ielts_programs = [
    "Computer Science",
    "Engineering",
    "Business Administration",
    "Data Science",
    "Artificial Intelligence",
    "Cybersecurity",
    "Biotechnology",
    "Environmental Science",
    "Psychology",
    "Economics"
]

# Indian States and Union Territories
states = [
    "Andhra Pradesh", "Telangana", "Karnataka", "Tamil Nadu", "Kerala",
    "Maharashtra", "Gujarat", "Rajasthan", "Madhya Pradesh", "Uttar Pradesh",
    "Bihar", "Jharkhand", "West Bengal", "Odisha", "Chhattisgarh",
    "Haryana", "Punjab", "Himachal Pradesh", "Uttarakhand", "Delhi",
    "Assam", "Meghalaya", "Manipur", "Tripura", "Nagaland",
    "Mizoram", "Arunachal Pradesh", "Goa", "Jammu & Kashmir", "Ladakh",
    "Andaman & Nicobar", "Chandigarh", "Dadra & Nagar Haveli", "Daman & Diu",
    "Lakshadweep", "Puducherry"
]

# College types and naming patterns
college_types = {
    "government": [
        "Government Engineering College",
        "Government Medical College", 
        "Government Institute of Technology",
        "Government College of Engineering",
        "Government Medical Institute",
        "Government Polytechnic",
        "Government Institute of Medical Sciences"
    ],
    "private": [
        "Private Engineering Institute",
        "Private Medical College",
        "Private Institute of Technology", 
        "Private College of Engineering",
        "Private Medical Institute",
        "Private Polytechnic",
        "Private Institute of Medical Sciences"
    ],
    "deemed": [
        "Deemed University",
        "Deemed Institute of Technology",
        "Deemed Medical University",
        "Deemed Engineering University"
    ],
    "central": [
        "Indian Institute of Technology",
        "National Institute of Technology",
        "All India Institute of Medical Sciences",
        "Central Institute of Technology"
    ]
}

def generate_college_name(college_type, state, index):
    """Generate a unique college name"""
    if college_type == "central":
        if "Technology" in college_types["central"][0]:
            return f"IIT {chr(65 + (index - 1) % 26)}"
        elif "Medical" in college_types["central"][2]:
            return f"AIIMS {chr(65 + (index - 1) % 26)}"
        else:
            return f"NIT {chr(65 + (index - 1) % 26)}"
    else:
        base_name = random.choice(college_types[college_type])
        if state:
            return f"{base_name} {state} - {index}"
        else:
            return f"{base_name} {index}"

def generate_jee_colleges():
    """Generate 400 JEE engineering colleges with rank 100000"""
    colleges = []
    
    # Generate colleges for each state
    for state in states:
        # Government colleges (more prestigious, lower ranks)
        for i in range(1, 9):  # 8 government colleges per state
            base_rank = 50000 + (i * 5000)
            factor = base_rank + (i * 10000)
            colleges.append({
                "name": generate_college_name("government", state, i),
                "location": state,
                "base_rank": base_rank,
                "factor": min(factor, 200000),
                "type": "government"
            })
        
        # Private colleges (higher ranks, including rank 100000)
        for i in range(1, 17):  # 16 private colleges per state
            if i == 1:  # First private college gets rank 100000
                base_rank = 100000
                factor = 120000
            else:
                base_rank = 80000 + (i * 8000)
                factor = base_rank + (i * 15000)
            
            colleges.append({
                "name": generate_college_name("private", state, i),
                "location": state,
                "base_rank": base_rank,
                "factor": min(factor, 300000),
                "type": "private"
            })
        
        # Deemed universities (prestigious)
        for i in range(1, 3):  # 2 deemed universities per state
            base_rank = 30000 + (i * 15000)
            factor = base_rank + (i * 25000)
            colleges.append({
                "name": generate_college_name("deemed", state, i),
                "location": state,
                "base_rank": base_rank,
                "factor": min(factor, 150000),
                "type": "deemed"
            })
    
    # Add some central institutes
    for i in range(1, 21):
        colleges.append({
            "name": generate_college_name("central", None, i),
            "location": random.choice(states),
            "base_rank": 1000 + (i * 2000),
            "factor": 5000 + (i * 5000),
            "type": "central"
        })
    
    return colleges

def generate_neet_colleges():
    """Generate 400 NEET medical colleges with rank 20000"""
    colleges = []
    
    for state in states:
        # Government medical colleges (prestigious)
        for i in range(1, 9):  # 8 government medical colleges per state
            if i == 1:  # First government college gets rank 20000
                base_rank = 20000
                factor = 25000
            else:
                base_rank = 15000 + (i * 3000)
                factor = base_rank + (i * 5000)
            
            colleges.append({
                "name": f"Government Medical College {state} - {i}",
                "location": state,
                "base_rank": base_rank,
                "factor": min(factor, 80000),
                "type": "government"
            })
        
        # Private medical colleges
        for i in range(1, 17):  # 16 private medical colleges per state
            base_rank = 30000 + (i * 4000)
            factor = base_rank + (i * 8000)
            colleges.append({
                "name": f"Private Medical Institute {state} - {i}",
                "location": state,
                "base_rank": base_rank,
                "factor": min(factor, 120000),
                "type": "private"
            })
        
        # Medical universities
        for i in range(1, 3):  # 2 medical universities per state
            base_rank = 25000 + (i * 5000)
            factor = base_rank + (i * 10000)
            colleges.append({
                "name": f"Medical University {state} - {i}",
                "location": state,
                "base_rank": base_rank,
                "factor": min(factor, 100000),
                "type": "deemed"
            })
    
    return colleges

def generate_ielts_colleges():
    """Generate 200 international colleges"""
    colleges = []
    
    # UK Universities
    for i in range(50):
        colleges.append({
            "name": f"University of {random.choice(['London', 'Manchester', 'Birmingham', 'Leeds', 'Liverpool', 'Sheffield', 'Newcastle', 'Bristol', 'Glasgow', 'Edinburgh'])} - {i+1}",
            "location": "United Kingdom",
            "base_rank": 5000 + (i * 2000),
            "factor": 8000 + (i * 3000),
            "type": "international"
        })
    
    # US Universities
    for i in range(50):
        colleges.append({
            "name": f"{random.choice(['Harvard', 'MIT', 'Stanford', 'Yale', 'Princeton', 'Columbia', 'University of California', 'University of Michigan', 'University of Texas', 'University of Illinois'])} - {i+1}",
            "location": "United States",
            "base_rank": 1000 + (i * 1500),
            "factor": 3000 + (i * 2000),
            "type": "international"
        })
    
    # Australian Universities
    for i in range(50):
        colleges.append({
            "name": f"{random.choice(['University of Melbourne', 'University of Sydney', 'Australian National University', 'University of Queensland', 'Monash University', 'University of New South Wales', 'University of Western Australia', 'University of Adelaide'])} - {i+1}",
            "location": "Australia",
            "base_rank": 8000 + (i * 3000),
            "factor": 12000 + (i * 4000),
            "type": "international"
        })
    
    # Canadian Universities
    for i in range(50):
        colleges.append({
            "name": f"{random.choice(['University of Toronto', 'University of British Columbia', 'McGill University', 'University of Alberta', 'University of Waterloo', 'University of Montreal', 'University of Calgary', 'University of Ottawa'])} - {i+1}",
            "location": "Canada",
            "base_rank": 6000 + (i * 2500),
            "factor": 10000 + (i * 3500),
            "type": "international"
        })
    
    return colleges

def generate_cutoffs(colleges, branches, exam_type):
    """Generate cutoff data for colleges"""
    cutoffs = []
    
    for college in colleges:
        # Determine how many branches this college offers based on type
        if college["type"] == "government":
            num_branches = random.randint(5, len(branches))
        elif college["type"] == "deemed":
            num_branches = random.randint(8, len(branches))
        elif college["type"] == "central":
            num_branches = random.randint(10, len(branches))
        elif college["type"] == "private":
            num_branches = random.randint(3, 8)
        else:  # international
            num_branches = random.randint(1, 5)
        
        # Select random branches
        selected_branches = random.sample(branches, min(num_branches, len(branches)))
        
        for branch in selected_branches:
            for category, multiplier in categories.items():
                opening_rank = max(1, int(college["base_rank"] * multiplier))
                closing_rank = min(1000000, int(college["factor"] * multiplier))
                
                # Add some randomization
                opening_rank = max(1, opening_rank + random.randint(-500, 500))
                closing_rank = min(1000000, closing_rank + random.randint(-1000, 1000))
                
                if opening_rank >= closing_rank:
                    opening_rank = max(1, closing_rank - 1000)
                
                cutoffs.append({
                    "college": college["name"],
                    "branch": branch,
                    "category": category,
                    "quota": "All India",
                    "opening_rank": opening_rank,
                    "closing_rank": closing_rank,
                    "year": 2024,
                    "exam_type": exam_type,
                    "location": college["location"],
                    "college_type": college["type"]
                })
    
    return cutoffs

def main():
    print("🚀 Creating 1000 Colleges Database with JEE, NEET, and IELTS...")
    
    # Generate colleges
    print("📚 Generating JEE Engineering Colleges...")
    jee_colleges = generate_jee_colleges()
    print(f"✅ Generated {len(jee_colleges)} JEE colleges")
    
    print("🏥 Generating NEET Medical Colleges...")
    neet_colleges = generate_neet_colleges()
    print(f"✅ Generated {len(neet_colleges)} NEET colleges")
    
    print("🌍 Generating IELTS International Colleges...")
    ielts_colleges = generate_ielts_colleges()
    print(f"✅ Generated {len(ielts_colleges)} IELTS colleges")
    
    total_colleges = len(jee_colleges) + len(neet_colleges) + len(ielts_colleges)
    print(f"\n🎯 Total Colleges Generated: {total_colleges}")
    
    # Verify specific ranks
    jee_rank_100000 = [c for c in jee_colleges if c["base_rank"] == 100000]
    neet_rank_20000 = [c for c in neet_colleges if c["base_rank"] == 20000]
    
    print(f"🎯 JEE Colleges with rank 100000: {len(jee_rank_100000)}")
    print(f"🎯 NEET Colleges with rank 20000: {len(neet_rank_20000)}")
    
    # Generate cutoffs
    print("\n📊 Generating Cutoff Data...")
    jee_cutoffs = generate_cutoffs(jee_colleges, jee_branches, "jee")
    neet_cutoffs = generate_cutoffs(neet_colleges, neet_branches, "neet")
    ielts_cutoffs = generate_cutoffs(ielts_colleges, ielts_programs, "ielts")
    
    print(f"✅ JEE Cutoffs: {len(jee_cutoffs)} entries")
    print(f"✅ NEET Cutoffs: {len(neet_cutoffs)} entries")
    print(f"✅ IELTS Cutoffs: {len(ielts_cutoffs)} entries")
    
    total_cutoffs = len(jee_cutoffs) + len(neet_cutoffs) + len(ielts_cutoffs)
    print(f"🎯 Total Cutoff Entries: {total_cutoffs}")
    
    # Save data
    print("\n💾 Saving Data Files...")
    
    # Save JEE data
    with open('data/jee_1000_colleges.json', 'w', encoding='utf-8') as f:
        json.dump(jee_colleges, f, indent=2, ensure_ascii=False)
    
    with open('data/jee_1000_cutoffs.json', 'w', encoding='utf-8') as f:
        json.dump(jee_cutoffs, f, indent=2, ensure_ascii=False)
    
    # Save NEET data
    with open('data/neet_1000_colleges.json', 'w', encoding='utf-8') as f:
        json.dump(neet_colleges, f, indent=2, ensure_ascii=False)
    
    with open('data/neet_1000_cutoffs.json', 'w', encoding='utf-8') as f:
        json.dump(neet_cutoffs, f, indent=2, ensure_ascii=False)
    
    # Save IELTS data
    with open('data/ielts_1000_colleges.json', 'w', encoding='utf-8') as f:
        json.dump(ielts_colleges, f, indent=2, ensure_ascii=False)
    
    with open('data/ielts_1000_cutoffs.json', 'w', encoding='utf-8') as f:
        json.dump(ielts_cutoffs, f, indent=2, ensure_ascii=False)
    
    # Create summary file
    summary = {
        "total_colleges": total_colleges,
        "total_cutoffs": total_cutoffs,
        "breakdown": {
            "jee": {
                "colleges": len(jee_colleges),
                "cutoffs": len(jee_cutoffs),
                "branches": len(jee_branches),
                "rank_100000_colleges": len(jee_rank_100000)
            },
            "neet": {
                "colleges": len(neet_colleges),
                "cutoffs": len(neet_cutoffs),
                "branches": len(neet_branches),
                "rank_20000_colleges": len(neet_rank_20000)
            },
            "ielts": {
                "colleges": len(ielts_colleges),
                "cutoffs": len(ielts_cutoffs),
                "programs": len(ielts_programs)
            }
        },
        "categories": list(categories.keys()),
        "states": len(states),
        "generated_at": "2024",
        "special_ranks": {
            "jee_rank_100000": len(jee_rank_100000),
            "neet_rank_20000": len(neet_rank_20000)
        }
    }
    
    with open('data/1000_colleges_summary.json', 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print("\n🎉 **1000 COLLEGES DATABASE CREATED SUCCESSFULLY!** 🎉")
    print(f"📚 Total Colleges: {total_colleges:,}")
    print(f"📊 Total Cutoff Entries: {total_cutoffs:,}")
    print(f"🏛️  States Covered: {len(states)}")
    print(f"🎯 Categories: {', '.join(categories.keys())}")
    print(f"🎯 JEE Colleges with rank 100000: {len(jee_rank_100000)}")
    print(f"🎯 NEET Colleges with rank 20000: {len(neet_rank_20000)}")
    
    print("\n📁 Files Created:")
    print("  • data/jee_1000_colleges.json")
    print("  • data/jee_1000_cutoffs.json")
    print("  • data/neet_1000_colleges.json")
    print("  • data/neet_1000_cutoffs.json")
    print("  • data/ielts_1000_colleges.json")
    print("  • data/ielts_1000_cutoffs.json")
    print("  • data/1000_colleges_summary.json")
    
    print("\n🚀 Next Steps:")
    print("  1. Restart your FastAPI server")
    print("  2. Update your main.py to load these new files")
    print("  3. Test predictions with the expanded database")

if __name__ == "__main__":
    main()
