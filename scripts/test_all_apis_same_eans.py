import urllib.request
import urllib.error
import json
import time

# API Keys
BARCODE_LOOKUP_KEY = "YOUR_BARCODE_LOOKUP_API_KEY_HERE"  # Replace with your actual key
# Note: Go-UPC trial key not yet received

# The exact 10 EAN/UPC codes from our test
test_codes = [
    {"upc": "711381332580", "ean": "0711381332580", "name": "Stonewall Kitchen Waffle Cookie"},
    {"upc": "849455000032", "ean": "0849455000032", "name": "Tumaro's Wraps"},
    {"upc": "858183005059", "ean": "0858183005059", "name": "Lillie's Q BBQ Sauce"},
    {"upc": "820581153908", "ean": "0820581153908", "name": "Bella Maria Cocktail Mix"},
    {"upc": "819046000420", "ean": "0819046000420", "name": "InkaCrops Giant Corn"},
    {"upc": "818617022571", "ean": "0818617022571", "name": "SUJA Immunity Shot"},
    {"upc": "186011000182", "ean": "0186011000182", "name": "Stella & Chewy's Dog Food"},
    {"upc": "312547171670", "ean": "0312547171670", "name": "Benadryl Itch Relief"},
    {"upc": "852466006016", "ean": "0852466006016", "name": "Simply Gum Mint"},
    {"upc": "824150401162", "ean": "0824150401162", "name": "POM Wonderful Juice"},
]

def test_barcode_lookup(upc):
    """Test Barcode Lookup API (we already tested this)"""
    try:
        url = f"https://api.barcodelookup.com/v3/products?barcode={upc}&key={BARCODE_LOOKUP_KEY}"
        req = urllib.request.Request(url, headers={'Accept': 'application/json'})
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode())
            if data.get('products'):
                product = data['products'][0]
                return {
                    'found': True,
                    'title': product.get('title', 'N/A'),
                    'images': len(product.get('images', [])),
                    'has_image': len(product.get('images', [])) > 0
                }
            return {'found': False, 'title': 'Not Found', 'images': 0, 'has_image': False}
    except Exception as e:
        return {'found': False, 'title': f'Error: {str(e)}', 'images': 0, 'has_image': False}

def test_upcitemdb(upc):
    """Test UPCitemdb API (Free trial - very limited)"""
    try:
        # Using the free trial endpoint
        url = f"https://api.upcitemdb.com/prod/trial/lookup?upc={upc}"
        req = urllib.request.Request(url, headers={'Accept': 'application/json'})
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode())
            if data.get('items') and len(data['items']) > 0:
                item = data['items'][0]
                return {
                    'found': True,
                    'title': item.get('title', 'N/A'),
                    'images': len(item.get('images', [])),
                    'has_image': len(item.get('images', [])) > 0
                }
            return {'found': False, 'title': 'Not Found', 'images': 0, 'has_image': False}
    except urllib.error.HTTPError as e:
        if e.code == 429:
            return {'found': False, 'title': 'Rate Limited', 'images': 0, 'has_image': False}
        return {'found': False, 'title': f'HTTP Error {e.code}', 'images': 0, 'has_image': False}
    except Exception as e:
        return {'found': False, 'title': f'Error: {str(e)}', 'images': 0, 'has_image': False}

def test_go_upc(upc):
    """Test Go-UPC API (Trial key pending)"""
    return {'found': False, 'title': 'Trial API Key Pending', 'images': 0, 'has_image': False}

print("=" * 100)
print("TESTING ALL 3 APIs WITH THE SAME 10 EAN/UPC CODES")
print("=" * 100)
print()
print("APIs to test:")
print("  1. Barcode Lookup API (Already tested - $249/month)")
print("  2. UPCitemdb (Free trial - very limited)")
print("  3. Go-UPC API (Trial key pending)")
print()
print("=" * 100)
print()

results = []

for i, code in enumerate(test_codes, 1):
    upc = code['upc']
    ean = code['ean']
    name = code['name']
    
    print(f"\n{'='*100}")
    print(f"TEST {i}/10: {name}")
    print(f"UPC: {upc} | EAN-13: {ean}")
    print('='*100)
    
    result = {
        'number': i,
        'name': name,
        'upc': upc,
        'ean': ean,
        'barcode_lookup': {},
        'upcitemdb': {},
        'go_upc': {}
    }
    
    # Test Barcode Lookup API
    print("\n[1] Barcode Lookup API...")
    bl_result = test_barcode_lookup(upc)
    result['barcode_lookup'] = bl_result
    if bl_result['found']:
        print(f"    [OK] Found: {bl_result['title'][:60]}...")
        print(f"    Images: {bl_result['images']}")
    else:
        print(f"    [X] {bl_result['title']}")
    
    time.sleep(1)  # Rate limiting
    
    # Test UPCitemdb
    print("\n[2] UPCitemdb (Free Trial)...")
    upc_result = test_upcitemdb(upc)
    result['upcitemdb'] = upc_result
    if upc_result['found']:
        print(f"    [OK] Found: {upc_result['title'][:60]}...")
        print(f"    Images: {upc_result['images']}")
    else:
        print(f"    [X] {upc_result['title']}")
    
    time.sleep(2)  # More conservative rate limiting for free tier
    
    # Test Go-UPC
    print("\n[3] Go-UPC API...")
    go_result = test_go_upc(upc)
    result['go_upc'] = go_result
    print(f"    [!] {go_result['title']}")
    
    results.append(result)
    
    if i < len(test_codes):
        print("\n[...] Waiting before next test...")
        time.sleep(1)

# Save results
with open('api_comparison_results.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2)

# Print summary
print("\n" + "="*100)
print("COMPARISON SUMMARY")
print("="*100)
print()

bl_found = sum(1 for r in results if r['barcode_lookup']['found'])
upc_found = sum(1 for r in results if r['upcitemdb']['found'])
go_found = sum(1 for r in results if r['go_upc']['found'])

bl_images = sum(1 for r in results if r['barcode_lookup']['has_image'])
upc_images = sum(1 for r in results if r['upcitemdb']['has_image'])
go_images = sum(1 for r in results if r['go_upc']['has_image'])

print(f"{'API Provider':<25} {'Found':<15} {'With Images':<15} {'Success Rate'}")
print("-" * 100)
print(f"{'Barcode Lookup API':<25} {bl_found}/10{'':<10} {bl_images}/10{'':<10} {bl_found*10}%")
print(f"{'UPCitemdb (Free Trial)':<25} {upc_found}/10{'':<10} {upc_images}/10{'':<10} {upc_found*10}%")
print(f"{'Go-UPC API':<25} {go_found}/10{'':<10} {go_images}/10{'':<10} {go_found*10}%")
print()
print("="*100)
print("Results saved to api_comparison_results.json")
print("="*100)

