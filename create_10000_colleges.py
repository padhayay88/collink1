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
        "Central Institute of Technology",
        "Central Medical Institute",
        "Central Engineering Institute",
        "Central University"
    ]
}

# International universities
international_universities = [
    "University of Oxford", "University of Cambridge", "Imperial College London",
    "University College London", "London School of Economics", "King's College London",
    "University of Edinburgh", "University of Manchester", "University of Bristol",
    "University of Warwick", "University of Glasgow", "University of Birmingham",
    "University of Leeds", "University of Sheffield", "University of Nottingham",
    "University of Southampton", "University of York", "University of Liverpool",
    "University of Newcastle", "University of Durham", "University of Exeter",
    "University of Reading", "University of Surrey", "University of Sussex",
    "University of Kent", "University of Essex", "University of Lancaster",
    "University of Bath", "University of St Andrews", "University of Aberdeen",
    "University of Dundee", "University of Stirling", "University of Strathclyde",
    "University of Heriot-Watt", "University of Glasgow Caledonian",
    "University of Abertay Dundee", "University of the West of Scotland",
    "University of the Highlands and Islands", "University of the West of England",
    "University of Plymouth", "University of Portsmouth", "University of Brighton",
    "University of Chichester", "University of Winchester", "University of Southampton Solent",
    "University of Bournemouth", "University of Bath Spa", "University of Gloucestershire",
    "University of Worcester", "University of Herefordshire", "University of Buckingham",
    "University of Bedfordshire", "University of Hertfordshire", "University of East Anglia",
    "University of Essex", "University of Kent", "University of Sussex", "University of Brighton",
    "University of Portsmouth", "University of Southampton", "University of Winchester",
    "University of Chichester", "University of Bournemouth", "University of Bath Spa",
    "University of Gloucestershire", "University of Worcester", "University of Herefordshire",
    "University of Buckingham", "University of Bedfordshire", "University of Hertfordshire"
]

def generate_college_name(college_type, state, index):
    """Generate realistic college names"""
    if college_type == "international":
        return random.choice(international_universities)
    
    base_name = random.choice(college_types[college_type])
    if state:
        return f"{base_name} {state} - {index}"
    else:
        return f"{base_name} - {index}"

def generate_jee_colleges():
    """Generate 6,000 JEE engineering colleges"""
    colleges = []
    
    # Generate colleges for each state
    for state in states:
        # Government colleges (more prestigious, lower ranks)
        for i in range(1, 51):  # 50 government colleges per state
            base_rank = 1000 + (i * 2000)
            factor = base_rank + (i * 5000)
            colleges.append({
                "name": generate_college_name("government", state, i),
                "location": state,
                "base_rank": base_rank,
                "factor": min(factor, 800000),
                "type": "government"
            })
        
        # Private colleges (higher ranks)
        for i in range(1, 101):  # 100 private colleges per state
            base_rank = 50000 + (i * 8000)
            factor = base_rank + (i * 15000)
            colleges.append({
                "name": generate_college_name("private", state, i),
                "location": state,
                "base_rank": base_rank,
                "factor": min(factor, 1000000),
                "type": "private"
            })
        
        # Deemed universities (prestigious)
        for i in range(1, 11):  # 10 deemed universities per state
            base_rank = 5000 + (i * 10000)
            factor = base_rank + (i * 20000)
            colleges.append({
                "name": generate_college_name("deemed", state, i),
                "location": state,
                "base_rank": base_rank,
                "factor": min(factor, 500000),
                "type": "deemed"
            })
    
    # Add some central institutes
    for i in range(1, 101):
        colleges.append({
            "name": generate_college_name("central", None, i),
            "location": random.choice(states),
            "base_rank": 100 + (i * 500),
            "factor": 1000 + (i * 2000),
            "type": "central"
        })
    
    return colleges

def generate_neet_colleges():
    """Generate 3,000 NEET medical colleges"""
    colleges = []
    
    for state in states:
        # Government medical colleges (prestigious)
        for i in range(1, 21):  # 20 government medical colleges per state
            base_rank = 100 + (i * 500)
            factor = base_rank + (i * 1000)
            colleges.append({
                "name": f"Government Medical College {state} - {i}",
                "location": state,
                "base_rank": base_rank,
                "factor": min(factor, 100000),
                "type": "government"
            })
        
        # Private medical colleges
        for i in range(1, 41):  # 40 private medical colleges per state
            base_rank = 5000 + (i * 2000)
            factor = base_rank + (i * 5000)
            colleges.append({
                "name": f"Private Medical Institute {state} - {i}",
                "location": state,
                "base_rank": base_rank,
                "factor": min(factor, 200000),
                "type": "private"
            })
        
        # Medical universities
        for i in range(1, 11):  # 10 medical universities per state
            base_rank = 1000 + (i * 3000)
            factor = base_rank + (i * 8000)
            colleges.append({
                "name": f"Medical University {state} - {i}",
                "location": state,
                "base_rank": base_rank,
                "factor": min(factor, 150000),
                "type": "deemed"
            })
    
    return colleges

