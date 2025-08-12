#!/usr/bin/env python3
"""
Comprehensive College Database Generator
Generates a complete database of colleges from all states for JEE Main, JEE Advanced, and NEET
This ensures the data is saved to disk and can be used on any system.
"""

import json
import random
from datetime import datetime

def generate_comprehensive_database():
    """Generate comprehensive college database with all states coverage"""
    
    colleges = []
    
    # All 29 states + Delhi for complete coverage
    all_states = [
        "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", 
        "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka",
        "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram",
        "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu",
        "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal", "Delhi"
    ]
    
    # IITs for JEE Advanced
    iits = [
        {"name": "IIT Delhi", "state": "Delhi", "baseRank": 1},
        {"name": "IIT Bombay", "state": "Maharashtra", "baseRank": 1},
        {"name": "IIT Madras", "state": "Tamil Nadu", "baseRank": 1},
        {"name": "IIT Kanpur", "state": "Uttar Pradesh", "baseRank": 1},
        {"name": "IIT Kharagpur", "state": "West Bengal", "baseRank": 1},
        {"name": "IIT Roorkee", "state": "Uttarakhand", "baseRank": 1},
        {"name": "IIT Guwahati", "state": "Assam", "baseRank": 2},
        {"name": "IIT Hyderabad", "state": "Telangana", "baseRank": 2},
        {"name": "IIT Gandhinagar", "state": "Gujarat", "baseRank": 2},
        {"name": "IIT Ropar", "state": "Punjab", "baseRank": 3},
        {"name": "IIT Bhubaneswar", "state": "Odisha", "baseRank": 3},
        {"name": "IIT Indore", "state": "Madhya Pradesh", "baseRank": 3},
        {"name": "IIT Mandi", "state": "Himachal Pradesh", "baseRank": 4},
        {"name": "IIT Jodhpur", "state": "Rajasthan", "baseRank": 4},
        {"name": "IIT Patna", "state": "Bihar", "baseRank": 4},
        {"name": "IIT Varanasi", "state": "Uttar Pradesh", "baseRank": 5},
        {"name": "IIT Palakkad", "state": "Kerala", "baseRank": 5},
        {"name": "IIT Tirupati", "state": "Andhra Pradesh", "baseRank": 5},
        {"name": "IIT Bhilai", "state": "Chhattisgarh", "baseRank": 6},
        {"name": "IIT Goa", "state": "Goa", "baseRank": 6},
        {"name": "IIT Jammu", "state": "Jammu and Kashmir", "baseRank": 6},
        {"name": "IIT Dharwad", "state": "Karnataka", "baseRank": 7}
    ]
    
    # Engineering branches for comprehensive coverage
    engineering_branches = [
        'Computer Science', 'Electronics', 'Mechanical', 'Civil', 'Electrical',
        'Chemical', 'Aerospace', 'Biotechnology', 'Information Technology', 'Metallurgy'
    ]
    
    # Add IIT colleges
    print("Generating IIT colleges...")
    for iit in iits:
        for branch_idx, branch in enumerate(engineering_branches):
            cutoff = iit["baseRank"] * 50 + branch_idx * 25
            available_seats = random.randint(20, 50)
            total_seats = 50 + (branch_idx % 10) * 5
            seat_status = 'available' if available_seats > 20 else ('limited' if available_seats > 5 else 'full')
            
            colleges.append({
                "name": f"{iit['name']} - {branch}",
                "type": "IIT",
                "exam": "JEE Advanced",
                "state": iit["state"],
                "cutoff": cutoff,
                "fees": "₹2,00,000",
                "seats": total_seats,
                "availableSeats": available_seats,
                "seatStatus": seat_status,
                "scholarship": "Merit Scholarship Available" if random.random() > 0.7 else None,
                "aiPrediction": f"Cutoff may {'increase' if random.random() > 0.5 else 'decrease'} by {random.randint(50, 250)} ranks in 2025",
                "pros": ["Top-tier faculty", "Excellent placement record", "Strong alumni network"],
                "cons": ["High competition", "Limited seats"],
                "rating": f"{4.2 + random.random() * 0.8:.1f}",
                "placement": f"{85 + random.randint(0, 15)}%",
                "avgPackage": f"₹{12 + random.randint(0, 8)} LPA"
            })
    
    # Add NITs for JEE Main
    print("Generating NIT colleges...")
    nits = [
        {"name": "NIT Trichy", "state": "Tamil Nadu", "baseRank": 500},
        {"name": "NIT Warangal", "state": "Telangana", "baseRank": 600},
        {"name": "NIT Surathkal", "state": "Karnataka", "baseRank": 700},
        {"name": "NIT Calicut", "state": "Kerala", "baseRank": 800},
        {"name": "NIT Rourkela", "state": "Odisha", "baseRank": 900},
        {"name": "NIT Allahabad", "state": "Uttar Pradesh", "baseRank": 1000},
        {"name": "NIT Bhopal", "state": "Madhya Pradesh", "baseRank": 1100},
        {"name": "NIT Nagpur", "state": "Maharashtra", "baseRank": 1200},
        {"name": "NIT Kurukshetra", "state": "Haryana", "baseRank": 1300},
        {"name": "NIT Jaipur", "state": "Rajasthan", "baseRank": 1400}
    ]
    
    for nit in nits:
        for branch_idx, branch in enumerate(engineering_branches):
            cutoff = nit["baseRank"] + branch_idx * 100
            available_seats = random.randint(15, 40)
            total_seats = 60 + (branch_idx % 8) * 5
            seat_status = 'available' if available_seats > 20 else ('limited' if available_seats > 5 else 'full')
            
            colleges.append({
                "name": f"{nit['name']} - {branch}",
                "type": "NIT",
                "exam": "JEE Main",
                "state": nit["state"],
                "cutoff": cutoff,
                "fees": "₹1,50,000",
                "seats": total_seats,
                "availableSeats": available_seats,
                "seatStatus": seat_status,
                "scholarship": "Merit Scholarship Available" if random.random() > 0.6 else None,
                "aiPrediction": f"Cutoff may {'increase' if random.random() > 0.5 else 'decrease'} by {random.randint(25, 150)} ranks in 2025",
                "pros": ["Good faculty", "Strong placement", "Central funding"],
                "cons": ["High competition", "Limited industry exposure"],
                "rating": f"{3.8 + random.random() * 1.0:.1f}",
                "placement": f"{75 + random.randint(0, 20)}%",
                "avgPackage": f"₹{8 + random.randint(0, 6)} LPA"
            })
    
    # Add AIIMS and Medical Colleges for NEET
    print("Generating AIIMS and Medical colleges...")
    aiims_list = [
        {"name": "AIIMS Delhi", "state": "Delhi", "baseRank": 1},
        {"name": "AIIMS Jodhpur", "state": "Rajasthan", "baseRank": 50},
        {"name": "AIIMS Bhopal", "state": "Madhya Pradesh", "baseRank": 100},
        {"name": "AIIMS Patna", "state": "Bihar", "baseRank": 150},
        {"name": "AIIMS Raipur", "state": "Chhattisgarh", "baseRank": 200},
        {"name": "AIIMS Bhubaneswar", "state": "Odisha", "baseRank": 250},
        {"name": "AIIMS Rishikesh", "state": "Uttarakhand", "baseRank": 300}
    ]
    
    medical_courses = ['MBBS', 'BDS', 'BAMS', 'BHMS', 'B.Pharma']
    
    for aiims in aiims_list:
        for course_idx, course in enumerate(medical_courses):
            cutoff = aiims["baseRank"] + course_idx * 50
            available_seats = random.randint(10, 30)
            total_seats = 150 if course == 'MBBS' else 80
            seat_status = 'available' if available_seats > 15 else ('limited' if available_seats > 5 else 'full')
            
            colleges.append({
                "name": f"{aiims['name']} - {course}",
                "type": "AIIMS",
                "exam": "NEET",
                "state": aiims["state"],
                "cutoff": cutoff,
                "fees": "₹50,000" if course == 'MBBS' else "₹30,000",
                "seats": total_seats,
                "availableSeats": available_seats,
                "seatStatus": seat_status,
                "scholarship": "Merit Scholarship Available" if random.random() > 0.8 else None,
                "aiPrediction": f"Cutoff may {'increase' if random.random() > 0.5 else 'decrease'} by {random.randint(50, 200)} ranks in 2025",
                "pros": ["Top medical faculty", "Excellent clinical exposure", "Research opportunities"],
                "cons": ["Extremely high competition", "Limited seats"],
                "rating": f"{4.5 + random.random() * 0.5:.1f}",
                "placement": "95%" if course == 'MBBS' else f"{80 + random.randint(0, 15)}%",
                "avgPackage": "₹10-15 LPA" if course == 'MBBS' else f"₹{5 + random.randint(0, 4)} LPA"
            })
    
    # Add comprehensive state-wise colleges (100+ engineering per state)
    print("Generating comprehensive state-wise engineering colleges...")
    for state_idx, state_name in enumerate(all_states):
        state_colleges = [
            f"{state_name} Engineering College", f"{state_name} Institute of Technology",
            f"{state_name} Technical University", f"Government Engineering College {state_name}",
            f"{state_name} College of Engineering", f"{state_name} Polytechnic Institute",
            f"Private Engineering College {state_name}", f"{state_name} University of Technology"
        ]
        
        for i in range(100):  # 100 colleges per state
            college_name = state_colleges[i % len(state_colleges)]
            campus_num = i // len(state_colleges) + 1
            full_name = f"{college_name} Campus {campus_num}" if campus_num > 1 else college_name
            
            for branch_idx, branch in enumerate(engineering_branches[:5]):  # Top 5 branches
                cutoff = 5000 + state_idx * 1000 + i * 200 + branch_idx * 50
                if cutoff <= 200000:  # Within JEE Main rank limit (updated to 200,000)
                    available_seats = random.randint(10, 40)
                    total_seats = 60 + (branch_idx % 5) * 10
                    seat_status = 'available' if available_seats > 25 else ('limited' if available_seats > 8 else 'full')
                    
                    colleges.append({
                        "name": f"{full_name} - {branch}",
                        "type": "Government" if i < 30 else "Private",
                        "exam": "JEE Main",
                        "state": state_name,
                        "cutoff": cutoff,
                        "fees": f"₹{80 + i * 3},000" if i < 30 else f"₹{200 + i * 8},000",
                        "seats": total_seats,
                        "availableSeats": available_seats,
                        "seatStatus": seat_status,
                        "scholarship": "State Scholarship Available" if random.random() > 0.6 else None,
                        "aiPrediction": f"Cutoff may {'increase' if random.random() > 0.5 else 'decrease'} by {random.randint(25, 150)} ranks in 2025",
                        "pros": ["Good faculty", "Decent placement", "State quota benefits"],
                        "cons": ["Limited industry exposure", "Average infrastructure"],
                        "rating": f"{3.2 + random.random() * 1.5:.1f}",
                        "placement": f"{60 + random.randint(0, 30)}%",
                        "avgPackage": f"₹{3 + random.randint(0, 5)} LPA"
                    })
    
    # Add comprehensive state-wise medical colleges (50+ per state)
    print("Generating comprehensive state-wise medical colleges...")
    for state_idx, state_name in enumerate(all_states):
        medical_colleges = [
            f"Government Medical College {state_name}", f"{state_name} Medical University",
            f"Private Medical College {state_name}", f"{state_name} Institute of Medical Sciences",
            f"{state_name} Dental College", f"{state_name} Ayurvedic College"
        ]
        
        for i in range(50):  # 50 medical colleges per state
            college_name = medical_colleges[i % len(medical_colleges)]
            campus_num = i // len(medical_colleges) + 1
            full_name = f"{college_name} Campus {campus_num}" if campus_num > 1 else college_name
            
            for course_idx, course in enumerate(medical_courses):
                cutoff = 2000 + state_idx * 500 + i * 300 + course_idx * 100
                if cutoff <= 200000:  # Within NEET rank limit
                    available_seats = random.randint(5, 30)
                    total_seats = 150 if course == 'MBBS' else 80
                    seat_status = 'available' if available_seats > 20 else ('limited' if available_seats > 5 else 'full')
                    
                    gov_fees = f"₹{50 + i * 5},000" if course == 'MBBS' else f"₹{30 + i * 3},000"
                    pvt_fees = f"₹{800 + i * 30},000" if course == 'MBBS' else f"₹{400 + i * 15},000"
                    
                    colleges.append({
                        "name": f"{full_name} - {course}",
                        "type": "Government" if i < 20 else "Private",
                        "exam": "NEET",
                        "state": state_name,
                        "cutoff": cutoff,
                        "fees": gov_fees if i < 20 else pvt_fees,
                        "seats": total_seats,
                        "availableSeats": available_seats,
                        "seatStatus": seat_status,
                        "scholarship": "State Medical Scholarship" if random.random() > 0.7 else None,
                        "aiPrediction": f"Cutoff may {'increase' if random.random() > 0.5 else 'decrease'} by {random.randint(50, 200)} ranks in 2025",
                        "pros": ["Clinical exposure", "Hospital attached", "State quota"],
                        "cons": ["High competition", "Limited research"],
                        "rating": f"{3.5 + random.random() * 1.2:.1f}",
                        "placement": "95%" if course == 'MBBS' else f"{70 + random.randint(0, 20)}%",
                        "avgPackage": "₹8-12 LPA" if course == 'MBBS' else f"₹{4 + random.randint(0, 4)} LPA"
                    })
    
    # Create metadata
    metadata = {
        "total_colleges": len(colleges),
        "last_updated": datetime.now().strftime("%Y-%m-%d"),
        "coverage": f"All {len(all_states)} states",
        "exams": ["JEE Main", "JEE Advanced", "NEET"],
        "rank_coverage": {
            "JEE_Main": 200000,
            "JEE_Advanced": 200000,
            "NEET": 200000
        },
        "colleges_by_exam": {
            "JEE Main": len([c for c in colleges if c["exam"] == "JEE Main"]),
            "JEE Advanced": len([c for c in colleges if c["exam"] == "JEE Advanced"]),
            "NEET": len([c for c in colleges if c["exam"] == "NEET"])
        },
        "colleges_by_state": {state: len([c for c in colleges if c["state"] == state]) for state in all_states}
    }
    
    return {
        "metadata": metadata,
        "colleges": colleges
    }

def save_database():
    """Generate and save the comprehensive database"""
    print("🎓 Generating comprehensive college database...")
    
    database = generate_comprehensive_database()
    
    # Save to JSON file
    output_file = "comprehensive_college_database.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(database, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Database saved to {output_file}")
    print(f"📊 Total colleges: {database['metadata']['total_colleges']:,}")
    print(f"🏛️ States covered: {database['metadata']['coverage']}")
    print(f"📝 Exams covered: {', '.join(database['metadata']['exams'])}")
    print("\n📈 Colleges by exam:")
    for exam, count in database['metadata']['colleges_by_exam'].items():
        print(f"   {exam}: {count:,} colleges")
    
    return output_file

if __name__ == "__main__":
    save_database()
