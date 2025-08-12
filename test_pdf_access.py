#!/usr/bin/env python3
"""
Test PDF access and basic extraction
"""
import os
from pathlib import Path

def test_pdf_access():
    """Test if we can access the PDF file"""
    pdf_path = "Consolidated list of All Universities.pdf"
    
    print("Testing PDF access...")
    print(f"Current directory: {os.getcwd()}")
    print(f"Looking for: {pdf_path}")
    
    if Path(pdf_path).exists():
        size = Path(pdf_path).stat().st_size
        print(f"✓ PDF found! Size: {size:,} bytes")
        
        # Try to extract with PyMuPDF
        try:
            import PyMuPDF as fitz
            print("✓ PyMuPDF is available")
            
            doc = fitz.open(pdf_path)
            print(f"✓ PDF opened successfully")
            print(f"✓ Number of pages: {doc.page_count}")
            
            # Extract first page as test
            if doc.page_count > 0:
                page = doc[0]
                text = page.get_text()
                print(f"✓ First page text length: {len(text)} characters")
                
                # Save first 1000 characters to see content
                with open("first_page_sample.txt", "w", encoding="utf-8") as f:
                    f.write(text[:1000])
                print("✓ Saved first page sample to first_page_sample.txt")
                
                # Look for numbered entries in first page
                lines = text.split('\n')[:20]  # First 20 lines
                print("\nFirst 20 lines from PDF:")
                for i, line in enumerate(lines):
                    if line.strip():
                        print(f"{i+1:2d}: {line.strip()}")
            
            doc.close()
            return True
            
        except ImportError:
            print("❌ PyMuPDF not available")
            return False
        except Exception as e:
            print(f"❌ Error reading PDF: {e}")
            return False
    else:
        print("❌ PDF file not found")
        print("Files in current directory:")
        for file in Path(".").iterdir():
            if file.is_file():
                print(f"  - {file.name}")
        return False

if __name__ == "__main__":
    test_pdf_access()
