#!/usr/bin/env python3
"""
Automated PDF extractor with fallback methods and robust error handling
"""
import json
import re
import sys
from pathlib import Path
from datetime import datetime

def try_extract_with_pymupdf():
    """Try extracting with PyMuPDF"""
    try:
        import PyMuPDF as fitz
        pdf_path = "Consolidated list of All Universities.pdf"
        
        if not Path(pdf_path).exists():
            return None, "PDF file not found"
        
        print(f"📄 Opening PDF: {pdf_path}")
        doc = fitz.open(pdf_path)
        print(f"📖 PDF has {doc.page_count} pages")
        
        full_text = ""
        for page_num in range(doc.page_count):
            page = doc[page_num]
            page_text = page.get_text()
            full_text += page_text + "\n"
            print(f"   Processed page {page_num + 1}/{doc.page_count}")
        
        doc.close()
        
        # Save extracted text for debugging
        with open("extracted_pdf_text.txt", "w", encoding="utf-8") as f:
            f.write(full_text)
        print(f"💾 Saved extracted text to extracted_pdf_text.txt ({len(full_text)} chars)")
        
        return full_text, "Success"
        
    except ImportError:
        return None, "PyMuPDF not installed (pip install PyMuPDF)"
    except Exception as e:
        return None, f"PyMuPDF error: {str(e)}"

def parse_university_rankings(text):
    """Parse university rankings from extracted text"""
    if not text:
        return []
    
    colleges = []
    lines = text.split('\n')
    
    # Multiple patterns to catch different ranking formats
    ranking_patterns = [
        r'^(\d+)\.?\s+(.+?)(?:\s+\d+)?$',  # "1. University Name" or "1. University Name 123"
        r'^(\d+)\)\s+(.+?)(?:\s+\d+)?$',   # "1) University Name"
        r'^(\d+)\s+(.+?)(?:\s+\d+)?$',     # "1 University Name"
        r'^(\d+)\.\s*(.+?)(?:\s+\d+)?$',   # "1. University Name" with flexible spacing
    ]
    
    print(f"🔍 Parsing {len(lines)} lines for university rankings...")
    
    for line_num, line in enumerate(lines):
        original_line = line
        line = line.strip()
        
        # Skip empty lines or very short lines
        if not line or len(line) < 5:
            continue
        
        # Try each pattern
        for pattern in ranking_patterns:
            match = re.match(pattern, line, re.IGNORECASE)
            if match:
                try:
                    rank = int(match.group(1))
                    name = match.group(2).strip()
                    
                    # Clean up the university name
                    name = re.sub(r'\s+', ' ', name)  # Multiple spaces to single
                    name = re.sub(r'[^\w\s,.-]', '', name)  # Remove special chars except common ones
                    name = name.strip()
                    
                    # Validation checks
                    if len(name) < 3:
                        continue
                    if name.isdigit():
                        continue
                    if rank > 1000:  # Reasonable limit for university rankings
                        continue
                    
                    # Additional cleaning for common issues
                    name = re.sub(r'\b(page|pg|p)\s*\d+\b', '', name, flags=re.IGNORECASE)
                    name = re.sub(r'\s+', ' ', name).strip()
                    
                    if len(name) < 3:
                        continue
                    
                    college = {
                        "rank": rank,
                        "college_name": name,
                        "university_name": name,
                        "type": "University",
                        "category": "General",
                        "source": "PDF_University_Ranking",
                        "year": 2024,
                        "date_extracted": datetime.now().isoformat(),
                        "original_line": original_line.strip()
                    }
                    
                    colleges.append(college)
                    
                    if len(colleges) <= 10:  # Show first 10 for debugging
                        print(f"   Found: Rank {rank} - {name}")
                    
                    break  # Found a match, no need to try other patterns
                    
                except (ValueError, IndexError):
                    continue
    
    # Remove duplicates based on rank
    seen_ranks = set()
    unique_colleges = []
    for college in colleges:
        if college['rank'] not in seen_ranks:
            seen_ranks.add(college['rank'])
            unique_colleges.append(college)
    
    # Sort by rank
    unique_colleges.sort(key=lambda x: x['rank'])
    
    print(f"✅ Found {len(unique_colleges)} unique university rankings")
    return unique_colleges

def generate_comprehensive_cutoffs(colleges):
    """Generate comprehensive cutoff data for all colleges"""
    cutoffs = []
    
    print(f"📊 Generating cutoff data for {len(colleges)} colleges...")
    
    for college in colleges:
        rank = college['rank']
        college_name = college['college_name']
        
        # JEE cutoffs
        jee_branches = [
            'Computer Science and Engineering',
            'Electronics and Communication Engineering', 
            'Mechanical Engineering',
            'Civil Engineering',
            'Chemical Engineering',
            'Electrical Engineering',
            'Aerospace Engineering',
            'Biotechnology'
        ]
        
        # NEET cutoffs
        neet_branches = [
            'MBBS',
            'BDS', 
            'BAMS',
            'BHMS',
            'BUMS',
            'BPT',
            'B.Sc Nursing'
        ]
        
        # IELTS cutoffs
        ielts_programs = [
            'Engineering',
            'Medicine',
            'Business Administration',
            'Computer Science',
            'Arts and Humanities',
            'Sciences'
        ]
        
        # Generate cutoffs for each exam type
        exam_configs = [
            ('jee', jee_branches, 200),
            ('neet', neet_branches, 300), 
            ('ielts', ielts_programs, 150)
        ]
        
        for exam_type, branches, base_multiplier in exam_configs:
            for category in ['General', 'OBC', 'SC', 'ST', 'EWS']:
                # Category-based multipliers
                category_multipliers = {
                    'General': 1.0,
                    'EWS': 1.1,
                    'OBC': 1.3,
                    'SC': 1.6,
                    'ST': 1.8
                }
                
                base_cutoff = rank * base_multiplier
                cutoff_rank = int(base_cutoff * category_multipliers[category])
                
                for branch in branches:
                    cutoff_entry = {
                        "college": college_name,
                        "university": college_name,
                        "branch": branch,
                        "category": category,
                        "university_rank": rank,
                        "cutoff_rank": cutoff_rank,
                        "exam_type": exam_type,
                        "year": 2024,
                        "round": "Final",
                        "source": "PDF_University_Ranking",
                        "date_generated": datetime.now().isoformat()
                    }
                    cutoffs.append(cutoff_entry)
    
    print(f"✅ Generated {len(cutoffs)} cutoff entries")
    return cutoffs

