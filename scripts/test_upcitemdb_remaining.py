import urllib.request
import urllib.error
import json
import time

# The 4 UPC codes that hit rate limit on UPCitemdb (items 7-10)
remaining_upcs = [
    "186011000182",   # Stella & Chewy's Dog Food
    "312547171670",   # Benadryl Itch Relief
    "852466006016",   # Simply Gum Mint
    "824150401162",   # POM Wonderful Juice
]

product_names = [
    "Stella & Chewy's Dog Food",
    "Benadryl Itch Relief",
    "Simply Gum Mint",
    "POM Wonderful Juice"
]

print("=" * 80)
print("UPCITEMDB - RETEST OF ITEMS 7-10")
print("=" * 80)
print()
print("Retesting the 4 UPC codes that hit rate limit on UPCitemdb:")
print()

for i, (upc, name) in enumerate(zip(remaining_upcs, product_names), 7):
    print(f"{i}. UPC {upc} - {name}")

print()
print("=" * 80)
print()
print("NOTE: Using free trial endpoint (very limited)")
print("If this hits rate limit again, you would need to upgrade to a paid plan")
print()

results = []

for i, (upc, name) in enumerate(zip(remaining_upcs, product_names), 7):
    print(f"\nTesting {i}/10: {name}")
    print(f"UPC: {upc}")
    
    try:
        # Using the free trial endpoint
        url = f"https://api.upcitemdb.com/prod/trial/lookup?upc={upc}"
        req = urllib.request.Request(url, headers={'Accept': 'application/json'})
        
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode())
            
            if data.get('items') and len(data['items']) > 0:
                item = data['items'][0]
                result = {
                    'found': True,
                    'upc': upc,
                    'name': name,
                    'title': item.get('title', 'N/A'),
                    'brand': item.get('brand', 'N/A'),
                    'images': item.get('images', []),
                    'image_count': len(item.get('images', []))
                }
                print(f"  [OK] Found: {result['title'][:60]}...")
                print(f"  Brand: {result['brand']}")
                print(f"  Images: {result['image_count']}")
            else:
                result = {
                    'found': False,
                    'upc': upc,
                    'name': name,
                    'title': 'Not Found',
                    'brand': 'N/A',
                    'images': [],
                    'image_count': 0
                }
                print(f"  [X] Not found in database")
            
            results.append(result)
            
    except urllib.error.HTTPError as e:
        if e.code == 429:
            result = {
                'found': False,
                'upc': upc,
                'name': name,
                'title': 'Rate Limited',
                'brand': 'N/A',
                'images': [],
                'image_count': 0,
                'error': 'Rate Limited'
            }
            print(f"  [X] Rate Limited (HTTP 429)")
        else:
            result = {
                'found': False,
                'upc': upc,
                'name': name,
                'title': f'HTTP Error {e.code}',
                'brand': 'N/A',
                'images': [],
                'image_count': 0,
                'error': f'HTTP {e.code}'
            }
            print(f"  [X] HTTP Error {e.code}")
        results.append(result)
        
    except Exception as e:
        result = {
            'found': False,
            'upc': upc,
            'name': name,
            'title': f'Error: {str(e)}',
            'brand': 'N/A',
            'images': [],
            'image_count': 0,
            'error': str(e)
        }
        results.append(result)
        print(f"  [X] Error: {e}")
    
    # Be conservative with rate limiting - wait 3 seconds between requests
    if i < 10:
        print("  [...] Waiting 3 seconds before next request...")
        time.sleep(3)

# Save results
with open('upcitemdb_retest_results.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2)

print()
print("=" * 80)
print("RETEST RESULTS SUMMARY")
print("=" * 80)
print()

found_count = sum(1 for r in results if r['found'])
rate_limited = sum(1 for r in results if 'error' in r and r['error'] == 'Rate Limited')
not_found = sum(1 for r in results if not r['found'] and not r.get('error'))

print(f"Found: {found_count}/4")
print(f"Rate Limited: {rate_limited}/4")
print(f"Not Found: {not_found}/4")
print()

if found_count > 0:
    print("Successfully found products:")
    for r in results:
        if r['found']:
            print(f"  - {r['name']}: {r['title'][:60]}... ({r['image_count']} images)")
    print()

if rate_limited > 0:
    print(f"[!] Hit rate limit again after {found_count} requests")
    print("    The free trial tier is too restrictive for testing")
    print("    A paid plan ($99/month Developer tier) would be needed")
    print()

print("Results saved to upcitemdb_retest_results.json")
print("=" * 80)

