import sqlite3

def test_database():
    try:
        # Connect to the database
        conn = sqlite3.connect('colleges.db')
        cursor = conn.cursor()
        
        # Check if tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print("\nTables in database:")
        for table in tables:
            print(f"- {table[0]}")
        
        # Count records in each table
        for table in ['colleges', 'ranks']:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"\nTotal records in {table}: {count}")
            
            # Show sample data
            if count > 0:
                print(f"\nSample data from {table} (first 5 records):")
                cursor.execute(f"SELECT * FROM {table} LIMIT 5")
                columns = [description[0] for description in cursor.description]
                print("\t|".join(columns))
                for row in cursor.fetchall():
                    print("\t|".join(map(str, row)))
        
        # Show some statistics
        if 'ranks' in [t[0] for t in tables]:
            print("\nRank statistics by exam type:")
            cursor.execute("""
                SELECT exam_type, COUNT(*) as count, 
                       MIN(rank) as min_rank, 
                       MAX(rank) as max_rank
                FROM ranks
                GROUP BY exam_type
            """)
            for row in cursor.fetchall():
                print(f"{row[0]}: {row[1]} records, Rank range: {row[2]}-{row[3]}")
        
        conn.close()
        
    except Exception as e:
        print(f"Error testing database: {e}")

if __name__ == '__main__':
    print("Testing database...")
    test_database()
