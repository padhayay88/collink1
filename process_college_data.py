#!/usr/bin/env python3
"""
Script to process and organize college data by rank, state, and category
"""
import os
import json
import csv
import pandas as pd
from pathlib import Path
from typing import Dict, List, Any, Optional

class CollegeDataProcessor:
    def __init__(self, data_dir: str = 'data'):
        self.data_dir = Path(data_dir)
        self.colleges = []
        self.processed_data = {
            'by_rank': {},
            'by_state': {},
            'by_category': {}
        }
    
    def load_comprehensive_colleges(self) -> List[Dict[str, Any]]:
        """Load colleges from the comprehensive CSV file"""
        csv_path = self.data_dir / 'comprehensive_colleges_list.csv'
        if not csv_path.exists():
            csv_path = Path('comprehensive_colleges_list.csv')
            
        if not csv_path.exists():
            print(f"Error: Comprehensive colleges CSV not found at {csv_path}")
            return []
            
        try:
            df = pd.read_csv(csv_path)
            return df.to_dict('records')
        except Exception as e:
            print(f"Error loading comprehensive colleges: {e}")
            return []
    
    def load_json_data(self, filename: str) -> List[Dict[str, Any]]:
        """Load data from a JSON file"""
        try:
            filepath = self.data_dir / filename
            if not filepath.exists():
                filepath = Path(filename)
                if not filepath.exists():
                    print(f"File not found: {filename}")
                    return []
                    
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except Exception as e:
            print(f"Error loading {filename}: {e}")
            return []
    
    def process_colleges(self):
        """Process all college data and organize it"""
        print("Loading college data...")
        
        # Load comprehensive colleges first
        self.colleges = self.load_comprehensive_colleges()
        
        # Load additional college data from JSON files
        json_files = [
            'careers360_jee_colleges.json',
            'careers360_neet_colleges.json',
            'jee_1000_colleges.json',
            'neet_1000_colleges.json',
            'ielts_1000_colleges.json'
        ]
        
        for json_file in json_files:
            additional_colleges = self.load_json_data(json_file)
            if additional_colleges:
                self.colleges.extend(additional_colleges)
        
        print(f"Loaded {len(self.colleges)} colleges in total")
        
        # Process and organize the data
        self._organize_by_rank()
        self._organize_by_state()
        self._organize_by_category()
        
        return self.processed_data
    
    def _organize_by_rank(self):
        """Organize colleges by their ranking"""
        print("Organizing colleges by rank...")
        
        # Sort colleges by ranking (convert to int for proper numeric sorting)
        ranked_colleges = []
        for college in self.colleges:
            try:
                if 'Ranking' in college and str(college['Ranking']).isdigit():
                    college['rank'] = int(college['Ranking'])
                    ranked_colleges.append(college)
                elif 'rank' in college and str(college['rank']).isdigit():
                    college['rank'] = int(college['rank'])
                    ranked_colleges.append(college)
            except (ValueError, TypeError):
                continue
        
        # Sort by rank
        ranked_colleges.sort(key=lambda x: x.get('rank', float('inf')))
        
        # Group by rank ranges
        rank_ranges = [
            (1, 10, "Top 10"),
            (11, 50, "11-50"),
            (51, 100, "51-100"),
            (101, 200, "101-200"),
            (201, 500, "201-500"),
            (501, 1000, "501-1000"),
            (1001, float('inf'), "1000+")
        ]
        
        for min_rank, max_rank, range_name in rank_ranges:
            self.processed_data['by_rank'][range_name] = [
                c for c in ranked_colleges 
                if min_rank <= c.get('rank', float('inf')) <= max_rank
            ]
    
    def _organize_by_state(self):
        """Organize colleges by state"""
        print("Organizing colleges by state...")
        
        for college in self.colleges:
            state = college.get('State/UT') or college.get('state') or 'Unknown'
            if state not in self.processed_data['by_state']:
                self.processed_data['by_state'][state] = []
            self.processed_data['by_state'][state].append(college)
    
    def _organize_by_category(self):
        """Organize colleges by category"""
        print("Organizing colleges by category...")
        
        for college in self.colleges:
            # Determine category (Engineering, Medical, etc.)
            category = college.get('Category') or college.get('category') or 'Other'
            exam_type = college.get('Exam Type') or college.get('exam_type') or 'Other'
            
            # Map exam type to broader category if needed
            if exam_type in ['JEE Advanced', 'JEE Main']:
                category = 'Engineering'
            elif exam_type == 'NEET':
                category = 'Medical'
            
            if category not in self.processed_data['by_category']:
                self.processed_data['by_category'][category] = []
            self.processed_data['by_category'][category].append(college)
    
    def save_processed_data(self, output_dir: str = 'data/processed'):
        """Save the processed data to JSON files"""
        os.makedirs(output_dir, exist_ok=True)
        
        # Save by rank
        with open(f"{output_dir}/colleges_by_rank.json", 'w', encoding='utf-8') as f:
            json.dump(self.processed_data['by_rank'], f, indent=2)
        
        # Save by state
        with open(f"{output_dir}/colleges_by_state.json", 'w', encoding='utf-8') as f:
            json.dump(self.processed_data['by_state'], f, indent=2)
        
        # Save by category
        with open(f"{output_dir}/colleges_by_category.json", 'w', encoding='utf-8') as f:
            json.dump(self.processed_data['by_category'], f, indent=2)
        
        print(f"Processed data saved to {output_dir}/")

def main():
    # Initialize the processor
    processor = CollegeDataProcessor()
    
    # Process the data
    processed_data = processor.process_colleges()
    
    # Save the processed data
    processor.save_processed_data()
    
    # Print some statistics
    print("\nData Processing Complete!")
    print(f"Total colleges processed: {len(processor.colleges)}")
    print("\nColleges by rank range:")
    for rank_range, colleges in processed_data['by_rank'].items():
        print(f"- {rank_range}: {len(colleges)} colleges")
    
    print("\nTop 5 states with most colleges:")
    states_by_count = sorted(
        [(state, len(colleges)) for state, colleges in processed_data['by_state'].items()],
        key=lambda x: x[1], 
        reverse=True
    )
    for state, count in states_by_count[:5]:
        print(f"- {state}: {count} colleges")
    
    print("\nColleges by category:")
    for category, colleges in processed_data['by_category'].items():
        print(f"- {category}: {len(colleges)} colleges")

if __name__ == "__main__":
    main()
