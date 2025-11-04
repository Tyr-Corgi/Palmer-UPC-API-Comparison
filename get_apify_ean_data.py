import urllib.request
import json

# The 5 EAN-13 codes we just generated
ean_codes = [
    "0711381332580",
    "0849455000032",
    "0858183005059",
    "0820581153908",
    "0819046000420"
]

# Apify API endpoint to get dataset items
api_url = "https://api.apify.com/v2/datasets/iyo0vudLRPaddfFCG/items?token=apify_api_gBHMi6P36DOsvOU3SkYM3b8qmFFvWe0JJUdc"

print("Fetching data from Apify dataset...")

try:
    req = urllib.request.Request(api_url, headers={'Accept': 'application/json'})
    with urllib.request.urlopen(req, timeout=30) as response:
        data = json.loads(response.read().decode())
        
    print(f"Retrieved {len(data)} items from Apify dataset")
    print()
    
    # Filter for our 5 EAN codes
    matching_items = []
    for item in data:
        # Check if the item matches any of our EAN codes
        item_ean = item.get('ean', '') or item.get('gtin', '') or item.get('barcode', '')
        if item_ean in ean_codes:
            matching_items.append(item)
    
    # Save as JSON for HTML generation
    with open('apify_ean_results.json', 'w', encoding='utf-8') as f:
        json.dump({
            'ean_codes': ean_codes,
            'matching_items': matching_items,
            'all_items': data
        }, f, indent=2)
    
    print(f"Found {len(matching_items)} matching items")
    print(f"Total items in dataset: {len(data)}")
    print()
    print("Sample of dataset structure:")
    if data:
        print(json.dumps(data[0], indent=2))
    
except Exception as e:
    print(f"Error: {e}")

