#!/usr/bin/env python3
"""
Simple PDF extraction script for college data
"""
import PyMuPDF
import json
import re
from pathlib import Path

def extract_colleges_from_pdf():
    """Extract colleges from PDF with error handling"""
    pdf_path = "Consolidated list of All Universities.pdf"
    
    try:
        print(f"Opening PDF: {pdf_path}")
        doc = PyMuPDF.open(pdf_path)
        print(f"PDF has {doc.page_count} pages")
        
        all_text = ""
        for page_num in range(doc.page_count):
            page = doc[page_num]
            page_text = page.get_text()
            all_text += page_text + "\n"
            print(f"Extracted page {page_num + 1}")
        
        doc.close()
        
        # Save raw text for inspection
        with open("pdf_raw_text.txt", "w", encoding="utf-8") as f:
            f.write(all_text)
        print("Saved raw text to pdf_raw_text.txt")
        
        # Parse colleges
        colleges = []
        lines = all_text.split('\n')
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
                
            # Look for numbered entries (potential rankings)
            if re.match(r'^\d+\.?\s+', line):
                rank_match = re.match(r'^(\d+)\.?\s+(.*)', line)
                if rank_match:
                    rank = int(rank_match.group(1))
                    name = rank_match.group(2).strip()
                    
                    college = {
                        "rank": rank,
                        "college_name": name,
                        "university_name": name,
                        "type": "University",
                        "category": "General",
                        "source": "PDF_Ranking_List"
                    }
                    colleges.append(college)
        
        print(f"Found {len(colleges)} colleges")
        
        # Save colleges
        data_dir = Path("data")
        colleges_file = data_dir / "pdf_ranking_colleges.json"
        
        with open(colleges_file, "w", encoding="utf-8") as f:
            json.dump(colleges, f, indent=2, ensure_ascii=False)
        
        print(f"Saved colleges to {colleges_file}")
        
        # Show preview
        print("\nFirst 10 colleges:")
        for college in colleges[:10]:
            print(f"Rank {college['rank']}: {college['college_name']}")
            
        return colleges
        
    except Exception as e:
        print(f"Error: {e}")
        return []

if __name__ == "__main__":
    colleges = extract_colleges_from_pdf()
    print(f"\nTotal colleges extracted: {len(colleges)}")
