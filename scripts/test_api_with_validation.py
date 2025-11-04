"""
API Testing with Built-in Validation
Tests APIs and automatically validates results against Palmer's master list
"""

import urllib.request
import urllib.error
import json
import csv
import random
from validate_api_results import validate_single_product, generate_validation_report

# API Configuration
BARCODE_LOOKUP_API_KEY = "YOUR_BARCODE_LOOKUP_API_KEY_HERE"
APIFY_API_TOKEN = "YOUR_APIFY_API_TOKEN_HERE"

def get_random_upcs(count=10):
    """Get random UPCs from master list with product names"""
    products = []
    
    with open('../palmers-barcodes-master-list-with-upc-check.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        
        all_rows = []
        for row in reader:
            if len(row) > 3:
                upc = row[1].strip()
                product_name = row[3].strip()
                
                if upc and product_name and upc.isdigit() and len(upc) == 12:
                    all_rows.append({
                        'upc': upc,
                        'expected_name': product_name
                    })
        
        products = random.sample(all_rows, min(count, len(all_rows)))
    
    return products

def test_barcode_lookup_with_validation(upc, expected_name):
    """Test Barcode Lookup API and validate result"""
    url = f"https://api.barcodelookup.com/v3/products?barcode={upc}&key={BARCODE_LOOKUP_API_KEY}"
    
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            
            if data.get('products'):
                product = data['products'][0]
                api_name = product.get('title', '')
                
                # Validate the result
                validation = validate_single_product(upc, api_name, "Barcode Lookup API")
                
                return {
                    'success': True,
                    'api_product': api_name,
                    'expected_product': expected_name,
                    'validation': validation,
                    'brand': product.get('brand', ''),
                    'category': product.get('category', '')
                }
            else:
                return {
                    'success': False,
                    'error': 'No products found'
                }
    
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def test_upcitemdb_with_validation(upc, expected_name):
    """Test UPCitemdb API and validate result"""
    url = f"https://api.upcitemdb.com/prod/trial/lookup?upc={upc}"
    
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            
            if data.get('items'):
                item = data['items'][0]
                api_name = item.get('title', '')
                
                # Validate the result
                validation = validate_single_product(upc, api_name, "UPCitemdb")
                
                return {
                    'success': True,
                    'api_product': api_name,
                    'expected_product': expected_name,
                    'validation': validation,
                    'brand': item.get('brand', ''),
                    'images': len(item.get('images', []))
                }
            else:
                return {
                    'success': False,
                    'error': 'No items found'
                }
    
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def main():
    """Run API tests with validation"""
    print("=" * 80)
    print("API TESTING WITH AUTOMATIC VALIDATION")
    print("=" * 80)
    print()
    
    # Get random products
    print("Selecting 10 random products from master list...")
    products = get_random_upcs(10)
    print(f"Selected {len(products)} products")
    print()
    
    all_validations = []
    
    for i, product in enumerate(products, 1):
        print(f"\n{'=' * 80}")
        print(f"PRODUCT {i}/10: {product['expected_name']}")
        print(f"UPC: {product['upc']}")
        print(f"{'=' * 80}")
        
        # Test Barcode Lookup API
        print("\n  Testing Barcode Lookup API...")
        result = test_barcode_lookup_with_validation(product['upc'], product['expected_name'])
        
        if result['success']:
            validation = result['validation']
            status_symbol = {
                'MATCH': '✅',
                'PARTIAL_MATCH': '⚠️',
                'NO_MATCH': '❌',
                'CRITICAL_MISMATCH': '🚨'
            }.get(validation['status'], '?')
            
            print(f"    API Response: {result['api_product']}")
            print(f"    Validation: {status_symbol} {validation['status']}")
            print(f"    Similarity: {validation['similarity_score']:.1%}")
            print(f"    {validation['message']}")
            
            all_validations.append(validation)
        else:
            print(f"    ERROR: {result['error']}")
        
        print()
    
    # Generate summary report
    if all_validations:
        print("\n" + "=" * 80)
        print("VALIDATION SUMMARY")
        print("=" * 80)
        
        matches = sum(1 for v in all_validations if v['status'] == 'MATCH')
        partial = sum(1 for v in all_validations if v['status'] == 'PARTIAL_MATCH')
        no_match = sum(1 for v in all_validations if v['status'] == 'NO_MATCH')
        critical = sum(1 for v in all_validations if v['status'] == 'CRITICAL_MISMATCH')
        
        print(f"  ✅ Perfect Matches: {matches}/{len(all_validations)}")
        print(f"  ⚠️  Partial Matches: {partial}/{len(all_validations)}")
        print(f"  ❌ No Match: {no_match}/{len(all_validations)}")
        print(f"  🚨 Critical Mismatches: {critical}/{len(all_validations)}")
        
        accuracy = (matches / len(all_validations)) * 100 if all_validations else 0
        print(f"\n  Overall Accuracy: {accuracy:.1f}%")
        
        if critical > 0:
            print("\n  ⚠️  WARNING: Critical mismatches detected!")
            print("     These products are in completely wrong categories.")
            print("     Review these results carefully before using this API.")

if __name__ == "__main__":
    main()

