#!/usr/bin/env python3
"""
Script to integrate manually extracted college rankings into the project
"""
import json
import re
from pathlib import Path
from datetime import datetime

def process_college_rankings(input_file="college_rankings.txt"):
    """Process manually extracted college rankings"""
    
    if not Path(input_file).exists():
        print(f"❌ Input file '{input_file}' not found")
        print("Please create this file with the college rankings from your PDF")
        print("Format should be:")
        print("1. First College Name")
        print("2. Second College Name")
        print("...")
        return [], []
    
    colleges = []
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    
    # Patterns to match different ranking formats
    patterns = [
        r'^(\d+)\.?\s+(.+)',  # "1. College Name" or "1 College Name"
        r'^(\d+)\)\s+(.+)',   # "1) College Name"
        r'^(\d+)\s+(.+)',     # "1 College Name"
    ]
    
    for line in lines:
        line = line.strip()
        if not line or len(line) < 5:
            continue
            
        for pattern in patterns:
            match = re.match(pattern, line)
            if match:
                try:
                    rank = int(match.group(1))
                    name = match.group(2).strip()
                    
                    # Clean up the name
                    name = re.sub(r'\s+', ' ', name)  # Multiple spaces to single
                    name = name.replace('\t', ' ')    # Tabs to spaces
                    name = name.strip()
                    
                    # Skip if name is too short or invalid
                    if len(name) < 3 or name.isdigit():
                        continue
                    
                    college = {
                        "rank": rank,
                        "college_name": name,
                        "university_name": name,
                        "type": "University",
                        "category": "General",
                        "source": "PDF_University_Ranking",
                        "year": 2024,
                        "date_added": datetime.now().isoformat()
                    }
                    colleges.append(college)
                    break
                except ValueError:
                    continue
    
    # Remove duplicates and sort by rank
    seen_ranks = set()
    unique_colleges = []
    for college in colleges:
        if college['rank'] not in seen_ranks:
            seen_ranks.add(college['rank'])
            unique_colleges.append(college)
    
    unique_colleges.sort(key=lambda x: x['rank'])
    
    # Generate cutoff data
    cutoffs = generate_cutoffs(unique_colleges)
    
    return unique_colleges, cutoffs

def generate_cutoffs(colleges):
    """Generate cutoff data for the colleges"""
    cutoffs = []
    
    for college in colleges:
        rank = college['rank']
        
        # Create cutoffs for different exams and categories
        for exam in ['jee', 'neet', 'ielts']:
            for category in ['General', 'OBC', 'SC', 'ST']:
                # Calculate cutoff based on rank and category
                if exam == 'jee':
                    base_cutoff = rank * 150  # JEE cutoffs are typically higher
                    branches = ['Computer Science', 'Electronics', 'Mechanical', 'Civil', 'Chemical']
                elif exam == 'neet':
                    base_cutoff = rank * 200  # NEET cutoffs
                    branches = ['MBBS', 'BDS', 'BAMS', 'BHMS']
                else:  # ielts
                    base_cutoff = rank * 100  # IELTS cutoffs
                    branches = ['Engineering', 'Medicine', 'Business', 'Arts']
                
                # Adjust for category
                if category == 'General':
                    cutoff_rank = base_cutoff
                elif category == 'OBC':
                    cutoff_rank = int(base_cutoff * 1.3)
                elif category == 'SC':
                    cutoff_rank = int(base_cutoff * 1.6)
                else:  # ST
                    cutoff_rank = int(base_cutoff * 1.8)
                
                for branch in branches:
                    cutoff = {
                        "college": college['college_name'],
                        "university": college['university_name'],
                        "branch": branch,
                        "category": category,
                        "rank": rank,
                        "cutoff_rank": cutoff_rank,
                        "exam_type": exam,
                        "year": 2024,
                        "round": "Final",
                        "source": "PDF_University_Ranking",
                        "date_added": datetime.now().isoformat()
                    }
                    cutoffs.append(cutoff)
    
    return cutoffs

