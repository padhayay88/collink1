import pandas as pd
import random
from faker import Faker

# Initialize Faker for generating realistic data
fake = Faker('en_IN')

# List of states in India
states = [
    'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh',
    'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jharkhand', 'Karnataka',
    'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
    'Nagaland', 'Odisha', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu',
    'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal', 'Delhi'
]

# Medical college types and their approximate distributions
types = {
    'AIIMS': 20, 'JIPMER': 2, 'PGIMER': 1, 'CMC': 1, 'AFMC': 1,
    'Government': 300, 'Private': 400, 'Deemed': 100, 'Trust': 50
}

# Generate college data
def generate_medical_colleges():
    colleges = []
    college_id = 1
    
    # Add top medical colleges (AIIMS, JIPMER, etc.)
    for i in range(1, 21):
        if i == 1:
            name = "All India Institute of Medical Sciences (AIIMS), New Delhi"
            state = "Delhi"
            college_type = "AIIMS"
            cutoff_min, cutoff_max = 1, 100
            fees = 50000 + random.randint(0, 10000)
        else:
            name = f"All India Institute of Medical Sciences (AIIMS), {fake.city()}"
            state = random.choice(states)
            college_type = "AIIMS"
            cutoff_min, cutoff_max = i*100, (i+1)*100
            fees = 60000 + random.randint(0, 20000)
            
        colleges.append({
            'S.No': college_id,
            'College Name': name,
            'State/UT': state,
            'Type': college_type,
            'Exam Type': 'NEET',
            'Category': 'Medical',
            'Ranking': i,
            'Entrance Exam Cutoff': f"{cutoff_min}-{cutoff_max}",
            'Annual Fees (INR)': fees,
            'Seats': 100 + random.randint(0, 50),
            'Established': 1950 + random.randint(0, 70),
            'Website': f"www.{name.lower().replace(' ', '')}.edu.in",
            'Address': fake.address().replace('\n', ', '),
            'Contact Email': f"contact@{name.lower().replace(' ', '')}.edu.in",
            'Contact Phone': f"0{random.randint(70, 99)}{random.randint(1000000, 9999999)}"
        })
        college_id += 1
    
    # Add other government medical colleges
    for i in range(1, 301):
        name = f"{fake.city()} Medical College"
        state = random.choice(states)
        college_type = "Government"
        cutoff_min = 100 + (i * 50)
        cutoff_max = cutoff_min + 500
        
        colleges.append({
            'S.No': college_id,
            'College Name': name,
            'State/UT': state,
            'Type': college_type,
            'Exam Type': 'NEET',
            'Category': 'Medical',
            'Ranking': 20 + i,
            'Entrance Exam Cutoff': f"{cutoff_min}-{cutoff_max}",
            'Annual Fees (INR)': 50000 + random.randint(0, 100000),
            'Seats': 100 + random.randint(0, 100),
            'Established': 1950 + random.randint(0, 70),
            'Website': f"www.{name.lower().replace(' ', '')}.edu.in",
            'Address': fake.address().replace('\n', ', '),
            'Contact Email': f"contact@{name.lower().replace(' ', '')}.edu.in",
            'Contact Phone': f"0{random.randint(70, 99)}{random.randint(1000000, 9999999)}"
        })
        college_id += 1
    
    # Add private medical colleges
    for i in range(1, 401):
        name = f"{fake.company()} Medical College and Hospital"
        state = random.choice(states)
        college_type = "Private"
        cutoff_min = 5000 + (i * 100)
        cutoff_max = cutoff_min + 1000
        
        colleges.append({
            'S.No': college_id,
            'College Name': name,
            'State/UT': state,
            'Type': college_type,
            'Exam Type': 'NEET',
            'Category': 'Medical',
            'Ranking': 320 + i,
            'Entrance Exam Cutoff': f"{cutoff_min}-{cutoff_max}",
            'Annual Fees (INR)': 500000 + random.randint(0, 2000000),
            'Seats': 100 + random.randint(0, 50),
            'Established': 1980 + random.randint(0, 40),
            'Website': f"www.{name.lower().replace(' ', '')}.com",
            'Address': fake.address().replace('\n', ', '),
            'Contact Email': f"admission@{name.lower().replace(' ', '')}.com",
            'Contact Phone': f"0{random.randint(70, 99)}{random.randint(1000000, 9999999)}"
        })
        college_id += 1
    
    return pd.DataFrame(colleges)

# Main function
def main():
    # Generate medical colleges
    print("Generating medical colleges data...")
    medical_colleges = generate_medical_colleges()
    
    # Try to read existing data
    try:
        existing_data = pd.read_csv('comprehensive_colleges_list.csv')
        # Remove any existing medical colleges to avoid duplicates
        existing_data = existing_data[existing_data['Category'] != 'Medical']
        # Append new medical colleges
        combined_data = pd.concat([existing_data, medical_colleges], ignore_index=True)
    except FileNotFoundError:
        combined_data = medical_colleges
    
    # Save to CSV
    combined_data.to_csv('comprehensive_colleges_list.csv', index=False)
    print(f"Successfully updated comprehensive_colleges_list.csv with {len(medical_colleges)} medical colleges.")

if __name__ == "__main__":
    main()
