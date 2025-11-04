import csv

def create_html_report():
    """Create an HTML report with product images"""
    
    input_file = 'palmers-barcodes-verified-with-images.csv'
    output_file = 'Palmers_Verified_Products_with_Images.html'
    
    # Read verified products with images
    products = []
    
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        
        for row in reader:
            if len(row) > 4 and row[0] == 'YES':
                status = row[0]
                db_product = row[1]
                source = row[2]
                image_url = row[3]
                upc = row[4]
                dept = row[5] if len(row) > 5 else ''
                item_name = row[6] if len(row) > 6 else ''
                size = row[7] if len(row) > 7 else ''
                price = row[9] if len(row) > 9 else ''
                
                products.append({
                    'upc': upc,
                    'dept': dept,
                    'item_name': item_name,
                    'db_product': db_product,
                    'size': size,
                    'price': price,
                    'image_url': image_url,
                    'source': source
                })
    
    # Create HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Palmer's Verified Products with Images</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            color: #333;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        
        header {{
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-bottom: 30px;
            text-align: center;
        }}
        
        h1 {{
            color: #667eea;
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .subtitle {{
            color: #666;
            font-size: 1.2em;
        }}
        
        .stats {{
            display: flex;
            gap: 20px;
            justify-content: center;
            margin-top: 20px;
            flex-wrap: wrap;
        }}
        
        .stat-box {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 30px;
            border-radius: 10px;
            font-size: 1.1em;
            font-weight: bold;
        }}
        
        .stat-box span {{
            font-size: 1.5em;
            display: block;
            margin-top: 5px;
        }}
        
        .products-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 25px;
        }}
        
        .product-card {{
            background: white;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}
        
        .product-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }}
        
        .product-image {{
            width: 100%;
            height: 250px;
            object-fit: contain;
            background: #f8f9fa;
            padding: 20px;
        }}
        
        .no-image {{
            height: 250px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            color: #666;
            font-size: 1.2em;
        }}
        
        .product-info {{
            padding: 20px;
        }}
        
        .product-name {{
            font-size: 1.1em;
            font-weight: bold;
            color: #333;
            margin-bottom: 10px;
            line-height: 1.4;
        }}
        
        .product-db-name {{
            font-size: 0.9em;
            color: #667eea;
            margin-bottom: 10px;
            font-style: italic;
        }}
        
        .product-details {{
            display: grid;
            gap: 8px;
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid #eee;
        }}
        
        .detail-row {{
            display: flex;
            justify-content: space-between;
            font-size: 0.9em;
        }}
        
        .detail-label {{
            color: #666;
            font-weight: 500;
        }}
        
        .detail-value {{
            color: #333;
            font-weight: bold;
        }}
        
        .upc {{
            font-family: 'Courier New', monospace;
            background: #f8f9fa;
            padding: 5px 10px;
            border-radius: 5px;
            font-size: 0.85em;
        }}
        
        .price {{
            color: #28a745;
            font-size: 1.2em;
        }}
        
        .source-badge {{
            display: inline-block;
            padding: 3px 8px;
            border-radius: 5px;
            font-size: 0.75em;
            font-weight: bold;
            margin-top: 10px;
        }}
        
        .source-upcitemdb {{
            background: #ffd700;
            color: #333;
        }}
        
        .source-openfoodfacts {{
            background: #28a745;
            color: white;
        }}
        
        footer {{
            text-align: center;
            color: white;
            margin-top: 40px;
            padding: 20px;
            background: rgba(255,255,255,0.1);
            border-radius: 10px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🛒 Palmer's Verified Products</h1>
            <p class="subtitle">UPC Database Verification Report with Product Images</p>
            <div class="stats">
                <div class="stat-box">
                    <div>Total Verified</div>
                    <span>{len(products)}</span>
                </div>
                <div class="stat-box">
                    <div>Products with Images</div>
                    <span>{len([p for p in products if p['image_url']])}</span>
                </div>
                <div class="stat-box">
                    <div>Data Sources</div>
                    <span>2</span>
                </div>
            </div>
        </header>
        
        <div class="products-grid">
"""
    
    # Add product cards
    for product in products:
        image_html = ''
        if product['image_url']:
            image_html = f'<img src="{product["image_url"]}" alt="{product["item_name"]}" class="product-image">'
        else:
            image_html = '<div class="no-image">No Image Available</div>'
        
        source_class = 'source-' + product['source'].lower().replace(' ', '')
        
        html += f"""
            <div class="product-card">
                {image_html}
                <div class="product-info">
                    <div class="product-name">{product['item_name']}</div>
                    <div class="product-db-name">"{product['db_product']}"</div>
                    <div class="product-details">
                        <div class="detail-row">
                            <span class="detail-label">UPC:</span>
                            <span class="detail-value upc">{product['upc']}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Department:</span>
                            <span class="detail-value">{product['dept']}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Size:</span>
                            <span class="detail-value">{product['size']}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Price:</span>
                            <span class="detail-value price">{product['price']}</span>
                        </div>
                    </div>
                    <span class="source-badge {source_class}">{product['source']}</span>
                </div>
            </div>
"""
    
    html += """
        </div>
        
        <footer>
            <p><strong>Report Generated:</strong> November 2, 2025</p>
            <p>Data sources: UPCitemdb & OpenFoodFacts</p>
            <p>Palmer's Barcode Master List - 500 Sample Verification</p>
        </footer>
    </div>
</body>
</html>
"""
    
    # Write HTML file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"HTML report created: {output_file}")
    print(f"Total products: {len(products)}")
    print(f"Products with images: {len([p for p in products if p['image_url']])}")
    print(f"\nOpen the file in your web browser to view!")

if __name__ == '__main__':
    create_html_report()

