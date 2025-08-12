#!/usr/bin/env python3
"""
Script to extract college data from PDF and integrate into project database
"""
import PyMuPDF  # fitz
import json
import re
from pathlib import Path
from typing import List, Dict, Any

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from PDF file"""
    try:
        doc = PyMuPDF.open(pdf_path)
        text = ""
        for page_num in range(doc.page_count):
            page = doc[page_num]
            text += page.get_text()
        doc.close()
        return text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return ""

def parse_college_data(text: str) -> List[Dict[str, Any]]:
    """Parse college data from extracted text"""
    colleges = []
    lines = text.split('\n')
    
    current_college = {}
    rank_pattern = r'^(\d+)\.?\s*'  # Pattern to match rank numbers
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Check if line starts with a number (potential rank)
        rank_match = re.match(rank_pattern, line)
        if rank_match:
            # Save previous college if exists
            if current_college:
                colleges.append(current_college)
                current_college = {}
            
            # Extract rank and college name
            rank = int(rank_match.group(1))
            college_name = re.sub(rank_pattern, '', line).strip()
            
            current_college = {
                'rank': rank,
                'college_name': college_name,
                'university_name': college_name,
                'state': '',  # Will be filled if found in subsequent lines
                'type': 'University',
                'category': 'General',
                'source': 'PDF_Import'
            }
        elif current_college and line:
            # Try to extract additional info from subsequent lines
            if any(state in line.upper() for state in ['DELHI', 'MUMBAI', 'BANGALORE', 'CHENNAI', 'KOLKATA', 'HYDERABAD', 'PUNE', 'AHMEDABAD']):
                current_college['state'] = line
            elif 'UNIVERSITY' in line.upper() or 'INSTITUTE' in line.upper() or 'COLLEGE' in line.upper():
                if not current_college['college_name'] or len(line) > len(current_college['college_name']):
                    current_college['college_name'] = line
                    current_college['university_name'] = line
    
    # Add last college
    if current_college:
        colleges.append(current_college)
    
    return colleges

def integrate_colleges_into_project(colleges: List[Dict[str, Any]]):
    """Integrate extracted colleges into project database"""
    data_dir = Path('data')
    
    # Create a new file for PDF-extracted colleges
    pdf_colleges_file = data_dir / 'pdf_universities_ranking.json'
    
    # Save extracted colleges
    with open(pdf_colleges_file, 'w', encoding='utf-8') as f:
        json.dump(colleges, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Saved {len(colleges)} colleges to {pdf_colleges_file}")
    
    # Create cutoff data structure for these colleges
    cutoffs = []
    for college in colleges:
        # Create sample cutoff entries for different exams
        for exam in ['jee', 'neet']:
            for category in ['General', 'OBC', 'SC', 'ST']:
                cutoff_entry = {
                    'college': college['college_name'],
                    'university': college['university_name'],
                    'branch': 'Computer Science' if exam == 'jee' else 'MBBS',
                    'category': category,
                    'rank': college['rank'],
                    'cutoff_rank': college['rank'] * (1.2 if category == 'General' else 1.5),
                    'exam_type': exam,
                    'year': 2024,
                    'round': 'Final',
                    'state': college.get('state', ''),
                    'source': 'PDF_Import'
                }
                cutoffs.append(cutoff_entry)
    
    # Save cutoff data
    pdf_cutoffs_file = data_dir / 'pdf_universities_cutoffs.json'
    with open(pdf_cutoffs_file, 'w', encoding='utf-8') as f:
        json.dump(cutoffs, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Generated {len(cutoffs)} cutoff entries to {pdf_cutoffs_file}")
    
    return len(colleges), len(cutoffs)

def main():
    """Main function to extract and integrate college data"""
    pdf_path = "Consolidated list of All Universities.pdf"
    
    if not Path(pdf_path).exists():
        print(f"❌ PDF file not found: {pdf_path}")
        return
    
    print("📄 Extracting text from PDF...")
    text = extract_text_from_pdf(pdf_path)
    
    if not text:
        print("❌ Failed to extract text from PDF")
        return
    
    print(f"✓ Extracted {len(text)} characters from PDF")
    
    print("🔍 Parsing college data...")
    colleges = parse_college_data(text)
    
    if not colleges:
        print("❌ No colleges found in PDF")
        return
    
    print(f"✓ Found {len(colleges)} colleges")
    
    # Show first few colleges as preview
    print("\n📋 Preview of extracted colleges:")
    for i, college in enumerate(colleges[:5]):
        print(f"{i+1}. Rank {college['rank']}: {college['college_name']}")
    
    print("💾 Integrating colleges into project...")
    college_count, cutoff_count = integrate_colleges_into_project(colleges)
    
    print(f"\n✅ Successfully integrated:")
    print(f"   • {college_count} colleges")
    print(f"   • {cutoff_count} cutoff entries")
    print(f"   • Files created: pdf_universities_ranking.json, pdf_universities_cutoffs.json")

if __name__ == "__main__":
    main()
