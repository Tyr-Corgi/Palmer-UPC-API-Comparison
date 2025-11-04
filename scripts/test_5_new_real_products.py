"""
Test 5 NEW UPCs (not previously tested) with all 4 APIs
UPCs selected: 727915126457, 850042382189, 810291007752, 819898010110, 606274400456
"""
import urllib.request
import urllib.error
import json
import time

# ====================
# API KEYS - REPLACE WITH YOUR KEYS
# ====================
BARCODE_LOOKUP_API_KEY = "YOUR_BARCODE_LOOKUP_KEY_HERE"
APIFY_API_TOKEN = "YOUR_APIFY_TOKEN_HERE"
GO_UPC_API_KEY = "YOUR_GO_UPC_KEY_HERE"

# The 5 new UPCs to test
test_upcs = [
    "727915126457",
    "850042382189",
    "810291007752",
    "819898010110",
    "606274400456"
]

# Convert to EAN-13 (add leading 0)
test_eans = ["0" + upc for upc in test_upcs]

def test_barcode_lookup(upc):
    """Test Barcode Lookup API"""
    try:
        url = f"https://api.barcodelookup.com/v3/products?barcode={upc}&key={BARCODE_LOOKUP_API_KEY}"
        headers = {'Accept': 'application/json', 'User-Agent': 'PalmersTest/1.0'}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode())
            if data.get('products') and len(data['products']) > 0:
                product = data['products'][0]
                return {
                    'found': True,
                    'title': product.get('title', 'N/A'),
                    'brand': product.get('brand', 'N/A'),
                    'category': product.get('category', 'N/A'),
                    'manufacturer': product.get('manufacturer', 'N/A'),
                    'description': product.get('description', 'N/A'),
                    'images': product.get('images', []),
                    'barcode_formats': product.get('barcode_formats', 'N/A'),
                    'size': product.get('size', 'N/A'),
                    'weight': product.get('weight', 'N/A')
                }
            return {'found': False}
    except Exception as e:
        return {'found': False, 'error': str(e)}

def test_upcitemdb(upc):
    """Test UPCitemdb API"""
    try:
        url = f"https://api.upcitemdb.com/prod/trial/lookup?upc={upc}"
        req = urllib.request.Request(url, headers={'Accept': 'application/json'})
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode())
            if data.get('items') and len(data['items']) > 0:
                item = data['items'][0]
                return {
                    'found': True,
                    'title': item.get('title', 'N/A'),
                    'brand': item.get('brand', 'N/A'),
                    'images': item.get('images', []),
                    'image_count': len(item.get('images', []))
                }
            return {'found': False}
    except Exception as e:
        return {'found': False, 'error': str(e)}

def test_apify(ean):
    """Test Apify EAN/GTIN Image Extractor"""
    try:
        actor_id = "s-r~ean-product-image-search---extract-images-from-any-ean-gtin"
        url = f"https://api.apify.com/v2/acts/{actor_id}/runs?token={APIFY_API_TOKEN}"
        
        payload = {
            "eans": [ean],
            "maxImages": 1
        }
        
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode('utf-8'),
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            method='POST'
        )
        
        with urllib.request.urlopen(req, timeout=30) as response:
            run_data = json.loads(response.read().decode())
            run_id = run_data.get('data', {}).get('id')
            
            if not run_id:
                return {'found': False, 'error': 'No run ID returned'}
            
            print(f"  Apify run started: {run_id}")
            print(f"  Waiting 15 seconds for Apify to process...")
            time.sleep(15)
            
            # Get dataset items
            dataset_url = f"https://api.apify.com/v2/datasets/{run_data.get('data', {}).get('defaultDatasetId')}/items?token={APIFY_API_TOKEN}"
            dataset_req = urllib.request.Request(dataset_url, headers={'Accept': 'application/json'})
            
            try:
                with urllib.request.urlopen(dataset_req, timeout=15) as dataset_response:
                    dataset_data = json.loads(dataset_response.read().decode())
                    if dataset_data and len(dataset_data) > 0:
                        item = dataset_data[0]
                        return {
                            'found': True,
                            'title': item.get('title', 'N/A'),
                            'country_found': item.get('country_found', 'N/A'),
                            'image_url': item.get('image_url', 'N/A'),
                            'width': item.get('width', 'N/A'),
                            'height': item.get('height', 'N/A'),
                            'size_bytes': item.get('size_bytes', 'N/A'),
                            'scraped_at': item.get('scraped_at', 'N/A')
                        }
            except Exception as e:
                return {'found': False, 'error': f'Dataset fetch failed: {str(e)}'}
            
            return {'found': False, 'error': 'No data returned'}
    except Exception as e:
        return {'found': False, 'error': str(e)}

