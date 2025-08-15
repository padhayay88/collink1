import fitz  # PyMuPDF
import json
import os
from pathlib import Path
import re
from typing import List, Dict, Any

def extract_colleges_from_pdf(pdf_path: str) -> List[Dict[str, Any]]:
    """Extract college data and ranks from PDF"""
    colleges = []
    
    try:
        doc = fitz.open(pdf_path)
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text()
            
            # Extract university rankings using regex patterns
            patterns = [
                r'(\d+)\.\s*([A-Za-z\s&,.-]+(?:University|Institute|College))',
                r'(\d+)\s+([A-Za-z\s&,.-]+(?:University|Institute|College))',
                r'Rank\s*(\d+)[:\s]*([A-Za-z\s&,.-]+)'
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                for match in matches:
                    rank = int(match[0])
                    name = match[1].strip()
                    
                    if rank <= 100 and len(name) > 5:  # Filter reasonable entries
                        colleges.append({
                            "name": name,
                            "rank": rank,
                            "type": "University",
                            "source": "PDF_Extract"
                        })
        
        doc.close()
        
    except Exception as e:
        print(f"Error extracting from PDF: {e}")
    
    # Remove duplicates and sort by rank
    unique_colleges = {}
    for college in colleges:
        key = college["name"].lower()
        if key not in unique_colleges or college["rank"] < unique_colleges[key]["rank"]:
            unique_colleges[key] = college
    
    return sorted(list(unique_colleges.values()), key=lambda x: x["rank"])

def generate_cutoff_data(colleges: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Generate cutoff data for extracted colleges"""
    cutoffs = []
    
    for college in colleges:
        rank = college["rank"]
        base_cutoff = rank * 100  # Base cutoff calculation
        
        # Generate cutoffs for different categories and exams
        for exam in ["JEE", "NEET"]:
            for category in ["General", "OBC", "SC", "ST", "EWS"]:
                multiplier = {"General": 1.0, "OBC": 1.2, "SC": 1.5, "ST": 1.5, "EWS": 1.1}[category]
                
                cutoffs.append({
                    "college": college["name"],
                    "exam": exam,
                    "category": category,
                    "opening_rank": int(base_cutoff * 0.8 * multiplier),
                    "closing_rank": int(base_cutoff * multiplier),
                    "quota": "All India",
                    "branch": "General" if exam == "NEET" else "Computer Science",
                    "source": "PDF_Generated"
                })
    
    return cutoffs

if __name__ == "__main__":
    pdf_path = "../../Consolidated list of All Universities.pdf"
    
    if os.path.exists(pdf_path):
        print("Extracting colleges from PDF...")
        colleges = extract_colleges_from_pdf(pdf_path)
        
        print(f"Extracted {len(colleges)} colleges")
        
        # Generate cutoff data
        cutoffs = generate_cutoff_data(colleges)
        
        # Save data
        os.makedirs("../../data/pdf_extracted", exist_ok=True)
        
        with open("../../data/pdf_extracted/colleges.json", "w") as f:
            json.dump(colleges, f, indent=2)
        
        with open("../../data/pdf_extracted/cutoffs.json", "w") as f:
            json.dump(cutoffs, f, indent=2)
        
        print(f"Saved {len(colleges)} colleges and {len(cutoffs)} cutoffs")
    else:
        print(f"PDF file not found: {pdf_path}")
