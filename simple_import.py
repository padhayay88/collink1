import os
import json
import sqlite3
from tqdm import tqdm

def main():
    print("Starting data import...")
    
    # Create or connect to SQLite database
    conn = sqlite3.connect('colleges.db')
    cursor = conn.cursor()
    
    # Create tables if they don't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS colleges (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        state TEXT,
        type TEXT,
        website TEXT
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ranks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        college_id INTEGER,
        exam_type TEXT,
        rank INTEGER,
        category TEXT,
        year INTEGER,
        FOREIGN KEY (college_id) REFERENCES colleges(id)
    )
    ''')
    
    # Process JSON files
    data_dir = 'data'
    processed_files = 0
    
    for filename in os.listdir(data_dir):
        if not filename.endswith('.json'):
            continue
            
        filepath = os.path.join(data_dir, filename)
        exam_type = 'NEET' if 'neet' in filename.lower() else 'JEE' if 'jee' in filename.lower() else 'OTHER'
        
        print(f"\nProcessing {filename}...")
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            if not isinstance(data, list):
                data = [data]
                
            for item in tqdm(data, desc=filename):
                try:
                    # Insert college
                    cursor.execute(
                        'INSERT OR IGNORE INTO colleges (name, state, type, website) VALUES (?, ?, ?, ?)',
                        (
                            item.get('college_name') or item.get('name', ''),
                            item.get('state'),
                            item.get('type'),
                            item.get('website') or item.get('url')
                        )
                    )
                    
                    # Get college ID
                    cursor.execute(
                        'SELECT id FROM colleges WHERE name = ?',
                        (item.get('college_name') or item.get('name'),)
                    )
                    college_id = cursor.fetchone()[0]
                    
                    # Insert rank if available
                    rank = item.get('rank') or item.get('closing_rank')
                    if rank and str(rank).isdigit():
                        cursor.execute(
                            'INSERT INTO ranks (college_id, exam_type, rank, category, year) VALUES (?, ?, ?, ?, ?)',
                            (
                                college_id,
                                exam_type,
                                int(rank),
                                item.get('category', 'General'),
                                item.get('year', 2024)
                            )
                        )
                        
                except Exception as e:
                    print(f"Error processing item: {e}")
                    continue
                    
            processed_files += 1
            conn.commit()
            print(f"Successfully processed {len(data)} records from {filename}")
            
        except Exception as e:
            print(f"Error processing {filename}: {e}")
    
    # Print summary
    cursor.execute('SELECT COUNT(*) FROM colleges')
    print(f"\nTotal colleges in database: {cursor.fetchone()[0]}")
    
    cursor.execute('SELECT COUNT(*) FROM ranks')
    print(f"Total rank records: {cursor.fetchone()[0]}")
    
    conn.close()
    print("\nImport completed!")

if __name__ == '__main__':
    main()
