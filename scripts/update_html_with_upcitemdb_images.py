import json
import re

# Load UPCitemdb images
with open('upcitemdb_all_images.json', 'r') as f:
    upcitemdb_data = json.load(f)

def get_resolution_from_url(url):
    """Extract resolution from URL if available"""
    # Target images: ?wid=1000&hei=1000
    target_match = re.search(r'wid=(\d+)&hei=(\d+)', url)
    if target_match:
        return f"{target_match.group(1)} x {target_match.group(2)}px"
    
    # Walmart images: ?odnHeight=450&odnWidth=450
    walmart_match = re.search(r'odnHeight=(\d+)&odnWidth=(\d+)', url)
    if walmart_match:
        return f"{walmart_match.group(2)} x {walmart_match.group(1)}px"
    
    # Some URLs have _ex=512x512
    ex_match = re.search(r'_ex=(\d+)x(\d+)', url)
    if ex_match:
        return f"{ex_match.group(1)} x {ex_match.group(2)}px"
    
    # Petco images: w_700
    petco_match = re.search(r'w_(\d+)', url)
    if petco_match:
        return f"~{petco_match.group(1)}px width"
    
    return "Variable/Unknown"

# Product mapping
products = {
    "0849455000032": 2,  # Tumaro's
    "0858183005059": 3,  # Lillie's Q
    "0820581153908": 4,  # Bella Maria
    "0819046000420": 5,  # InkaCrops
    "0818617022571": 6,  # SUJA
    "0186011000182": 7,  # Stella & Chewy's
    "0312547171670": 8,  # Benadryl
    "0852466006016": 9,  # Simply Gum
    "0824150401162": 10,  # POM
}

print("UPCitemdb Image URLs for HTML:")
print("=" * 80)
for ean, product_num in products.items():
    if ean in upcitemdb_data:
        data = upcitemdb_data[ean]
        if data['images']:
            first_image = data['images'][0]
            resolution = get_resolution_from_url(first_image)
            print(f"\nProduct {product_num} (EAN {ean}):")
            print(f"  Image URL: {first_image}")
            print(f"  Resolution: {resolution}")
            print(f"  Total images: {data['image_count']}")
        else:
            print(f"\nProduct {product_num} (EAN {ean}): No images")

print("\n" + "=" * 80)
print("Ready to update HTML!")

