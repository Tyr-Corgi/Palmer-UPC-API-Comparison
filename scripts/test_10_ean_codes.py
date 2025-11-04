import csv
import random
import urllib.request
import json
import time

API_KEY = "YOUR_BARCODE_LOOKUP_API_KEY_HERE"  # Replace with your actual key

# Get 5 more random UPCs from the master list
with open('palmers-barcodes-master-list-with-upc-check.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)
    
    # Get all rows with valid UPCs
    all_rows = []
    for row in reader:
        if row and len(row) > 1:
            upc = row[1].strip()
            if upc.isdigit() and len(upc) == 12:
                all_rows.append(row)
    
    # Get 5 random rows
    random_rows = random.sample(all_rows, 5)
    
    test_items = []
    for row in random_rows:
        upc = row[1].strip()
        ean = "0" + upc
        size = row[7] if len(row) > 7 else "Unknown"
        test_items.append({"upc": upc, "ean": ean, "size": size})

print("=" * 80)
print("Testing 5 MORE Random EAN Codes with Barcode Lookup API")
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

# Save new results
with open('ean_test_results_additional.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2)

# Load previous results
with open('ean_test_results.json', 'r', encoding='utf-8') as f:
    previous_results = json.load(f)

# Combine all results
all_results = previous_results + results

# Save combined results
with open('ean_test_results_combined.json', 'w', encoding='utf-8') as f:
    json.dump(all_results, f, indent=2)

print("=" * 80)
print(f"New results: Found {sum(1 for r in results if r['found'])}/5")
print(f"Total results: Found {sum(1 for r in all_results if r['found'])}/10")
print("Combined results saved to ean_test_results_combined.json")
print("=" * 80)

