import json

# Load the results
with open('additional_5_items_results.json', 'r', encoding='utf-8') as f:
    results = json.load(f)

def format_description(desc, max_length=200):
    """Truncate description if too long"""
    if not desc or desc == 'N/A':
        return ''
    if len(desc) > max_length:
        return desc[:max_length] + '...'
    return desc

def format_size(size):
    """Format size"""
    if not size or size == 'N/A' or size == '':
        return ''
    return size

def format_resolution(width, height):
    """Format resolution"""
    if width and height and width != 'N/A' and height != 'N/A':
        return f"{width} x {height}px"
    return "Unknown (Standard)"

def format_file_size(size_bytes):
    """Format file size"""
    if not size_bytes or size_bytes == 'N/A':
        return ''
    try:
        size_kb = int(size_bytes) / 1024
        return f"{int(size_bytes):,} bytes (~{int(size_kb)} KB)"
    except:
        return ''

def format_date(date_str):
    """Format date"""
    if not date_str or date_str == 'N/A':
        return ''
    # Parse "2025-11-03 23:58:23" to "November 3, 2025 23:58:23"
    try:
        parts = date_str.split(' ')
        date_parts = parts[0].split('-')
        months = ['January', 'February', 'March', 'April', 'May', 'June',
                  'July', 'August', 'September', 'October', 'November', 'December']
        month = months[int(date_parts[1]) - 1]
        day = int(date_parts[2])
        year = date_parts[0]
        time = parts[1] if len(parts) > 1 else ''
        return f"{month} {day}, {year} {time}"
    except:
        return date_str

# Product names (simplified from titles)
product_names = {
    11: "Think Thin Protein Bar",
    12: "Organic Dancing Leaves Tea",
    13: "Vital Proteins Collagen Creamer",
    14: "RJ45 Ethernet Connector",
    15: "Drumroll Mini Donuts"
}

html_sections = []

