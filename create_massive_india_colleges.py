import json
import random
from typing import List, Dict, Any

# All Indian States and Union Territories
INDIAN_STATES = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
    "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka",
    "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram",
    "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu",
    "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal"
]

UNION_TERRITORIES = [
    "Andaman and Nicobar Islands", "Chandigarh", "Dadra and Nagar Haveli and Daman and Diu",
    "Delhi", "Jammu and Kashmir", "Ladakh", "Lakshadweep", "Puducherry"
]

ALL_REGIONS = INDIAN_STATES + UNION_TERRITORIES

# Major cities in each state for better distribution
STATE_CITIES = {
    "Andhra Pradesh": ["Visakhapatnam", "Vijayawada", "Guntur", "Nellore", "Kurnool", "Anantapur", "Kadapa", "Tirupati"],
    "Arunachal Pradesh": ["Itanagar", "Naharlagun", "Pasighat", "Tezu", "Ziro", "Bomdila", "Along", "Roing"],
    "Assam": ["Guwahati", "Dibrugarh", "Silchar", "Jorhat", "Tezpur", "Dhubri", "Sivasagar", "Nagaon"],
    "Bihar": ["Patna", "Gaya", "Bhagalpur", "Muzaffarpur", "Purnia", "Darbhanga", "Arrah", "Bettiah"],
    "Chhattisgarh": ["Raipur", "Bhilai", "Bilaspur", "Korba", "Jagdalpur", "Ambikapur", "Rajnandgaon", "Durg"],
    "Goa": ["Panaji", "Margao", "Vasco da Gama", "Mapusa", "Ponda", "Mormugao", "Bicholim", "Sanquelim"],
    "Gujarat": ["Ahmedabad", "Surat", "Vadodara", "Rajkot", "Bhavnagar", "Jamnagar", "Gandhinagar", "Anand"],
    "Haryana": ["Gurgaon", "Faridabad", "Panipat", "Yamunanagar", "Rohtak", "Hisar", "Karnal", "Sonipat"],
    "Himachal Pradesh": ["Shimla", "Mandi", "Solan", "Kullu", "Kangra", "Hamirpur", "Una", "Chamba"],
    "Jharkhand": ["Ranchi", "Jamshedpur", "Dhanbad", "Bokaro", "Hazaribagh", "Deoghar", "Giridih", "Dumka"],
    "Karnataka": ["Bangalore", "Mysore", "Hubli", "Mangalore", "Belgaum", "Gulbarga", "Bellary", "Tumkur"],
    "Kerala": ["Thiruvananthapuram", "Kochi", "Kozhikode", "Thrissur", "Kollam", "Alappuzha", "Palakkad", "Kannur"],
    "Madhya Pradesh": ["Bhopal", "Indore", "Jabalpur", "Gwalior", "Ujjain", "Sagar", "Rewa", "Satna"],
    "Maharashtra": ["Mumbai", "Pune", "Nagpur", "Thane", "Nashik", "Aurangabad", "Solapur", "Kolhapur"],
    "Manipur": ["Imphal", "Thoubal", "Bishnupur", "Churachandpur", "Ukhrul", "Senapati", "Tamenglong", "Chandel"],
    "Meghalaya": ["Shillong", "Tura", "Jowai", "Nongstoin", "Nongpoh", "Williamnagar", "Baghmara", "Resubelpara"],
    "Mizoram": ["Aizawl", "Lunglei", "Saiha", "Champhai", "Kolasib", "Serchhip", "Lawngtlai", "Mamit"],
    "Nagaland": ["Kohima", "Dimapur", "Mokokchung", "Tuensang", "Wokha", "Zunheboto", "Phek", "Mon"],
    "Odisha": ["Bhubaneswar", "Cuttack", "Rourkela", "Brahmapur", "Sambalpur", "Puri", "Balasore", "Bhadrak"],
    "Punjab": ["Ludhiana", "Amritsar", "Jalandhar", "Patiala", "Bathinda", "Pathankot", "Hoshiarpur", "Moga"],
    "Rajasthan": ["Jaipur", "Jodhpur", "Kota", "Bikaner", "Ajmer", "Udaipur", "Bhilwara", "Alwar"],
    "Sikkim": ["Gangtok", "Namchi", "Geyzing", "Mangan", "Ravongla", "Jorethang", "Singtam", "Rangpo"],
    "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai", "Salem", "Tiruchirappalli", "Vellore", "Erode", "Thoothukkudi"],
    "Telangana": ["Hyderabad", "Warangal", "Nizamabad", "Karimnagar", "Ramagundam", "Khammam", "Mahbubnagar", "Nalgonda"],
    "Tripura": ["Agartala", "Udaipur", "Dharmanagar", "Kailasahar", "Belonia", "Khowai", "Teliamura", "Sabroom"],
    "Uttar Pradesh": ["Lucknow", "Kanpur", "Ghaziabad", "Agra", "Varanasi", "Meerut", "Allahabad", "Bareilly"],
    "Uttarakhand": ["Dehradun", "Haridwar", "Roorkee", "Haldwani", "Rudrapur", "Kashipur", "Rishikesh", "Mussoorie"],
    "West Bengal": ["Kolkata", "Howrah", "Durgapur", "Asansol", "Siliguri", "Bardhaman", "Malda", "Baharampur"],
    "Delhi": ["New Delhi", "Delhi Cantonment", "Dwarka", "Rohini", "Pitampura", "Janakpuri", "Lajpat Nagar", "Connaught Place"],
    "Chandigarh": ["Chandigarh", "Sector 17", "Sector 22", "Sector 35", "Sector 47", "Industrial Area", "Manimajra", "Daria"],
    "Jammu and Kashmir": ["Srinagar", "Jammu", "Anantnag", "Baramulla", "Udhampur", "Kathua", "Pulwama", "Kupwara"],
    "Ladakh": ["Leh", "Kargil", "Drass", "Zanskar", "Nubra Valley", "Pangong Tso", "Tso Moriri", "Hemis"]
}

