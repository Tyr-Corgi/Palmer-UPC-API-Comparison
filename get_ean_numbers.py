import urllib.request
import json
import time

API_KEY = "YOUR_BARCODE_LOOKUP_API_KEY_HERE"  # Replace with your actual key

# The 10 UPCs we tested
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

print("=" * 80)
print("UPC to EAN-13 Conversion - Barcode Lookup API")
print("=" * 80)
print()

for i, upc in enumerate(test_upcs, 1):
    try:
        url = f"https://api.barcodelookup.com/v3/products?barcode={upc}&key={API_KEY}"
        req = urllib.request.Request(url, headers={'Accept': 'application/json'})
        
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode())
            
            if data.get('products') and len(data['products']) > 0:
                product = data['products'][0]
                title = product.get('title', 'Unknown Product')
                barcode_formats = product.get('barcode_formats', 'N/A')
                
                # Extract EAN-13 from barcode_formats
                ean13 = "Not found"
                if 'EAN-13' in barcode_formats:
                    ean13 = barcode_formats.split('EAN-13 ')[1].strip()
                
                print(f"{i:2}. UPC: {upc}")
                print(f"    Product: {title}")
                print(f"    EAN-13: {ean13}")
                print(f"    All Formats: {barcode_formats}")
                print()
            else:
                print(f"{i:2}. UPC: {upc}")
                print(f"    Status: NOT FOUND in database")
                print(f"    EAN-13: N/A")
                print()
        
        if i < len(test_upcs):
            time.sleep(1)
            
    except Exception as e:
        print(f"{i:2}. UPC: {upc}")
        print(f"    Error: {e}")
        print()

print("=" * 80)