def test_go_upc(upc):
    """Test Go-UPC API"""
    try:
        url = f"https://go-upc.com/api/v1/code/{upc}?key={GO_UPC_API_KEY}"
        headers = {'Accept': 'application/json'}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode())
            if data.get('product'):
                product = data['product']
                return {
                    'found': True,
                    'name': product.get('name', 'N/A'),
                    'description': product.get('description', 'N/A'),
                    'brand': product.get('brand', 'N/A'),
                    'category': product.get('category', 'N/A'),
                    'image_url': product.get('imageUrl', 'N/A')
                }
            return {'found': False}
    except Exception as e:
        return {'found': False, 'error': str(e)}

# Test all APIs
results = []

print("=" * 80)
print("TESTING 5 NEW UPCs WITH ALL 4 APIs")
print("=" * 80)
print("\nIMPORTANT: Make sure you've added your API keys at the top of this script!")
print("=" * 80)

for i, (upc, ean) in enumerate(zip(test_upcs, test_eans), 1):
    print(f"\n{'='*80}")
    print(f"PRODUCT {i+15}/20: UPC {upc} (EAN {ean})")
    print('='*80)
    
    item_result = {
        'number': i + 15,  # Continue from 15
        'upc': upc,
        'ean': ean
    }
    
    # Test Barcode Lookup
    print("\n[1/4] Testing Barcode Lookup API...")
    barcode_result = test_barcode_lookup(upc)
    item_result['barcode_lookup'] = barcode_result
    if barcode_result.get('found'):
        print(f"  [OK] Found: {barcode_result.get('title', 'N/A')[:60]}...")
    else:
        print(f"  [X] Not found: {barcode_result.get('error', 'No match')}")
    time.sleep(1)
    
    # Test UPCitemdb
    print("\n[2/4] Testing UPCitemdb...")
    upcitemdb_result = test_upcitemdb(upc)
    item_result['upcitemdb'] = upcitemdb_result
    if upcitemdb_result.get('found'):
        print(f"  [OK] Found: {upcitemdb_result.get('title', 'N/A')[:60]}...")
        print(f"  Images: {upcitemdb_result.get('image_count', 0)}")
    else:
        print(f"  [X] Not found")
    time.sleep(2)
    
    # Test Apify
    print("\n[3/4] Testing Apify EAN/GTIN...")
    apify_result = test_apify(ean)
    item_result['apify'] = apify_result
    if apify_result.get('found'):
        print(f"  [OK] Found: {apify_result.get('title', 'N/A')[:60]}...")
    else:
        print(f"  [X] Not found: {apify_result.get('error', 'Unknown error')}")
    time.sleep(2)
    
    # Test Go-UPC
    print("\n[4/4] Testing Go-UPC...")
    go_upc_result = test_go_upc(upc)
    item_result['go_upc'] = go_upc_result
    if go_upc_result.get('found'):
        print(f"  [OK] Found: {go_upc_result.get('name', 'N/A')[:60]}...")
    else:
        print(f"  [X] Not found: {go_upc_result.get('error', 'No match')}")
    
    results.append(item_result)
    
    if i < len(test_upcs):
        print("\n[...] Waiting 3 seconds before next product...")
        time.sleep(3)

# Save results
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
json_file = os.path.join(project_root, 'json-data', 'new_5_products_results.json')

with open(json_file, 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2)

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
barcode_found = sum(1 for r in results if r['barcode_lookup'].get('found'))
upcitemdb_found = sum(1 for r in results if r['upcitemdb'].get('found'))
apify_found = sum(1 for r in results if r['apify'].get('found'))
go_upc_found = sum(1 for r in results if r['go_upc'].get('found'))

print(f"Barcode Lookup: {barcode_found}/5 found ({barcode_found*20}%)")
print(f"UPCitemdb: {upcitemdb_found}/5 found ({upcitemdb_found*20}%)")
print(f"Apify: {apify_found}/5 found ({apify_found*20}%)")
print(f"Go-UPC: {go_upc_found}/5 found ({go_upc_found*20}%)")
print("\nResults saved to json-data/new_5_products_results.json")
print("\nNext step: Run generate_html_for_new_5.py to add these to the HTML file")

