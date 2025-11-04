"""
Test Go-UPC API with sample products
"""

import urllib.request
import urllib.error
import json
import csv
import random
import time

# Go-UPC API Key
GO_UPC_API_KEY = "c74e46d117cd569c11ae68c88bae8f00c11f66b9ca5f662dd397550a4ea5d7ce"

def get_random_upcs(count=10):
    """Get random UPCs from master list"""
    products = []
    
    with open('../palmers-barcodes-master-list-with-upc-check.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        
        all_rows = []
        for row in reader:
            if len(row) > 3:
                upc = row[1].strip()
                product_name = row[3].strip()
                size = row[4].strip() if len(row) > 4 else ""
                
                if upc and product_name and upc.isdigit() and len(upc) == 12:
                    all_rows.append({
                        'upc': upc,
                        'ean': '0' + upc,  # Convert to EAN-13
                        'expected_name': product_name,
                        'size': size
                    })
        
        products = random.sample(all_rows, min(count, len(all_rows)))
    
    return products

def test_go_upc_api(upc):
    """Test Go-UPC API with a single UPC"""
    url = f"https://go-upc.com/api/v1/code/{upc}"
    
    try:
        req = urllib.request.Request(url)
        req.add_header('Authorization', f'Bearer {GO_UPC_API_KEY}')
        
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            
            return {
                'success': True,
                'data': data
            }
    
    except urllib.error.HTTPError as e:
        return {
            'success': False,
            'error': f'HTTP {e.code}: {e.reason}'
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def main():
    """Run Go-UPC API tests"""
    print("=" * 80)
    print("GO-UPC API TEST")
    print("=" * 80)
    print()
    print(f"API Key: {GO_UPC_API_KEY[:20]}...")
    print(f"Limit: ~150 calls")
    print()
    
    # Get 10 random products
    print("Selecting 10 random products from master list...")
    products = get_random_upcs(10)
    print(f"Selected {len(products)} products")
    print()
    
    results = []
    
    for i, product in enumerate(products, 1):
        print(f"\n{'=' * 80}")
        print(f"PRODUCT {i}/10: {product['expected_name']}")
        print(f"UPC: {product['upc']} | EAN: {product['ean']}")
        print(f"{'=' * 80}")
        
        # Test with UPC
        print("\n  Testing with UPC...")
        result = test_go_upc_api(product['upc'])
        
        if result['success']:
            data = result['data']
            product_info = data.get('product', {})
            
            print(f"    Status: Success")
            print(f"    Product Name: {product_info.get('name', 'N/A')}")
            print(f"    Brand: {product_info.get('brand', 'N/A')}")
            print(f"    Category: {product_info.get('category', 'N/A')}")
            
            images = product_info.get('images', [])
            print(f"    Images: {len(images)} available")
            
            results.append({
                'upc': product['upc'],
                'ean': product['ean'],
                'expected_name': product['expected_name'],
                'api_name': product_info.get('name', ''),
                'brand': product_info.get('brand', ''),
                'category': product_info.get('category', ''),
                'images': images,
                'success': True
            })
        else:
            print(f"    Status: Failed")
            print(f"    Error: {result['error']}")
            
            results.append({
                'upc': product['upc'],
                'ean': product['ean'],
                'expected_name': product['expected_name'],
                'error': result['error'],
                'success': False
            })
        
        # Small delay to avoid rate limiting
        if i < len(products):
            time.sleep(1)
    
    # Save results
    output_file = '../json-data/go_upc_test_results.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n{'=' * 80}")
    print("TEST SUMMARY")
    print(f"{'=' * 80}")
    
    successful = sum(1 for r in results if r['success'])
    failed = len(results) - successful
    
    print(f"  Total Tests: {len(results)}")
    print(f"  Successful: {successful} ({successful/len(results)*100:.1f}%)")
    print(f"  Failed: {failed}")
    print(f"\n  Results saved to: {output_file}")
    print()

if __name__ == "__main__":
    main()

