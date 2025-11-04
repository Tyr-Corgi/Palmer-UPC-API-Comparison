import re

# Read the HTML file
with open('../API_Compare_Chart.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern to find Go-UPC columns that are nested inside product-details or other divs
# They appear after </div> (closing product-details) but before the parent api-column closes

# Find all instances where Go-UPC is improperly nested
# Pattern: </div> followed by spaces and <div class="api-column go-upc">
# where there's excessive indentation (more than 16 spaces)

pattern = r'(</div>\s{20,})<div class="api-column go-upc">'

matches = list(re.finditer(pattern, content))
print(f"Found {len(matches)} improperly indented Go-UPC columns")

# Replace excessive indentation with proper indentation
# Go-UPC should be at the same level as other api-columns (16 spaces)
content = re.sub(
    r'(</div>)\s{20,}<div class="api-column go-upc">',
    r'\1\n                </div>\n                <div class="api-column go-upc">',
    content
)

# Write back
with open('../API_Compare_Chart.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Fixed {len(matches)} Go-UPC nesting issues")
print("All Go-UPC columns should now be properly positioned!")

