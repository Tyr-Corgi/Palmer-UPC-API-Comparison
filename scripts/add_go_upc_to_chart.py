import json
import sys

# Load Go-UPC test results
with open('../json-data/go_upc_15_products_test.json', 'r', encoding='utf-8') as f:
    go_upc_data = json.load(f)

# Create a mapping of EAN to product data
ean_to_data = {}
for item in go_upc_data:
    ean = item['ean']
    ean_to_data[ean] = item

# Read the HTML file
with open('../API_Compare_Chart.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# List of EANs in order (from the chart)
eans = [
    "0711381332580",  # 1. Stonewall Kitchen
    "0849455000032",  # 2. Tumaro's Wraps
    "0858183005059",  # 3. Lillie's Q
    "0820581153908",  # 4. Bella Maria
    "0819046000420",  # 5. Inka Giant Corn
    "0818617022571",  # 6. Suja Immunity
    "0186011000182",  # 7. Stella & Chewy's
    "0312547171670",  # 8. Benadryl
    "0852466006016",  # 9. Simply Gum
    "0824150401162",  # 10. POM Wonderful
    "0753656710990",  # 11. Think Thin
    "0742676400592",  # 12. Trot Dancing Leaves
    "0810089955197",  # 13. Collagen Creamer
    "0818290019592",  # 14. Chobani Coffee
    "0850017604032",  # 15. Drumroll Chocolate
]

# Generate Go-UPC HTML snippets for each product
snippets = []
for i, ean in enumerate(eans, 1):
    data = ean_to_data[ean]
    
    snippet = f'''                <div class="api-column go-upc">
                    <div class="api-name" style="background: linear-gradient(135deg, #757575 0%, #9e9e9e 100%); color: white; padding: 8px; border-radius: 5px; font-weight: bold; margin-bottom: 10px;">Go-UPC API</div>
                    <div class="api-title">{data['api_name']}</div>
                    <div class="not-found" style="background: #fff3cd; border: 2px solid #ffc107; color: #856404;">
                        ⚠️ No Images<br>
                        <small>Go-UPC provides data but no product images</small>
                    </div>
                    <div class="product-details">
                        <h4>Product Details</h4>
                        <div class="detail-row"><span class="detail-label">Brand:</span> <span class="detail-value">{data['brand']}</span></div>
                        <div class="detail-row"><span class="detail-label">Category:</span> <span class="detail-value">{data['category']}</span></div>
                        <div class="description-text">{data['description']}</div>
                    </div>
                </div>'''
    
    snippets.append(snippet)

# Print snippets for manual insertion
print("=" * 80)
print("Go-UPC COLUMNS TO ADD TO EACH PRODUCT")
print("=" * 80)
for i, snippet in enumerate(snippets, 1):
    print(f"\n\n{'='*80}")
    print(f"PRODUCT {i}")
    print('='*80)
    print(snippet)

print("\n\n" + "="*80)
print("SUMMARY")
print("="*80)
print(f"Total snippets generated: {len(snippets)}")
print("These should be inserted AFTER the last </div> of each UPCitemdb column")
print("and BEFORE the closing </div> of the image-comparison div")

