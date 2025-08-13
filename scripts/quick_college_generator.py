#!/usr/bin/env python3
"""
Quick College Generator - Add 4000+ colleges to the database
"""

import json
import random

def generate_quick_colleges():
    """Generate 4000+ colleges quickly"""
    colleges = []
    
    # Load existing colleges
    try:
        with open('frontend/public/data/comprehensive_colleges.json', 'r', encoding='utf-8') as f:
            colleges = json.load(f)
    except:
        colleges = []
    
    print(f"Starting with {len(colleges)} existing colleges")
    
    states = [
        "Andhra Pradesh", "Assam", "Bihar", "Chhattisgarh", "Goa", "Gujarat",
        "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka", "Kerala",
        "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram",
        "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu",
        "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal", "Delhi"
    ]
    
    # Generate JEE Main colleges (2000)
    for i in range(2000):
        cutoff = 5000 + (i * 50)
        colleges.append({
            "name": f"Engineering College {i+1} - Computer Science",
            "rank": 100 + i,
            "type": "Engineering",
            "exam_type": "JEE Main",
            "state": states[i % len(states)],
            "cutoff_jee_main": cutoff,
            "cutoff_jee_advanced": None,
            "cutoff_neet": None,
            "fees": f"₹{random.randint(200, 800)},000",
            "seats": random.randint(60, 120),
            "branches": ["Computer Science"],
            "source": "Generated"
        })
    
    # Generate JEE Advanced colleges (500)
    for i in range(500):
        cutoff = 1000 + (i * 20)
        colleges.append({
            "name": f"Premium Engineering Institute {i+1} - Electronics",
            "rank": 10 + i,
            "type": "Premium",
            "exam_type": "JEE Advanced",
            "state": states[i % len(states)],
            "cutoff_jee_advanced": cutoff,
            "cutoff_jee_main": None,
            "cutoff_neet": None,
            "fees": f"₹{random.randint(300, 600)},000",
            "seats": random.randint(40, 80),
            "branches": ["Electronics"],
            "source": "Generated"
        })
    
    # Generate NEET colleges (1500)
    for i in range(1500):
        cutoff = 2000 + (i * 100)
        colleges.append({
            "name": f"Medical College {i+1} - MBBS",
            "rank": 20 + i,
            "type": "Medical",
            "exam_type": "NEET",
            "state": states[i % len(states)],
            "cutoff_neet": cutoff,
            "cutoff_jee_main": None,
            "cutoff_jee_advanced": None,
            "fees": f"₹{random.randint(500, 2000)},000",
            "seats": random.randint(50, 100),
            "specializations": ["MBBS"],
            "source": "Generated"
        })
    
    # Save updated database
    with open('frontend/public/data/comprehensive_colleges.json', 'w', encoding='utf-8') as f:
        json.dump(colleges, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Generated {len(colleges)} total colleges!")
    
    # Count by exam type
    jee_main = len([c for c in colleges if c.get('exam_type') == 'JEE Main'])
    jee_advanced = len([c for c in colleges if c.get('exam_type') == 'JEE Advanced'])
    neet = len([c for c in colleges if c.get('exam_type') == 'NEET'])
    
    print(f"📊 JEE Main: {jee_main}")
    print(f"📊 JEE Advanced: {jee_advanced}")
    print(f"📊 NEET: {neet}")

if __name__ == "__main__":
    generate_quick_colleges()
