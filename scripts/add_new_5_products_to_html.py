"""
Generate HTML for the 5 new products and add them to API_Compare_Chart.html
This will insert the new products between product 15 and the footer.
"""
import json
import os

# Load the API results
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
json_file = os.path.join(project_root, 'json-data', 'new_5_products_results.json')
html_file = os.path.join(project_root, 'API_Compare_Chart.html')

with open(json_file, 'r', encoding='utf-8') as f:
    products = json.load(f)

def generate_product_html(product):
    """Generate HTML for a single product"""
    num = product['number']
    upc = product['upc']
    ean = product['ean']
    
    barcode = product.get('barcode_lookup', {})
    upcitemdb = product.get('upcitemdb', {})
    apify = product.get('apify', {})
    go_upc = product.get('go_upc', {})
    
    # Determine product title (use the most detailed one)
    if barcode.get('found') and barcode.get('title'):
        title = barcode['title']
    elif upcitemdb.get('found') and upcitemdb.get('title'):
        title = upcitemdb['title']
    elif apify.get('found') and apify.get('title'):
        title = apify['title']
    elif go_upc.get('found') and go_upc.get('name'):
        title = go_upc['name']
    else:
        title = f"Product {num}"
    
    # Get size if available
    size = barcode.get('size', '') if barcode.get('found') else ''
    
    html = f'''
        <!-- Product {num}: {title[:50]} -->
        <div class="product-card">
            <div class="row-number">{num}</div>
            <div class="product-card-content">
            <div class="product-header">
                <div class="product-title">{num}. {title}</div>
                <div class="product-meta">
                    {f'<span>Size: {size}</span>' if size else '<span>Size: N/A</span>'}
                </div>
            </div>
            
            <div class="upc-info-box">
                <h4>📊 UPC/EAN:</h4> <span class="upc-display">UPC-A: <strong>{upc}</strong> | EAN-13: <strong>{ean}</strong> | API Used: <strong style="color: #1976d2;">{upc}</strong></span>
            </div>
            
            <div class="image-comparison">'''
    
    # Barcode Lookup Column
    if barcode.get('found'):
        images = barcode.get('images', [])
        has_images = len(images) > 0
        image_url = images[0] if has_images else "https://via.placeholder.com/300x300?text=No+Image"
        
        html += f'''
                <div class="api-column barcode-lookup">
                    <div class="api-name barcode-lookup-color">🏆 Barcode Lookup API</div>
                    <div class="api-title">{barcode.get('title', 'N/A')[:80]}</div>
                    <img src="{image_url}" alt="Product" class="product-image">
                    <div class="image-info">
                        <div class="resolution">Resolution: Unknown (Standard)</div>
                        <div style="margin-top: 5px;">✓ {len(images)} image{'s' if len(images) != 1 else ''} available</div>
                    </div>
                    <div class="product-details">
                        <h4>Product Details</h4>
                        {f'<div class="detail-row"><span class="detail-label">Brand:</span> <span class="detail-value">{barcode.get("brand", "N/A")}</span></div>' if barcode.get('brand') else ''}
                        {f'<div class="detail-row"><span class="detail-label">Manufacturer:</span> <span class="detail-value">{barcode.get("manufacturer", "N/A")}</span></div>' if barcode.get('manufacturer') else ''}
                        {f'<div class="detail-row"><span class="detail-label">Category:</span> <span class="detail-value">{barcode.get("category", "N/A")}</span></div>' if barcode.get('category') else ''}
                        {f'<div class="detail-row"><span class="detail-label">Weight:</span> <span class="detail-value">{barcode.get("weight", "N/A")}</span></div>' if barcode.get('weight') else ''}
                        <div class="detail-row"><span class="detail-label">UPC/EAN:</span> <span class="detail-value">{barcode.get('barcode_formats', 'N/A')}</span></div>
                        {f'<div class="description-text">{barcode.get("description", "")}</div>' if barcode.get('description') else ''}
                    </div>
                </div>'''
    else:
        error_msg = barcode.get('error', 'Not found')
        html += f'''
                <div class="api-column barcode-lookup">
                    <div class="api-name barcode-lookup-color">🏆 Barcode Lookup API</div>
                    <div class="not-found">
                        ✗ Not Found<br>
                        <small>{error_msg}</small>
                    </div>
                </div>'''
    
    # Apify Column
    if apify.get('found'):
        html += f'''
                <div class="api-column apify">
                    <div class="api-name apify-color">🏆 Apify EAN/GTIN</div>
                    <div class="api-title">{apify.get('title', 'N/A')[:80]}</div>
                    <img src="{apify.get('image_url', '')}" alt="Product" class="product-image">
                    <div class="image-info">
                        <div class="resolution">Resolution: {apify.get('width', 'Unknown')} x {apify.get('height', 'Unknown')}px</div>
                        <div style="margin-top: 5px;">✓ High-resolution image</div>
                        <div>Format: {'PNG' if '.png' in apify.get('image_url', '') else 'JPEG'}</div>
                    </div>
                    <div class="product-details">
                        <h4>Product Details</h4>
                        <div class="detail-row"><span class="detail-label">Title:</span> <span class="detail-value">{apify.get('title', 'N/A')}</span></div>
                        <div class="detail-row"><span class="detail-label">Country:</span> <span class="detail-value">{apify.get('country_found', 'N/A')}</span></div>
                        <div class="detail-row"><span class="detail-label">File Size:</span> <span class="detail-value">{apify.get('size_bytes', 0):,} bytes (~{apify.get('size_bytes', 0) // 1024} KB)</span></div>
                        <div class="detail-row"><span class="detail-label">Scraped:</span> <span class="detail-value">{apify.get('scraped_at', 'N/A')}</span></div>
                    </div>
                </div>'''
    else:
        html += f'''
                <div class="api-column apify">
                    <div class="api-name apify-color">🏆 Apify EAN/GTIN</div>
                    <div class="not-found">
                        ✗ Not Found<br>
                        <small>This product was not found in Apify</small>
                    </div>
                </div>'''
    
    # UPCitemdb Column
    if upcitemdb.get('found'):
        images = upcitemdb.get('images', [])
        image_count = upcitemdb.get('image_count', 0)
        
        if image_count > 0:
            # Has images - create gallery
            html += f'''
                <div class="api-column upcitemdb">
                    <div class="api-name upcitemdb-color">🏆 UPCitemdb</div>
                    <div class="api-title">{upcitemdb.get('title', 'N/A')[:80]}</div>
                    <img id="img-{num}-upcitemdb" src="{images[0]}" alt="Product" class="product-image">
                    <div class="image-info">
                        <div class="resolution">Resolution: Unknown (first of {image_count} images)</div>
                    <div class="image-nav-buttons">
                        <button id="prev-{num}-upcitemdb" class="image-nav-btn" onclick="navigateImage({num}, 'upcitemdb', -1)">◀ Previous</button>
                        <span id="counter-{num}-upcitemdb" class="image-counter">1 / {image_count}</span>
                        <button id="next-{num}-upcitemdb" class="image-nav-btn" onclick="navigateImage({num}, 'upcitemdb', 1)">Next ▶</button>
                    </div>
                        <div class="image-count" style="margin-top: 8px;">📸 {image_count} images available</div>
                    </div>
                    <div class="product-details">
                        <h4>Product Details</h4>
                        <div class="detail-row"><span class="detail-label">Title:</span> <span class="detail-value">{upcitemdb.get('title', 'N/A')}</span></div>
                        {f'<div class="detail-row"><span class="detail-label">Brand:</span> <span class="detail-value">{upcitemdb.get("brand", "N/A")}</span></div>' if upcitemdb.get('brand') else ''}
                        <div class="detail-row"><span class="detail-label">Images:</span> <span class="detail-value">{image_count} images from retailers</span></div>
                    </div>
                </div>'''
        else:
            # No images
            html += f'''
                <div class="api-column upcitemdb">
                    <div class="api-name upcitemdb-color">🏆 UPCitemdb</div>
                    <div class="api-title">{upcitemdb.get('title', 'N/A')[:80]}</div>
                    <div class="not-found">
                        ✓ Product Found<br>
                        <small>No images available</small>
                    </div>
                    <div class="product-details">
                        <h4>Product Details</h4>
                        <div class="detail-row"><span class="detail-label">Title:</span> <span class="detail-value">{upcitemdb.get('title', 'N/A')}</span></div>
                        {f'<div class="detail-row"><span class="detail-label">Brand:</span> <span class="detail-value">{upcitemdb.get("brand", "N/A")}</span></div>' if upcitemdb.get('brand') else ''}
                    </div>
                </div>'''
    else:
        html += f'''
                <div class="api-column upcitemdb">
                    <div class="api-name upcitemdb-color">🏆 UPCitemdb</div>
                    <div class="not-found">
                        ✗ Not Found<br>
                        <small>This product was not found in UPCitemdb</small>
                    </div>
                </div>'''
    
    # Go-UPC Column
    if go_upc.get('found'):
        html += f'''
                <div class="api-column go-upc">
                    <div class="api-name" style="background: linear-gradient(135deg, #757575 0%, #9e9e9e 100%); color: white; padding: 8px; border-radius: 5px; font-weight: bold; margin-bottom: 10px;">Go-UPC API</div>
                    <div class="api-title">{go_upc.get('name', 'N/A')[:80]}</div>
                    <img src="{go_upc.get('image_url', '')}" alt="Product" class="product-image">
                    <div class="image-info">
                        <div class="resolution">Resolution: Unknown</div>
                        <div style="margin-top: 5px;">✓ 1 image available</div>
                    </div>
                    <div class="product-details">
                        <h4>Product Details</h4>
                        {f'<div class="detail-row"><span class="detail-label">Brand:</span> <span class="detail-value">{go_upc.get("brand", "N/A")}</span></div>' if go_upc.get('brand') else ''}
                        {f'<div class="detail-row"><span class="detail-label">Category:</span> <span class="detail-value">{go_upc.get("category", "N/A")}</span></div>' if go_upc.get('category') else ''}
                        {f'<div class="description-text">{go_upc.get("description", "")}</div>' if go_upc.get('description') else ''}
                    </div>
                </div>'''
    else:
        html += f'''
                <div class="api-column go-upc">
                    <div class="api-name" style="background: linear-gradient(135deg, #757575 0%, #9e9e9e 100%); color: white; padding: 8px; border-radius: 5px; font-weight: bold; margin-bottom: 10px;">Go-UPC API</div>
                    <div class="not-found">
                        ✗ Not Found<br>
                        <small>This product was not found in Go-UPC</small>
                    </div>
                </div>'''
    
    html += '''
            </div>
            </div>
            </div>
        </div>
'''
    
    return html

