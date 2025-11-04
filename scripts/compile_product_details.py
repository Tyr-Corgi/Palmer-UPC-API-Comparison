import json

# Load all data sources
with open('ean_test_results.json', 'r') as f:
    barcode_lookup = json.load(f)

with open('apify_dataset_results.json', 'r') as f:
    apify_first = json.load(f)

with open('apify_retest_results.json', 'r') as f:
    apify_second = json.load(f)

with open('upcitemdb_all_images.json', 'r') as f:
    upcitemdb_data = json.load(f)

with open('upcitemdb_retest_results.json', 'r') as f:
    upcitemdb_retest = json.load(f)

# Create lookup dictionaries
barcode_lookup_dict = {}
for item in barcode_lookup:
    barcode_lookup_dict[item['ean']] = item

apify_dict = {}
for item in apify_first + apify_second:
    apify_dict[item['ean']] = item

# Add retest UPCitemdb data
for item in upcitemdb_retest:
    ean = "0" + item['upc']
    upcitemdb_data[ean] = {
        'title': item['title'],
        'brand': item.get('brand', 'N/A'),
        'images': item['images'],
        'image_count': item['image_count']
    }

# Products list
products = [
    {"ean": "0711381332580", "name": "Stonewall Kitchen Waffle Cookie"},
    {"ean": "0849455000032", "name": "Tumaro's Wraps"},
    {"ean": "0858183005059", "name": "Lillie's Q BBQ Sauce"},
    {"ean": "0820581153908", "name": "Bella Maria Cocktail Mix"},
    {"ean": "0819046000420", "name": "InkaCrops Giant Corn"},
    {"ean": "0818617022571", "name": "SUJA Immunity Shot"},
    {"ean": "0186011000182", "name": "Stella & Chewy's Dog Food"},
    {"ean": "0312547171670", "name": "Benadryl Itch Relief"},
    {"ean": "0852466006016", "name": "Simply Gum Mint"},
    {"ean": "0824150401162", "name": "POM Wonderful Juice"},
]

compiled_data = []

for product in products:
    ean = product['ean']
    
    item = {
        'ean': ean,
        'name': product['name'],
        'barcode_lookup': barcode_lookup_dict.get(ean),
        'apify': apify_dict.get(ean),
        'upcitemdb': upcitemdb_data.get(ean)
    }
    
    compiled_data.append(item)

# Save compiled data
with open('all_product_details.json', 'w', encoding='utf-8') as f:
    json.dump(compiled_data, f, indent=2)

print(f"Compiled product details for {len(compiled_data)} products")
print("Saved to all_product_details.json")
print()

# Show sample
for item in compiled_data[:2]:
    print(f"Product: {item['name']}")
    if item['barcode_lookup']:
        print(f"  Barcode Lookup: {item['barcode_lookup']['title']}")
        print(f"    Brand: {item['barcode_lookup'].get('brand', 'N/A')}")
        print(f"    Category: {item['barcode_lookup'].get('category', 'N/A')}")
        print(f"    Description: {item['barcode_lookup'].get('description', 'N/A')[:80]}...")
    if item['apify']:
        print(f"  Apify: {item['apify']['title']}")
        print(f"    Country: {item['apify'].get('country_found', 'N/A')}")
    if item['upcitemdb']:
        print(f"  UPCitemdb: {item['upcitemdb']['title']}")
        print(f"    Brand: {item['upcitemdb'].get('brand', 'N/A')}")
    print()

