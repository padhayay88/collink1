from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import json
import os
from pathlib import Path

router = APIRouter()

class CollegeDetail(BaseModel):
    name: str
    overview: str
    pros: List[str]
    cons: List[str]
    location: str
    established: int
    nirf_rank: Optional[int]
    website: str
    contact: Dict[str, str]
    facilities: List[str]
    placement_stats: Dict[str, Any]
    courses_offered: List[str]

@router.get("/college/{college_name}")
async def get_college_details(college_name: str):
        """
        Get detailed information about a specific college
        """
        try:
            # Load enhanced college data
            data_path = Path("data/college_info_enhanced.json")
            if not data_path.exists():
                # Fallback to original data
                data_path = Path("data/college_info.json")
                if not data_path.exists():
                    raise HTTPException(status_code=404, detail="College data not found")

            with open(data_path, 'r', encoding='utf-8') as f:
                colleges_data = json.load(f)

            # Search for college (case-insensitive)
            college_name_lower = college_name.lower()
            college_info = None

            for college in colleges_data:
                if college_name_lower in college["name"].lower():
                    college_info = college
                    break

            if not college_info:
                raise HTTPException(
                    status_code=404,
                    detail=f"College '{college_name}' not found"
                )

            return college_info

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

@router.get("/college/{college_name}/cutoffs")
async def get_college_cutoffs(college_name: str, exam: str = "jee"):
    """
    Get cutoff information for a specific college
    """
    try:
        # Load cutoff data based on exam - prioritize new 1000 colleges data
        cutoff_files = [
            f"data/{exam}_1000_cutoffs.json",  # New 1000 colleges data
            f"data/{exam}_cutoffs.json"        # Fallback to existing data
        ]
        
        cutoffs_data = []
        for cutoff_file in cutoff_files:
            data_path = Path(cutoff_file)
            if data_path.exists():
                try:
                    with open(data_path, 'r', encoding='utf-8') as f:
                        file_data = json.load(f)
                        cutoffs_data.extend(file_data)
                        print(f"Loaded {len(file_data)} records from {cutoff_file}")
                except Exception as e:
                    print(f"Error loading {cutoff_file}: {e}")
        
        if not cutoffs_data:
            raise HTTPException(
                status_code=404, 
                detail=f"Cutoff data for {exam} not found"
            )
        
        # Filter cutoffs for the specific college
        college_cutoffs = []
        college_name_lower = college_name.lower()
        
        for cutoff in cutoffs_data:
            if college_name_lower in cutoff["college"].lower():
                college_cutoffs.append(cutoff)
        
        if not college_cutoffs:
            raise HTTPException(
                status_code=404,
                detail=f"No cutoff data found for {college_name} in {exam}"
            )
        
        return {
            "college": college_name,
            "exam": exam,
            "cutoffs": college_cutoffs
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/colleges")
async def get_all_colleges(
    exam: Optional[str] = None,
    limit: int = Query(1000, description="Maximum number of colleges to return; pass 0 or a negative value for no limit")
):
    """
    Get list of all colleges, optionally filtered by exam
    """
    try:
        colleges = []
        
        if exam:
            # Load colleges from specific exam data - prioritize new 1000 colleges data
            cutoff_files = [
                f"data/{exam}_1000_cutoffs.json",  # New 1000 colleges data
                f"data/{exam}_cutoffs.json"        # Fallback to existing data
            ]
            
            cutoffs_data = []
            for cutoff_file in cutoff_files:
                data_path = Path(cutoff_file)
                if data_path.exists():
                    try:
                        with open(data_path, 'r', encoding='utf-8') as f:
                            file_data = json.load(f)
                            cutoffs_data.extend(file_data)
                            print(f"Loaded {len(file_data)} records from {cutoff_file}")
                    except Exception as e:
                        print(f"Error loading {cutoff_file}: {e}")
            
            if cutoffs_data:
                # Extract unique colleges
                college_names = set()
                for cutoff in cutoffs_data:
                    college_names.add(cutoff["college"])

                colleges_list = list(college_names)
                colleges = colleges_list[:limit] if limit > 0 else colleges_list
        else:
            # Load from enhanced college data
            data_path = Path("data/college_info_enhanced.json")
            if not data_path.exists():
                data_path = Path("data/college_info.json")
            
            if data_path.exists():
                with open(data_path, 'r', encoding='utf-8') as f:
                    colleges_data = json.load(f)

                # Return enhanced college info
                all_enhanced: list[dict] = []
                for college in colleges_data:
                    all_enhanced.append({
                        "name": college["name"],
                        "location": college.get("location", "N/A"),
                        "nirf_rank": college.get("nirf_rank"),
                        "world_rank": college.get("world_rank"),
                        "overall_rating": college.get("ratings", {}).get("overall"),
                        "overview": college.get("overview", "")[:200] + "..." if len(college.get("overview", "")) > 200 else college.get("overview", "")
                    })

                enhanced_colleges = all_enhanced[:limit] if limit > 0 else all_enhanced

                return {
                    "colleges": enhanced_colleges,
                    "total": len(all_enhanced),
                    "exam": exam
                }
        
        return {
            "colleges": colleges,
            "total": len(colleges),
            "exam": exam
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/colleges/by-ranking")
async def get_colleges_by_ranking(category: str = "engineering", limit: int = 20):
    """
    Get colleges sorted by NIRF ranking
    """
    try:
        # Load enhanced college data
        data_path = Path("data/college_info_enhanced.json")
        if not data_path.exists():
            data_path = Path("data/college_info.json")
        
        if not data_path.exists():
            raise HTTPException(status_code=404, detail="College data not found")
        
        with open(data_path, 'r', encoding='utf-8') as f:
            colleges_data = json.load(f)
        
        # Filter colleges based on category and rank
        filtered_colleges = []
        
        for college in colleges_data:
            nirf_rank = college.get("nirf_rank")
            if nirf_rank is not None:  # Only include colleges with NIRF rank
                # Category filtering
                if category == "engineering" and ("IIT" in college["name"] or "NIT" in college["name"]):
                    filtered_colleges.append(college)
                elif category == "medical" and "AIIMS" in college["name"]:
                    filtered_colleges.append(college)
                elif category == "all":
                    filtered_colleges.append(college)
        
        # Sort by NIRF rank (lower rank number = better rank)
        filtered_colleges.sort(key=lambda x: x.get("nirf_rank", float('inf')))
        
        # Limit results
        filtered_colleges = filtered_colleges[:limit]
        
        # Format response
        ranked_colleges = []
        for college in filtered_colleges:
            ranked_colleges.append({
                "name": college["name"],
                "nirf_rank": college.get("nirf_rank"),
                "location": college.get("location", "N/A"),
                "established": college.get("established"),
                "overall_rating": college.get("ratings", {}).get("overall"),
                "placement_percentage": college.get("placement_stats", {}).get("placement_percentage"),
                "average_package": college.get("placement_stats", {}).get("average_package"),
                "overview": college.get("overview", "")[:150] + "..." if len(college.get("overview", "")) > 150 else college.get("overview", "")
            })
        
        return {
            "category": category,
            "colleges": ranked_colleges,
            "total": len(ranked_colleges),
            "message": f"Top {len(ranked_colleges)} colleges sorted by NIRF ranking"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/college/{college_name}/insights")
async def get_college_insights(college_name: str):
    """
    Get comprehensive insights about a college including ratings, pros/cons, fees
    """
    try:
        # Load enhanced college data
        data_path = Path("data/college_info_enhanced.json")
        if not data_path.exists():
            raise HTTPException(status_code=404, detail="Enhanced college data not found")

        with open(data_path, 'r', encoding='utf-8') as f:
            colleges_data = json.load(f)

        # Search for college
        college_name_lower = college_name.lower()
        college_info = None

        for college in colleges_data:
            if college_name_lower in college["name"].lower():
                college_info = college
                break

        if not college_info:
            raise HTTPException(
                status_code=404,
                detail=f"College '{college_name}' not found"
            )

        # Return insights
        return {
            "college_name": college_info["name"],
            "overview": college_info.get("overview", ""),
            "established": college_info.get("established"),
            "location": college_info.get("location"),
            "affiliation": college_info.get("affiliation"),
            "nirf_rank": college_info.get("nirf_rank"),
            "world_rank": college_info.get("world_rank"),
            "ratings": college_info.get("ratings", {}),
            "pros": college_info.get("pros", []),
            "cons": college_info.get("cons", []),
            "fees": college_info.get("fees", {}),
            "placement_stats": college_info.get("placement_stats", {}),
            "facilities": college_info.get("facilities", []),
            "courses_offered": college_info.get("courses_offered", []),
            "contact": college_info.get("contact", {}),
            "website": college_info.get("website"),
            "scholarships": college_info.get("scholarships", {
                "merit_based": ["Academic Excellence", "Sports Achievement"],
                "need_based": ["Income-based", "First Generation"],
                "government": ["PM Scholarship", "State Merit"],
                "external": ["Corporate Sponsorship", "NGO Support"]
            })
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/college/{college_name}/ratings")
async def get_college_ratings(college_name: str):
    """
    Get detailed ratings breakdown for a college
    """
    try:
        # Load enhanced college data
        data_path = Path("data/college_info_enhanced.json")
        if not data_path.exists():
            raise HTTPException(status_code=404, detail="Enhanced college data not found")

        with open(data_path, 'r', encoding='utf-8') as f:
            colleges_data = json.load(f)

        # Search for college
        college_name_lower = college_name.lower()
        college_info = None

        for college in colleges_data:
            if college_name_lower in college["name"].lower():
                college_info = college
                break

        if not college_info:
            raise HTTPException(
                status_code=404,
                detail=f"College '{college_name}' not found"
            )

        ratings = college_info.get("ratings", {})
        
        return {
            "college_name": college_info["name"],
            "overall_rating": ratings.get("overall"),
            "detailed_ratings": {
                "academics": ratings.get("academics"),
                "campus": ratings.get("campus"),
                "placements": ratings.get("placements"),
                "roi": ratings.get("roi"),
                "faculty": ratings.get("faculty"),
                "infrastructure": ratings.get("infrastructure")
            },
            "nirf_rank": college_info.get("nirf_rank"),
            "world_rank": college_info.get("world_rank")
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/college/{college_name}/fees")
async def get_college_fees(college_name: str):
    """
    Get detailed fee structure for a college
    """
    try:
        # Load enhanced college data
        data_path = Path("data/college_info_enhanced.json")
        if not data_path.exists():
            raise HTTPException(status_code=404, detail="Enhanced college data not found")

        with open(data_path, 'r', encoding='utf-8') as f:
            colleges_data = json.load(f)

        # Search for college
        college_name_lower = college_name.lower()
        college_info = None

        for college in colleges_data:
            if college_name_lower in college["name"].lower():
                college_info = college
                break

        if not college_info:
            raise HTTPException(
                status_code=404,
                detail=f"College '{college_name}' not found"
            )

        fees = college_info.get("fees", {})
        
        return {
            "college_name": college_info["name"],
            "fee_structure": {
                "tuition_fee": fees.get("tuition_fee"),
                "hostel_fee": fees.get("hostel_fee"),
                "mess_fee": fees.get("mess_fee"),
                "other_charges": fees.get("other_charges"),
                "total_annual": fees.get("total_annual")
            },
            "currency": "INR" if "IIT" in college_info["name"] or "NIT" in college_info["name"] or "AIIMS" in college_info["name"] else "CAD",
            "notes": "Fees are approximate and may vary. Contact college for exact details."
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/college/{college_name}/placement")
async def get_college_placement(college_name: str):
    """
    Get detailed placement statistics for a college
    """
    try:
        # Load enhanced college data
        data_path = Path("data/college_info_enhanced.json")
        if not data_path.exists():
            raise HTTPException(status_code=404, detail="Enhanced college data not found")

        with open(data_path, 'r', encoding='utf-8') as f:
            colleges_data = json.load(f)

        # Search for college
        college_name_lower = college_name.lower()
        college_info = None

        for college in colleges_data:
            if college_name_lower in college["name"].lower():
                college_info = college
                break

        if not college_info:
            raise HTTPException(
                status_code=404,
                detail=f"College '{college_name}' not found"
            )

        placement_stats = college_info.get("placement_stats", {})
        
        return {
            "college_name": college_info["name"],
            "placement_statistics": {
                "average_package": placement_stats.get("average_package"),
                "highest_package": placement_stats.get("highest_package"),
                "placement_percentage": placement_stats.get("placement_percentage"),
                "internship_offers": placement_stats.get("internship_offers"),
                "international_offers": placement_stats.get("international_offers")
            },
            "top_recruiters": placement_stats.get("top_recruiters", []),
            "currency": "INR" if "IIT" in college_info["name"] or "NIT" in college_info["name"] or "AIIMS" in college_info["name"] else "CAD"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/colleges/fee-filter")
async def filter_colleges_by_fee(
    min_fee: int = 0,
    max_fee: int = 1000000,
    category: str = "general",
    exam_type: str = "engineering",
    limit: int = 50
):
    """
    Filter colleges by fee range with caste-based fee consideration
    category options: general, obc_ncl, sc_st, pwd
    exam_type options: engineering, medical, all
    """
    try:
        # Load enhanced college data
        data_path = Path("data/college_info_enhanced.json")
        if not data_path.exists():
            data_path = Path("data/college_info.json")
        
        if not data_path.exists():
            raise HTTPException(status_code=404, detail="College data not found")
        
        with open(data_path, 'r', encoding='utf-8') as f:
            colleges_data = json.load(f)
        
        filtered_colleges = []
        
        for college in colleges_data:
            # Filter by exam type
            if exam_type == "engineering" and not ("IIT" in college["name"] or "NIT" in college["name"] or "IISC" in college["name"]):
                continue
            elif exam_type == "medical" and "AIIMS" not in college["name"]:
                continue
            
            # Get fee based on category
            college_fee = 0
            
            # Check if detailed fee structure exists
            fee_structure = college.get("fee_structure_detailed", {})
            if fee_structure and category in fee_structure:
                college_fee = fee_structure[category].get("total_annual", 0)
            else:
                # Fallback to general fee structure
                fees = college.get("fees", {})
                college_fee = fees.get("total_annual", 0)
                
                # Apply category-based discounts if detailed structure doesn't exist
                if category == "sc_st" or category == "pwd":
                    # SC/ST and PWD typically get free tuition and hostel
                    tuition_fee = fees.get("tuition_fee", 0)
                    hostel_fee = fees.get("hostel_fee", 0)
                    college_fee = college_fee - tuition_fee - hostel_fee
            
            # Filter by fee range
            if min_fee <= college_fee <= max_fee:
                filtered_colleges.append({
                    "name": college["name"],
                    "location": college.get("location", "N/A"),
                    "nirf_rank": college.get("nirf_rank"),
                    "total_fee": college_fee,
                    "category_applied": category,
                    "fee_breakdown": fee_structure.get(category, fees) if fee_structure else fees,
                    "placement_percentage": college.get("placement_stats", {}).get("placement_percentage"),
                    "average_package": college.get("placement_stats", {}).get("average_package"),
                    "established": college.get("established"),
                    "website": college.get("website"),
                    "overview": college.get("overview", "")[:200] + "..." if len(college.get("overview", "")) > 200 else college.get("overview", "")
                })
        
        # Sort by fee (ascending)
        filtered_colleges.sort(key=lambda x: x["total_fee"])
        
        # Limit results
        filtered_colleges = filtered_colleges[:limit]
        
        return {
            "filters_applied": {
                "min_fee": min_fee,
                "max_fee": max_fee,
                "category": category,
                "exam_type": exam_type
            },
            "colleges": filtered_colleges,
            "total_found": len(filtered_colleges),
            "category_info": {
                "general": "No reservation benefits",
                "obc_ncl": "OBC Non-Creamy Layer - Same fee as General",
                "sc_st": "SC/ST - Free tuition and hostel fees",
                "pwd": "Persons with Disabilities - Free tuition and hostel fees"
            }.get(category, "Unknown category")
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/colleges/fee-comparison")
async def compare_fees_by_category(
    college_names: str,
    exam_type: str = "engineering"
):
    """
    Compare fees across different categories for specified colleges
    college_names: comma-separated list of college names
    """
    try:
        # Parse college names
        colleges_to_compare = [name.strip() for name in college_names.split(",")]
        
        # Load enhanced college data
        data_path = Path("data/college_info_enhanced.json")
        if not data_path.exists():
            data_path = Path("data/college_info.json")
        
        if not data_path.exists():
            raise HTTPException(status_code=404, detail="College data not found")
        
        with open(data_path, 'r', encoding='utf-8') as f:
            colleges_data = json.load(f)
        
        comparison_data = []
        
        for college in colleges_data:
            # Check if this college is in the comparison list
            college_name = college["name"]
            if not any(compare_name.lower() in college_name.lower() for compare_name in colleges_to_compare):
                continue
            
            # Filter by exam type
            if exam_type == "engineering" and not ("IIT" in college["name"] or "NIT" in college["name"] or "IISC" in college["name"]):
                continue
            elif exam_type == "medical" and "AIIMS" not in college["name"]:
                continue
            
            fee_structure = college.get("fee_structure_detailed", {})
            general_fees = college.get("fees", {})
            
            college_comparison = {
                "name": college_name,
                "location": college.get("location"),
                "nirf_rank": college.get("nirf_rank"),
                "fee_by_category": {},
                "reservation_info": college.get("admission_criteria", {}).get("reservation_details", {})
            }
            
            # Categories to compare
            categories = ["general", "obc_ncl", "sc_st", "pwd"]
            
            for category in categories:
                if fee_structure and category in fee_structure:
                    college_comparison["fee_by_category"][category] = fee_structure[category]
                else:
                    # Calculate fees for categories without detailed structure
                    if category == "general" or category == "obc_ncl":
                        college_comparison["fee_by_category"][category] = general_fees
                    else:  # sc_st or pwd
                        reduced_fees = general_fees.copy()
                        reduced_fees["tuition_fee"] = 0
                        reduced_fees["hostel_fee"] = 0
                        reduced_fees["total_annual"] = reduced_fees.get("mess_fee", 0) + reduced_fees.get("other_charges", 0)
                        college_comparison["fee_by_category"][category] = reduced_fees
            
            comparison_data.append(college_comparison)
        
        if not comparison_data:
            raise HTTPException(
                status_code=404,
                detail=f"No colleges found matching: {college_names}"
            )
        
        return {
            "colleges_compared": len(comparison_data),
            "comparison_data": comparison_data,
            "category_explanations": {
                "general": "Full fees applicable",
                "obc_ncl": "OBC Non-Creamy Layer - Same fees as General category",
                "sc_st": "Scheduled Caste/Scheduled Tribe - Tuition and hostel fees waived",
                "pwd": "Persons with Disabilities - Tuition and hostel fees waived"
            },
            "reservation_percentages": {
                "general": "50%",
                "obc_ncl": "27%",
                "sc": "15%",
                "st": "7.5%",
                "pwd": "5% (horizontal reservation)"
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/colleges/affordable")
async def get_affordable_colleges(
    category: str = "general",
    max_budget: int = 200000,
    exam_type: str = "engineering",
    limit: int = 20
):
    """
    Get most affordable colleges for a specific category and budget
    """
    try:
        # Load enhanced college data
        data_path = Path("data/college_info_enhanced.json")
        if not data_path.exists():
            data_path = Path("data/college_info.json")
        
        if not data_path.exists():
            raise HTTPException(status_code=404, detail="College data not found")
        
        with open(data_path, 'r', encoding='utf-8') as f:
            colleges_data = json.load(f)
        
        affordable_colleges = []
        
        for college in colleges_data:
            # Filter by exam type
            if exam_type == "engineering" and not ("IIT" in college["name"] or "NIT" in college["name"] or "IISC" in college["name"]):
                continue
            elif exam_type == "medical" and "AIIMS" not in college["name"]:
                continue
            
            # Get fee for the category
            fee_structure = college.get("fee_structure_detailed", {})
            general_fees = college.get("fees", {})
            
            if fee_structure and category in fee_structure:
                annual_fee = fee_structure[category].get("total_annual", 0)
                fee_details = fee_structure[category]
            else:
                # Calculate based on category
                if category == "general" or category == "obc_ncl":
                    annual_fee = general_fees.get("total_annual", 0)
                    fee_details = general_fees
                else:  # sc_st or pwd
                    annual_fee = general_fees.get("mess_fee", 0) + general_fees.get("other_charges", 0)
                    fee_details = {
                        "tuition_fee": 0,
                        "hostel_fee": 0,
                        "mess_fee": general_fees.get("mess_fee", 0),
                        "other_charges": general_fees.get("other_charges", 0),
                        "total_annual": annual_fee
                    }
            
            if annual_fee <= max_budget:
                affordable_colleges.append({
                    "name": college["name"],
                    "location": college.get("location"),
                    "nirf_rank": college.get("nirf_rank"),
                    "annual_fee": annual_fee,
                    "fee_details": fee_details,
                    "savings_from_general": (general_fees.get("total_annual", 0) - annual_fee) if category != "general" else 0,
                    "placement_percentage": college.get("placement_stats", {}).get("placement_percentage"),
                    "average_package": college.get("placement_stats", {}).get("average_package"),
                    "roi_years": round((annual_fee * 4) / max(college.get("placement_stats", {}).get("average_package", 1), 1), 2),
                    "website": college.get("website")
                })
        
        # Sort by annual fee (ascending) and then by NIRF rank
        affordable_colleges.sort(key=lambda x: (x["annual_fee"], x["nirf_rank"] or 999))
        
        # Limit results
        affordable_colleges = affordable_colleges[:limit]
        
        return {
            "search_criteria": {
                "category": category,
                "max_budget": max_budget,
                "exam_type": exam_type
            },
            "colleges": affordable_colleges,
            "total_found": len(affordable_colleges),
            "budget_info": {
                "category": category,
                "max_budget": max_budget,
                "note": f"Fees shown are for {category} category. Actual fees may vary."
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 

@router.get("/colleges/states")
async def get_supported_states(exam: Optional[str] = Query("jee", description="Exam dataset to derive states from")):
    """
    Return the list of states available in the datasets.
    """
    try:
        states: set[str] = set()

        def extract_state_from_location(location: str) -> Optional[str]:
            if not location:
                return None
            # Expect formats like "City, State" or just "State"
            parts = [p.strip() for p in location.split(",")]
            if len(parts) >= 2:
                return parts[-1]
            return parts[0] if parts else None

        # Scan primary cutoff files - prioritize new 1000 colleges data
        for fname in [f"data/{exam}_1000_cutoffs.json", f"data/{exam}_cutoffs_extended.json", f"data/{exam}_cutoffs.json"]:
            data_path = Path(fname)
            if data_path.exists():
                try:
                    with open(data_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    for row in data:
                        st = extract_state_from_location(row.get("location", ""))
                        if st:
                            states.add(st)
                except Exception as e:
                    print(f"Error loading {fname}: {e}")

        # Scan state-specific collections (e.g., uttar_pradesh_colleges_jee.json)
        data_dir = Path("data")
        if data_dir.exists():
            for child in data_dir.iterdir():
                name = child.name.lower()
                if name.endswith("_colleges_jee.json") and child.is_file():
                    with open(child, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    for row in data:
                        st = extract_state_from_location(row.get("location", ""))
                        if st:
                            states.add(st)

        return {"states": sorted(states)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/colleges/by-state")
async def get_colleges_by_state(
    state: str = Query(..., description="State name to filter by (case-insensitive)"),
    ownership: Optional[str] = Query(None, description="Filter by ownership: government | private"),
    exam: str = Query("jee", description="Exam dataset to query against"),
    limit: int = Query(100, description="Maximum number of colleges to return; pass 0 or a negative value for no limit")
):
    """
    Get colleges for a given state, optionally filtered by ownership (Government/Private).
    Ownership is taken from state-specific datasets when available; otherwise inferred best-effort.
    """
    try:
        normalized_state = state.strip().lower()
        results: dict[str, dict] = {}

        def extract_state_from_location(location: str) -> Optional[str]:
            if not location:
                return None
            parts = [p.strip() for p in location.split(",")]
            if len(parts) >= 2:
                return parts[-1]
            return parts[0] if parts else None

        def infer_ownership(college_name: str) -> Optional[str]:
            if not college_name:
                return None
            name = college_name.lower()
            gov_keywords = ["iit", "nit", "iiit", "government", "aiims", "nlud", "nlu", "iisc", "central university"]
            if any(k in name for k in gov_keywords):
                return "Government"
            return None

        # Helper to add a row to results with ownership resolution
        def add_result(row: dict):
            college_name = row.get("college") or row.get("name")
            if not college_name:
                return
            location = row.get("location", "")
            st = extract_state_from_location(location)
            if not st or st.strip().lower() != normalized_state:
                return

            detected_type = row.get("type")
            if not detected_type:
                detected_type = infer_ownership(college_name)
            # Normalize
            if detected_type:
                if detected_type.lower().startswith("gov"):
                    detected_type = "Government"
                elif detected_type.lower().startswith("priv"):
                    detected_type = "Private"

            key = college_name.lower()
            if key not in results:
                results[key] = {
                    "name": college_name,
                    "location": location,
                    "type": detected_type or "Unknown",
                    "exam_type": row.get("exam_type") or exam,
                    "branch": row.get("branch"),
                    "opening_rank": row.get("opening_rank"),
                    "closing_rank": row.get("closing_rank")
                }
            else:
                # Prefer a known ownership if previously unknown
                if results[key]["type"] == "Unknown" and detected_type:
                    results[key]["type"] = detected_type

        # Load from exam cutoff files - prioritize new 1000 colleges data
        for fname in [f"data/{exam}_1000_cutoffs.json", f"data/{exam}_cutoffs_extended.json", f"data/{exam}_cutoffs.json"]:
            data_path = Path(fname)
            if data_path.exists():
                try:
                    with open(data_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    for row in data:
                        add_result(row)
                except Exception as e:
                    print(f"Error loading {fname}: {e}")

        # Load from state-specific files
        data_dir = Path("data")
        if data_dir.exists():
            for child in data_dir.iterdir():
                name = child.name.lower()
                if name.endswith("_colleges_jee.json") and child.is_file():
                    with open(child, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    for row in data:
                        add_result(row)

        colleges = list(results.values())

        # Apply ownership filter if provided
        if ownership:
            own = ownership.strip().lower()
            if own in ("government", "gov", "govt"):
                colleges = [c for c in colleges if c.get("type") == "Government"]
            elif own in ("private",):
                colleges = [c for c in colleges if c.get("type") == "Private"]

        # Sort: Government first, then name
        ownership_rank = {"Government": 0, "Private": 1, "Unknown": 2}
        colleges.sort(key=lambda c: (ownership_rank.get(c.get("type"), 9), c.get("name", "")))

        if limit > 0:
            colleges = colleges[:limit]

        counts = {
            "government": sum(1 for c in colleges if c.get("type") == "Government"),
            "private": sum(1 for c in colleges if c.get("type") == "Private"),
            "unknown": sum(1 for c in colleges if c.get("type") == "Unknown"),
        }

        return {
            "state": state,
            "ownership_filter": ownership,
            "exam": exam,
            "counts": counts,
            "colleges": colleges,
            "total": len(colleges)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
