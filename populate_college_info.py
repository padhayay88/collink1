#!/usr/bin/env python3
"""
Script to populate college_info_enhanced.json with college data from other files
"""

import json
import os
from collections import defaultdict

def load_json_file(filepath):
    """Load and parse a JSON file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return []

def populate_college_info_enhanced():
    """Populate college_info_enhanced.json with data from other files"""
    
    # Load data from various sources
    sources = [
        ('data/college_info.json', 'college_info'),
        ('data/jee_10000_colleges.json', 'jee_colleges'),
        ('data/neet_10000_colleges.json', 'neet_colleges'),
        ('data/ielts_10000_colleges.json', 'ielts_colleges'),
        ('data/jee_comprehensive_colleges.json', 'jee_comprehensive'),
        ('data/neet_comprehensive_colleges.json', 'neet_comprehensive'),
        ('data/ielts_massive_colleges.json', 'ielts_massive'),
        ('data/careers360_jee_colleges.json', 'careers360_jee'),
        ('data/careers360_neet_colleges.json', 'careers360_neet'),
    ]
    
    all_colleges = []
    college_names = set()
    
    print("Loading college data from various sources...")
    
    for filepath, source_name in sources:
        if os.path.exists(filepath):
            data = load_json_file(filepath)
            print(f"  {source_name}: {len(data)} colleges")
            
            for college in data:
                # Extract college name
                college_name = college.get('college', college.get('university', college.get('name', '')))
                if not college_name:
                    continue
                
                # Skip if we already have this college
                if college_name in college_names:
                    continue
                
                college_names.add(college_name)
                
                # Create enhanced college entry
                enhanced_college = {
                    'college': college_name,
                    'university': college_name,
                    'source_files': [source_name],
                    'exam_types': [],
                    'branches': [],
                    'locations': [],
                    'categories': set(),
                    'quotas': set()
                }
                
                # Extract exam types
                if 'jee' in source_name.lower():
                    enhanced_college['exam_types'].append('jee')
                if 'neet' in source_name.lower():
                    enhanced_college['exam_types'].append('neet')
                if 'ielts' in source_name.lower():
                    enhanced_college['exam_types'].append('ielts')
                
                # Extract branches
                branch = college.get('branch', college.get('course', ''))
                if branch and branch not in enhanced_college['branches']:
                    enhanced_college['branches'].append(branch)
                
                # Extract location
                location = college.get('location', college.get('city', college.get('state', '')))
                if location and location not in enhanced_college['locations']:
                    enhanced_college['locations'].append(location)
                
                # Extract category and quota
                category = college.get('category', '')
                if category:
                    enhanced_college['categories'].add(category)
                
                quota = college.get('quota', '')
                if quota:
                    enhanced_college['quotas'].add(quota)
                
                # Add any additional fields
                for key, value in college.items():
                    if key not in ['college', 'university', 'name', 'branch', 'course', 'location', 'city', 'state', 'category', 'quota']:
                        if key not in enhanced_college:
                            enhanced_college[key] = value
                
                all_colleges.append(enhanced_college)
        else:
            print(f"  {source_name}: File not found")
    
    # Convert sets to lists for JSON serialization
    for college in all_colleges:
        college['categories'] = list(college['categories'])
        college['quotas'] = list(college['quotas'])
    
    print(f"\nTotal unique colleges found: {len(all_colleges)}")
    
    # Save to college_info_enhanced.json
    output_file = 'data/college_info_enhanced.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_colleges, f, indent=2, ensure_ascii=False)
    
    print(f"Saved {len(all_colleges)} colleges to {output_file}")
    
    # Show some sample colleges
    print("\nSample colleges:")
    for i, college in enumerate(all_colleges[:5]):
        print(f"  {i+1}. {college['college']}")
        print(f"     Exam types: {college['exam_types']}")
        print(f"     Branches: {college['branches']}")
        print(f"     Locations: {college['locations']}")
        print()
    
    return all_colleges

if __name__ == "__main__":
    populate_college_info_enhanced()
