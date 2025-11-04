import urllib.request
import urllib.error
import json
import time

# Barcode Lookup API Key
API_KEY = "YOUR_BARCODE_LOOKUP_API_KEY_HERE"  # Replace with your actual key

# Sample 10 UPCs from Palmer's list
test_upcs = [
    "673316036539",  # Soft Pretzel Mini Buns
    "770981031026",  # SPRING ASST CUPCAKES
    "691355885260",  # Hammonds Spiral Rainbow Blast Lollipop
    "657522750021",  # Ecce Panis Multigrain Boule
    "606991010402",  # Chabaso Classic Ciabatta Bread
    "770981044101",  # Valentines Chocolate Cupcakes
    "739398207400",  # Eli's Brioche Hamburger Rolls
    "701826100010",  # Grandma's Cinnamon Walnut Coffee Cake
    "770981034034",  # VANILLA SPRING CUPCAKES
    "705105677736",  # Tom Cat Baguette
]

def test_barcode_lookup(upc):
    """Test Barcode Lookup API"""
    try:
        url = f"https://api.barcodelookup.com/v3/products?barcode={upc}&key={API_KEY}"
        headers = {
            'Accept': 'application/json',
            'User-Agent': 'PalmersTestScript/1.0'
        }
        
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode())
            return data
    except Exception as e:
        return {"error": str(e)}

print("=" * 80)
print("BARCODE LOOKUP API TESTING - 10 Random Palmer's UPCs")
print("=" * 80)
print()
print(f"API Key: {API_KEY[:10]}...{API_KEY[-10:]}")
print("Plan: Testing with your API key")
print()
print("=" * 80)
print()

results_summary = {
    'found': 0,
    'not_found': 0,
    'errors': 0
}

for i, upc in enumerate(test_upcs, 1):
    print(f"\n{'='*80}")
    print(f"TEST {i}/10: UPC {upc}")
    print('='*80)
    
    result = test_barcode_lookup(upc)
    
    if 'error' in result:
        print(f"[X] Error: {result['error']}")
        results_summary['errors'] += 1
    elif result.get('products') and len(result['products']) > 0:
        product = result['products'][0]
        print(f"[OK] FOUND!")
        print(f"\n--- Product Information ---")
        print(f"   Title: {product.get('title', 'N/A')}")
        print(f"   Brand: {product.get('brand', 'N/A')}")
        print(f"   Category: {product.get('category', 'N/A')}")
        print(f"   Manufacturer: {product.get('manufacturer', 'N/A')}")
        print(f"   UPC: {product.get('barcode_number', 'N/A')}")
        
        # Images
        images = product.get('images', [])
        print(f"\n--- Images ---")
        print(f"   Total Images: {len(images)}")
        if images:
            for idx, img in enumerate(images[:3], 1):  # Show first 3 images
                print(f"   Image {idx}: {img[:70]}...")
        
        # Pricing
        print(f"\n--- Pricing ---")
        print(f"   MSRP: {product.get('msrp', 'N/A')}")
        
        # Stores
        stores = product.get('stores', [])
        print(f"\n--- Retailers ---")
        print(f"   Available at: {len(stores)} stores")
        if stores:
            for idx, store in enumerate(stores[:3], 1):  # Show first 3 stores
                store_name = store.get('store_name', 'Unknown')
                store_price = store.get('store_price', 'N/A')
                print(f"   {idx}. {store_name}: {store_price}")
        
        # Additional Details
        print(f"\n--- Additional Info ---")
        print(f"   Description: {product.get('description', 'N/A')[:100]}...")
        print(f"   Features: {product.get('features', 'N/A')[:100]}...")
        print(f"   Size: {product.get('size', 'N/A')}")
        print(f"   Weight: {product.get('weight', 'N/A')}")
        
        results_summary['found'] += 1
    else:
        print(f"[X] Not found in database")
        print(f"   Response: {result}")
        results_summary['not_found'] += 1
    
    # Rate limiting - be respectful
    if i < len(test_upcs):
        print(f"\n[...] Waiting 1 second before next request...")
        time.sleep(1)

print("\n" + "="*80)
print("TESTING COMPLETE")
print("="*80)
print()
print("RESULTS SUMMARY:")
print(f"  [OK] Found: {results_summary['found']}/10 ({results_summary['found']*10}%)")
print(f"  [X]  Not Found: {results_summary['not_found']}/10 ({results_summary['not_found']*10}%)")
print(f"  [X]  Errors: {results_summary['errors']}/10 ({results_summary['errors']*10}%)")
print()
print("DATA PROVIDED BY BARCODE LOOKUP API:")
print("  - Product title, brand, manufacturer")
print("  - Category hierarchy")
print("  - Multiple product images")
print("  - MSRP pricing")
print("  - Retailer/store availability with prices")
print("  - Product descriptions and features")
print("  - Size, weight, and dimensions")
print()
print("="*80)

