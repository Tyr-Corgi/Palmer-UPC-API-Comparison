import re

# Read the HTML file
with open('../API_Compare_Chart.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# The problem: Go-UPC columns are nested inside the UPCitemdb's closing </div>
# Pattern: We need to find where product-details closes, then find the Go-UPC column
# and move it outside the UPCitemdb column

# Find all occurrences where Go-UPC is nested inside product-details
# Pattern: </div> (closes product-details) followed by <div class="api-column go-upc">
# but NOT followed by proper closing structure

# Better approach: Find all Go-UPC columns and check if they're improperly nested
count = 0
while True:
    # Find pattern: </div> (product-details closing) followed eventually by <div class="api-column go-upc">
    # with improper indentation (missing a closing div for the parent api-column)
    
    pattern = r'(</div>\s*<div class="api-column go-upc">)'
    match = re.search(pattern, html_content)
    
    if not match:
        break
    
    # Found an issue - Go-UPC starts right after a closing div (likely product-details)
    # We need to find the complete Go-UPC block and move it outside its parent
    
    start_pos = match.start()
    
    # Find the complete Go-UPC column (everything until its closing </div>)
    # Start from the opening <div class="api-column go-upc">
    go_upc_start = html_content.find('<div class="api-column go-upc">', start_pos)
    
    if go_upc_start == -1:
        break
    
    # Find the matching closing </div> for this api-column
    # Count opening and closing divs
    depth = 0
    pos = go_upc_start
    go_upc_end = -1
    
    while pos < len(html_content):
        if html_content[pos:pos+5] == '<div ':
            depth += 1
            pos += 5
        elif html_content[pos:pos+6] == '</div>':
            if depth == 0:
                go_upc_end = pos + 6
                break
            depth -= 1
            pos += 6
        else:
            pos += 1
    
    if go_upc_end == -1:
        print("Could not find closing div for Go-UPC column")
        break
    
    # Extract the Go-UPC column HTML
    go_upc_html = html_content[go_upc_start:go_upc_end]
    
    # Remove it from current location
    html_content = html_content[:go_upc_start] + html_content[go_upc_end:]
    
    # Now find where the parent api-column (upcitemdb/barcode-lookup/apify) ends
    # Work backwards from go_upc_start to find the opening of the current api-column
    section_before = html_content[:go_upc_start]
    
    # Find the last api-column opening before our position
    last_api_col = max(
        section_before.rfind('<div class="api-column barcode-lookup">'),
        section_before.rfind('<div class="api-column apify">'),
        section_before.rfind('<div class="api-column upcitemdb">')
    )
    
    # From that api-column, find its closing </div>
    # Count divs from last_api_col to go_upc_start
    depth = 0
    pos = last_api_col
    parent_end = -1
    
    while pos < go_upc_start:
        if html_content[pos:pos+5] == '<div ':
            depth += 1
            pos += 5
        elif html_content[pos:pos+6] == '</div>':
            if depth == 1:  # This closes the parent api-column
                parent_end = pos + 6
                break
            depth -= 1
            pos += 6
        else:
            pos += 1
    
    if parent_end == -1:
        print("Could not find parent closing div")
        break
    
    # Insert Go-UPC column after the parent's closing div
    html_content = html_content[:parent_end] + '\n' + go_upc_html + html_content[parent_end:]
    
    count += 1
    print(f"Fixed nesting issue #{count}")

# Write the fixed HTML
with open('../API_Compare_Chart.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"\nSuccessfully fixed {count} Go-UPC nesting issues!")

