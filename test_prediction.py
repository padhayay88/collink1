from utils.match_logic import CollegePredictor

predictor = CollegePredictor()

# Test different ranks and categories
test_cases = [
    {'rank': 1000, 'category': 'General'},
    {'rank': 1000, 'category': 'OBC'},
    {'rank': 1000, 'category': 'SC'},
    {'rank': 1000, 'category': 'ST'},
    {'rank': 50000, 'category': 'General'},
    {'rank': 50000, 'category': 'OBC'},
    {'rank': 150000, 'category': 'General'},
    {'rank': 150000, 'category': 'SC'},
    {'rank': 300000, 'category': 'General'},
    {'rank': 300000, 'category': 'ST'}
]

for test_case in test_cases:
    predictions = predictor.predict_colleges('jee', test_case['rank'], test_case['category'])
    print(f'\n=== RANK {test_case["rank"]:,} | CATEGORY: {test_case["category"]} ===')
    print(f'Found {len(predictions)} predictions')
    
    if predictions:
        print('Top 5 predictions:')
        for i, p in enumerate(predictions[:5]):
            print(f'{i+1}. {p["college"]} - Closing: {p["closing_rank"]:,} (Confidence: {p["confidence_level"]})')
    else:
        print('No predictions found for this rank/category')
