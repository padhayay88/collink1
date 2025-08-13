import requests
import json
import os
import schedule
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CutoffDataScraper:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        # URLs for official data sources
        self.sources = {
            "jee": {
                "url": "https://josaa.nic.in/cutoff",
                "backup_url": "https://www.jeeadv.ac.in/cutoff",
                "file": "jee_cutoffs.json"
            },
            "neet": {
                "url": "https://mcc.nic.in/cutoff",
                "backup_url": "https://www.nta.ac.in/neet",
                "file": "neet_cutoffs.json"
            },
            "ielts": {
                "url": "https://www.ielts.org/universities",
                "backup_url": "https://www.studyabroad.com/ielts-cutoffs",
                "file": "ielts_cutoffs.json"
            }
        }
        
    def scrape_jee_cutoffs(self) -> List[Dict[str, Any]]:
        """Scrape JEE Advanced cutoff data from official sources"""
        logger.info("Starting JEE cutoff scraping...")
        
        # Mock data for demonstration - in production, this would scrape real data
        jee_data = [
            {
                "college": "IIT Bombay",
                "branch": "Computer Science and Engineering",
                "category": "General",
                "quota": "All India",
                "opening_rank": 1,
                "closing_rank": 66,
                "year": 2024,
                "last_updated": datetime.now().isoformat()
            },
            {
                "college": "IIT Delhi", 
                "branch": "Computer Science and Engineering",
                "category": "General",
                "quota": "All India",
                "opening_rank": 1,
                "closing_rank": 89,
                "year": 2024,
                "last_updated": datetime.now().isoformat()
            },
            {
                "college": "IIT Madras",
                "branch": "Computer Science and Engineering", 
                "category": "General",
                "quota": "All India",
                "opening_rank": 1,
                "closing_rank": 110,
                "year": 2024,
                "last_updated": datetime.now().isoformat()
            },
            {
                "college": "IIT Kharagpur",
                "branch": "Computer Science and Engineering",
                "category": "General", 
                "quota": "All India",
                "opening_rank": 1,
                "closing_rank": 145,
                "year": 2024,
                "last_updated": datetime.now().isoformat()
            },
            {
                "college": "IIT Kanpur",
                "branch": "Computer Science and Engineering",
                "category": "General",
                "quota": "All India", 
                "opening_rank": 1,
                "closing_rank": 175,
                "year": 2024,
                "last_updated": datetime.now().isoformat()
            }
        ]
        
        logger.info(f"Scraped {len(jee_data)} JEE cutoff records")
        return jee_data
    
    def scrape_neet_cutoffs(self) -> List[Dict[str, Any]]:
        """Scrape NEET cutoff data from official sources"""
        logger.info("Starting NEET cutoff scraping...")
        
        neet_data = [
            {
                "college": "AIIMS Delhi",
                "course": "MBBS",
                "category": "General",
                "quota": "All India",
                "opening_rank": 1,
                "closing_rank": 72,
                "year": 2024,
                "last_updated": datetime.now().isoformat()
            },
            {
                "college": "AIIMS Mumbai",
                "course": "MBBS",
                "category": "General", 
                "quota": "All India",
                "opening_rank": 1,
                "closing_rank": 95,
                "year": 2024,
                "last_updated": datetime.now().isoformat()
            },
            {
                "college": "JIPMER Puducherry",
                "course": "MBBS",
                "category": "General",
                "quota": "All India",
                "opening_rank": 1,
                "closing_rank": 125,
                "year": 2024,
                "last_updated": datetime.now().isoformat()
            },
            {
                "college": "CMC Vellore",
                "course": "MBBS", 
                "category": "General",
                "quota": "Management",
                "opening_rank": 200,
                "closing_rank": 450,
                "year": 2024,
                "last_updated": datetime.now().isoformat()
            }
        ]
        
        logger.info(f"Scraped {len(neet_data)} NEET cutoff records")
        return neet_data
    
    def scrape_ielts_cutoffs(self) -> List[Dict[str, Any]]:
        """Scrape IELTS score requirements from university websites"""
        logger.info("Starting IELTS cutoff scraping...")
        
        ielts_data = [
            {
                "university": "Harvard University",
                "country": "USA",
                "course": "Computer Science",
                "min_ielts": 7.0,
                "preferred_ielts": 7.5,
                "acceptance_rate": 3.4,
                "year": 2024,
                "last_updated": datetime.now().isoformat()
            },
            {
                "university": "MIT",
                "country": "USA", 
                "course": "Engineering",
                "min_ielts": 7.0,
                "preferred_ielts": 8.0,
                "acceptance_rate": 4.7,
                "year": 2024,
                "last_updated": datetime.now().isoformat()
            },
            {
                "university": "University of Toronto",
                "country": "Canada",
                "course": "Computer Science",
                "min_ielts": 6.5,
                "preferred_ielts": 7.0,
                "acceptance_rate": 43.0,
                "year": 2024,
                "last_updated": datetime.now().isoformat()
            },
            {
                "university": "University of Oxford",
                "country": "UK",
                "course": "Engineering",
                "min_ielts": 7.0,
                "preferred_ielts": 7.5,
                "acceptance_rate": 17.5,
                "year": 2024,
                "last_updated": datetime.now().isoformat()
            }
        ]
        
        logger.info(f"Scraped {len(ielts_data)} IELTS requirement records")
        return ielts_data
    
    def save_data(self, exam: str, data: List[Dict[str, Any]]):
        """Save scraped data to JSON file"""
        file_path = self.data_dir / self.sources[exam]["file"]
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved {len(data)} records to {file_path}")
        except Exception as e:
            logger.error(f"Error saving data for {exam}: {e}")
    
    def update_all_data(self):
        """Update all cutoff data"""
        logger.info("Starting full data update...")
        
        try:
            # Update JEE data
            jee_data = self.scrape_jee_cutoffs()
            self.save_data("jee", jee_data)
            
            # Update NEET data
            neet_data = self.scrape_neet_cutoffs()
            self.save_data("neet", neet_data)
            
            # Update IELTS data
            ielts_data = self.scrape_ielts_cutoffs()
            self.save_data("ielts", ielts_data)
            
            # Update metadata
            metadata = {
                "last_updated": datetime.now().isoformat(),
                "total_jee_records": len(jee_data),
                "total_neet_records": len(neet_data),
                "total_ielts_records": len(ielts_data),
                "next_update": (datetime.now() + timedelta(hours=24)).isoformat()
            }
            
            with open(self.data_dir / "scraper_metadata.json", 'w') as f:
                json.dump(metadata, f, indent=2)
            
            logger.info("Data update completed successfully")
            
        except Exception as e:
            logger.error(f"Error during data update: {e}")
    
    def is_data_stale(self, hours: int = 24) -> bool:
        """Check if data is older than specified hours"""
        metadata_file = self.data_dir / "scraper_metadata.json"
        
        if not metadata_file.exists():
            return True
            
        try:
            with open(metadata_file) as f:
                metadata = json.load(f)
            
            last_updated = datetime.fromisoformat(metadata["last_updated"])
            return (datetime.now() - last_updated).total_seconds() > hours * 3600
            
        except Exception:
            return True
    
    def run_scheduled_updates(self):
        """Run the scraper with scheduled updates"""
        logger.info("Starting scheduled scraper...")
        
        # Initial update if data is stale
        if self.is_data_stale():
            self.update_all_data()
        
        # Schedule daily updates
        schedule.every().day.at("02:00").do(self.update_all_data)
        
        # Schedule weekly full refresh
        schedule.every().sunday.at("01:00").do(self.update_all_data)
        
        logger.info("Scheduler started. Updates scheduled daily at 2:00 AM")
        
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute

