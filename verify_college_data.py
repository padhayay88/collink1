#!/usr/bin/env python3
"""
Comprehensive verification of college data files
"""
import json
import os
import pandas as pd
from pathlib import Path
from collections import defaultdict

def analyze_file(filepath, exam_type):
    """Analyze a single college data file"""
    try:
        if not os.path.exists(filepath):
            return {
                'status': 'error',
                'message': f'File not found: {filepath}'
            }
            
        print(f"\nAnalyzing {os.path.basename(filepath)}...")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        if not isinstance(data, list):
            data = [data]
            
        # Initialize stats
        stats = {
            'total_colleges': len(data),
            'rank_fields': defaultdict(int),
            'ranks': [],
            'states': set(),
            'categories': set(),
            'has_duplicates': False,
            'duplicate_colleges': []
        }
        
        # Track seen colleges for duplicate detection
        seen_colleges = set()
        
        # Analyze each college
        for college in data:
            if not isinstance(college, dict):
                continue
                
            # Track rank fields
            rank_found = False
            for field in ['rank', 'Rank', 'closing_rank', 'cutoff_rank']:
                if field in college and college[field] is not None:
                    stats['rank_fields'][field] += 1
                    try:
                        rank = int(college[field])
                        stats['ranks'].append(rank)
                        rank_found = True
                    except (ValueError, TypeError):
                        pass
            
            # Track states
            if 'state' in college:
                stats['states'].add(college['state'])
            
            # Track categories
            if 'category' in college:
                stats['categories'].add(college['category'])
            
            # Check for duplicates
            college_key = (
                college.get('name', '').lower().strip(),
                college.get('state', '').lower().strip()
            )
            if college_key in seen_colleges:
                stats['has_duplicates'] = True
                stats['duplicate_colleges'].append(college_key[0])
            seen_colleges.add(college_key)
        
        # Calculate rank statistics
        if stats['ranks']:
            stats['min_rank'] = min(stats['ranks'])
            stats['max_rank'] = max(stats['ranks'])
            stats['rank_range'] = stats['max_rank'] - stats['min_rank'] + 1
            stats['rank_coverage'] = len(stats['ranks']) / stats['total_colleges'] * 100
        
        # Convert sets to lists for JSON serialization
        stats['states'] = list(stats['states'])
        stats['categories'] = list(stats['categories'])
        
        return {
            'status': 'success',
            'filename': os.path.basename(filepath),
            'exam_type': exam_type,
            'stats': stats
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'filename': os.path.basename(filepath),
            'error': str(e)
        }

def generate_report(results):
    """Generate a comprehensive report from analysis results"""
    report = {
        'summary': {
            'total_files_analyzed': 0,
            'total_colleges': 0,
            'exam_types': set(),
            'rank_coverage': {},
            'highest_rank': {},
            'lowest_rank': {}
        },
        'details': {}
    }
    
    for result in results:
        if result['status'] != 'success':
            continue
            
        filename = result['filename']
        exam_type = result['exam_type']
        stats = result['stats']
        
        # Update summary
        report['summary']['total_files_analyzed'] += 1
        report['summary']['total_colleges'] += stats['total_colleges']
        report['summary']['exam_types'].add(exam_type)
        
        # Update rank coverage
        if 'rank_range' in stats:
            report['summary']['rank_coverage'][filename] = {
                'min_rank': stats['min_rank'],
                'max_rank': stats['max_rank'],
                'rank_range': stats['rank_range'],
                'coverage_percent': stats.get('rank_coverage', 0)
            }
        
        # Store detailed stats
        report['details'][filename] = {
            'exam_type': exam_type,
            'total_colleges': stats['total_colleges'],
            'states_count': len(stats['states']),
            'categories_count': len(stats['categories']),
            'has_duplicates': stats['has_duplicates'],
            'duplicate_count': len(stats['duplicate_colleges'])
        }
        
        # Add rank info if available
        if 'min_rank' in stats and 'max_rank' in stats:
            report['details'][filename].update({
                'min_rank': stats['min_rank'],
                'max_rank': stats['max_rank']
            })
    
    # Convert sets to lists for JSON serialization
    report['summary']['exam_types'] = list(report['summary']['exam_types'])
    
    return report

def main():
    # Files to analyze
    files_to_analyze = [
        ('NEET', 'data/neet_massive_colleges.json'),
        ('NEET', 'data/neet_comprehensive_colleges.json'),
        ('NEET', 'data/neet_10000_colleges.json'),
        ('NEET', 'data/neet_1000_colleges.json'),
        ('JEE', 'data/jee_massive_colleges.json'),
        ('JEE', 'data/jee_comprehensive_colleges.json'),
        ('JEE', 'data/jee_10000_colleges.json'),
        ('JEE', 'data/jee_1000_colleges.json')
    ]
    
    print("Starting comprehensive analysis of college data files...")
    
    # Analyze each file
    results = []
    for exam_type, filepath in files_to_analyze:
        result = analyze_file(filepath, exam_type)
        results.append(result)
    
    # Generate and save report
    report = generate_report(results)
    with open('college_data_analysis_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)
    
    # Print summary
    print("\n=== Analysis Complete ===")
    print(f"\nAnalyzed {report['summary']['total_files_analyzed']} files")
    print(f"Total colleges across all files: {report['summary']['total_colleges']:,}")
    print(f"Exam types found: {', '.join(report['summary']['exam_types'])}")
    
    # Print rank information
    print("\nRank Ranges:")
    for filename, ranks in report['summary']['rank_coverage'].items():
        print(f"\n{filename}:")
        print(f"  Rank Range: {ranks['min_rank']:,} - {ranks['max_rank']:,}")
        print(f"  Coverage: {ranks['coverage_percent']:.1f}% of colleges have rank data")
    
    print("\nDetailed report saved to: college_data_analysis_report.json")

if __name__ == "__main__":
    main()
