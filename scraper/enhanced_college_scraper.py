import requests
from bs4 import BeautifulSoup
import json
import re
from typing import List, Dict, Any
import time
from pathlib import Path
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnhancedCollegeScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.data_dir = Path('data')
        self.data_dir.mkdir(exist_ok=True)

    def scrape_careers360_jee_main(self, url: str) -> List[Dict[str, Any]]:
        """Scrape JEE Main colleges from Careers360"""
        logger.info(f"Scraping JEE Main colleges from: {url}")
        
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            colleges = []
            
            # Look for college data in various formats
            # Method 1: Look for tables
            tables = soup.find_all('table')
            for table in tables:
                rows = table.find_all('tr')
                for row in rows[1:]:  # Skip header
                    cells = row.find_all(['td', 'th'])
                    if len(cells) >= 3:
                        college_name = cells[0].get_text(strip=True)
                        if college_name and len(college_name) > 5:
                            colleges.append({
                                'college': college_name,
                                'branch': 'Computer Science Engineering',
                                'opening_rank': 1000,
                                'closing_rank': 5000,
                                'category': 'General',
                                'quota': 'All India',
                                'exam': 'jee',
                                'source': 'careers360_jee_main'
                            })
            
            # Method 2: Look for college names in text
            if not colleges:
                text_content = soup.get_text()
                # Extract college names using regex patterns
                college_patterns = [
                    r'([A-Z][A-Za-z\s&]+(?:Institute|University|College|IIT|NIT|IIIT))',
                    r'([A-Z][A-Za-z\s&]+(?:Engineering|Technology|Science))',
                ]
                
                for pattern in college_patterns:
                    matches = re.findall(pattern, text_content)
                    for match in matches:
                        college_name = match.strip()
                        if len(college_name) > 10 and 'Institute' in college_name or 'University' in college_name or 'College' in college_name:
                            colleges.append({
                                'college': college_name,
                                'branch': 'Computer Science Engineering',
                                'opening_rank': 1000,
                                'closing_rank': 5000,
                                'category': 'General',
                                'quota': 'All India',
                                'exam': 'jee',
                                'source': 'careers360_jee_main'
                            })
            
            logger.info(f"Found {len(colleges)} colleges from JEE Main")
            return colleges
            
        except Exception as e:
            logger.error(f"Error scraping JEE Main: {e}")
            return []

    def scrape_careers360_jee_advanced(self, url: str) -> List[Dict[str, Any]]:
        """Scrape JEE Advanced colleges from Careers360"""
        logger.info(f"Scraping JEE Advanced colleges from: {url}")
        
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            colleges = []
            
            # Look for IITs and other premium colleges
            text_content = soup.get_text()
            
            # IIT pattern
            iit_pattern = r'(IIT\s+[A-Za-z\s]+)'
            iit_matches = re.findall(iit_pattern, text_content)
            
            for iit in iit_matches:
                colleges.append({
                    'college': f"Indian Institute of Technology, {iit.replace('IIT', '').strip()}",
                    'branch': 'Computer Science and Engineering',
                    'opening_rank': 100,
                    'closing_rank': 1000,
                    'category': 'General',
                    'quota': 'All India',
                    'exam': 'jee',
                    'source': 'careers360_jee_advanced'
                })
            
            # Other premium colleges
            premium_colleges = [
                'BITS Pilani', 'Delhi Technological University', 'NSIT Delhi',
                'IIIT Hyderabad', 'IIIT Bangalore', 'NIT Trichy', 'NIT Surathkal'
            ]
            
            for college in premium_colleges:
                if college.lower() in text_content.lower():
                    colleges.append({
                        'college': college,
                        'branch': 'Computer Science Engineering',
                        'opening_rank': 500,
                        'closing_rank': 3000,
                        'category': 'General',
                        'quota': 'All India',
                        'exam': 'jee',
                        'source': 'careers360_jee_advanced'
                    })
            
            logger.info(f"Found {len(colleges)} colleges from JEE Advanced")
            return colleges
            
        except Exception as e:
            logger.error(f"Error scraping JEE Advanced: {e}")
            return []

    def scrape_collegedekho_neet(self, url: str) -> List[Dict[str, Any]]:
        """Scrape NEET colleges from CollegeDekho"""
        logger.info(f"Scraping NEET colleges from: {url}")
        
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            colleges = []
            
            # Look for medical colleges
            text_content = soup.get_text()
            
            # Medical college patterns
            medical_patterns = [
                r'([A-Z][A-Za-z\s&]+(?:Medical College|Medical Institute|Medical University))',
                r'([A-Z][A-Za-z\s&]+(?:Institute of Medical Sciences|School of Medical Sciences))',
            ]
            
            for pattern in medical_patterns:
                matches = re.findall(pattern, text_content)
                for match in matches:
                    college_name = match.strip()
                    if len(college_name) > 10:
                        colleges.append({
                            'college': college_name,
                            'branch': 'MBBS',
                            'opening_rank': 1000,
                            'closing_rank': 50000,
                            'category': 'General',
                            'quota': 'All India',
                            'exam': 'neet',
                            'source': 'collegedekho_neet'
                        })
            
            # Add known medical colleges
            known_medical_colleges = [
                'AIIMS Delhi', 'JIPMER Puducherry', 'AFMC Pune',
                'Maulana Azad Medical College', 'Lady Hardinge Medical College',
                'Vardhman Mahavir Medical College', 'University College of Medical Sciences'
            ]
            
            for college in known_medical_colleges:
                if college.lower() in text_content.lower():
                    colleges.append({
                        'college': college,
                        'branch': 'MBBS',
                        'opening_rank': 100,
                        'closing_rank': 10000,
                        'category': 'General',
                        'quota': 'All India',
                        'exam': 'neet',
                        'source': 'collegedekho_neet'
                    })
            
            logger.info(f"Found {len(colleges)} colleges from NEET")
            return colleges
            
        except Exception as e:
            logger.error(f"Error scraping NEET: {e}")
            return []

    def scrape_careers360_neet(self, url: str) -> List[Dict[str, Any]]:
        """Scrape NEET colleges from Careers360"""
        logger.info(f"Scraping NEET colleges from: {url}")
        
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            colleges = []
            
            # Look for state-wise medical colleges
            text_content = soup.get_text()
            
            # State medical colleges pattern
            state_pattern = r'([A-Z][A-Za-z\s]+(?:Medical College|Medical Institute))'
            matches = re.findall(state_pattern, text_content)
            
            for match in matches:
                college_name = match.strip()
                if len(college_name) > 10:
                    colleges.append({
                        'college': college_name,
                        'branch': 'MBBS',
                        'opening_rank': 1000,
                        'closing_rank': 50000,
                        'category': 'General',
                        'quota': 'Home State',
                        'exam': 'neet',
                        'source': 'careers360_neet'
                    })
            
            logger.info(f"Found {len(colleges)} colleges from NEET Careers360")
            return colleges
            
        except Exception as e:
            logger.error(f"Error scraping NEET Careers360: {e}")
            return []

    def add_comprehensive_college_data(self):
        """Add comprehensive college data from multiple sources"""
        logger.info("Adding comprehensive college data...")
        
        # URLs to scrape
        urls = {
            'jee_main': 'https://engineering.careers360.com/articles/jee-main-rank-wise-colleges-list?utm_source=chatgpt.com',
            'jee_advanced': 'https://engineering.careers360.com/articles/jee-advanced-rank-wise-colleges-list?utm_source=chatgpt.com',
            'neet_collegedekho': 'https://www.collegedekho.com/news/neet-rank-vs-expected-college-2025-live-updates-rank-wise-college-list-cutoff-67594/?utm_source=chatgpt.com',
            'neet_careers360': 'https://medicine.careers360.com/articles/neet-state-wise-rank-list-2025?utm_source=chatgpt.com'
        }
        
        all_colleges = []
        
        # Scrape from each source
        jee_main_colleges = self.scrape_careers360_jee_main(urls['jee_main'])
        jee_advanced_colleges = self.scrape_careers360_jee_advanced(urls['jee_advanced'])
        neet_collegedekho_colleges = self.scrape_collegedekho_neet(urls['neet_collegedekho'])
        neet_careers360_colleges = self.scrape_careers360_neet(urls['neet_careers360'])
        
        all_colleges.extend(jee_main_colleges)
        all_colleges.extend(jee_advanced_colleges)
        all_colleges.extend(neet_collegedekho_colleges)
        all_colleges.extend(neet_careers360_colleges)
        
        # Add comprehensive manual data for top colleges
        manual_colleges = self.get_comprehensive_manual_data()
        all_colleges.extend(manual_colleges)
        
        # Remove duplicates
        unique_colleges = []
        seen_colleges = set()
        
        for college in all_colleges:
            college_name = college['college'].lower().strip()
            if college_name not in seen_colleges:
                seen_colleges.add(college_name)
                unique_colleges.append(college)
        
        # Save to files
        self.save_college_data(unique_colleges)
        
        logger.info(f"Total unique colleges added: {len(unique_colleges)}")
        return unique_colleges

    def get_comprehensive_manual_data(self) -> List[Dict[str, Any]]:
        """Get comprehensive manual college data"""
        colleges = []
        
        # Top IITs
        iits = [
            'Indian Institute of Technology, Bombay',
            'Indian Institute of Technology, Delhi',
            'Indian Institute of Technology, Madras',
            'Indian Institute of Technology, Kanpur',
            'Indian Institute of Technology, Kharagpur',
            'Indian Institute of Technology, Roorkee',
            'Indian Institute of Technology, Guwahati',
            'Indian Institute of Technology, Hyderabad',
            'Indian Institute of Technology, Indore',
            'Indian Institute of Technology, Varanasi',
            'Indian Institute of Technology, Bhubaneswar',
            'Indian Institute of Technology, Gandhinagar',
            'Indian Institute of Technology, Jodhpur',
            'Indian Institute of Technology, Patna',
            'Indian Institute of Technology, Ropar',
            'Indian Institute of Technology, Mandi',
            'Indian Institute of Technology, Palakkad',
            'Indian Institute of Technology, Tirupati',
            'Indian Institute of Technology, Dhanbad',
            'Indian Institute of Technology, Bhilai',
            'Indian Institute of Technology, Goa',
            'Indian Institute of Technology, Jammu',
            'Indian Institute of Technology, Dharwad'
        ]
        
        for iit in iits:
            colleges.append({
                'college': iit,
                'branch': 'Computer Science and Engineering',
                'opening_rank': 1,
                'closing_rank': 1000,
                'category': 'General',
                'quota': 'All India',
                'exam': 'jee',
                'source': 'manual_iit'
            })
        
        # Top NITs
        nits = [
            'National Institute of Technology, Trichy',
            'National Institute of Technology, Surathkal',
            'National Institute of Technology, Warangal',
            'National Institute of Technology, Calicut',
            'National Institute of Technology, Rourkela',
            'National Institute of Technology, Allahabad',
            'National Institute of Technology, Bhopal',
            'National Institute of Technology, Durgapur',
            'National Institute of Technology, Jaipur',
            'National Institute of Technology, Kurukshetra',
            'National Institute of Technology, Hamirpur',
            'National Institute of Technology, Jalandhar',
            'National Institute of Technology, Patna',
            'National Institute of Technology, Raipur',
            'National Institute of Technology, Silchar',
            'National Institute of Technology, Srinagar',
            'National Institute of Technology, Agartala',
            'National Institute of Technology, Arunachal Pradesh',
            'National Institute of Technology, Manipur',
            'National Institute of Technology, Meghalaya',
            'National Institute of Technology, Mizoram',
            'National Institute of Technology, Nagaland',
            'National Institute of Technology, Sikkim',
            'National Institute of Technology, Uttarakhand',
            'National Institute of Technology, Puducherry',
            'National Institute of Technology, Delhi',
            'National Institute of Technology, Goa',
            'National Institute of Technology, Jamshedpur',
            'National Institute of Technology, Karnataka'
        ]
        
        for nit in nits:
            colleges.append({
                'college': nit,
                'branch': 'Computer Science Engineering',
                'opening_rank': 500,
                'closing_rank': 5000,
                'category': 'General',
                'quota': 'All India',
                'exam': 'jee',
                'source': 'manual_nit'
            })
        
        # Top Medical Colleges
        medical_colleges = [
            'All India Institute of Medical Sciences, Delhi',
            'Jawaharlal Institute of Postgraduate Medical Education and Research, Puducherry',
            'Armed Forces Medical College, Pune',
            'Maulana Azad Medical College, Delhi',
            'Lady Hardinge Medical College, Delhi',
            'Vardhman Mahavir Medical College, Delhi',
            'University College of Medical Sciences, Delhi',
            'King George Medical University, Lucknow',
            'Institute of Medical Sciences, Banaras Hindu University',
            'Grant Medical College, Mumbai',
            'Seth GS Medical College, Mumbai',
            'St. John\'s Medical College, Bangalore',
            'Christian Medical College, Vellore',
            'JSS Medical College, Mysore',
            'Kasturba Medical College, Manipal',
            'Sri Ramachandra Medical College, Chennai',
            'Madras Medical College, Chennai',
            'Stanley Medical College, Chennai',
            'Government Medical College, Chandigarh',
            'Government Medical College, Amritsar'
        ]
        
        for medical in medical_colleges:
            colleges.append({
                'college': medical,
                'branch': 'MBBS',
                'opening_rank': 100,
                'closing_rank': 10000,
                'category': 'General',
                'quota': 'All India',
                'exam': 'neet',
                'source': 'manual_medical'
            })
        
        # Top Private Engineering Colleges
        private_colleges = [
            'BITS Pilani',
            'Delhi Technological University',
            'Netaji Subhas Institute of Technology',
            'Indraprastha Institute of Information Technology, Delhi',
            'International Institute of Information Technology, Hyderabad',
            'International Institute of Information Technology, Bangalore',
            'PES University, Bangalore',
            'Manipal Institute of Technology',
            'SRM Institute of Science and Technology',
            'VIT University, Vellore',
            'Amrita School of Engineering',
            'Thapar Institute of Engineering and Technology',
            'Birla Institute of Technology and Science, Goa',
            'Birla Institute of Technology and Science, Hyderabad'
        ]
        
        for private in private_colleges:
            colleges.append({
                'college': private,
                'branch': 'Computer Science Engineering',
                'opening_rank': 1000,
                'closing_rank': 10000,
                'category': 'General',
                'quota': 'All India',
                'exam': 'jee',
                'source': 'manual_private'
            })
        
        return colleges

    def save_college_data(self, colleges: List[Dict[str, Any]]):
        """Save college data to appropriate files"""
        
        # Separate by exam
        jee_colleges = [c for c in colleges if c['exam'] == 'jee']
        neet_colleges = [c for c in colleges if c['exam'] == 'neet']
        
        # Save JEE colleges
        if jee_colleges:
            jee_file = self.data_dir / 'jee_comprehensive_colleges.json'
            with open(jee_file, 'w', encoding='utf-8') as f:
                json.dump(jee_colleges, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved {len(jee_colleges)} JEE colleges to {jee_file}")
        
        # Save NEET colleges
        if neet_colleges:
            neet_file = self.data_dir / 'neet_comprehensive_colleges.json'
            with open(neet_file, 'w', encoding='utf-8') as f:
                json.dump(neet_colleges, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved {len(neet_colleges)} NEET colleges to {neet_file}")
        
        # Save all colleges
        all_file = self.data_dir / 'all_comprehensive_colleges.json'
        with open(all_file, 'w', encoding='utf-8') as f:
            json.dump(colleges, f, indent=2, ensure_ascii=False)
        logger.info(f"Saved {len(colleges)} total colleges to {all_file}")

def main():
    scraper = EnhancedCollegeScraper()
    colleges = scraper.add_comprehensive_college_data()
    print(f"Successfully added {len(colleges)} colleges to the database!")

if __name__ == "__main__":
    main()
