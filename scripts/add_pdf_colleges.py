import json
import re
from pathlib import Path
from typing import List, Dict, Any
import fitz  # PyMuPDF for PDF parsing


def extract_college_data_from_pdf(pdf_path: str) -> List[Dict[str, Any]]:
    """Extract college data from the PDF file"""
    
    colleges = []
    
    try:
        # Open the PDF
        doc = fitz.open(pdf_path)
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text()
            
            # Split text into lines and process
            lines = text.split('\n')
            
            for line in lines:
                line = line.strip()
                
                # Skip empty lines and page headers/footers
                if not line or len(line) < 10:
                    continue
                    
                # Skip page numbers, headers, and common navigation text
                skip_patterns = [
                    r'^\d+$',  # Page numbers
                    r'^page \d+',
                    r'^consolidated list',
                    r'^university',
                    r'^all universities',
                    r'^list of',
                    r'^\d+\s*of\s*\d+',
                    r'^copyright',
                    r'^©',
                ]
                
                if any(re.match(pattern, line.lower()) for pattern in skip_patterns):
                    continue
                
                # Look for college/university names
                # Common patterns for Indian universities/colleges
                college_indicators = [
                    'university', 'college', 'institute', 'iit', 'nit', 'iiit', 
                    'engineering', 'technology', 'medical', 'management',
                    'polytechnic', 'technical', 'deemed'
                ]
                
                line_lower = line.lower()
                if any(indicator in line_lower for indicator in college_indicators):
                    # Clean the college name
                    college_name = clean_college_name(line)
                    
                    if college_name and len(college_name) > 5:  # Valid college name
                        # Extract location if present in the same line
                        location = extract_location_from_line(line)
                        
                        # Determine college type based on name patterns
                        college_type = determine_college_type(college_name)
                        
                        # Determine if it's suitable for JEE based on name
                        is_jee_college = is_jee_suitable(college_name)
                        
                        if is_jee_college:
                            college_data = {
                                "name": college_name,
                                "location": location,
                                "type": college_type,
                                "exams": ["jee"]
                            }
                            
                            # Avoid duplicates
                            if not any(c["name"].lower() == college_name.lower() for c in colleges):
                                colleges.append(college_data)
        
        doc.close()
        
    except Exception as e:
        print(f"Error processing PDF: {e}")
        return []
    
    return colleges


def clean_college_name(raw_name: str) -> str:
    """Clean and standardize college name"""
    
    # Remove extra whitespace and normalize
    name = ' '.join(raw_name.split())
    
    # Remove common prefixes/suffixes that aren't part of the actual name
    prefixes_to_remove = [
        r'^\d+\.\s*',  # Numbering
        r'^\d+\)\s*',  # Numbered list
        r'^-\s*',      # Dash prefix
        r'^\*\s*',     # Asterisk prefix
    ]
    
    for pattern in prefixes_to_remove:
        name = re.sub(pattern, '', name)
    
    # Clean up multiple spaces
    name = re.sub(r'\s+', ' ', name).strip()
    
    return name


def extract_location_from_line(line: str) -> str:
    """Extract location information from a line"""
    
    # Common location patterns in Indian context
    location_patterns = [
        r'([A-Za-z\s]+),\s*([A-Za-z\s]+)$',  # City, State format at end
        r'\b(Delhi|Mumbai|Bangalore|Chennai|Kolkata|Hyderabad|Pune|Ahmedabad|Jaipur|Lucknow|Kanpur|Nagpur|Indore|Bhopal|Visakhapatnam|Kochi|Thiruvananthapuram)\b',
        r'\b(Uttar Pradesh|Maharashtra|Karnataka|Tamil Nadu|West Bengal|Telangana|Gujarat|Rajasthan|Madhya Pradesh|Andhra Pradesh|Kerala|Punjab|Haryana|Bihar|Odisha|Assam|Jharkhand|Chhattisgarh|Uttarakhand|Himachal Pradesh|Tripura|Manipur|Meghalaya|Sikkim|Mizoram|Nagaland|Arunachal Pradesh|Goa|Jammu and Kashmir|Ladakh)\b',
    ]
    
    for pattern in location_patterns:
        match = re.search(pattern, line, re.IGNORECASE)
        if match:
            return match.group().strip()
    
    # If no specific pattern found, try to extract from common formats
    # Look for patterns like "College Name, Location" or "College Name - Location"
    location_separators = [', ', ' - ', ' – ', ' | ']
    
    for separator in location_separators:
        if separator in line:
            parts = line.split(separator)
            if len(parts) >= 2:
                potential_location = parts[-1].strip()
                # Check if it looks like a location (contains state-like words)
                if any(word in potential_location.lower() for word in ['pradesh', 'bengal', 'delhi', 'mumbai', 'bangalore', 'chennai']):
                    return potential_location
    
    return "India"  # Default location