# Engineering branches for JEE
JEE_BRANCHES = [
    "Computer Science and Engineering", "Mechanical Engineering", "Electrical Engineering",
    "Electronics and Communication Engineering", "Civil Engineering", "Information Technology",
    "Chemical Engineering", "Biotechnology", "Aeronautical Engineering", "Automobile Engineering",
    "Mining Engineering", "Metallurgical Engineering", "Textile Engineering", "Agricultural Engineering",
    "Food Technology", "Petroleum Engineering", "Nuclear Engineering", "Robotics Engineering"
]

# Medical branches for NEET
NEET_BRANCHES = [
    "MBBS", "BDS", "BAMS", "BHMS", "BSc Nursing", "BSc Medical Technology",
    "BSc Physiotherapy", "BSc Occupational Therapy", "BSc Medical Laboratory Technology",
    "BSc Radiography", "BSc Optometry", "BSc Audiology", "BSc Nutrition and Dietetics"
]

# Programs for IELTS
IELTS_PROGRAMS = [
    "Computer Science", "Business Administration", "Engineering", "Medicine", "Arts and Humanities",
    "Social Sciences", "Natural Sciences", "Law", "Education", "Agriculture", "Architecture",
    "Design", "Media and Communication", "Tourism and Hospitality", "Environmental Science"
]

def generate_college_name(state: str, city: str, college_type: str, index: int) -> str:
    """Generate realistic college names"""
    prefixes = [
        "Government", "Private", "Institute of", "College of", "University of",
        "National Institute of", "Regional", "State", "Central", "Modern",
        "Advanced", "Professional", "Technical", "Engineering", "Medical",
        "Science and Technology", "Arts and Science", "Management", "Computer"
    ]
    
    suffixes = [
        "Engineering College", "Institute of Technology", "Medical College",
        "University", "College", "Institute", "Academy", "School",
        "Polytechnic", "Technical Institute", "Science College"
    ]
    
    if college_type == "jee":
        prefix = random.choice([p for p in prefixes if "Engineering" in p or "Technical" in p])
        suffix = random.choice([s for s in suffixes if "Engineering" in s or "Technology" in s])
    elif college_type == "neet":
        prefix = random.choice([p for p in prefixes if "Medical" in p or "Health" in p])
        suffix = random.choice([s for s in suffixes if "Medical" in s or "College" in s])
    else:  # ielts
        prefix = random.choice(prefixes)
        suffix = random.choice(suffixes)
    
    # Add city/state identifier
    if random.random() < 0.3:
        name = f"{prefix} {city}"
    elif random.random() < 0.5:
        name = f"{prefix} {state}"
    else:
        name = f"{prefix} {city} {state}"
    
    name += f" {suffix}"
    
    # Add unique identifier if needed
    if index > 0:
        name += f" {chr(65 + (index % 26))}"
    
    return name

