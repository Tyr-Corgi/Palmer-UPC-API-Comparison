import urllib.request
import json
import time

API_KEY = "YOUR_BARCODE_LOOKUP_API_KEY_HERE"  # Replace with your actual key

# The 5 random EAN codes (we'll use UPC format for the API)
test_items = [
    {"upc": "711381332580", "ean": "0711381332580", "size": "1.1 OZ"},
    {"upc": "849455000032", "ean": "0849455000032", "size": "11.2 OZ"},
    {"upc": "858183005059", "ean": "0858183005059", "size": "16 OZ"},
    {"upc": "820581153908", "ean": "0820581153908", "size": "3.5 OZ"},
    {"upc": "819046000420", "ean": "0819046000420", "size": "4.0 Ounce"},
]

print("=" * 80)
print("Testing 5 Random EAN Codes with Barcode Lookup API")
print("=" * 80)
print()

results = []

for i, item in enumerate(test_items, 1):
    upc = item['upc']
    ean = item['ean']
    
    print(f"Testing {i}/5: EAN {ean} (UPC {upc})")
    
    try:
        url = f"https://api.barcodelookup.com/v3/products?barcode={upc}&key={API_KEY}"
        req = urllib.request.Request(url, headers={'Accept': 'application/json'})
        
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode())
            
            if data.get('products') and len(data['products']) > 0:
                product = data['products'][0]
                result = {
                    'found': True,
                    'upc': upc,
                    'ean': ean,
                    'size': item['size'],
                    'title': product.get('title', 'N/A'),
                    'brand': product.get('brand', 'N/A'),
                    'category': product.get('category', 'N/A'),
                    'manufacturer': product.get('manufacturer', 'N/A'),
                    'description': product.get('description', 'N/A'),
                    'images': product.get('images', []),
                    'barcode_formats': product.get('barcode_formats', 'N/A'),
                    'weight': product.get('weight', 'N/A'),
                    'msrp': product.get('msrp', 'N/A')
                }
                print(f"  [OK] Found: {result['title']}")
            else:
                result = {
                    'found': False,
                    'upc': upc,
                    'ean': ean,
                    'size': item['size'],
                    'title': 'Not Found',
                    'brand': 'N/A',
                    'category': 'N/A',
                    'manufacturer': 'N/A',
                    'description': 'Product not found in database',
                    'images': [],
                    'barcode_formats': 'N/A',
                    'weight': 'N/A',
                    'msrp': 'N/A'
                }
                print(f"  [X] Not found in database")
            
            results.append(result)
            
    except Exception as e:
        result = {
            'found': False,
            'upc': upc,
            'ean': ean,
            'size': item['size'],
            'title': 'Error',
            'brand': 'N/A',
            'category': 'N/A',
            'manufacturer': 'N/A',
            'description': f'Error: {str(e)}',
            'images': [],
            'barcode_formats': 'N/A',
            'weight': 'N/A',
            'msrp': 'N/A'
        }
        results.append(result)
        print(f"  [X] Error: {e}")
    
    if i < len(test_items):
        time.sleep(1)
    print()

# Save results to JSON
with open('ean_test_results.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2)

print("=" * 80)
print(f"Results saved to ean_test_results.json")
print(f"Found: {sum(1 for r in results if r['found'])}/5")
print("=" * 80)

