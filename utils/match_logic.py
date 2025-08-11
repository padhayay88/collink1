import json
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

class CollegePredictor:
    def __init__(self):
        self.data_path = Path("data")
        self.cutoff_data = {}
        self.load_cutoff_data()
    
    def load_cutoff_data(self):
        """Load all cutoff data from JSON files"""
        exam_files = {
            "jee": ["jee_1000_cutoffs.json", "jee_massive_cutoffs.json", "jee_cutoffs_extended.json", "jee_cutoffs_extended_v2.json", "diverse_colleges_jee.json", "gujarat_colleges_jee.json", "uttar_pradesh_colleges_jee.json"],  # New 1000 colleges + Massive database + existing sources
            "neet": ["neet_1000_cutoffs.json", "neet_massive_cutoffs.json", "neet_cutoffs.json", "neet_cutoffs_extended.json"],
            "ielts": ["ielts_1000_cutoffs.json", "ielts_massive_cutoffs.json", "ielts_cutoffs.json"]
        }
        
        for exam, filenames in exam_files.items():
            all_data = []
            
            # Handle single file or list of files
            if isinstance(filenames, str):
                filenames = [filenames]
            
            for filename in filenames:
                file_path = self.data_path / filename
                if file_path.exists():
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            raw_data = json.load(f)
                            all_data.extend(raw_data)
                            print(f"Loaded {len(raw_data)} records from {filename}")
                    except Exception as e:
                        print(f"Error loading {filename}: {e}")
                else:
                    print(f"Data file not found: {filename}")
            
            # Clean and store the combined data
            self.cutoff_data[exam] = self._clean_cutoff_data(all_data, exam)
            print(f"Total valid records for {exam}: {len(self.cutoff_data[exam])}")
    
    def _clean_cutoff_data(self, raw_data: List[Dict[str, Any]], exam: str) -> List[Dict[str, Any]]:
        """Clean and validate cutoff data"""
        cleaned_data = []
        
        for record in raw_data:
            try:
                # Skip records with invalid or negative ranks
                if exam in ["jee", "neet"]:
                    # Handle both old format (closing_rank/opening_rank) and new format (rank)
                    closing_rank = record.get("closing_rank") or record.get("rank")
                    opening_rank = record.get("opening_rank")
                    
                    # Skip if closing rank is negative or zero
                    if not closing_rank or closing_rank <= 0:
                        continue
                    
                    # Ensure closing_rank is set in the record for consistency
                    record["closing_rank"] = closing_rank
                    
                    # For new format without opening rank, set it to closing rank
                    if opening_rank is None:
                        opening_rank = closing_rank
                        record["opening_rank"] = opening_rank
                        
                    # Skip if opening rank is negative (but allow 0 and 1 as valid)
                    if opening_rank < 0:
                        continue
                    
                    # Skip if opening rank is greater than closing rank
                    if opening_rank > closing_rank:
                        continue
                        
                # Ensure required fields exist - handle both old and new formats
                college_name = record.get("college") or record.get("college_name")
                branch_name = record.get("branch") or record.get("program")
                
                if not college_name or not branch_name:
                    continue
                
                # Standardize field names
                record["college"] = college_name
                record["branch"] = branch_name
                
                if exam == "ielts":
                    # For IELTS, check score ranges - handle both old and new formats
                    min_score = record.get("min_score") or record.get("score")
                    max_score = record.get("max_score") or record.get("score")
                    
                    if not min_score:
                        continue
                    
                    # For new format, we have single score, for old format we have range
                    if record.get("max_score"):  # Old format with range
                        if min_score <= 0 or max_score <= 0 or min_score > max_score:
                            continue
                    else:  # New format with single score
                        if min_score < 0:
                            continue
                        # Set max_score to min_score for new format
                        record["max_score"] = min_score
                    
                    college_name = record.get("college") or record.get("college_name")
                    if not college_name:
                        continue
                    
                    # Standardize field names
                    record["college"] = college_name
                
                # Add exam_type if not present
                if "exam_type" not in record:
                    record["exam_type"] = exam
                    
                cleaned_data.append(record)
                
            except (ValueError, TypeError, KeyError) as e:
                # Skip invalid records
                continue
        
        return cleaned_data
    
    def predict_colleges(
        self, 
        exam: str, 
        rank: int, 
        category: str = "General",
        gender: str = "All",
        quota: str = "All India",
        tolerance_percent: float = 0.0,
        states: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Predict colleges based on rank and exam
        """
        if exam not in self.cutoff_data:
            return []
        
        predictions = []
        cutoff_data = self.cutoff_data[exam]
        
        normalized_states = None
        if states:
            normalized_states = {s.strip().lower() for s in states if isinstance(s, str) and s.strip()}

        for cutoff in cutoff_data:
            # Check if rank falls within the cutoff range
            if self._is_rank_eligible(cutoff, rank, category, gender, quota, tolerance_percent):
                # Optional state filter (India exams only)
                if exam in ["jee", "neet"] and normalized_states:
                    # Handle both old format (location) and new format (state)
                    location = cutoff.get("location") or cutoff.get("state") or ""
                    loc = location.lower()
                    # accept match if any chosen state appears anywhere in the location/state
                    if not any(st in loc for st in normalized_states):
                        continue
                prediction = self._create_prediction(cutoff, rank, exam)
                predictions.append(prediction)
        
        # Sort by confidence level (High, Medium, Low) and then by closing rank
        confidence_order = {"High": 0, "Medium": 1, "Low": 2}
        predictions.sort(key=lambda x: (confidence_order.get(x.get("confidence_level"), 3), x.get("closing_rank", float('inf'))))
        
        # Expand capacity but keep response bounded
        return predictions[:500]
    
    def _is_rank_eligible(
        self,
        cutoff: Dict[str, Any],
        rank: int,
        category: str,
        gender: str,
        quota: str,
        tolerance_percent: float = 0.0,
    ) -> bool:
        """Check if rank is eligible for this college/branch"""
        try:
            # Case-insensitive matching
            if category.lower() != 'all' and cutoff.get("category", "").strip().lower() != category.strip().lower():
                return False

            if quota.lower() != 'all' and cutoff.get("quota", "").strip().lower() != quota.strip().lower():
                return False

            if gender.lower() != 'all' and cutoff.get("gender") and cutoff.get("gender", "").strip().lower() != gender.strip().lower():
                return False

            exam_type = cutoff.get("exam_type")

            if exam_type == "ielts":
                min_score = cutoff.get("min_score")
                max_score = cutoff.get("max_score")
                if min_score is None or max_score is None:
                    return False
                score = float(rank) / 10.0
                return min_score <= score <= max_score

            elif exam_type in ["jee", "neet"]:
                # More realistic eligibility: show colleges where user rank is within reasonable range
                opening_rank = cutoff.get("opening_rank")
                closing_rank = cutoff.get("closing_rank")

                if closing_rank is None:
                    return False

                # Apply optional tolerance on the upper bound
                try:
                    tol = max(0.0, float(tolerance_percent))
                except (ValueError, TypeError):
                    tol = 0.0
                closing_with_tol = closing_rank * (1.0 + tol / 100.0)

                # More flexible approach: if opening_rank is 1 (top colleges), allow broader range
                if isinstance(opening_rank, (int, float)) and opening_rank > 0:
                    if opening_rank == 1:
                        # For top colleges (opening_rank = 1), allow ranks up to 2x closing_rank
                        # This is more realistic as top colleges often have broader admission ranges
                        return rank <= closing_with_tol * 2
                    else:
                        # For other colleges, use the normal range check
                        return opening_rank <= rank <= closing_with_tol

                # Fallback: enforce upper bound only
                return rank <= closing_with_tol

            return False

        except (ValueError, TypeError):
            return False
    
    def _create_prediction(
        self, 
        cutoff: Dict[str, Any], 
        rank: int, 
        exam: str
    ) -> Dict[str, Any]:
        """Create a prediction object"""
        
        if exam == "ielts":
            # Handle IELTS predictions
            min_score = cutoff.get("min_score", 0)
            max_score = cutoff.get("max_score", 9.0)
            score = float(rank) / 10.0
            
            # Calculate confidence for IELTS
            if score >= min_score and score <= max_score:
                confidence_score = 1.0
            else:
                confidence_score = 0.0
            
            confidence_level = "High" if confidence_score >= 0.8 else "Medium" if confidence_score >= 0.5 else "Low"
            
            return {
                "college": cutoff["college"],
                "branch": cutoff.get("branch", "N/A"),
                "exam": exam,
                "min_score": min_score,
                "max_score": max_score,
                "your_score": score,
                "confidence_score": confidence_score,
                "confidence_level": confidence_level,
                "location": cutoff.get("location", "N/A"),
                "category": cutoff.get("category", "International"),
                "quota": cutoff.get("quota", "International"),
                "last_updated": cutoff.get("last_updated", datetime.now().isoformat())
            }
        else:
            # Handle JEE/NEET predictions
            closing_rank = cutoff.get("closing_rank", 0)
            opening_rank = cutoff.get("opening_rank", 0)
            
            # Calculate confidence score
            confidence_score = self._calculate_confidence(rank, closing_rank, opening_rank)
            
            # Determine confidence level
            if confidence_score >= 0.8:
                confidence_level = "High"
            elif confidence_score >= 0.5:
                confidence_level = "Medium"
            else:
                confidence_level = "Low"
            
            return {
                "college": cutoff["college"],
                "branch": cutoff.get("branch", "N/A"),
                "exam": exam,
                "opening_rank": opening_rank,
                "closing_rank": closing_rank,
                "your_rank": rank,
                "confidence_score": confidence_score,
                "confidence_level": confidence_level,
                "location": cutoff.get("location", "N/A"),
                "category": cutoff.get("category", "General"),
                "quota": cutoff.get("quota", "All India"),
                "last_updated": cutoff.get("last_updated", datetime.now().isoformat())
            }
    
    def _calculate_confidence(self, rank: int, closing_rank: int, opening_rank: int) -> float:
        """Calculate confidence score based on rank position"""
        try:
            if closing_rank == 0:
                return 0.0
            
            # Calculate position within the rank range
            if closing_rank > opening_rank:
                total_range = closing_rank - opening_rank
                position = closing_rank - rank
                
                if position <= 0:
                    return 0.0
                elif position >= total_range:
                    return 1.0
                else:
                    return position / total_range
            else:
                # If closing rank is lower than opening rank (unusual case)
                return 0.5 if rank <= closing_rank else 0.0
                
        except Exception:
            return 0.0
    
    def get_college_stats(self, college_name: str, exam: str) -> Dict[str, Any]:
        """Get statistics for a specific college"""
        if exam not in self.cutoff_data:
            return {}
        
        college_cutoffs = []
        for cutoff in self.cutoff_data[exam]:
            if cutoff["college"].lower() == college_name.lower():
                college_cutoffs.append(cutoff)
        
        if not college_cutoffs:
            return {}
        
        # Calculate statistics
        total_branches = len(college_cutoffs)
        avg_closing_rank = sum(c.get("closing_rank", 0) for c in college_cutoffs) / total_branches
        best_rank = min(c.get("closing_rank", float('inf')) for c in college_cutoffs)
        worst_rank = max(c.get("closing_rank", 0) for c in college_cutoffs)
        
        return {
            "college": college_name,
            "exam": exam,
            "total_branches": total_branches,
            "average_closing_rank": round(avg_closing_rank, 2),
            "best_rank": best_rank,
            "worst_rank": worst_rank,
            "branches": [c.get("branch", "N/A") for c in college_cutoffs]
        }
    
    def get_rank_trends(self, exam: str, college_name: str = None) -> Dict[str, Any]:
        """Get rank trends for colleges"""
        if exam not in self.cutoff_data:
            return {}
        
        cutoff_data = self.cutoff_data[exam]
        
        if college_name:
            # Filter for specific college
            cutoff_data = [c for c in cutoff_data if c["college"].lower() == college_name.lower()]
        
        # Group by year if available
        trends = {}
        for cutoff in cutoff_data:
            year = cutoff.get("year", "Unknown")
            if year not in trends:
                trends[year] = []
            trends[year].append(cutoff)
        
        return {
            "exam": exam,
            "college": college_name,
            "trends": trends,
            "total_records": len(cutoff_data)
        } 