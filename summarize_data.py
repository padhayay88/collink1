#!/usr/bin/env python3
"""
Script to summarize college data files
"""
import os
import json
import pandas as pd
from pathlib import Path

def get_file_info(filepath):
    """Get information about a file"""
    try:
        size_mb = os.path.getsize(filepath) / (1024 * 1024)
        return {
            'filename': os.path.basename(filepath),
            'size_mb': round(size_mb, 2),
            'type': 'JSON' if filepath.endswith('.json') else 'CSV' if filepath.endswith('.csv') else 'Other'
        }
    except Exception as e:
        print(f"Error getting info for {filepath}: {e}")
        return None

def summarize_json(filepath):
    """Summarize a JSON file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        if isinstance(data, list):
            sample = data[0] if data else {}
            return {
                'items': len(data),
                'sample_keys': list(sample.keys()) if isinstance(sample, dict) else []
            }
        elif isinstance(data, dict):
            return {
                'items': len(data),
                'sample_keys': list(data.keys())[:5] if data else []
            }
        return {'items': 1, 'sample_keys': []}
    except Exception as e:
        return {'error': str(e)}

def summarize_csv(filepath):
    """Summarize a CSV file"""
    try:
        df = pd.read_csv(filepath, nrows=5)
        return {
            'rows': len(df) + 4,  # +4 because we only read 5 rows
            'columns': df.columns.tolist(),
            'sample': df.head(1).to_dict(orient='records')[0] if not df.empty else {}
        }
    except Exception as e:
        return {'error': str(e)}

def main():
    data_dir = Path('data')
    output = {
        'files': [],
        'summary': {}
    }
    
    # Scan data directory
    for root, _, files in os.walk(data_dir):
        for file in files:
            if file.endswith(('.json', '.csv')) and not file.startswith('.'):
                filepath = os.path.join(root, file)
                info = get_file_info(filepath)
                if info:
                    if file.endswith('.json'):
                        info.update(summarize_json(filepath))
                    elif file.endswith('.csv'):
                        info.update(summarize_csv(filepath))
                    output['files'].append(info)
    
    # Also check root directory for CSV files
    for file in os.listdir('.'):
        if file.endswith('.csv') and os.path.isfile(file):
            info = get_file_info(file)
            if info:
                info.update(summarize_csv(file))
                output['files'].append(info)
    
    # Generate summary
    total_files = len(output['files'])
    total_size_mb = sum(f['size_mb'] for f in output['files'])
    file_types = {}
    
    for file in output['files']:
        file_type = file['type']
        file_types[file_type] = file_types.get(file_type, 0) + 1
    
    output['summary'] = {
        'total_files': total_files,
        'total_size_mb': round(total_size_mb, 2),
        'file_types': file_types
    }
    
    # Save summary to file
    with open('data_summary.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2)
    
    # Print summary
    print("\nData Summary:")
    print(f"Total files: {total_files}")
    print(f"Total size: {total_size_mb:.2f} MB")
    print("\nFile types:")
    for ftype, count in file_types.items():
        print(f"- {ftype}: {count} files")
    
    print("\nSample file info:")
    for file in output['files'][:5]:  # Show first 5 files
        print(f"\n{file['filename']} ({file['type']}, {file['size_mb']} MB)")
        if 'items' in file:
            print(f"  Items: {file['items']}")
        if 'rows' in file:
            print(f"  Rows: {file['rows']}")
        if 'columns' in file:
            print(f"  Columns: {len(file['columns'])}")
        if 'sample_keys' in file and file['sample_keys']:
            print(f"  Sample keys: {', '.join(file['sample_keys'][:5])}...")
    
    print("\nFull summary saved to data_summary.json")

if __name__ == "__main__":
    main()