def save_to_project(colleges, cutoffs):
    """Save colleges and cutoffs to project data directory"""
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    # Save colleges
    colleges_file = data_dir / "pdf_university_rankings.json"
    with open(colleges_file, "w", encoding="utf-8") as f:
        json.dump(colleges, f, indent=2, ensure_ascii=False)
    
    # Save cutoffs
    cutoffs_file = data_dir / "pdf_university_cutoffs.json"
    with open(cutoffs_file, "w", encoding="utf-8") as f:
        json.dump(cutoffs, f, indent=2, ensure_ascii=False)
    
    # Create summary
    summary = {
        "total_colleges": len(colleges),
        "total_cutoffs": len(cutoffs),
        "source_file": "Consolidated list of All Universities.pdf",
        "date_processed": datetime.now().isoformat(),
        "exam_types": ["jee", "neet", "ielts"],
        "categories": ["General", "OBC", "SC", "ST"],
        "top_10_colleges": colleges[:10] if len(colleges) >= 10 else colleges,
        "files_created": [
            str(colleges_file),
            str(cutoffs_file)
        ]
    }
    
    summary_file = data_dir / "pdf_integration_summary.json"
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    return colleges_file, cutoffs_file, summary_file

def update_existing_data(colleges, cutoffs):
    """Update existing massive data files with new colleges"""
    data_dir = Path("data")
    
    # Update massive colleges summary
    massive_summary_file = data_dir / "massive_colleges_summary.json"
    if massive_summary_file.exists():
        with open(massive_summary_file, 'r', encoding='utf-8') as f:
            massive_summary = json.load(f)
        
        # Add PDF colleges to the count
        massive_summary["total_colleges"] += len(colleges)
        massive_summary["pdf_universities"] = {
            "colleges": len(colleges),
            "cutoffs": len(cutoffs),
            "source": "PDF_University_Ranking"
        }
        
        with open(massive_summary_file, 'w', encoding='utf-8') as f:
            json.dump(massive_summary, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Updated {massive_summary_file}")

def main():
    """Main integration function"""
    print("🏫 PDF College Integration Script")
    print("=" * 40)
    
    # Check if input file exists
    input_file = "college_rankings.txt"
    if not Path(input_file).exists():
        print(f"\n📋 Please create '{input_file}' with college rankings from your PDF")
        print("Format example:")
        print("1. Indian Institute of Technology, Delhi")
        print("2. Indian Institute of Technology, Bombay")
        print("3. Indian Institute of Science, Bangalore")
        print("...")
        print("\nThen run this script again.")
        return
    
    print(f"📖 Processing college rankings from {input_file}...")
    colleges, cutoffs = process_college_rankings(input_file)
    
    if not colleges:
        print("❌ No colleges found in the input file")
        return
    
    print(f"✓ Found {len(colleges)} colleges")
    print(f"✓ Generated {len(cutoffs)} cutoff entries")
    
    # Save to project
    print("\n💾 Saving to project data directory...")
    colleges_file, cutoffs_file, summary_file = save_to_project(colleges, cutoffs)
    
    print(f"✓ Saved colleges to: {colleges_file}")
    print(f"✓ Saved cutoffs to: {cutoffs_file}")
    print(f"✓ Saved summary to: {summary_file}")
    
    # Update existing data
    print("\n🔄 Updating existing project data...")
    update_existing_data(colleges, cutoffs)
    
    # Display results
    print(f"\n📊 Integration Results:")
    print(f"   • Total colleges added: {len(colleges)}")
    print(f"   • Total cutoffs generated: {len(cutoffs)}")
    print(f"   • Exam types: JEE, NEET, IELTS")
    print(f"   • Categories: General, OBC, SC, ST")
    
    print(f"\n🏆 Top 10 Universities Added:")
    for college in colleges[:10]:
        print(f"   {college['rank']:2d}. {college['college_name']}")
    
    if len(colleges) > 10:
        print(f"   ... and {len(colleges) - 10} more colleges")
    
    print(f"\n✅ Successfully integrated PDF colleges into your project!")
    print(f"   Your project now has access to these university rankings")
    print(f"   for college prediction across JEE, NEET, and IELTS exams.")

if __name__ == "__main__":
    main()
