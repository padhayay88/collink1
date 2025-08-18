import json
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
import time

# Safe print for consoles that don't support unicode emojis (e.g., Windows cp1252)
def safe_print(message: str) -> None:
    try:
        print(message)
    except Exception:
        try:
            print(str(message).encode('ascii', 'ignore').decode())
        except Exception:
            # Last resort: print without emojis by filtering non-ascii
            fallback = ''.join(ch for ch in str(message) if ord(ch) < 128)
            print(fallback)

class CollegePredictorOptimized:
    def __init__(self, load_essential_only=True):
        # Get the directory of the current script
        script_dir = Path(__file__).parent.parent
        self.data_path = script_dir / "data"
        self.cutoff_data = {}
        self.data_loaded = {}
        self.load_essential_only = load_essential_only
        self.load_essential_data()
    
    def load_essential_data(self):
        """Load only essential data for fast startup"""
        safe_print("Loading essential college data for fast startup...")
        start_time = time.time()
        
        # Load massive datasets for comprehensive coverage
        essential_files = {
            "jee": ["jee_massive_cutoffs.json", "jee_comprehensive_cutoffs.json", "jee_10000_cutoffs.json"],
            "neet": ["neet_massive_cutoffs.json", "neet_comprehensive_cutoffs.json", "neet_10000_cutoffs.json"], 
            "ielts": ["ielts_massive_cutoffs.json", "ielts_10000_cutoffs.json"],
            "cat": ["cat_mba_colleges_from_pdf.json"]
        }
        
        for exam, filenames in essential_files.items():
            all_data = []
            
            for filename in filenames:
                file_path = self.data_path / filename
                if file_path.exists():
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            raw_data = json.load(f)
                            all_data.extend(raw_data)
                            safe_print(f"Loaded {len(raw_data)} records from {filename}")
                    except Exception as e:
                        safe_print(f"Error loading {filename}: {e}")
                else:
                    safe_print(f"Data file not found: {filename}")
            
            # Clean and store the essential data
            self.cutoff_data[exam] = self._clean_cutoff_data(all_data, exam)
            self.data_loaded[exam] = "essential"
            safe_print(f"Total valid records for {exam}: {len(self.cutoff_data[exam])}")
        
        load_time = time.time() - start_time
        safe_print(f"Essential data loaded in {load_time:.2f} seconds")
    
    def load_full_data(self, exam: str):
        """Lazy load full data for a specific exam when needed"""
        if self.data_loaded.get(exam) == "full":
            return  # Already loaded
        
        safe_print(f"Loading full data for {exam.upper()}...")
        start_time = time.time()
        
        # Load additional data files
        additional_files = {
            "jee": [
                "jee_10000_cutoffs.json",
                "jee_massive_cutoffs.json",
                "jee_main_10000_cutoffs.json",
                "jee_main_massive_cutoffs.json",
                "jee_cutoffs_extended.json",
                "jee_cutoffs_extended_v2.json",
                "diverse_colleges_jee.json",
                "gujarat_colleges_jee.json",
                "uttar_pradesh_colleges_jee.json"
            ],
            "neet": [
                "neet_10000_cutoffs.json",
                "neet_massive_cutoffs.json",
                "neet_cutoffs.json",
                "neet_cutoffs_extended.json"
            ],
            "ielts": [
                "ielts_10000_cutoffs.json",
                "ielts_massive_cutoffs.json",
                "ielts_cutoffs.json"
            ]
        }
        
        if exam in additional_files:
            all_data = list(self.cutoff_data.get(exam, []))  # Start with existing data
            
            for filename in additional_files[exam]:
                file_path = self.data_path / filename
                if file_path.exists():
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            raw_data = json.load(f)
                            all_data.extend(raw_data)
                            safe_print(f"Loaded {len(raw_data)} additional records from {filename}")
                    except Exception as e:
                        safe_print(f"Error loading {filename}: {e}")
            
            # Clean and store the combined data
            self.cutoff_data[exam] = self._clean_cutoff_data(all_data, exam)
            self.data_loaded[exam] = "full"
            
            load_time = time.time() - start_time
            safe_print(f"Full data loaded for {exam} in {load_time:.2f} seconds")
            safe_print(f"Total records for {exam}: {len(self.cutoff_data[exam])}")
    
    def _clean_cutoff_data(self, raw_data: List[Dict[str, Any]], exam: str) -> List[Dict[str, Any]]:
        """Clean and validate cutoff data with optimized processing"""
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
                
                # Add timestamp for tracking
                if "last_updated" not in record:
                    record["last_updated"] = datetime.now().isoformat()
                
                cleaned_data.append(record)
                
            except Exception as e:
                # Skip malformed records
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
        states: Optional[List[str]] = None,
        load_full_data: bool = False,
        limit: int = 300,
        per_college_limit: int = 1,
        ownership: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Predict colleges based on exam rank and category
        """
        try:
            # Load full data if requested or if essential data doesn't have enough results
            if load_full_data or exam not in self.cutoff_data:
                self.load_full_data(exam)
            
            if exam not in self.cutoff_data:
                return []
            
            # Normalize ownership filter
            own = (ownership or "").strip().lower()
            if own in ("any", ""):
                own = ""

            def ownership_ok(c: Dict[str, Any]) -> bool:
                if not own:
                    return True
                # Try common fields that may encode ownership
                raw = (
                    c.get("ownership")
                    or c.get("ownership_type")
                    or c.get("college_type")
                    or c.get("type")
                    or c.get("management")
                    or c.get("institute_type")
                    or ""
                )
                val = str(raw).strip().lower()
                if not val:
                    return False  # if user asked ownership, skip unknowns
                # Government synonyms
                gov_tokens = ["government", "govt", "public", "central", "state", "national"]
                # Private synonyms
                prv_tokens = ["private", "self", "deemed", "trust"]
                is_gov = any(t in val for t in gov_tokens)
                is_prv = any(t in val for t in prv_tokens) and not is_gov
                if own.startswith("gov") or own == "government" or own == "public":
                    return is_gov
                if own.startswith("priv"):
                    return is_prv
                # If an unrecognized ownership string is provided, do not filter out
                return True

            # Filter cutoffs based on strict criteria first
            def state_ok(c):
                if not states:
                    return True
                loc = c.get("location") or ""
                cutoff_state = loc.split(",")[-1].strip() if "," in loc else loc
                return cutoff_state in states if cutoff_state else False

            # Keep a copy without state filter for later broad fallback
            all_cutoffs_no_state = [c for c in self.cutoff_data[exam] if ownership_ok(c)]
            all_cutoffs = [c for c in self.cutoff_data[exam] if state_ok(c) and ownership_ok(c)]

            # If coverage looks thin, auto-load full data once to boost matches
            if not load_full_data and len(all_cutoffs) < 1000:
                try:
                    self.load_full_data(exam)
                    all_cutoffs_no_state = [c for c in self.cutoff_data[exam] if ownership_ok(c)]
                    all_cutoffs = [c for c in self.cutoff_data[exam] if state_ok(c) and ownership_ok(c)]
                except Exception:
                    pass

            strict_matches: List[Dict[str, Any]] = []
            for cutoff in all_cutoffs:
                if self._is_rank_eligible(cutoff, rank, category, gender, quota, tolerance_percent):
                    strict_matches.append(cutoff)

            # Sort by proximity to rank
            strict_matches.sort(key=lambda x: abs(x.get("closing_rank", 0) - rank))

            # Start building predictions from strict matches
            predictions: List[Dict[str, Any]] = []
            seen_keys = set()
            cap = max(1, min(limit, 10000))
            # Track how many entries we have per college to diversify results
            per_college_limit = max(1, int(per_college_limit))
            per_college_counts: Dict[str, int] = {}

            def add_cutoff(c):
                # Less aggressive deduplication - allow different branches and categories
                k = (c.get("college", "").lower(), c.get("branch", "").lower())
                if k in seen_keys:
                    return False
                college_key = c.get("college", "").strip().lower()
                if college_key:
                    count = per_college_counts.get(college_key, 0)
                    if count >= per_college_limit:
                        return False
                predictions.append(self._create_prediction(c, rank, exam))
                seen_keys.add(k)
                if college_key:
                    per_college_counts[college_key] = per_college_counts.get(college_key, 0) + 1
                return True

            for c in strict_matches:
                if len(predictions) >= cap:
                    break
                add_cutoff(c)

            # If not enough, relax constraints progressively. For NEET, use wider proximity windows
            if len(predictions) < cap:
                # Proximity windows (adaptive)
                near_window = 20000
                far_window = 80000
                very_far_window = 120000
                ex = exam.lower()
                # NEET needs wider windows; support ranks up to 200k+
                if ex == "neet":
                    near_window = 60000 if rank >= 100000 else 50000
                    far_window = 140000 if rank >= 100000 else 120000
                    very_far_window = 250000
                else:  # JEE and others
                    if rank >= 100000:
                        near_window = 50000
                        far_window = 120000
                        very_far_window = 200000

                # 1) Ignore category/quota, keep branch and state, sort by proximity
                relaxed = sorted(all_cutoffs, key=lambda x: abs(x.get("closing_rank", 0) - rank))
                for c in relaxed:
                    if len(predictions) >= cap:
                        break
                    # Only add if the user's rank is within a reasonable range of the closing rank
                    if abs(c.get("closing_rank", 0) - rank) < near_window:
                        add_cutoff(c)

            if len(predictions) < cap:
                # 2) Expand to far window within current state filter
                for c in relaxed:
                    if len(predictions) >= cap:
                        break
                    if abs(c.get("closing_rank", 0) - rank) < far_window:
                        add_cutoff(c)

            if len(predictions) < cap and states:
                # 3) If state was restricting, try without state filter using proximity
                relaxed_ns = sorted(all_cutoffs_no_state, key=lambda x: abs(x.get("closing_rank", 0) - rank))
                for c in relaxed_ns:
                    if len(predictions) >= cap:
                        break
                    if abs(c.get("closing_rank", 0) - rank) < near_window:
                        add_cutoff(c)
                if len(predictions) < cap:
                    for c in relaxed_ns:
                        if len(predictions) >= cap:
                            break
                        if abs(c.get("closing_rank", 0) - rank) < far_window:
                            add_cutoff(c)

            if len(predictions) < cap:
                # 4) Very broad final fill to ensure enough options
                # Prefer proximity order from all data
                relaxed_all = sorted(all_cutoffs_no_state, key=lambda x: abs(x.get("closing_rank", 0) - rank))
                for c in relaxed_all:
                    if len(predictions) >= cap:
                        break
                    if abs(c.get("closing_rank", 0) - rank) < very_far_window:
                        add_cutoff(c)
            
            return predictions
            
        except Exception as e:
            print(f"Error during prediction: {e}")
            return []
    
    def _is_rank_eligible(
        self,
        cutoff: Dict[str, Any],
        rank: int,
        category: str,
        gender: str,
        quota: str,
        tolerance_percent: float = 0.0,
    ) -> bool:
        """Check if a rank is eligible for a specific cutoff"""
        try:
            # Basic quota and gender matching
            cutoff_quota = cutoff.get("quota", "All India")
            if quota != "All India" and cutoff_quota != quota:
                return False
            
            # More flexible category matching - allow cross-category eligibility
            cutoff_category = cutoff.get("category", "General")
            
            # Category hierarchy: General is most competitive, ST is least competitive
            category_hierarchy = {"General": 1, "EWS": 2, "OBC": 3, "SC": 4, "ST": 5}
            user_level = category_hierarchy.get(category, 1)
            cutoff_level = category_hierarchy.get(cutoff_category, 1)
            
            # Users can apply to their own category or more competitive categories
            # For example: OBC students can apply to General seats if their rank is good enough
            # But General category students cannot apply to reserved seats
            if user_level > cutoff_level:
                # User is from reserved category trying to apply to more competitive category
                # This is allowed - reserved category students can compete in general category
                pass
            elif user_level < cutoff_level:
                # General category student trying to apply to reserved seats - not allowed
                return False
            # If user_level == cutoff_level, it's the same category - allowed
            
            # Rank eligibility check - handle both old and new data formats
            closing_rank = cutoff.get("closing_rank", 0)
            opening_rank = cutoff.get("opening_rank", 0)
            single_rank = cutoff.get("rank", 0)  # New format from massive files
            
            # Determine the cutoff rank to use
            cutoff_rank = 0
            if closing_rank and closing_rank > 0:
                cutoff_rank = closing_rank
            elif single_rank and single_rank > 0:
                cutoff_rank = single_rank  # Use single rank as cutoff
            elif opening_rank and opening_rank > 0:
                cutoff_rank = opening_rank
            
            if cutoff_rank <= 0:
                return False
            
            # Apply tolerance to make cutoff more lenient
            effective_cutoff_rank = cutoff_rank
            if tolerance_percent > 0:
                tolerance_factor = 1 + (tolerance_percent / 100)
                effective_cutoff_rank = int(cutoff_rank * tolerance_factor)
            
            # User can get admission if their rank is better than or equal to cutoff rank
            return rank <= effective_cutoff_rank
            
        except Exception:
            return False
    
    def _create_prediction(
        self, 
        cutoff: Dict[str, Any], 
        rank: int, 
        exam: str
    ) -> Dict[str, Any]:
        """Create a prediction result from cutoff data"""
        try:
            closing_rank = cutoff.get("closing_rank", 0)
            opening_rank = cutoff.get("opening_rank", 0)
            
            # Calculate confidence
            confidence_score = self._calculate_confidence(rank, closing_rank, opening_rank)
            confidence_level = self._get_confidence_level(confidence_score)
            
            return {
                "college": cutoff.get("college", "Unknown"),
                "branch": cutoff.get("branch", "Unknown"),
                "exam": exam,
                "opening_rank": opening_rank,
                "closing_rank": closing_rank,
                "your_rank": rank,
                "confidence_score": confidence_score,
                "confidence_level": confidence_level,
                "location": cutoff.get("location", "Unknown"),
                "category": cutoff.get("category", "General"),
                "quota": cutoff.get("quota", "All India"),
                "ownership": cutoff.get("ownership") or cutoff.get("ownership_type") or cutoff.get("college_type") or cutoff.get("type") or cutoff.get("management") or cutoff.get("institute_type"),
                "last_updated": cutoff.get("last_updated", datetime.now().isoformat())
            }
        except Exception as e:
            print(f"Error creating prediction: {e}")
            return {}
    
    def _calculate_confidence(self, rank: int, closing_rank: int, opening_rank: int) -> float:
        """Calculate confidence score based on rank position"""
        try:
            if closing_rank == opening_rank:
                return 1.0
            
            # Calculate position within the range
            range_size = closing_rank - opening_rank
            if range_size <= 0:
                return 0.5
            
            position = (closing_rank - rank) / range_size
            position = max(0.0, min(1.0, position))  # Clamp between 0 and 1
            
            # Higher confidence for ranks closer to opening rank
            return position
        except Exception:
            return 0.5
    
    def _get_confidence_level(self, confidence_score: float) -> str:
        """Convert confidence score to level"""
        if confidence_score >= 0.8:
            return "High"
        elif confidence_score >= 0.5:
            return "Medium"
        else:
            return "Low"
    
    def get_data_status(self) -> Dict[str, Any]:
        """Get current data loading status"""
        return {
            "data_loaded": self.data_loaded,
            "record_counts": {exam: len(data) for exam, data in self.cutoff_data.items()},
            "load_essential_only": self.load_essential_only
        }
    
    def preload_full_data(self, exam: str = None):
        """Preload full data for better performance"""
        if exam:
            self.load_full_data(exam)
        else:
            for exam_type in ["jee", "neet", "ielts"]:
                self.load_full_data(exam_type)
