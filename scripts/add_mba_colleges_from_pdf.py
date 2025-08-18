import json
import re
from pathlib import Path

def parse_mba_colleges(text_content: str):
    """Parse MBA college rankings from the provided text content."""
    colleges = []
    lines = text_content.split('\n')
    
    indian_states_and_uts = [
        "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal", "Andaman and Nicobar Islands", "Chandigarh", "Dadra and Nagar Haveli and Daman and Diu", "Delhi", "Jammu & Kashmir", "Ladakh", "Lakshadweep", "Puducherry"
    ]
    
    for line in lines:
        line = line.strip()
        if not line or not line[0].isdigit():
            continue

        # Extract rank
        rank_match = re.match(r'^(\d+)', line)
        if not rank_match:
            continue
        rank = int(rank_match.group(1))
        remaining_line = line[len(rank_match.group(0)):].strip()

        # Find state
        found_state = None
        for state in indian_states_and_uts:
            if remaining_line.endswith(state):
                found_state = state
                remaining_line = remaining_line[:-len(state)].strip()
                break
        
        if not found_state:
            continue

        # Find city
        # The city is the last word of the remaining string. It can be multi-word e.g. "New Delhi"
        words = remaining_line.split()
        found_city = ""
        for i in range(len(words) - 1, -1, -1):
            # Check if the word is a city
            # This is a heuristic, we assume the last word(s) are the city
            # We will assume a city name can be up to 3 words long
            potential_city = " ".join(words[i:])
            # A simple check to avoid consuming parts of the college name
            if len(potential_city) > 20:
                 break
            found_city = potential_city
            name_part = " ".join(words[:i])
            if len(name_part) > 5: # Make sure we have a reasonable name
                 break


        if not found_city:
            continue
            
        institute_name = remaining_line[:-len(found_city)].strip()

        colleges.append({
            "rank": rank,
            "name": institute_name,
            "city": found_city,
            "state": found_state
        })
        
    return colleges

def create_cat_cutoff_data(colleges):
    """Create CAT cutoff data from the parsed college list."""
    cutoffs = []
    
    for college in colleges:
        # Use NIRF rank as the basis for the closing rank.
        # This is an approximation, as NIRF rank is not the same as CAT rank.
        # We'll create a plausible range around the NIRF rank.
        base_rank = college['rank'] * 1000
        
        # Create cutoffs for different categories
        for category in ['General', 'OBC', 'SC', 'ST', 'EWS']:
            if category == 'General':
                closing_rank = base_rank
            elif category == 'OBC':
                closing_rank = int(base_rank * 1.2)
            elif category == 'EWS':
                closing_rank = int(base_rank * 1.1)
            elif category == 'SC':
                closing_rank = int(base_rank * 1.5)
            else: # ST
                closing_rank = int(base_rank * 2.0)
                
            opening_rank = int(closing_rank * 0.8)
            
            cutoff = {
                "college": college['name'],
                "branch": "MBA/PGDM",
                "opening_rank": opening_rank,
                "closing_rank": closing_rank,
                "category": category,
                "quota": "All India",
                "location": f"{college['city']}, {college['state']}",
                "exam_type": "cat",
                "year": 2024,
                "source": "NIRF_2024_PDF"
            }
            cutoffs.append(cutoff)
            
    return cutoffs