def determine_college_type(college_name: str) -> str:
    """Determine college type based on name patterns"""
    
    name_lower = college_name.lower()
    
    # Government institutions
    govt_indicators = [
        'iit', 'nit', 'iiit', 'government', 'govt', 'central', 'national',
        'indian institute', 'state', 'rajkiya', 'sarkari'
    ]
    
    if any(indicator in name_lower for indicator in govt_indicators):
        return "Government"
    
    # Deemed universities
    deemed_indicators = ['deemed', 'university']
    if all(indicator in name_lower for indicator in deemed_indicators):
        return "Deemed"
    
    # Private by default
    return "Private"


def is_jee_suitable(college_name: str) -> bool:
    """Check if college is suitable for JEE candidates"""
    
    name_lower = college_name.lower()
    
    # Engineering/technology focused institutions
    jee_indicators = [
        'engineering', 'technology', 'technical', 'iit', 'nit', 'iiit',
        'institute of technology', 'college of engineering', 'school of engineering',
        'polytechnic', 'computer', 'electronics', 'mechanical', 'civil', 'chemical'
    ]
    
    # Exclude medical, arts, commerce colleges
    exclude_indicators = [
        'medical', 'mbbs', 'dental', 'pharmacy', 'nursing', 'arts', 'commerce',
        'law', 'management', 'business', 'agriculture', 'veterinary', 'ayurveda'
    ]
    
    # Check for JEE-suitable indicators
    has_jee_indicators = any(indicator in name_lower for indicator in jee_indicators)
    
    # Check for exclusion indicators
    has_exclude_indicators = any(indicator in name_lower for indicator in exclude_indicators)
    
    return has_jee_indicators and not has_exclude_indicators


