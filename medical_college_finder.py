import pandas as pd
import sys

def find_medical_colleges(rank):
    try:
        # Read the CSV file
        df = pd.read_csv('comprehensive_colleges_list.csv')
        
        # Filter medical colleges
        medical_colleges = df[df['Category'].str.lower() == 'medical'].copy()
        
        if medical_colleges.empty:
            print("No medical colleges found in the database.")
            return
        
        # Convert cutoff ranges to min and max values
        def get_cutoff_range(cutoff_str):
            if pd.isna(cutoff_str):
                return (0, 0)
            try:
                if '-' in str(cutoff_str):
                    min_val, max_val = map(int, str(cutoff_str).split('-'))
                    return (min_val, max_val)
                else:
                    return (0, 0)
            except:
                return (0, 0)
        
        medical_colleges[['Min_Cutoff', 'Max_Cutoff']] = medical_colleges['Entrance Exam Cutoff'].apply(
            lambda x: pd.Series(get_cutoff_range(x))
        )
        
        # Filter colleges where the rank is within the cutoff range
        eligible_colleges = medical_colleges[
            (medical_colleges['Min_Cutoff'] <= rank) & 
            (medical_colleges['Max_Cutoff'] >= rank)
        ]
        
        # Sort by ranking
        eligible_colleges = eligible_colleges.sort_values('Ranking')
        
        if eligible_colleges.empty:
            print(f"No medical colleges found for rank {rank}.")
            print("Here are some top medical colleges you might consider:")
            top_colleges = medical_colleges.head(5).sort_values('Ranking')
            display_colleges(top_colleges)
        else:
            print(f"\nMedical Colleges Available for Rank {rank}:\n")
            display_colleges(eligible_colleges)
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def display_colleges(colleges_df):
    # Display important columns
    display_columns = [
        'College Name', 'State/UT', 'Type', 'Ranking', 
        'Entrance Exam Cutoff', 'Annual Fees (INR)', 'Seats'
    ]
    
    # Format the output
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000)
    pd.set_option('display.colheader_justify', 'left')
    
    print(colleges_df[display_columns].to_string(index=False))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            rank = int(sys.argv[1])
            find_medical_colleges(rank)
        except ValueError:
            print("Please enter a valid rank number.")
    else:
        print("Usage: python medical_college_finder.py [YOUR_RANK]")
        print("Example: python medical_college_finder.py 5000")
