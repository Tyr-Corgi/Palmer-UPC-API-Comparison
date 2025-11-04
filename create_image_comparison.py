import json

# Load all the test results
print("Loading test results...")

# Barcode Lookup results (from our original test)
barcode_lookup_data = {
    "0711381332580": {"title": "Stonewall Kitchen Maple Brown Butter Waffle Cookie", "image": "https://images.barcodelookup.com/25514/255140441-1.jpg"},
    "0849455000032": {"title": "Tumaro's 8\" Carb Wise Multi Grain Wraps", "image": "https://images.barcodelookup.com/3801/38010513-1.jpg"},
    "0858183005059": {"title": "Lillies's Q Ivory BBQ Sauce", "image": "https://images.barcodelookup.com/3799/37998412-1.jpg"},
    "0820581153908": {"title": "Bella Maria Spanish Cocktail Mix 3.5oz", "image": "https://images.barcodelookup.com/9061/90616775-1.jpg"},
    "0819046000420": {"title": "InkaCrops Giant Corn Chile Picante 4 Oz", "image": "https://images.barcodelookup.com/1840/18403558-1.jpg"},
    "0818617022571": {"title": "KHCH00353688 2 Fl Oz Immunity Rebound Shot Juice", "image": "https://images.barcodelookup.com/19808/198086595-1.jpg"},
    "0186011000182": {"title": "Stella & Chewy's Freeze Dried Raw Dinner Patties", "image": "https://images.barcodelookup.com/1032/10320818-1.jpg"},
    "0312547171670": {"title": "Benadryl Itch Relief Cream, Topical Analgesic, 1 Oz", "image": "https://images.barcodelookup.com/1502/15022259-1.jpg"},
    "0852466006016": {"title": "Simply Gum Mint Natural Chewing Gum", "image": "https://images.barcodelookup.com/1033/10330920-1.jpg"},
    "0824150401162": {"title": "POM Wonderful 100% Pomegranate Juice 16 Ounce", "image": "https://images.barcodelookup.com/2974/29742076-1.jpg"},
}

# Load Apify results
with open('apify_dataset_results.json', 'r') as f:
    apify_first = json.load(f)

with open('apify_retest_results.json', 'r') as f:
    apify_second = json.load(f)

apify_data = {}
for item in apify_first + apify_second:
    ean = item['ean']
    apify_data[ean] = {
        'title': item['title'],
        'image': item['image_url'],
        'width': item['width'],
        'height': item['height']
    }

# UPCitemdb data - we need to compile this
# First 5 from original test
upcitemdb_data = {
    "0849455000032": {"title": "MULTI-GRAIN 8 LOW-IN-CARB WRAPS", "images": 4},
    "0858183005059": {"title": "IVORY TRADITIONAL ALABAMA STYLE BARBECUE SAUCE", "images": 2},
    "0820581153908": {"title": "SPANISH COCKTAIL MIX", "images": 0},
    "0819046000420": {"title": "ROASTED GIANT CORN, CHILE PICANTE", "images": 8},
    "0818617022571": {"title": "Suja Immunity Rebound Juice Shot", "images": 3},
}

# Load retest results
with open('upcitemdb_retest_results.json', 'r') as f:
    upcitemdb_retest = json.load(f)

for item in upcitemdb_retest:
    upc = item['upc']
    ean = "0" + upc
    if item['found']:
        upcitemdb_data[ean] = {
            'title': item['title'],
            'images': item['image_count']
        }

# Product list
products = [
    {"ean": "0711381332580", "name": "Stonewall Kitchen Waffle Cookie", "size": "1.1 OZ"},
    {"ean": "0849455000032", "name": "Tumaro's Wraps", "size": "11.2 OZ"},
    {"ean": "0858183005059", "name": "Lillie's Q BBQ Sauce", "size": "16 OZ"},
    {"ean": "0820581153908", "name": "Bella Maria Cocktail Mix", "size": "3.5 OZ"},
    {"ean": "0819046000420", "name": "InkaCrops Giant Corn", "size": "4.0 Ounce"},
    {"ean": "0818617022571", "name": "SUJA Immunity Shot", "size": "2 Fl Oz"},
    {"ean": "0186011000182", "name": "Stella & Chewy's Dog Food", "size": "14 Oz"},
    {"ean": "0312547171670", "name": "Benadryl Itch Relief", "size": "1 Oz"},
    {"ean": "0852466006016", "name": "Simply Gum Mint", "size": ""},
    {"ean": "0824150401162", "name": "POM Wonderful Juice", "size": "16 Ounce"},
]

print("Creating comparison data...")

comparison_data = []
for i, product in enumerate(products, 1):
    ean = product['ean']
    
    item = {
        'number': i,
        'ean': ean,
        'name': product['name'],
        'size': product['size'],
        'barcode_lookup': barcode_lookup_data.get(ean),
        'apify': apify_data.get(ean),
        'upcitemdb': upcitemdb_data.get(ean)
    }
    
    comparison_data.append(item)

# Save comparison data
with open('image_comparison_data.json', 'w', encoding='utf-8') as f:
    json.dump(comparison_data, f, indent=2)

print(f"Created comparison data for {len(comparison_data)} products")
print("Data saved to image_comparison_data.json")
print()
print("Summary:")
print(f"  Barcode Lookup: {sum(1 for item in comparison_data if item['barcode_lookup'])}/10 with images")
print(f"  Apify: {sum(1 for item in comparison_data if item['apify'])}/10 with images")
print(f"  UPCitemdb: {sum(1 for item in comparison_data if item['upcitemdb'])}/10 with data")

