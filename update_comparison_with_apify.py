import json

# Load the Apify results
with open('apify_dataset_results.json', 'r', encoding='utf-8') as f:
    apify_results = json.load(f)

# Create a lookup of EAN to Apify result
apify_lookup = {}
for result in apify_results:
    ean = result['ean']
    apify_lookup[ean] = {
        'found': True,
        'title': result['title'],
        'image_url': result['image_url'],
        'image_count': 1,  # This dataset shows 1 image per item
        'width': result['width'],
        'height': result['height'],
        'size_bytes': result['size_bytes']
    }

# Our 10 test EANs
test_eans = [
    "0711381332580",
    "0849455000032",
    "0858183005059",
    "0820581153908",
    "0819046000420",
    "0818617022571",
    "0186011000182",
    "0312547171670",
    "0852466006016",
    "0824150401162"
]

print("Apify Results for 10 Test EAN Codes:")
print("=" * 80)

found_count = 0
for i, ean in enumerate(test_eans, 1):
    if ean in apify_lookup:
        result = apify_lookup[ean]
        print(f"{i}. EAN {ean}: FOUND")
        print(f"   Title: {result['title']}")
        print(f"   Image: {result['width']}x{result['height']}px")
        found_count += 1
    else:
        print(f"{i}. EAN {ean}: NOT FOUND")

print("=" * 80)
print(f"Success Rate: {found_count}/10 ({found_count*10}%)")
print(f"Image Coverage: {found_count}/10 ({found_count*10}%)")

# Save results for HTML generation
comparison_data = {
    'test_eans': test_eans,
    'apify_results': apify_lookup,
    'found_count': found_count
}

with open('apify_comparison_data.json', 'w', encoding='utf-8') as f:
    json.dump(comparison_data, f, indent=2)

print("\nComparison data saved to apify_comparison_data.json")

