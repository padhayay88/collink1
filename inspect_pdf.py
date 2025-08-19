#!/usr/bin/env python3
"""
Script to inspect PDF structure and extract text
"""
import os
import PyPDF2
from pathlib import Path

def inspect_pdf(pdf_path: str):
    """Inspect the structure of a PDF file"""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            
            print(f"PDF has {len(reader.pages)} pages")
            
            # Extract text from first few pages
            for i, page in enumerate(reader.pages[:3]):  # Check first 3 pages
                print(f"\n--- Page {i+1} ---")
                text = page.extract_text()
                print(text[:1000])  # Print first 1000 chars of each page
                
    except Exception as e:
        print(f"Error reading PDF: {e}")

def main():
    # Path to the medical list PDF
    pdf_path = os.path.join('data', 'mediacal list.pdf')
    
    # Verify PDF exists
    if not os.path.exists(pdf_path):
        print(f"Error: PDF file not found at {pdf_path}")
        return
    
    # Inspect the PDF
    inspect_pdf(pdf_path)

if __name__ == "__main__":
    main()
