import csv
import re

# Read the HTML file
html_file = 'API_Image_Comparison.html'
with open(html_file, 'r', encoding='utf-8') as f:
    html_content = f.read()

# Extract EAN codes and their positions from HTML
ean_pattern = r'<span class="ean-code">EAN: (\d{13})</span>'
ean_matches = list(re.finditer(ean_pattern, html_content))

print(f"Found {len(ean_matches)} EAN codes in HTML")

# Convert EAN-13 to UPC-A (remove leading 0) and build mapping
ean_to_upc = {}
for match in ean_matches:
    ean = match.group(1)
    upc = ean[1:] if ean.startswith('0') else ean
    ean_to_upc[ean] = upc

print(f"Converted to {len(ean_to_upc)} UPC codes")

# Read the master list and build UPC -> Item Name mapping
master_list_file = 'palmers-barcodes-master-list-with-upc-check.csv'
upc_to_name = {}

with open(master_list_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)
    
    # Column 1 is Item ID (which contains UPC), Column 3 is Item Name
    upc_col = 1
    name_col = 3
    
    for row in reader:
        if len(row) > max(upc_col, name_col):
            upc = row[upc_col].strip()
            item_name = row[name_col].strip() if len(row) > name_col else ""
            
            # Only store if we have a valid UPC and name
            if upc and item_name and upc.isdigit() and len(upc) == 12:
                upc_to_name[upc] = item_name

print(f"Loaded {len(upc_to_name)} products from master list")

# Build EAN -> Item Name mapping
ean_to_name = {}
for ean, upc in ean_to_upc.items():
    if upc in upc_to_name:
        ean_to_name[ean] = upc_to_name[upc]
        print(f"  Matched: EAN {ean} (UPC {upc}) -> {upc_to_name[upc]}")

print(f"\nMatched {len(ean_to_name)} products")

# Update HTML product titles
# Pattern: <div class="product-title">N. Some Name</div> followed by EAN
# We need to find each product-title div and the EAN that follows it

# Split HTML into sections for each product
# Find all product cards
product_pattern = r'(<div class="product-card">.*?<div class="row-number">(\d+)</div>.*?<div class="product-title">(\d+)\.\s*)([^<]+)(</div>.*?<span class="ean-code">EAN: (\d{13})</span>)'

def replace_title(match):
    prefix = match.group(1)  # Everything up to product-title opening
    row_num = match.group(2)
    title_num = match.group(3)
    old_name = match.group(4)
    suffix = match.group(5)  # </div> and everything after
    ean = match.group(6)
    
    if ean in ean_to_name:
        new_name = ean_to_name[ean]
        return f'{prefix}{new_name}{suffix}'
    else:
        return match.group(0)  # No change

html_content = re.sub(product_pattern, replace_title, html_content, flags=re.DOTALL)

# Write updated HTML
with open(html_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"\nSuccessfully updated {html_file} with product names from master list")
