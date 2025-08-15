#!/usr/bin/env python3
"""
Simple script to combine NEET and JEE college data
"""
import json
import os
from pathlib import Path

def load_json(filepath):
    """Load JSON data from file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return []

def main():
    data_dir = Path('data')
    output_dir = Path('data/processed')
    output_dir.mkdir(exist_ok=True)
    
    # List of files to process
    neet_files = [
        'neet_massive_colleges.json',
        'neet_comprehensive_colleges.json',
        'neet_10000_colleges.json',
        'neet_1000_colleges.json',
        'careers360_neet_colleges.json'
    ]
    
    jee_files = [
        'jee_massive_colleges.json',
        'jee_comprehensive_colleges.json',
        'jee_10000_colleges.json',
        'jee_1000_colleges.json',
        'careers360_jee_colleges.json'
    ]
    
    combined = []
    seen = set()
    
    # Process NEET files
    for filename in neet_files:
        filepath = data_dir / filename
        if not filepath.exists():
            print(f"File not found: {filepath}")
            continue
            
        print(f"Processing {filename}...")
        data = load_json(filepath)
        if not isinstance(data, list):
            data = [data]
            
        for item in data:
            # Create a unique key for deduplication
            key = f"{item.get('name', '')}_{item.get('state', '')}"
            if key in seen:
                continue
                
            seen.add(key)
            item['exam_type'] = 'NEET'
            combined.append(item)
    
    # Process JEE files
    for filename in jee_files:
        filepath = data_dir / filename
        if not filepath.exists():
            print(f"File not found: {filepath}")
            continue
            
        print(f"Processing {filename}...")
        data = load_json(filepath)
        if not isinstance(data, list):
            data = [data]
            
        for item in data:
            # Create a unique key for deduplication
            key = f"{item.get('name', '')}_{item.get('state', '')}"
            if key in seen:
                continue
                
            seen.add(key)
            item['exam_type'] = 'JEE'
            combined.append(item)
    
    # Save combined data
    output_path = output_dir / 'combined_colleges.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(combined, f, indent=2)
    
    print(f"\nCombined {len(combined)} colleges into {output_path}")
    
    # Print summary
    neet_count = sum(1 for c in combined if c.get('exam_type') == 'NEET')
    jee_count = sum(1 for c in combined if c.get('exam_type') == 'JEE')
    
    print(f"- NEET colleges: {neet_count}")
    print(f"- JEE colleges: {jee_count}")

if __name__ == "__main__":
    main()