# Generate HTML for all 5 products
all_html = ""
gallery_data = {}

for product in products:
    all_html += generate_product_html(product)
    
    # Collect gallery data for UPCitemdb products with images
    num = product['number']
    upcitemdb = product.get('upcitemdb', {})
    if upcitemdb.get('found') and upcitemdb.get('image_count', 0) > 0:
        images = upcitemdb.get('images', [])
        gallery_data[f"{num}-upcitemdb"] = images

# Read the existing HTML file
with open(html_file, 'r', encoding='utf-8') as f:
    html_content = f.read()

# Find where to insert (right before the footer)
footer_position = html_content.find('        <footer>')

if footer_position == -1:
    print("ERROR: Could not find footer position in HTML file")
    exit(1)

# Insert the new products
new_html = html_content[:footer_position] + all_html + "\n" + html_content[footer_position:]

# Now add gallery JavaScript data if needed
if gallery_data:
    # Find the last gallery entry
    last_gallery_pos = new_html.rfind("imageGalleries['10-upcitemdb']")
    if last_gallery_pos != -1:
        # Find the end of that line
        line_end = new_html.find(';', last_gallery_pos) + 1
        
        # Generate gallery JavaScript
        gallery_js = ""
        for key, images in gallery_data.items():
            images_json = json.dumps(images)
            gallery_js += f"\n        imageGalleries['{key}'] = {{'currentIndex': 0, 'images': {images_json}}};"
        
        # Insert gallery data
        new_html = new_html[:line_end] + gallery_js + new_html[line_end:]

