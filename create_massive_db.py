import json
import random

# Categories with rank multipliers
categories = {
    "General": 1.0,
    "OBC": 1.8,  # 80% higher ranks allowed
    "SC": 3.5,   # 250% higher ranks allowed
    "ST": 4.5    # 350% higher ranks allowed
}

# Branches
branches = [
    "Computer Science and Engineering",
    "Electronics and Communication Engineering", 
    "Mechanical Engineering",
    "Civil Engineering",
    "Electrical Engineering",
    "Information Technology",
    "Chemical Engineering"
]

# Massive list of Indian engineering colleges
colleges = [
    # Top Tier Colleges (Rank 1-10,000)
    {"name": "IIT Bombay", "location": "Mumbai, Maharashtra", "base_rank": 1, "factor": 66},
    {"name": "IIT Delhi", "location": "New Delhi", "base_rank": 1, "factor": 89},
    {"name": "IIT Madras", "location": "Chennai, Tamil Nadu", "base_rank": 1, "factor": 110},
    {"name": "IIT Kharagpur", "location": "Kharagpur, West Bengal", "base_rank": 1, "factor": 145},
    {"name": "IIT Kanpur", "location": "Kanpur, Uttar Pradesh", "base_rank": 1, "factor": 175},
    {"name": "IIT Roorkee", "location": "Roorkee, Uttarakhand", "base_rank": 150, "factor": 210},
    {"name": "IIT Guwahati", "location": "Guwahati, Assam", "base_rank": 180, "factor": 250},
    {"name": "IISC Bangalore", "location": "Bangalore, Karnataka", "base_rank": 50, "factor": 300},
    {"name": "BITS Pilani", "location": "Pilani, Rajasthan", "base_rank": 1000, "factor": 5000},
    {"name": "VJTI Mumbai", "location": "Mumbai, Maharashtra", "base_rank": 2000, "factor": 8000},
    
    # Second Tier (10,000-50,000)
    {"name": "VIT Vellore", "location": "Vellore, Tamil Nadu", "base_rank": 2000, "factor": 15000},
    {"name": "SRM Chennai", "location": "Chennai, Tamil Nadu", "base_rank": 5000, "factor": 25000},
    {"name": "Manipal Institute", "location": "Manipal, Karnataka", "base_rank": 8000, "factor": 35000},
    {"name": "SASTRA University", "location": "Thanjavur, Tamil Nadu", "base_rank": 12000, "factor": 40000},
    {"name": "PSG Tech", "location": "Coimbatore, Tamil Nadu", "base_rank": 8000, "factor": 30000},
    {"name": "Anna University CEG", "location": "Chennai, Tamil Nadu", "base_rank": 3000, "factor": 15000},
    
    # Maharashtra Colleges
    {"name": "College of Engineering Pune", "location": "Pune, Maharashtra", "base_rank": 5000, "factor": 20000},
    {"name": "Pune Institute of Computer Technology", "location": "Pune, Maharashtra", "base_rank": 8000, "factor": 25000},
    {"name": "Walchand College Sangli", "location": "Sangli, Maharashtra", "base_rank": 15000, "factor": 50000},
    {"name": "Government College of Engineering Aurangabad", "location": "Aurangabad, Maharashtra", "base_rank": 20000, "factor": 80000},
    
    # Karnataka Colleges  
    {"name": "RV College of Engineering", "location": "Bangalore, Karnataka", "base_rank": 5000, "factor": 25000},
    {"name": "BMS College of Engineering", "location": "Bangalore, Karnataka", "base_rank": 8000, "factor": 40000},
    {"name": "Dayananda Sagar College", "location": "Bangalore, Karnataka", "base_rank": 15000, "factor": 80000},
    {"name": "PES University", "location": "Bangalore, Karnataka", "base_rank": 10000, "factor": 45000},
    {"name": "MS Ramaiah Institute", "location": "Bangalore, Karnataka", "base_rank": 12000, "factor": 60000},
    
    # Tamil Nadu Colleges
    {"name": "Thiagarajar College of Engineering", "location": "Madurai, Tamil Nadu", "base_rank": 12000, "factor": 65000},
    {"name": "SSN College of Engineering", "location": "Chennai, Tamil Nadu", "base_rank": 10000, "factor": 50000},
    {"name": "Government College of Technology", "location": "Coimbatore, Tamil Nadu", "base_rank": 15000, "factor": 75000},
    {"name": "Coimbatore Institute of Technology", "location": "Coimbatore, Tamil Nadu", "base_rank": 20000, "factor": 100000},
    
    # Delhi/NCR Colleges
    {"name": "Delhi Technological University", "location": "Delhi", "base_rank": 800, "factor": 2500},
    {"name": "NSUT Delhi", "location": "Delhi", "base_rank": 1200, "factor": 3000},
    {"name": "IGDTUW", "location": "Delhi", "base_rank": 3000, "factor": 15000},
    {"name": "Jaypee Institute Noida", "location": "Noida, UP", "base_rank": 20000, "factor": 100000},
    {"name": "Amity University", "location": "Noida, UP", "base_rank": 25000, "factor": 120000},
    
    # West Bengal Colleges
    {"name": "Jadavpur University", "location": "Kolkata, West Bengal", "base_rank": 400, "factor": 1200},
    {"name": "Bengal Engineering College", "location": "Howrah, West Bengal", "base_rank": 8000, "factor": 30000},
    {"name": "Kalyani Government Engineering College", "location": "Kalyani, West Bengal", "base_rank": 25000, "factor": 100000},
    {"name": "Heritage Institute of Technology", "location": "Kolkata, West Bengal", "base_rank": 45000, "factor": 200000},
    
    # Gujarat Colleges
    {"name": "SVNIT Surat", "location": "Surat, Gujarat", "base_rank": 800, "factor": 3000},
    {"name": "LD College of Engineering", "location": "Ahmedabad, Gujarat", "base_rank": 15000, "factor": 60000},
    {"name": "Nirma Institute of Technology", "location": "Ahmedabad, Gujarat", "base_rank": 12000, "factor": 50000},
    {"name": "Government Engineering College Gandhinagar", "location": "Gandhinagar, Gujarat", "base_rank": 20000, "factor": 80000},
    
    # Rajasthan Colleges
    {"name": "MNIT Jaipur", "location": "Jaipur, Rajasthan", "base_rank": 1000, "factor": 3500},
    {"name": "MBM Engineering College Jodhpur", "location": "Jodhpur, Rajasthan", "base_rank": 25000, "factor": 100000},
    {"name": "Government Engineering College Ajmer", "location": "Ajmer, Rajasthan", "base_rank": 35000, "factor": 150000},
    {"name": "JECRC University", "location": "Jaipur, Rajasthan", "base_rank": 40000, "factor": 200000},
    {"name": "Poornima College of Engineering", "location": "Jaipur, Rajasthan", "base_rank": 50000, "factor": 250000},
    {"name": "Arya College of Engineering", "location": "Jaipur, Rajasthan", "base_rank": 80000, "factor": 400000},
    
    # Uttar Pradesh Colleges
    {"name": "IET Lucknow", "location": "Lucknow, UP", "base_rank": 20000, "factor": 100000},
    {"name": "HBTI Kanpur", "location": "Kanpur, UP", "base_rank": 25000, "factor": 120000},
    {"name": "MMMUT Gorakhpur", "location": "Gorakhpur, UP", "base_rank": 30000, "factor": 150000},
    {"name": "KIET Ghaziabad", "location": "Ghaziabad, UP", "base_rank": 45000, "factor": 220000},
    {"name": "ABES Engineering College", "location": "Ghaziabad, UP", "base_rank": 50000, "factor": 250000},
    {"name": "GL Bajaj Institute", "location": "Greater Noida, UP", "base_rank": 40000, "factor": 200000},
    {"name": "Galgotias University", "location": "Greater Noida, UP", "base_rank": 35000, "factor": 180000},
    
    # Punjab Colleges
    {"name": "Thapar Institute", "location": "Patiala, Punjab", "base_rank": 1500, "factor": 5000},
    {"name": "Punjab Engineering College", "location": "Chandigarh", "base_rank": 8000, "factor": 30000},
    {"name": "Lovely Professional University", "location": "Jalandhar, Punjab", "base_rank": 25000, "factor": 150000},
    {"name": "Chandigarh University", "location": "Chandigarh", "base_rank": 30000, "factor": 180000},
    
    # Haryana Colleges
    {"name": "NIT Kurukshetra", "location": "Kurukshetra, Haryana", "base_rank": 800, "factor": 2800},
    {"name": "YMCA University", "location": "Faridabad, Haryana", "base_rank": 25000, "factor": 120000},
    {"name": "Manav Rachna University", "location": "Faridabad, Haryana", "base_rank": 40000, "factor": 200000},
    {"name": "The NorthCap University", "location": "Gurugram, Haryana", "base_rank": 35000, "factor": 180000},
]