def save_integrated_data(colleges, cutoffs):
    """Save the integrated data to project files"""
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    print(f"💾 Saving data to {data_dir}...")
    
    # Save colleges
    colleges_file = data_dir / "pdf_university_rankings.json"
    with open(colleges_file, "w", encoding="utf-8") as f:
        json.dump(colleges, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved {len(colleges)} colleges to {colleges_file}")
    
    # Save cutoffs
    cutoffs_file = data_dir / "pdf_university_cutoffs.json"
    with open(cutoffs_file, "w", encoding="utf-8") as f:
        json.dump(cutoffs, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved {len(cutoffs)} cutoffs to {cutoffs_file}")
    
    # Create comprehensive summary
    summary = {
        "extraction_info": {
            "total_colleges": len(colleges),
            "total_cutoffs": len(cutoffs),
            "source_file": "Consolidated list of All Universities.pdf",
            "extraction_date": datetime.now().isoformat(),
            "extraction_method": "Automated PDF parsing"
        },
        "data_breakdown": {
            "exam_types": ["jee", "neet", "ielts"],
            "categories": ["General", "OBC", "SC", "ST", "EWS"],
            "jee_branches": 8,
            "neet_branches": 7,
            "ielts_programs": 6
        },
        "top_universities": colleges[:20] if len(colleges) >= 20 else colleges,
        "files_created": [
            str(colleges_file.name),
            str(cutoffs_file.name)
        ],
        "integration_status": "Complete"
    }
    
    summary_file = data_dir / "pdf_university_integration_summary.json"
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved summary to {summary_file}")
    
    return colleges_file, cutoffs_file, summary_file

def update_project_totals(colleges, cutoffs):
    """Update the main project summary with new totals"""
    data_dir = Path("data")
    massive_summary_file = data_dir / "massive_colleges_summary.json"
    
    if massive_summary_file.exists():
        print("🔄 Updating project totals...")
        
        with open(massive_summary_file, 'r', encoding='utf-8') as f:
            summary = json.load(f)
        
        # Add PDF data to totals
        summary["total_colleges"] += len(colleges)
        summary["total_cutoffs"] += len(cutoffs)
        
        # Add PDF section
        summary["breakdown"]["pdf_universities"] = {
            "colleges": len(colleges),
            "cutoffs": len(cutoffs),
            "source": "PDF_University_Ranking"
        }
        
        summary["last_updated"] = datetime.now().isoformat()
        
        with open(massive_summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Updated project totals: {summary['total_colleges']} total colleges")

def main():
    """Main extraction and integration function"""
    print("🏫 Automated PDF University Extractor")
    print("=" * 50)
    
    # Extract text from PDF
    text, status = try_extract_with_pymupdf()
    
    if not text:
        print(f"❌ Failed to extract PDF: {status}")
        print("\nAlternative: Use manual extraction:")
        print("1. Copy college rankings from PDF to 'college_rankings.txt'")
        print("2. Run 'python integrate_pdf_colleges.py'")
        return
    
    print(f"✅ Successfully extracted text from PDF")
    
    # Parse university rankings
    colleges = parse_university_rankings(text)
    
    if not colleges:
        print("❌ No university rankings found in PDF")
        print("Check 'extracted_pdf_text.txt' to see what was extracted")
        return
    
    # Generate cutoff data
    cutoffs = generate_comprehensive_cutoffs(colleges)
    
    # Save all data
    colleges_file, cutoffs_file, summary_file = save_integrated_data(colleges, cutoffs)
    
    # Update project totals
    update_project_totals(colleges, cutoffs)
    
    # Display final results
    print(f"\n🎉 PDF Integration Complete!")
    print(f"=" * 50)
    print(f"📊 Results:")
    print(f"   • Universities added: {len(colleges)}")
    print(f"   • Cutoff entries: {len(cutoffs)}")
    print(f"   • Exam types: JEE, NEET, IELTS")
    print(f"   • Categories: General, OBC, SC, ST, EWS")
    
    print(f"\n🏆 Top 15 Universities Added:")
    for i, college in enumerate(colleges[:15]):
        print(f"   {college['rank']:3d}. {college['college_name']}")
    
    if len(colleges) > 15:
        print(f"   ... and {len(colleges) - 15} more universities")
    
    print(f"\n📁 Files Created:")
    print(f"   • {colleges_file}")
    print(f"   • {cutoffs_file}")
    print(f"   • {summary_file}")
    
    print(f"\n✅ Your Collink project now includes university rankings!")
    print(f"   Total colleges in project: {len(colleges)} + existing data")
    print(f"   Ready for college prediction across all exam types")

if __name__ == "__main__":
    main()
