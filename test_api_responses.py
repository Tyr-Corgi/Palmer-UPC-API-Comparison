import urllib.request
import urllib.error
import json
import time

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

def test_upcitemdb(upc):
    """Test UPCitemdb free trial API"""
    try:
        url = f"https://api.upcitemdb.com/prod/trial/lookup?upc={upc}"
        headers = {
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0'
        }
        
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            return data
    except Exception as e:
        return {"error": str(e)}

def test_openfoodfacts(upc):
    """Test OpenFoodFacts API (free)"""
    try:
        url = f"https://world.openfoodfacts.org/api/v0/product/{upc}.json"
        headers = {
            'User-Agent': 'PalmersTestScript/1.0'
        }
        
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            return data
    except Exception as e:
        return {"error": str(e)}

print("=" * 80)
print("API RESPONSE TESTING - 10 Random Palmer's UPCs")
print("=" * 80)
print()
print("Testing APIs:")
print("  1. UPCitemdb (Free Trial)")
print("  2. OpenFoodFacts (Free)")
print()
print("Note: Barcode Lookup and Go-UPC require paid API keys to test")
print("=" * 80)
print()

for i, upc in enumerate(test_upcs, 1):
    print(f"\n{'='*80}")
    print(f"TEST {i}/10: UPC {upc}")
    print('='*80)
    
    # Test UPCitemdb
    print("\n--- UPCitemdb API Response ---")
    result = test_upcitemdb(upc)
    
    if 'error' in result:
        print(f"[X] Error: {result['error']}")
    elif result.get('code') == 'OK' and result.get('items'):
        item = result['items'][0]
        print(f"[OK] FOUND!")
        print(f"   Title: {item.get('title', 'N/A')}")
        print(f"   Brand: {item.get('brand', 'N/A')}")
        print(f"   Category: {item.get('category', 'N/A')}")
        print(f"   Images: {len(item.get('images', []))} available")
        if item.get('images'):
            print(f"   First Image URL: {item['images'][0][:80]}...")
        print(f"   Lowest Price: ${item.get('lowest_recorded_price', 'N/A')}")
        print(f"   Offers: {len(item.get('offers', []))} retailers")
    else:
        print(f"[X] Not found in database")
        print(f"   Response: {result.get('code', 'Unknown')}")
    
    # Test OpenFoodFacts
    print("\n--- OpenFoodFacts API Response ---")
    result = test_openfoodfacts(upc)
    
    if 'error' in result:
        print(f"[X] Error: {result['error']}")
    elif result.get('status') == 1 and result.get('product'):
        product = result['product']
        print(f"[OK] FOUND!")
        print(f"   Product Name: {product.get('product_name', 'N/A')}")
        print(f"   Brand: {product.get('brands', 'N/A')}")
        print(f"   Category: {product.get('categories', 'N/A')[:60]}...")
        print(f"   Image URL: {product.get('image_url', 'N/A')[:80]}...")
        print(f"   Nutriscore: {product.get('nutriscore_grade', 'N/A').upper()}")
    else:
        print(f"[X] Not found in database")
    
    # Rate limiting - be respectful
    if i < len(test_upcs):
        print("\n[...] Waiting 2 seconds before next request...")
        time.sleep(2)

print("\n" + "="*80)
print("TESTING COMPLETE")
print("="*80)
print("\nSUMMARY:")
print("  - Tested 10 random UPCs from Palmer's inventory")
print("  - UPCitemdb: Shows title, brand, images, pricing, offers")
print("  - OpenFoodFacts: Shows product name, brand, categories, nutrition")
print("  - Both APIs provide image URLs")
print("\nNOTE: Paid APIs (Barcode Lookup, Go-UPC) would provide similar data")
print("      but with better coverage and more detailed information.")
print("="*80)