# Generate additional colleges to reach 1000+ total
states = [
    "Andhra Pradesh", "Telangana", "Kerala", "Odisha", "Madhya Pradesh", 
    "Chhattisgarh", "Bihar", "Jharkhand", "Himachal Pradesh", "Uttarakhand",
    "Assam", "Meghalaya", "Manipur", "Tripura", "Nagaland", "Mizoram",
    "Arunachal Pradesh", "Goa", "Jammu & Kashmir"
]

for state in states:
    # Add government colleges for each state
    for i in range(1, 16):  # 15 government colleges per state
        base_rank = 30000 + (i * 10000)
        factor = base_rank + (i * 20000)
        colleges.append({
            "name": f"Government Engineering College {state} - {i}",
            "location": state,
            "base_rank": base_rank,
            "factor": min(factor, 500000)
        })
    
    # Add private colleges
    for i in range(1, 11):  # 10 private colleges per state
        base_rank = 50000 + (i * 15000)
        factor = base_rank + (i * 30000)
        colleges.append({
            "name": f"Private Engineering Institute {state} - {i}",
            "location": state,
            "base_rank": base_rank,
            "factor": min(factor, 500000)
        })

print(f"Total colleges: {len(colleges)}")

# Generate cutoff data
cutoffs = []

for college in colleges:
    for branch in branches:
        # Skip some branches for lower-tier colleges
        if college["base_rank"] > 100000 and branch in ["Chemical Engineering", "Aerospace Engineering"]:
            continue
            
        for category, multiplier in categories.items():
            opening_rank = max(1, int(college["base_rank"] * multiplier))
            closing_rank = min(500000, int(college["factor"] * multiplier))
            
            # Add some randomization
            opening_rank = max(1, opening_rank + random.randint(-500, 500))
            closing_rank = min(500000, closing_rank + random.randint(-1000, 1000))
            
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
                "exam_type": "jee",
                "location": college["location"]
            })

# Save the massive database
with open('data/jee_cutoffs.json', 'w', encoding='utf-8') as f:
    json.dump(cutoffs, f, indent=2, ensure_ascii=False)

print(f"Created massive database with {len(cutoffs)} cutoff entries")
print(f"Covering {len(set(cutoff['college'] for cutoff in cutoffs))} unique colleges")
print(f"Categories: {list(categories.keys())}")
print(f"Branches: {branches}")

# Show summary by category
for category in categories.keys():
    category_count = len([c for c in cutoffs if c['category'] == category])
    print(f"{category}: {category_count} entries")