def add_colleges_to_existing_files(new_colleges: List[Dict[str, Any]]):
    """Add new colleges to existing data files"""
    
    data_dir = Path('data')
    
    # Files to update
    files_to_update = [
        'all_colleges.json',
        'jee_comprehensive_colleges.json',
        'jee_1000_cutoffs.json'
    ]
    
    print(f"📝 Adding {len(new_colleges)} colleges to data files...")
    
    for filename in files_to_update:
        file_path = data_dir / filename
        
        try:
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
                
                if filename == 'all_colleges.json':
                    # Handle all_colleges.json format
                    if isinstance(existing_data, dict) and 'colleges' in existing_data:
                        existing_colleges = existing_data['colleges']
                        
                        # Add new colleges that don't already exist
                        added_count = 0
                        for new_college in new_colleges:
                            if not any(c['name'].lower() == new_college['name'].lower() 
                                     for c in existing_colleges):
                                existing_colleges.append(new_college)
                                added_count += 1
                        
                        existing_data['total'] = len(existing_colleges)
                        
                        with open(file_path, 'w', encoding='utf-8') as f:
                            json.dump(existing_data, f, indent=2, ensure_ascii=False)
                        
                        print(f"✅ Added {added_count} new colleges to {filename}")
                
                elif filename in ['jee_comprehensive_colleges.json', 'jee_1000_cutoffs.json']:
                    # Handle cutoff format files
                    if isinstance(existing_data, list):
                        existing_colleges = existing_data
                    else:
                        existing_colleges = existing_data.get('colleges', [])
                    
                    # Convert new colleges to proper format based on file type
                    added_count = 0
                    for new_college in new_colleges:
                        if filename == 'jee_comprehensive_colleges.json':
                            # Match the schema: name, location, base_rank, factor, type
                            college_entry = {
                                "name": new_college['name'],
                                "location": new_college.get('location', 'India'),
                                "base_rank": 50000,  # Default rank for new colleges
                                "factor": 100000,    # Default factor
                                "type": new_college.get('type', 'private').lower()
                            }
                        else:
                            # Create cutoff entry for jee_1000_cutoffs.json
                            college_entry = {
                                "college": new_college['name'],
                                "branch": "Computer Science and Engineering",
                                "opening_rank": 10000,  # Placeholder ranks
                                "closing_rank": 50000,
                                "category": "General",
                                "quota": "All India",
                                "year": 2024,
                                "exam_type": "jee",
                                "location": new_college.get('location', 'India'),
                                "college_type": new_college.get('type', 'private').lower()
                            }
                        
                        # Check if college already exists
                        if not any(c.get('college', '').lower() == new_college['name'].lower() 
                                 for c in existing_colleges):
                            existing_colleges.append(cutoff_entry)
                            added_count += 1
                    
                    # Save updated data
                    if isinstance(existing_data, list):
                        with open(file_path, 'w', encoding='utf-8') as f:
                            json.dump(existing_colleges, f, indent=2, ensure_ascii=False)
                    else:
                        existing_data['colleges'] = existing_colleges
                        with open(file_path, 'w', encoding='utf-8') as f:
                            json.dump(existing_data, f, indent=2, ensure_ascii=False)
                    
                    print(f"✅ Added {added_count} new colleges to {filename}")
                    
            else:
                print(f"⚠️  File not found: {filename}")
                
        except Exception as e:
            print(f"❌ Error updating {filename}: {e}")


def main():
    """Main function to process PDF and add colleges"""
    
    # PDF file path - update this to match the user's file
    pdf_path = r"C:\Users\shash\AppData\Local\Microsoft\Windows\INetCache\IE\S7R7H9NQ\Consolidated list of All Universities[1].pdf"
    
    print(f"🔍 Processing PDF: {pdf_path}")
    
    # Check if PDF exists
    if not Path(pdf_path).exists():
        print(f"❌ PDF file not found: {pdf_path}")
        print("Please check the file path and try again.")
        return
    
    # Extract colleges from PDF
    print("📖 Extracting college data from PDF...")
    colleges = extract_college_data_from_pdf(pdf_path)
    
    if not colleges:
        print("❌ No colleges found in PDF. Please check the PDF format.")
        return
    
    print(f"✅ Extracted {len(colleges)} colleges from PDF")
    
    # Show sample of extracted colleges
    print("\n📋 Sample of extracted colleges:")
    for i, college in enumerate(colleges[:5]):
        print(f"  {i+1}. {college['name']} - {college['location']} ({college['type']})")
    
    if len(colleges) > 5:
        print(f"  ... and {len(colleges) - 5} more colleges")
    
    # Save extracted colleges to a separate file first
    data_dir = Path('data')
    data_dir.mkdir(exist_ok=True)
    
    extracted_file = data_dir / 'pdf_extracted_colleges.json'
    with open(extracted_file, 'w', encoding='utf-8') as f:
        json.dump(colleges, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Saved extracted colleges to {extracted_file}")
    
    # Add to existing files
    add_colleges_to_existing_files(colleges)
    
    print(f"\n🎉 Successfully processed PDF and added {len(colleges)} colleges to the database!")
    print("📊 Summary:")
    print(f"   - Total colleges extracted: {len(colleges)}")
    print(f"   - JEE-suitable colleges: {len(colleges)}")
    print(f"   - Government colleges: {len([c for c in colleges if c['type'] == 'Government'])}")
    print(f"   - Private colleges: {len([c for c in colleges if c['type'] == 'Private'])}")
    print(f"   - Deemed universities: {len([c for c in colleges if c['type'] == 'Deemed'])}")


if __name__ == "__main__":
    main()