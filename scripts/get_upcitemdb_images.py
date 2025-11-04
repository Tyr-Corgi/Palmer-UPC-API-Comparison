import urllib.request
import json
import time

# Get UPCitemdb images for products 2-6 (we already have 7-10)
products_to_fetch = [
    {"upc": "849455000032", "ean": "0849455000032", "name": "Tumaro's Wraps"},
    {"upc": "858183005059", "ean": "0858183005059", "name": "Lillie's Q BBQ Sauce"},
    {"upc": "820581153908", "ean": "0820581153908", "name": "Bella Maria Cocktail Mix"},
    {"upc": "819046000420", "ean": "0819046000420", "name": "InkaCrops Giant Corn"},
    {"upc": "818617022571", "ean": "0818617022571", "name": "SUJA Immunity Shot"},
]

print("Fetching UPCitemdb images for products 2-6...")
print()

upcitemdb_images = {}

for product in products_to_fetch:
    upc = product['upc']
    ean = product['ean']
    
    print(f"Fetching {product['name']} (UPC: {upc})...")
    
    try:
        url = f"https://api.upcitemdb.com/prod/trial/lookup?upc={upc}"
        req = urllib.request.Request(url, headers={'Accept': 'application/json'})
        
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode())
            
            if data.get('items') and len(data['items']) > 0:
                item = data['items'][0]
                images = item.get('images', [])
                upcitemdb_images[ean] = {
                    'title': item.get('title', 'N/A'),
                    'images': images,
                    'image_count': len(images)
                }
                print(f"  Found {len(images)} images")
                if images:
                    print(f"  First image: {images[0][:60]}...")
            else:
                upcitemdb_images[ean] = {'images': [], 'image_count': 0}
                print(f"  No images found")
                
    except Exception as e:
        print(f"  Error: {e}")
        upcitemdb_images[ean] = {'images': [], 'image_count': 0}
    
    time.sleep(2)  # Rate limiting

# Load retest results (items 7-10)
with open('upcitemdb_retest_results.json', 'r') as f:
    retest_results = json.load(f)

for item in retest_results:
    ean = "0" + item['upc']
    upcitemdb_images[ean] = {
        'title': item['title'],
        'images': item['images'],
        'image_count': item['image_count']
    }

# Save all images
with open('upcitemdb_all_images.json', 'w', encoding='utf-8') as f:
    json.dump(upcitemdb_images, f, indent=2)

print()
print("=" * 80)
print("UPCITEMDB IMAGES SUMMARY")
print("=" * 80)
for ean, data in upcitemdb_images.items():
    print(f"EAN {ean}: {data['image_count']} images")
    if data['images']:
        print(f"  First: {data['images'][0][:60]}...")
print()
print("Saved to upcitemdb_all_images.json")

