import json
import random
import os
from pathlib import Path

# Create data directory if it doesn't exist
os.makedirs('data', exist_ok=True)

# Comprehensive list of top universities and colleges
comprehensive_colleges = {
    "jee": {
        "iits": [
            "Indian Institute of Technology Bombay", "Indian Institute of Technology Delhi",
            "Indian Institute of Technology Madras", "Indian Institute of Technology Kanpur",
            "Indian Institute of Technology Kharagpur", "Indian Institute of Technology Roorkee",
            "Indian Institute of Technology Guwahati", "Indian Institute of Technology Hyderabad",
            "Indian Institute of Technology Indore", "Indian Institute of Technology Jodhpur",
            "Indian Institute of Technology Patna", "Indian Institute of Technology Ropar",
            "Indian Institute of Technology Bhubaneswar", "Indian Institute of Technology Gandhinagar",
            "Indian Institute of Technology Mandi", "Indian Institute of Technology Varanasi",
            "Indian Institute of Technology Palakkad", "Indian Institute of Technology Tirupati",
            "Indian Institute of Technology Jammu", "Indian Institute of Technology Dharwad",
            "Indian Institute of Technology Bhilai", "Indian Institute of Technology Goa",
            "Indian Institute of Technology Dhanbad"
        ],
        "nits": [
            "National Institute of Technology Karnataka", "National Institute of Technology Trichy",
            "National Institute of Technology Warangal", "National Institute of Technology Calicut",
            "National Institute of Technology Surathkal", "National Institute of Technology Rourkela",
            "National Institute of Technology Silchar", "National Institute of Technology Hamirpur",
            "National Institute of Technology Jalandhar", "National Institute of Technology Kurukshetra",
            "National Institute of Technology Patna", "National Institute of Technology Raipur",
            "National Institute of Technology Srinagar", "National Institute of Technology Agartala",
            "National Institute of Technology Arunachal Pradesh", "National Institute of Technology Manipur",
            "National Institute of Technology Meghalaya", "National Institute of Technology Mizoram",
            "National Institute of Technology Nagaland", "National Institute of Technology Sikkim",
            "National Institute of Technology Uttarakhand", "National Institute of Technology Delhi",
            "National Institute of Technology Puducherry", "National Institute of Technology Andhra Pradesh",
            "National Institute of Technology Goa", "National Institute of Technology Jamshedpur"
        ],
        "iiits": [
            "International Institute of Information Technology Hyderabad",
            "International Institute of Information Technology Bangalore",
            "International Institute of Information Technology Allahabad",
            "International Institute of Information Technology Bhubaneswar",
            "International Institute of Information Technology Guwahati",
            "International Institute of Information Technology Jabalpur",
            "International Institute of Information Technology Lucknow",
            "International Institute of Information Technology Pune",
            "International Institute of Information Technology Vadodara",
            "International Institute of Information Technology Kota"
        ],
        "government_colleges": [
            "Delhi Technological University", "Netaji Subhas University of Technology",
            "Guru Gobind Singh Indraprastha University", "Maharaja Agrasen Institute of Technology",
            "Punjab Engineering College", "Thapar Institute of Engineering and Technology",
            "Birla Institute of Technology and Science Pilani", "Manipal Institute of Technology",
            "VIT University", "SRM Institute of Science and Technology",
            "Amrita School of Engineering", "PSG College of Technology",
            "College of Engineering Pune", "Veermata Jijabai Technological Institute",
            "Sardar Patel Institute of Technology", "Dwarkadas J. Sanghvi College of Engineering",
            "K.J. Somaiya College of Engineering", "Mukesh Patel School of Technology Management and Engineering",
            "Fr. Conceicao Rodrigues College of Engineering", "St. Francis Institute of Technology",
            "Pillai College of Engineering", "Vidyalankar Institute of Technology",
            "Shah and Anchor Kutchhi Engineering College", "Thakur College of Engineering and Technology"
        ]
    },
    "neet": {
        "aiims": [
            "All India Institute of Medical Sciences Delhi", "All India Institute of Medical Sciences Bhopal",
            "All India Institute of Medical Sciences Bhubaneswar", "All India Institute of Medical Sciences Jodhpur",
            "All India Institute of Medical Sciences Patna", "All India Institute of Medical Sciences Raipur",
            "All India Institute of Medical Sciences Rishikesh", "All India Institute of Medical Sciences Nagpur",
            "All India Institute of Medical Sciences Mangalagiri", "All India Institute of Medical Sciences Gorakhpur",
            "All India Institute of Medical Sciences Bathinda", "All India Institute of Medical Sciences Bibinagar",
            "All India Institute of Medical Sciences Deoghar", "All India Institute of Medical Sciences Kalyani",
            "All India Institute of Medical Sciences Madurai", "All India Institute of Medical Sciences Rae Bareli",
            "All India Institute of Medical Sciences Rajkot", "All India Institute of Medical Sciences Vijaypur",
            "All India Institute of Medical Sciences Bilaspur", "All India Institute of Medical Sciences Samba"
        ],
        "government_medical": [
            "Maulana Azad Medical College", "Lady Hardinge Medical College",
            "University College of Medical Sciences", "Vardhman Mahavir Medical College",
            "Atal Bihari Vajpayee Institute of Medical Sciences", "Dr. Baba Saheb Ambedkar Medical College",
            "Guru Teg Bahadur Hospital", "Safdarjung Hospital",
            "Ram Manohar Lohia Hospital", "Deen Dayal Upadhyay Hospital",
            "Lok Nayak Hospital", "Guru Nanak Eye Centre",
            "Institute of Human Behaviour and Allied Sciences", "Dr. Hedgewar Arogya Sansthan",
            "Chacha Nehru Bal Chikitsalaya", "Kasturba Hospital",
            "Rajiv Gandhi Super Speciality Hospital", "Chhatrapati Shahuji Maharaj Medical University",
            "King George's Medical University", "Sanjay Gandhi Postgraduate Institute of Medical Sciences",
            "Institute of Medical Sciences Banaras Hindu University", "Jawaharlal Institute of Postgraduate Medical Education and Research",
            "Post Graduate Institute of Medical Education and Research", "All India Institute of Medical Sciences Jodhpur",
            "Sawai Man Singh Medical College", "Dr. S.N. Medical College",
            "J.L.N. Medical College", "R.N.T. Medical College",
            "Sardar Patel Medical College", "Government Medical College Kota",
            "Government Medical College Ajmer", "Government Medical College Bikaner",
            "Government Medical College Udaipur", "Government Medical College Alwar",
            "Government Medical College Bharatpur", "Government Medical College Churu",
            "Government Medical College Dungarpur", "Government Medical College Hanumangarh",
            "Government Medical College Jhalawar", "Government Medical College Pali",
            "Government Medical College Sikar", "Government Medical College Sri Ganganagar",
            "Government Medical College Tonk", "Government Medical College Barmer",
            "Government Medical College Bhilwara", "Government Medical College Chittorgarh",
            "Government Medical College Dholpur", "Government Medical College Jaisalmer",
            "Government Medical College Jalore", "Government Medical College Nagaur",
            "Government Medical College Pratapgarh", "Government Medical College Sirohi"
        ]
    }
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

# Categories with rank multipliers
categories = {
    "General": 1.0,
    "OBC": 1.8,
    "SC": 3.5,
    "ST": 4.5
}

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

def generate_jee_comprehensive_colleges():
    """Generate comprehensive JEE colleges with realistic ranks"""
    colleges = []
    
    # IITs - Top tier (ranks 1-10000)
    for i, iit in enumerate(comprehensive_colleges["jee"]["iits"]):
        base_rank = 100 + (i * 500)
        factor = base_rank + (i * 1000)
        colleges.append({
            "name": iit,
            "location": random.choice(states),
            "base_rank": base_rank,
            "factor": min(factor, 50000),
            "type": "central"
        })
    
    # NITs - Second tier (ranks 5000-50000)
    for i, nit in enumerate(comprehensive_colleges["jee"]["nits"]):
        base_rank = 5000 + (i * 2000)
        factor = base_rank + (i * 4000)
        colleges.append({
            "name": nit,
            "location": random.choice(states),
            "base_rank": base_rank,
            "factor": min(factor, 100000),
            "type": "central"
        })
    
    # IIITs - Third tier (ranks 10000-80000)
    for i, iiit in enumerate(comprehensive_colleges["jee"]["iiits"]):
        base_rank = 10000 + (i * 3000)
        factor = base_rank + (i * 6000)
        colleges.append({
            "name": iiit,
            "location": random.choice(states),
            "base_rank": base_rank,
            "factor": min(factor, 150000),
            "type": "deemed"
        })
    
    # Government Colleges - Fourth tier (ranks 20000-150000)
    for i, college in enumerate(comprehensive_colleges["jee"]["government_colleges"]):
        base_rank = 20000 + (i * 4000)
        factor = base_rank + (i * 8000)
        colleges.append({
            "name": college,
            "location": random.choice(states),
            "base_rank": base_rank,
            "factor": min(factor, 200000),
            "type": "government"
        })
    
    # Add state-wise colleges for comprehensive coverage
    for state in states:
        # Government colleges per state
        for i in range(1, 11):
            base_rank = 30000 + (i * 5000)
            factor = base_rank + (i * 10000)
            colleges.append({
                "name": f"Government Engineering College {state} - {i}",
                "location": state,
                "base_rank": base_rank,
                "factor": min(factor, 250000),
                "type": "government"
            })
        
        # Private colleges per state
        for i in range(1, 21):
            base_rank = 50000 + (i * 8000)
            factor = base_rank + (i * 15000)
            colleges.append({
                "name": f"Private Engineering Institute {state} - {i}",
                "location": state,
                "base_rank": base_rank,
                "factor": min(factor, 300000),
                "type": "private"
            })
    
    return colleges

def generate_neet_comprehensive_colleges():
    """Generate comprehensive NEET colleges with realistic ranks"""
    colleges = []
    
    # AIIMS - Top tier (ranks 1-5000)
    for i, aiims in enumerate(comprehensive_colleges["neet"]["aiims"]):
        base_rank = 50 + (i * 200)
        factor = base_rank + (i * 500)
        colleges.append({
            "name": aiims,
            "location": random.choice(states),
            "base_rank": base_rank,
            "factor": min(factor, 20000),
            "type": "central"
        })
    
    # Government Medical Colleges - Second tier (ranks 1000-50000)
    for i, college in enumerate(comprehensive_colleges["neet"]["government_medical"]):
        base_rank = 1000 + (i * 1000)
        factor = base_rank + (i * 2000)
        colleges.append({
            "name": college,
            "location": random.choice(states),
            "base_rank": base_rank,
            "factor": min(factor, 80000),
            "type": "government"
        })
    
    # Add state-wise medical colleges
    for state in states:
        # Government medical colleges per state
        for i in range(1, 8):
            base_rank = 5000 + (i * 3000)
            factor = base_rank + (i * 6000)
            colleges.append({
                "name": f"Government Medical College {state} - {i}",
                "location": state,
                "base_rank": base_rank,
                "factor": min(factor, 100000),
                "type": "government"
            })
        
        # Private medical colleges per state
        for i in range(1, 15):
            base_rank = 15000 + (i * 4000)
            factor = base_rank + (i * 8000)
            colleges.append({
                "name": f"Private Medical Institute {state} - {i}",
                "location": state,
                "base_rank": base_rank,
                "factor": min(factor, 150000),
                "type": "private"
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
        else:
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
    print("🚀 Creating Comprehensive College Database...")
    
    # Generate comprehensive colleges
    print("📚 Generating Comprehensive JEE Colleges...")
    jee_colleges = generate_jee_comprehensive_colleges()
    print(f"✅ Generated {len(jee_colleges)} JEE colleges")
    
    print("🏥 Generating Comprehensive NEET Colleges...")
    neet_colleges = generate_neet_comprehensive_colleges()
    print(f"✅ Generated {len(neet_colleges)} NEET colleges")
    
    total_colleges = len(jee_colleges) + len(neet_colleges)
    print(f"\n🎯 Total Colleges Generated: {total_colleges}")
    
    # Generate cutoffs
    print("\n📊 Generating Cutoff Data...")
    jee_cutoffs = generate_cutoffs(jee_colleges, jee_branches, "jee")
    neet_cutoffs = generate_cutoffs(neet_colleges, neet_branches, "neet")
    
    print(f"✅ JEE Cutoffs: {len(jee_cutoffs)} entries")
    print(f"✅ NEET Cutoffs: {len(neet_cutoffs)} entries")
    
    total_cutoffs = len(jee_cutoffs) + len(neet_cutoffs)
    print(f"🎯 Total Cutoff Entries: {total_cutoffs}")
    
    # Save data
    print("\n💾 Saving Data Files...")
    
    # Save JEE data
    with open('data/jee_comprehensive_colleges.json', 'w', encoding='utf-8') as f:
        json.dump(jee_colleges, f, indent=2, ensure_ascii=False)
    
    with open('data/jee_comprehensive_cutoffs.json', 'w', encoding='utf-8') as f:
        json.dump(jee_cutoffs, f, indent=2, ensure_ascii=False)
    
    # Save NEET data
    with open('data/neet_comprehensive_colleges.json', 'w', encoding='utf-8') as f:
        json.dump(neet_colleges, f, indent=2, ensure_ascii=False)
    
    with open('data/neet_comprehensive_cutoffs.json', 'w', encoding='utf-8') as f:
        json.dump(neet_cutoffs, f, indent=2, ensure_ascii=False)
    
    # Create summary file
    summary = {
        "total_colleges": total_colleges,
        "total_cutoffs": total_cutoffs,
        "breakdown": {
            "jee": {
                "colleges": len(jee_colleges),
                "cutoffs": len(jee_cutoffs),
                "branches": len(jee_branches),
                "iits": len(comprehensive_colleges["jee"]["iits"]),
                "nits": len(comprehensive_colleges["jee"]["nits"]),
                "iiits": len(comprehensive_colleges["jee"]["iiits"]),
                "government_colleges": len(comprehensive_colleges["jee"]["government_colleges"])
            },
            "neet": {
                "colleges": len(neet_colleges),
                "cutoffs": len(neet_cutoffs),
                "branches": len(neet_branches),
                "aiims": len(comprehensive_colleges["neet"]["aiims"]),
                "government_medical": len(comprehensive_colleges["neet"]["government_medical"])
            }
        },
        "categories": list(categories.keys()),
        "states": len(states),
        "generated_at": "2024",
        "comprehensive_coverage": True
    }
    
    with open('data/comprehensive_colleges_summary.json', 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print("\n🎉 **COMPREHENSIVE COLLEGE DATABASE CREATED SUCCESSFULLY!** 🎉")
    print(f"📚 Total Colleges: {total_colleges:,}")
    print(f"📊 Total Cutoff Entries: {total_cutoffs:,}")
    print(f"🏛️  States Covered: {len(states)}")
    print(f"🎯 Categories: {', '.join(categories.keys())}")
    
    print("\n📁 Files Created:")
    print("  • data/jee_comprehensive_colleges.json")
    print("  • data/jee_comprehensive_cutoffs.json")
    print("  • data/neet_comprehensive_colleges.json")
    print("  • data/neet_comprehensive_cutoffs.json")
    print("  • data/comprehensive_colleges_summary.json")
    
    print("\n🚀 Next Steps:")
    print("  1. Update your main.py to load these comprehensive files")
    print("  2. Restart your FastAPI server")
    print("  3. Test predictions with the expanded database")

if __name__ == "__main__":
    main()