for item in results:
    num = item['number']
    upc = item['upc']
    ean = item['ean']
    name = product_names.get(num, f"Product {num}")
    
    bl = item.get('barcode_lookup', {})
    apify = item.get('apify', {})
    upcitemdb = item.get('upcitemdb', {})
    
    # Determine size from barcode lookup
    size = format_size(bl.get('size', ''))
    size_display = f'<span>Size: {size}</span>' if size else ''
    
    html = f'''
        <!-- Product {num}: {name} -->
        <div class="product-card">
            <div class="product-header">
                <div class="product-title">{num}. {name}</div>
                <div class="product-meta">
                    <span class="ean-code">EAN: {ean}</span>
                    {size_display}
                </div>
            </div>
            <div class="image-comparison">
'''
    
    # Barcode Lookup Column
    if bl.get('found'):
        first_image = bl.get('images', [None])[0] if bl.get('images') else None
        image_html = f'<img src="{first_image}" alt="Product" class="product-image">' if first_image else '<div class="not-found">No image available</div>'
        image_count = len(bl.get('images', []))
        
        html += f'''                <div class="api-column barcode-lookup">
                    <div class="api-name barcode-lookup-color">🏆 Barcode Lookup API</div>
                    <div class="api-title">{bl.get('title', 'N/A')[:80]}</div>
                    {image_html}
                    <div class="image-info">
                        <div class="resolution">Resolution: Unknown (Standard)</div>
                        <div style="margin-top: 5px;">✓ {image_count} image{'s' if image_count != 1 else ''} available</div>
                    </div>
                    <div class="product-details">
                        <h4>Product Details</h4>
                        <div class="detail-row"><span class="detail-label">Brand:</span> <span class="detail-value">{bl.get('brand', 'N/A')}</span></div>
                        <div class="detail-row"><span class="detail-label">Manufacturer:</span> <span class="detail-value">{bl.get('manufacturer', 'N/A')}</span></div>
                        <div class="detail-row"><span class="detail-label">Category:</span> <span class="detail-value">{bl.get('category', 'N/A')}</span></div>
                        <div class="detail-row"><span class="detail-label">Weight:</span> <span class="detail-value">{bl.get('weight', 'N/A')}</span></div>
                        <div class="detail-row"><span class="detail-label">UPC/EAN:</span> <span class="detail-value">{bl.get('barcode_formats', 'N/A')}</span></div>
                        {f'<div class="description-text">{format_description(bl.get("description", ""))}</div>' if format_description(bl.get('description', '')) else ''}
                    </div>
                </div>
'''
    else:
        html += '''                <div class="api-column barcode-lookup">
                    <div class="api-name barcode-lookup-color">🏆 Barcode Lookup API</div>
                    <div class="not-found">
                        ✗ Not Found<br>
                        <small>This product was not found in Barcode Lookup API</small>
                    </div>
                </div>
'''
    
    # Apify Column
    if apify.get('found'):
        image_url = apify.get('image_url', '')
        width = apify.get('width', '')
        height = apify.get('height', '')
        resolution = format_resolution(width, height)
        
        html += f'''                <div class="api-column apify">
                    <div class="api-name apify-color">🏆 Apify EAN/GTIN</div>
                    <div class="api-title">{apify.get('title', 'N/A')[:80]}</div>
                    <img src="{image_url}" alt="Product" class="product-image">
                    <div class="image-info">
                        <div class="resolution">Resolution: {resolution}</div>
                        <div style="margin-top: 5px;">✓ High-resolution image</div>
                        <div>Format: {apify.get('image_url', '').split('.')[-1].upper() if '.' in apify.get('image_url', '') else 'Unknown'}</div>
                    </div>
                    <div class="product-details">
                        <h4>Product Details</h4>
                        <div class="detail-row"><span class="detail-label">Title:</span> <span class="detail-value">{apify.get('title', 'N/A')}</span></div>
                        <div class="detail-row"><span class="detail-label">Country:</span> <span class="detail-value">{apify.get('country_found', 'N/A')}</span></div>
                        <div class="detail-row"><span class="detail-label">File Size:</span> <span class="detail-value">{format_file_size(apify.get('size_bytes', ''))}</span></div>
                        <div class="detail-row"><span class="detail-label">Scraped:</span> <span class="detail-value">{format_date(apify.get('scraped_at', ''))}</span></div>
                    </div>
                </div>
'''
    else:
        html += '''                <div class="api-column apify">
                    <div class="api-name apify-color">🏆 Apify EAN/GTIN</div>
                    <div class="not-found">
                        ✗ Not Found<br>
                        <small>This product was not found in Apify</small>
                    </div>
                </div>
'''
    
    # UPCitemdb Column
    if upcitemdb.get('found'):
        images = upcitemdb.get('images', [])
        image_count = upcitemdb.get('image_count', 0)
        
        if images:
            # Try to find Target or Walmart image first (higher quality)
            first_image = None
            for img in images:
                if 'target.scene7.com' in img or 'walmartimages.com' in img:
                    first_image = img
                    break
            if not first_image:
                first_image = images[0]
            
            # Get resolution from URL
            resolution = "450 x 450px"
            if 'wid=1000&hei=1000' in first_image:
                resolution = "1000 x 1000px (Target image)"
            elif 'odnHeight=450&odnWidth=450' in first_image:
                resolution = "450 x 450px"
            
            html += f'''                <div class="api-column upcitemdb">
                    <div class="api-name upcitemdb-color">🏆 UPCitemdb</div>
                    <div class="api-title">{upcitemdb.get('title', 'N/A')[:80]}</div>
                    <img src="{first_image}" alt="Product" class="product-image">
                    <div class="image-info">
                        <div class="resolution">Resolution: {resolution}</div>
                        <div class="image-count" style="margin-top: 8px;">📸 {image_count} image{'s' if image_count != 1 else ''} available</div>
                    </div>
                    <div class="product-details">
                        <h4>Product Details</h4>
                        <div class="detail-row"><span class="detail-label">Title:</span> <span class="detail-value">{upcitemdb.get('title', 'N/A')}</span></div>
                        {f'<div class="detail-row"><span class="detail-label">Brand:</span> <span class="detail-value">{upcitemdb.get("brand", "N/A")}</span></div>' if upcitemdb.get('brand') else ''}
                        <div class="detail-row"><span class="detail-label">Images:</span> <span class="detail-value">{image_count} image{'s' if image_count != 1 else ''} from retailers</span></div>
                    </div>
                </div>
'''
        else:
            html += f'''                <div class="api-column upcitemdb">
                    <div class="api-name upcitemdb-color">🏆 UPCitemdb</div>
                    <div class="api-title">{upcitemdb.get('title', 'N/A')[:80]}</div>
                    <div class="not-found" style="padding: 40px;">
                        ✓ Found<br>
                        <div style="margin-top: 10px;">📸 0 images available</div>
                        <small style="display: block; margin-top: 10px;">No images for this product</small>
                    </div>
                    <div class="product-details">
                        <h4>Product Details</h4>
                        <div class="detail-row"><span class="detail-label">Title:</span> <span class="detail-value">{upcitemdb.get('title', 'N/A')}</span></div>
                        <div class="detail-row"><span class="detail-label">Images:</span> <span class="detail-value">No images available</span></div>
                    </div>
                </div>
'''
    else:
        html += '''                <div class="api-column upcitemdb">
                    <div class="api-name upcitemdb-color">🏆 UPCitemdb</div>
                    <div class="not-found">
                        ✗ Not Found<br>
                        <small>This product was not found in UPCitemdb</small>
                    </div>
                </div>
'''
    
    html += '''            </div>
        </div>
'''
    
    html_sections.append(html)

# Write all sections
with open('new_items_html.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(html_sections))

print("Generated HTML for 5 new items")
print(f"Total sections: {len(html_sections)}")
print("Saved to new_items_html.txt")