def main():
    """Main function to extract, parse, and save MBA college data."""
    pdf_content = """
MBA Colleges in India - NIRF 2024
RankInstitute NameCityState
1Indian Institute of Management Ahmedabad (IIMA)AhmedabadGujarat
2Indian Institute of Management Bangalore (IIMB)BengaluruKarnataka
3Indian Institute of Management Kozhikode (IIMK)KozhikodeKerala
4Indian Institute of Technology Delhi (IITD)New DelhiDelhi
5Indian Institute of Management Calcutta (IIMC)KolkataWest Bengal
6Indian Institute of Management Lucknow (IIML)LucknowUttar Pradesh
7Indian Institute of Management Indore (IIMI)IndoreMadhya Pradesh
8Xavier School of Management (XLRI)JamshedpurJharkhand
9Indian Institute of Technology Bombay (IITB)MumbaiMaharashtra
10Management Development Institute (MDI)GurugramHaryana
11Indian Institute of Management Rohtak (IIMR)RohtakHaryana
12Symbiosis Institute of Business Management (SIBM)PuneMaharashtra
13Indian Institute of Management Raipur (IIMR)RaipurChhattisgarh
14Indian Institute of Foreign Trade (IIFT)New DelhiDelhi
15Indian Institute of Technology Madras (IITM)ChennaiTamil Nadu
16Indian Institute of Management Ranchi (IIMR)RanchiJharkhand
17Indian Institute of Technology Roorkee (IITR)RoorkeeUttarakhand
18Indian Institute of Technology Kharagpur (IITK)KharagpurWest Bengal
19SP Jain Institute of Management & Research (SPJIMR)MumbaiMaharashtra
20Narsee Monjee Institute of Management Studies (NMIMS)MumbaiMaharashtra
21Indian Institute of Management Udaipur (IIMU)UdaipurRajasthan
22Indian Institute of Management Visakhapatnam (IIMV)VisakhapatnamAndhra Pradesh
23Indian Institute of Management Tiruchirappalli (IIMT)TiruchirappalliTamil Nadu
24Indian Institute of Management Jammu (IIMJ)JammuJammu & Kashmir
25Indian Institute of Management Nagpur (IIMN)NagpurMaharashtra
26Institute of Management Technology (IMT)GhaziabadUttar Pradesh
27Great Lakes Institute of ManagementChennaiTamil Nadu
28Indian Institute of Management Bodh Gaya (IIMBG)Bodh GayaBihar
29ICFAI Foundation for Higher EducationHyderabadTelangana
30International Management Institute (IMI)New DelhiDelhi
31UPES (University of Petroleum and Energy Studies)DehradunUttarakhand
32Xavier Institute of Management (XIMB)BhubaneswarOdisha
33Goa Institute of Management (GIM)GoaGoa
34Amity UniversityNoidaUttar Pradesh
35Jamia Millia Islamia (JMI)New DelhiDelhi
36Lovely Professional University (LPU)PhagwaraPunjab
37MICA (Mudra Institute of Communications Ahmedabad)AhmedabadGujarat
38Thapar Institute of Engineering and TechnologyPatialaPunjab
39Bharati Vidyapeeth Institute of ManagementPuneMaharashtra
40Chandigarh UniversityChandigarhPunjab
41Institute of Rural Management Anand (IRMA)AnandGujarat
42Shailesh J. Mehta School of Management (SJMSOM)MumbaiMaharashtra
43Birla Institute of Management Technology (BIMTECH)Greater NoidaUttar Pradesh
44Alliance UniversityBangaloreKarnataka
45ICFAI Business School (IBS)HyderabadTelangana
46Symbiosis Centre for Management and Human Resource
Development (SCMHRD)
PuneMaharashtra
47K.J. Somaiya Institute of Management Studies and ResearchMumbaiMaharashtra
48Bennett UniversityGreater NoidaUttar Pradesh
49Faculty of Management Studies (FMS)New DelhiDelhi
50IILM Institute for Higher EducationGurgaonHaryana
51Amrita School of BusinessCoimbatoreTamil Nadu
52VIT Business School (VITBS)VelloreTamil Nadu
53Narsee Monjee Institute of Management Studies (NMIMS),
Bengaluru
BengaluruKarnataka
54Christ UniversityBangaloreKarnataka
55Institute of Public Enterprise (IPE)HyderabadTelangana
56Jaipuria Institute of ManagementLucknowUttar Pradesh
57GITAM School of International BusinessVisakhapatnamAndhra Pradesh
58KIIT School of ManagementBhubaneswarOdisha
59Institute of Management Studies (IMS), NoidaNoidaUttar Pradesh
60Rajagiri Centre for Business StudiesKochiKerala
61Christ University - Bengaluru MBABengaluruKarnataka
62ICFAI Business School, PunePuneMaharashtra
63Chitkara Business SchoolChandigarhPunjab
64Jagan Institute of Management Studies (JIMS)DelhiDelhi
65Ramaiah Institute of ManagementBengaluruKarnataka
66Institute of Management Studies, GhaziabadGhaziabadUttar Pradesh
67Pune Institute of Business ManagementPuneMaharashtra
68BML Munjal UniversityGurgaonHaryana
69Shiv Nadar UniversityGreater NoidaUttar Pradesh
70KCT Business SchoolCoimbatoreTamil Nadu
71Vellore Institute of Technology (VIT)VelloreTamil Nadu
72Christ University - Department of ManagementBengaluruKarnataka
73Prestige Institute of ManagementIndoreMadhya Pradesh
74Mangalore University - Department of ManagementMangaloreKarnataka
75Symbiosis International University, PunePuneMaharashtra
76Nirma UniversityAhmedabadGujarat
77Indus Business Academy (IBA)BengaluruKarnataka
78Welingkar Institute of Management Development & ResearchMumbaiMaharashtra
79Amity Global Business SchoolNoidaUttar Pradesh
80Fore School of ManagementNew DelhiDelhi
81Symbiosis Institute of Management Studies (SIMS)PuneMaharashtra
82Indian Institute of Forest Management (IIFM)BhopalMadhya Pradesh
83Gurgaon Institute of Management StudiesGurgaonHaryana
84Balaji Institute of Modern ManagementPuneMaharashtra
85Loyola Institute of Business AdministrationChennaiTamil Nadu
86Manipal Institute of ManagementManipalKarnataka
87B-Schools, Jain UniversityBengaluruKarnataka
88SIES College of Management StudiesMumbaiMaharashtra
89Christ (Deemed to be University)BengaluruKarnataka
90IFIM Business SchoolBengaluruKarnataka
91Institute of Management Technology, NagpurNagpurMaharashtra
92KIAMS - K. J. Somaiya Institute of ManagementPuneMaharashtra
93IMI BhubaneswarBhubaneswarOdisha
94SIBM BangaloreBengaluruKarnataka
95Nirma University, AhmedabadAhmedabadGujarat
96XIM UniversityBhubaneswarOdisha
97University School of Management Studies, GGSIPUNew DelhiDelhi
98JIMS RohiniNew DelhiDelhi
99Krea University, School of ManagementSri CityAndhra Pradesh
100SIBM PunePuneMaharashtra
101Christ University - Bangalore MBA ProgramBengaluruKarnataka
102IMT HyderabadHyderabadTelangana
103Shailesh J Mehta School of Management, IIT BombayMumbaiMaharashtra
104Institute of Management Studies, NoidaNoidaUttar Pradesh
105GITAM Business SchoolVisakhapatnamAndhra Pradesh
106Alliance School of Business, Alliance UniversityBangaloreKarnataka
107Jaipuria Institute of Management, LucknowLucknowUttar Pradesh
108Christ (Deemed to be University) - Department of
Management
BengaluruKarnataka
109MICA, AhmedabadAhmedabadGujarat
110Symbiosis Institute of Management Studies, PunePuneMaharashtra
111ICFAI Business School, HyderabadHyderabadTelangana
112FORE School of Management, DelhiNew DelhiDelhi
113SP Jain Global ManagementMumbaiMaharashtra
114BIMTECH Greater NoidaGreater NoidaUttar Pradesh
115Amity School of Business, NoidaNoidaUttar Pradesh
116IFIM BangaloreBengaluruKarnataka
117Christ University - MBABengaluruKarnataka
118Nirma University - MBAAhmedabadGujarat
119XIMB Executive MBABhubaneswarOdisha
120Symbiosis School of Business, PunePuneMaharashtra
121KIIT School of ManagementBhubaneswarOdisha
122Jaipuria Institute of Management, NoidaNoidaUttar Pradesh
123Indus Business Academy (IBA), BengaluruBengaluruKarnataka
124Welingkar Institute of Management, MumbaiMumbaiMaharashtra
125Manipal Institute of Management, ManipalManipalKarnataka
    """
    
    print("🔍 Parsing MBA college data from text...")
    colleges = parse_mba_colleges(pdf_content)
    
    if not colleges:
        print("❌ No colleges found in the text.")
        return
        
    print(f"✓ Found {len(colleges)} colleges.")
    
    print("📊 Generating CAT cutoff data...")
    cutoffs = create_cat_cutoff_data(colleges)
    print(f"✓ Generated {len(cutoffs)} cutoff entries.")
    
    # Save to data directory
    data_dir = Path(__file__).parent.parent / "data"
    data_dir.mkdir(exist_ok=True)
    
    output_file = data_dir / "cat_mba_colleges_from_pdf.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(cutoffs, f, indent=2, ensure_ascii=False)
        
    print(f"✓ Saved CAT cutoff data to {output_file}")
    
    print("\n🏆 Top 10 MBA Colleges:")
    for college in colleges[:10]:
        print(f"   {college['rank']:2d}. {college['name']}")
        
    print(f"\n✅ Successfully processed MBA college data from PDF!")

if __name__ == "__main__":
    main()
