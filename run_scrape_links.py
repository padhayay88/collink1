#!/usr/bin/env python3
from scraper.real_data_scraper import RealDataScraper

if __name__ == "__main__":
    links_jee = [
        "https://www.pw.live/iit-jee/exams/jee-advanced-rank-wise-colleges-list?utm_source=chatgpt.com",
        "https://engineering.careers360.com/articles/jee-advanced-rank-wise-colleges-list?utm_source=chatgpt.com",
        "https://collegedunia.com/news/e-301-jee-main-college-list-rank-wise?utm_source=chatgpt.com",
        "https://engineering.careers360.com/articles/jee-main-rank-wise-colleges-list?utm_source=chatgpt.com",
        "https://engineering.careers360.com/articles/jee-main-rank-wise-colleges-list?",
    ]
    links_neet = [
        "https://medicine.careers360.com/articles/neet-state-wise-rank-list?utm_source=chatgpt.com",
        "https://www.collegedekho.com/news/neet-rank-vs-expected-college-2025-live-updates-rank-wise-college-list-cutoff-67594/?utm_source=chatgpt.com",
        "https://www.selfstudys.com/update/neet-2025-rank-vs-college-cutoff-list?utm_source=chatgpt.com",
    ]
    scraper = RealDataScraper()
    result = scraper.scrape_from_links(links_jee, links_neet)
    print("Scrape result:", result)

    # Optional: show totals in merged files
    import json
    from pathlib import Path
    data_dir = Path("data")
    jee_path = data_dir / "jee_cutoffs_extended_v2.json"
    neet_path = data_dir / "neet_cutoffs_extended.json"
    jee_n = len(json.loads(jee_path.read_text(encoding="utf-8"))) if jee_path.exists() else 0
    neet_n = len(json.loads(neet_path.read_text(encoding="utf-8"))) if neet_path.exists() else 0
    print({"jee_extended_rows": jee_n, "neet_extended_rows": neet_n})


