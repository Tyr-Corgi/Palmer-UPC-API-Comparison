import re

# Read the HTML file
with open('../API_Compare_Chart.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# Pattern to find Go-UPC columns that are nested inside other divs
# They should be moved to be siblings of the other api-column divs

# Find all Go-UPC columns and their positions
go_upc_pattern = r'(<div class="api-column go-upc">.*?</div>\s*</div>)'
matches = list(re.finditer(go_upc_pattern, html_content, re.DOTALL))

print(f"Found {len(matches)} Go-UPC columns")

# For each match, we need to:
# 1. Extract the Go-UPC column HTML
# 2. Remove it from its current location
# 3. Insert it at the correct location (after the last api-column but before the closing image-comparison div)

# Work backwards to avoid offset issues
for match in reversed(matches):
    go_upc_html = match.group(1)
    start_pos = match.start()
    end_pos = match.end()
    
    # Remove the incorrectly nested Go-UPC column (including the extra closing divs)
    # The pattern captured includes 2 closing divs, we only want the api-column content
    # Let's extract just the api-column part
    inner_pattern = r'(<div class="api-column go-upc">.*?</div>)\s*</div>'
    inner_match = re.search(inner_pattern, go_upc_html, re.DOTALL)
    if inner_match:
        clean_go_upc = inner_match.group(1)
        
        # Remove the Go-UPC from its current location (including the extra closing div)
        html_content = html_content[:start_pos] + html_content[end_pos:]
        
        # Now find where to insert it - look backwards from start_pos to find the image-comparison div
        # and find the last api-column closing tag before our removed content
        section_before = html_content[:start_pos]
        
        # Find the image-comparison div opening
        img_comp_start = section_before.rfind('<div class="image-comparison">')
        
        # Find the closing </div></div></div> pattern that closes the product-card
        # We want to insert before the closing </div> of image-comparison
        
        # Look for the pattern: last </div> before the product-card-content closing
        # The structure should be: image-comparison contains api-columns, then closes
        # Then product-card-content closes, then product-card closes
        
        # Find where image-comparison section ends (before we removed Go-UPC)
        # We need to insert the Go-UPC column before the </div> that closes image-comparison
        
        # Since we removed Go-UPC, we need to find the closing </div> for image-comparison
        # which should be right after our removal point
        section_after = html_content[start_pos:]
        
        # The next closing divs should be: </div> for image-comparison, </div> for product-card-content, </div> for product-card
        # We want to insert before the first </div>
        
        # Insert the Go-UPC column
        html_content = html_content[:start_pos] + '\n' + clean_go_upc + '\n            ' + html_content[start_pos:]
        
        print(f"Fixed nesting for Go-UPC column at position {start_pos}")

# Write the fixed HTML
with open('../API_Compare_Chart.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("\nSuccessfully fixed Go-UPC nesting issues!")