def generate_ielts_colleges():
    """Generate 1,000 international colleges"""
    colleges = []
    
    # UK Universities
    for i in range(200):
        colleges.append({
            "name": f"UK University {i+1}",
            "location": "United Kingdom",
            "base_rank": 1 + (i * 10),
            "factor": 100 + (i * 50),
            "type": "international"
        })
    
    # US Universities
    for i in range(200):
        colleges.append({
            "name": f"US University {i+1}",
            "location": "United States",
            "base_rank": 1 + (i * 15),
            "factor": 150 + (i * 75),
            "type": "international"
        })
    
    # Australian Universities
    for i in range(150):
        colleges.append({
            "name": f"Australian University {i+1}",
            "location": "Australia",
            "base_rank": 1 + (i * 20),
            "factor": 200 + (i * 100),
            "type": "international"
        })
    
    # Canadian Universities
    for i in range(150):
        colleges.append({
            "name": f"Canadian University {i+1}",
            "location": "Canada",
            "base_rank": 1 + (i * 25),
            "factor": 250 + (i * 125),
            "type": "international"
        })
    
    # European Universities
    for i in range(150):
        colleges.append({
            "name": f"European University {i+1}",
            "location": "Europe",
            "base_rank": 1 + (i * 30),
            "factor": 300 + (i * 150),
            "type": "international"
        })
    
    # Asian Universities
    for i in range(150):
        colleges.append({
            "name": f"Asian University {i+1}",
            "location": "Asia",
            "base_rank": 1 + (i * 35),
            "factor": 350 + (i * 175),
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
                opening_rank = max(1, opening_rank + random.randint(-1000, 1000))
                closing_rank = min(1000000, closing_rank + random.randint(-2000, 2000))
                
                if opening_rank >= closing_rank:
                    opening_rank = max(1, closing_rank - 2000)
                
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
    print("🚀 Creating Massive College Database (10,000+ colleges)...")
    
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
    with open('data/jee_10000_colleges.json', 'w', encoding='utf-8') as f:
        json.dump(jee_colleges, f, indent=2, ensure_ascii=False)
    
    with open('data/jee_10000_cutoffs.json', 'w', encoding='utf-8') as f:
        json.dump(jee_cutoffs, f, indent=2, ensure_ascii=False)
    
    # Save NEET data
    with open('data/neet_10000_colleges.json', 'w', encoding='utf-8') as f:
        json.dump(neet_colleges, f, indent=2, ensure_ascii=False)
    
    with open('data/neet_10000_cutoffs.json', 'w', encoding='utf-8') as f:
        json.dump(neet_cutoffs, f, indent=2, ensure_ascii=False)
    
    # Save IELTS data
    with open('data/ielts_10000_colleges.json', 'w', encoding='utf-8') as f:
        json.dump(ielts_colleges, f, indent=2, ensure_ascii=False)
    
    with open('data/ielts_10000_cutoffs.json', 'w', encoding='utf-8') as f:
        json.dump(ielts_cutoffs, f, indent=2, ensure_ascii=False)
    
    # Create summary file
    summary = {
        "total_colleges": total_colleges,
        "total_cutoffs": total_cutoffs,
        "breakdown": {
            "jee": {
                "colleges": len(jee_colleges),
                "cutoffs": len(jee_cutoffs),
                "branches": len(jee_branches)
            },
            "neet": {
                "colleges": len(neet_colleges),
                "cutoffs": len(neet_cutoffs),
                "branches": len(neet_branches)
            },
            "ielts": {
                "colleges": len(ielts_colleges),
                "cutoffs": len(ielts_cutoffs),
                "programs": len(ielts_programs)
            }
        },
        "categories": list(categories.keys()),
        "states": len(states),
        "generated_at": "2024"
    }
    
    with open('data/10000_colleges_summary.json', 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print("\n🎉 **MASSIVE COLLEGE DATABASE CREATED SUCCESSFULLY!** 🎉")
    print(f"📚 Total Colleges: {total_colleges:,}")
    print(f"📊 Total Cutoff Entries: {total_cutoffs:,}")
    print(f"🏛️  States Covered: {len(states)}")
    print(f"🎯 Categories: {', '.join(categories.keys())}")
    
    print("\n📁 Files Created:")
    print("  • data/jee_10000_colleges.json")
    print("  • data/jee_10000_cutoffs.json")
    print("  • data/neet_10000_colleges.json")
    print("  • data/neet_10000_cutoffs.json")
    print("  • data/ielts_10000_colleges.json")
    print("  • data/ielts_10000_cutoffs.json")
    print("  • data/10000_colleges_summary.json")
    
    print("\n🚀 Next Steps:")
    print("  1. Restart your FastAPI server")
    print("  2. Update your main.py to load these new files")
    print("  3. Test predictions with the expanded database")

if __name__ == "__main__":
    main()
