#!/usr/bin/env python3
"""
Script to enrich college data with official URLs and search links
"""

import sys
import os

# Add the scraper directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'scraper'))

from real_data_scraper import (
    test_careers360_enrichment,
    update_college_info_enhanced_with_careers360,
    generate_official_college_links,
    enrich_colleges_with_generated_links,
    update_college_info_enhanced_with_generated_links
)

def test_generated_links():
    """
    Test the generated links approach on sample colleges
    """
    test_colleges = [
        {"college": "IIT Bombay", "university": "IIT Bombay"},
        {"college": "NIT Trichy", "university": "NIT Trichy"},
        {"college": "AIIMS Delhi", "university": "AIIMS Delhi"}
    ]
    
    print("Testing generated links enrichment on sample colleges...")
    enriched = enrich_colleges_with_generated_links(test_colleges)
    
    for college in enriched:
        print(f"\n{college.get('college', 'Unknown')}:")
        if 'official_links' in college:
            print("  Official Website Patterns:")
            for pattern in college['official_links']['website_patterns']:
                print(f"    {pattern}")
        if 'search_queries' in college:
            print("  Search Queries:")
            for key, url in list(college['search_queries'].items())[:3]:  # Show first 3
                print(f"    {key}: {url}")
        if 'contact_queries' in college:
            print("  Contact Queries:")
            for key, url in college['contact_queries'].items():
                print(f"    {key}: {url}")
    
    return enriched

def main():
    print("College Data Enrichment Tool")
    print("=" * 40)
    
    while True:
        print("\nChoose an option:")
        print("1. Test generated links enrichment")
        print("2. Test Careers360 enrichment (may fail)")
        print("3. Run full generated links enrichment")
        print("4. Run full Careers360 enrichment (may fail)")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == "1":
            print("\nTesting generated links enrichment...")
            test_generated_links()
            
        elif choice == "2":
            print("\nTesting Careers360 enrichment...")
            test_careers360_enrichment()
            
        elif choice == "3":
            print("\nStarting full generated links enrichment...")
            print("This will generate official URLs and search links for all colleges...")
            confirm = input("Continue? (y/n): ").strip().lower()
            
            if confirm == 'y':
                enriched_data = update_college_info_enhanced_with_generated_links()
                if enriched_data:
                    print(f"\n✅ Successfully enriched {len(enriched_data)} colleges!")
                    print("Check data/college_info_enhanced.json for the updated data.")
                else:
                    print("\n❌ Enrichment process failed.")
            else:
                print("Enrichment cancelled.")
                
        elif choice == "4":
            print("\nStarting full Careers360 enrichment...")
            print("This may fail due to website access issues...")
            confirm = input("Continue? (y/n): ").strip().lower()
            
            if confirm == 'y':
                enriched_data = update_college_info_enhanced_with_careers360()
                if enriched_data:
                    print(f"\n✅ Successfully enriched {len(enriched_data)} colleges!")
                    print("Check data/college_info_enhanced.json for the updated data.")
                else:
                    print("\n❌ Enrichment process failed.")
            else:
                print("Enrichment cancelled.")
                
        elif choice == "5":
            print("Goodbye!")
            break
            
        else:
            print("Invalid choice. Please enter 1-5.")

if __name__ == "__main__":
    main()