def generate_college_data(college_type: str, state: str, city: str, index: int) -> Dict[str, Any]:
    """Generate college data based on type"""
    college_name = generate_college_name(state, city, college_type, index)
    
    base_data = {
        "name": college_name,
        "location": f"{city}, {state}",
        "state": state,
        "city": city,
        "type": "Government" if random.random() < 0.3 else "Private",
        "established": random.randint(1960, 2020),
        "accreditation": random.choice(["AICTE", "UGC", "NAAC A+", "NAAC A", "NAAC B+", "NAAC B"]),
        "website": f"www.{college_name.lower().replace(' ', '').replace(',', '')}.edu.in"
    }
    
    if college_type == "jee":
        base_data.update({
            "branches": random.sample(JEE_BRANCHES, random.randint(8, 15)),
            "total_seats": random.randint(300, 1200),
            "fees_range": {
                "min": random.randint(50000, 200000),
                "max": random.randint(300000, 800000)
            }
        })
    elif college_type == "neet":
        base_data.update({
            "branches": random.sample(NEET_BRANCHES, random.randint(5, 10)),
            "total_seats": random.randint(100, 500),
            "fees_range": {
                "min": random.randint(100000, 500000),
                "max": random.randint(800000, 2000000)
            }
        })
    else:  # ielts
        base_data.update({
            "programs": random.sample(IELTS_PROGRAMS, random.randint(8, 15)),
            "total_seats": random.randint(200, 800),
            "fees_range": {
                "min": random.randint(80000, 300000),
                "max": random.randint(400000, 1200000)
            }
        })
    
    return base_data

def generate_cutoff_data(college_data: Dict[str, Any], college_type: str) -> List[Dict[str, Any]]:
    """Generate cutoff data for colleges"""
    cutoffs = []
    
    if college_type == "jee":
        branches = college_data.get("branches", [])
        categories = ["General", "OBC", "SC", "ST"]
        quotas = ["All India", "State", "Management", "NRI"]
        
        for branch in branches:
            for category in categories:
                for quota in quotas:
                    base_rank = random.randint(1000, 200000)
                    tolerance = random.randint(0, 20)
                    
                    cutoff = {
                        "college_name": college_data["name"],
                        "branch": branch,
                        "category": category,
                        "quota": quota,
                        "rank": base_rank,
                        "tolerance_percent": tolerance,
                        "state": college_data["state"],
                        "city": college_data["city"]
                    }
                    cutoffs.append(cutoff)
    
    elif college_type == "neet":
        branches = college_data.get("branches", [])
        categories = ["General", "OBC", "SC", "ST"]
        quotas = ["All India", "State", "Management", "NRI"]
        
        for branch in branches:
            for category in categories:
                for quota in quotas:
                    base_rank = random.randint(100, 100000)
                    tolerance = random.randint(0, 15)
                    
                    cutoff = {
                        "college_name": college_data["name"],
                        "branch": branch,
                        "category": category,
                        "quota": quota,
                        "rank": base_rank,
                        "tolerance_percent": tolerance,
                        "state": college_data["state"],
                        "city": college_data["city"]
                    }
                    cutoffs.append(cutoff)
    
    else:  # ielts
        programs = college_data.get("programs", [])
        categories = ["General", "OBC", "SC", "ST"]
        quotas = ["All India", "State", "Management", "International"]
        
        for program in programs:
            for category in categories:
                for quota in quotas:
                    base_score = random.uniform(5.5, 9.0)
                    tolerance = random.uniform(0.0, 1.0)
                    
                    cutoff = {
                        "college_name": college_data["name"],
                        "program": program,
                        "category": category,
                        "quota": quota,
                        "score": round(base_score, 1),
                        "tolerance_percent": round(tolerance, 1),
                        "state": college_data["state"],
                        "city": college_data["city"]
                    }
                    cutoffs.append(cutoff)
    
    return cutoffs