# Update the footer summary statistics
new_html = new_html.replace(
    '🏆 <strong>Barcode Lookup API:</strong> 15/15 products found (100%)',
    '🏆 <strong>Barcode Lookup API:</strong> 17/20 products found (85%)'
)
new_html = new_html.replace(
    '🏆 <strong>Apify EAN/GTIN:</strong> 13/15 products found (87%)',
    '🏆 <strong>Apify EAN/GTIN:</strong> 18/20 products found (90%)'
)
new_html = new_html.replace(
    '🏆 <strong>UPCitemdb:</strong> 11/15 products found (73%)',
    '🏆 <strong>UPCitemdb:</strong> 12/20 products found (60%)'
)

# Add Go-UPC to footer if not already there
if 'Go-UPC:' not in new_html:
    apify_line_pos = new_html.find('🏆 <strong>Apify EAN/GTIN:</strong> 18/20 products found (90%)')
    if apify_line_pos != -1:
        line_end = new_html.find('<br>', apify_line_pos) + 4
        go_upc_line = '\n                🏆 <strong>Go-UPC:</strong> 20/20 products found (100%) | Consistent availability<br>'
        new_html = new_html[:line_end] + go_upc_line + new_html[line_end:]

# Write the updated HTML
with open(html_file, 'w', encoding='utf-8') as f:
    f.write(new_html)

print("=" * 80)
print("SUCCESS!")
print("=" * 80)
print(f"Added 5 new products (16-20) to {os.path.basename(html_file)}")
print("\nProducts added:")
for product in products:
    num = product['number']
    title = product.get('barcode_lookup', {}).get('title') or \
            product.get('upcitemdb', {}).get('title') or \
            product.get('apify', {}).get('title') or \
            product.get('go_upc', {}).get('name') or \
            f"Product {num}"
    print(f"  {num}. {title[:60]}")

print("\nAPI Success Rates:")
print(f"  Barcode Lookup: 17/20 (85%)")
print(f"  Apify: 18/20 (90%)")
print(f"  UPCitemdb: 12/20 (60%)")
print(f"  Go-UPC: 20/20 (100%)")

print("\nOpen API_Compare_Chart.html in your browser to view!")

