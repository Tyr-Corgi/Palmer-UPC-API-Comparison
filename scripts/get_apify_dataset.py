import urllib.request
import json

# Your existing dataset ID
APIFY_TOKEN = "YOUR_APIFY_API_TOKEN_HERE"  # Replace with your actual token
DATASET_ID = "iyo0vudLRPaddfFCG"

print("=" * 80)
print("RETRIEVING APIFY DATASET RESULTS")
print("=" * 80)
print()
print(f"Dataset ID: {DATASET_ID}")
print()

try:
    # Get dataset items
    url = f"https://api.apify.com/v2/datasets/{DATASET_ID}/items?token={APIFY_TOKEN}"
    
    req = urllib.request.Request(url, headers={'Accept': 'application/json'})
    with urllib.request.urlopen(req, timeout=30) as response:
        results = json.loads(response.read().decode())
        
    print(f"[OK] Retrieved {len(results)} items from dataset")
    print()
    
    # Save results
    with open('apify_dataset_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    
    print("Results saved to apify_dataset_results.json")
    print()
    print("=" * 80)
    print("DATASET SUMMARY")
    print("=" * 80)
    print()
    
    for i, item in enumerate(results[:10], 1):  # Show first 10
        print(f"{i}. Item keys: {list(item.keys())}")
        if 'ean' in item or 'gtin' in item or 'barcode' in item:
            ean = item.get('ean') or item.get('gtin') or item.get('barcode')
            print(f"   EAN/GTIN: {ean}")
        if 'title' in item or 'name' in item:
            title = item.get('title') or item.get('name')
            print(f"   Title: {title[:60] if title else 'N/A'}...")
        if 'images' in item or 'imageUrl' in item or 'image' in item:
            images = item.get('images') or item.get('imageUrl') or item.get('image')
            if isinstance(images, list):
                print(f"   Images: {len(images)} found")
            else:
                print(f"   Image: {images[:60] if images else 'N/A'}...")
        print()
        
    print("=" * 80)
    print(f"Total items in dataset: {len(results)}")
    print("=" * 80)
    
except Exception as e:
    print(f"[X] Error: {e}")
    import traceback
    traceback.print_exc()