def main():
    """Main function to generate massive college database"""
    print("🚀 Starting massive college generation for all Indian states...")
    
    all_colleges = {"jee": [], "neet": [], "ielts": []}
    all_cutoffs = {"jee": [], "neet": [], "ielts": []}
    
    # Generate colleges for each state
    for state in ALL_REGIONS:
        print(f"📍 Generating colleges for {state}...")
        cities = STATE_CITIES.get(state, [state])
        
        # Generate more colleges for larger states
        if state in ["Maharashtra", "Uttar Pradesh", "Tamil Nadu", "Karnataka", "Andhra Pradesh"]:
            colleges_per_city = random.randint(25, 40)
        elif state in ["Gujarat", "Rajasthan", "Madhya Pradesh", "West Bengal", "Telangana"]:
            colleges_per_city = random.randint(20, 35)
        else:
            colleges_per_city = random.randint(15, 30)
        
        for city in cities:
            for i in range(colleges_per_city):
                # JEE Colleges (Engineering)
                jee_college = generate_college_data("jee", state, city, i)
                all_colleges["jee"].append(jee_college)
                all_cutoffs["jee"].extend(generate_cutoff_data(jee_college, "jee"))
                
                # NEET Colleges (Medical)
                if random.random() < 0.7:  # 70% chance of medical college
                    neet_college = generate_college_data("neet", state, city, i)
                    all_colleges["neet"].append(neet_college)
                    all_cutoffs["neet"].extend(generate_cutoff_data(neet_college, "neet"))
                
                # IELTS Colleges (General)
                if random.random() < 0.6:  # 60% chance of general college
                    ielts_college = generate_college_data("ielts", state, city, i)
                    all_colleges["ielts"].append(ielts_college)
                    all_cutoffs["ielts"].extend(generate_cutoff_data(ielts_college, "ielts"))
    
    # Save colleges data
    print("💾 Saving colleges data...")
    for exam_type in ["jee", "neet", "ielts"]:
        colleges_file = f"data/{exam_type}_massive_colleges.json"
        cutoffs_file = f"data/{exam_type}_massive_cutoffs.json"
        
        with open(colleges_file, 'w', encoding='utf-8') as f:
            json.dump(all_colleges[exam_type], f, indent=2, ensure_ascii=False)
        
        with open(cutoffs_file, 'w', encoding='utf-8') as f:
            json.dump(all_cutoffs[exam_type], f, indent=2, ensure_ascii=False)
        
        print(f"✅ Saved {len(all_colleges[exam_type])} colleges to {colleges_file}")
        print(f"✅ Saved {len(all_cutoffs[exam_type])} cutoffs to {cutoffs_file}")
    
    # Generate summary
    total_colleges = sum(len(colleges) for colleges in all_colleges.values())
    total_cutoffs = sum(len(cutoffs) for cutoffs in all_cutoffs.values())
    
    summary = {
        "total_colleges": total_colleges,
        "total_cutoffs": total_cutoffs,
        "breakdown": {
            "jee": {
                "colleges": len(all_colleges["jee"]),
                "cutoffs": len(all_cutoffs["jee"]),
                "branches": len(JEE_BRANCHES)
            },
            "neet": {
                "colleges": len(all_colleges["neet"]),
                "cutoffs": len(all_cutoffs["neet"]),
                "branches": len(NEET_BRANCHES)
            },
            "ielts": {
                "colleges": len(all_colleges["ielts"]),
                "cutoffs": len(all_cutoffs["ielts"]),
                "programs": len(IELTS_PROGRAMS)
            }
        },
        "states_covered": len(ALL_REGIONS),
        "regions": ALL_REGIONS,
        "generated_at": "2024"
    }
    
    with open("data/massive_colleges_summary.json", 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print("\n🎉 MASSIVE COLLEGE GENERATION COMPLETE!")
    print(f"📊 Total Colleges: {total_colleges:,}")
    print(f"📊 Total Cutoffs: {total_cutoffs:,}")
    print(f"🗺️  States Covered: {len(ALL_REGIONS)}")
    print(f"📁 Summary saved to: data/massive_colleges_summary.json")
    
    # Print breakdown
    for exam_type, data in summary["breakdown"].items():
        print(f"   {exam_type.upper()}: {data['colleges']:,} colleges, {data['cutoffs']:,} cutoffs")

if __name__ == "__main__":
    main()