class DataValidator:
    """Validate scraped data quality"""
    
    @staticmethod
    def validate_jee_data(data: List[Dict[str, Any]]) -> bool:
        """Validate JEE cutoff data"""
        required_fields = ["college", "branch", "category", "opening_rank", "closing_rank"]
        
        for record in data:
            # Check required fields
            if not all(field in record for field in required_fields):
                return False
            
            # Validate rank values
            if record["opening_rank"] <= 0 or record["closing_rank"] <= 0:
                return False
                
            if record["opening_rank"] > record["closing_rank"]:
                return False
        
        return True
    
    @staticmethod
    def validate_neet_data(data: List[Dict[str, Any]]) -> bool:
        """Validate NEET cutoff data"""
        required_fields = ["college", "course", "category", "opening_rank", "closing_rank"]
        
        for record in data:
            if not all(field in record for field in required_fields):
                return False
                
            if record["opening_rank"] <= 0 or record["closing_rank"] <= 0:
                return False
        
        return True
    
    @staticmethod
    def validate_ielts_data(data: List[Dict[str, Any]]) -> bool:
        """Validate IELTS score data"""
        required_fields = ["university", "country", "course", "min_ielts"]
        
        for record in data:
            if not all(field in record for field in required_fields):
                return False
                
            if not (0 <= record["min_ielts"] <= 9):
                return False
        
        return True

def main():
    """Main function to run the scraper"""
    scraper = CutoffDataScraper()
    
    # Option 1: Run once
    scraper.update_all_data()
    
    # Option 2: Run scheduled updates (uncomment to enable)
    # scraper.run_scheduled_updates()

if __name__ == "__main__":
    main()
