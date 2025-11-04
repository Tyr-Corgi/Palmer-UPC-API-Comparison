import csv
import urllib.request
import urllib.error
import json
import time

def get_product_image_url(upc_code):
    """
    Fetch product image URL from UPC databases
    Returns: (image_url: str, source: str)
    """
    
    # Method 1: Try UPCitemdb
    try:
        url = f"https://api.upcitemdb.com/prod/trial/lookup?upc={upc_code}"
        headers = {
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            
            if data.get('code') == 'OK' and data.get('items'):
                item = data['items'][0]
                images = item.get('images', [])
                if images:
                    return images[0], 'UPCitemdb'
    except Exception as e:
        pass
    
    # Method 2: Try OpenFoodFacts
    try:
        url = f"https://world.openfoodfacts.org/api/v0/product/{upc_code}.json"
        headers = {
            'User-Agent': 'PalmersUPCScanner/1.0'
        }
        
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            
            if data.get('status') == 1 and data.get('product'):
                product = data['product']
                image_url = product.get('image_url', '')
                if image_url:
                    return image_url, 'OpenFoodFacts'
                
                # Try alternative image fields
                image_front = product.get('image_front_url', '')
                if image_front:
                    return image_front, 'OpenFoodFacts'
    except Exception as e:
        pass
    
    return '', ''

def main():
    input_file = 'palmers-barcodes-master-list-verified-500.csv'
    output_file = 'palmers-barcodes-verified-with-images.csv'
    
    print("=" * 80)
    print("Adding Product Images to Verified UPCs")
    print("=" * 80)
    print()
    
    # Read the verified results and identify items that need images
    verified_items = []
    all_rows = []
    
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        
        for row in reader:
            all_rows.append(row)
            if len(row) > 3 and row[0] == 'YES':
                upc = row[3]
                verified_items.append(upc)
    
    print(f"Found {len(verified_items)} verified UPCs to fetch images for")
    print()
    
    # Fetch images for verified UPCs
    print("Fetching product images...")
    print("-" * 80)
    
    image_data = {}
    
    for i, upc in enumerate(verified_items, 1):
        percentage = (i / len(verified_items)) * 100
        print(f"[{i}/{len(verified_items)} - {percentage:.0f}%] {upc}...", end=' ')
        
        image_url, source = get_product_image_url(upc)
        
        if image_url:
            print(f"FOUND image ({source})")
            image_data[upc] = image_url
        else:
            print(f"No image available")
            image_data[upc] = ''
        
        time.sleep(0.8)  # Rate limiting
    
    print()
    print("=" * 80)
    print(f"Image fetching complete!")
    print(f"Found images for {len([url for url in image_data.values() if url])} out of {len(verified_items)} products")
    print("=" * 80)
    print()
    
    # Write new CSV with image column
    print(f"Creating output file: {output_file}")
    
    with open(output_file, 'w', encoding='utf-8', newline='') as f_out:
        writer = csv.writer(f_out)
        
        # Write header with new Image URL column
        new_header = ['Verified in DB', 'Database Product Name', 'Source', 'Product Image URL'] + header[3:]
        writer.writerow(new_header)
        
        # Write data rows
        for row in all_rows:
            if len(row) > 3:
                status = row[0]
                upc = row[3]
                
                if status == 'YES' and upc in image_data:
                    # Add image URL for verified items
                    new_row = [row[0], row[1], row[2], image_data[upc]] + row[3:]
                else:
                    # No image for non-verified items
                    new_row = [row[0], row[1], row[2], ''] + row[3:]
                
                writer.writerow(new_row)
    
    print(f"Complete! Output saved to: {output_file}")
    print()
    
    # Show sample of products with images
    products_with_images = [upc for upc, url in image_data.items() if url]
    if products_with_images:
        print("Sample of products with images:")
        print("-" * 80)
        for i, upc in enumerate(products_with_images[:5], 1):
            print(f"{i}. UPC {upc}")
            print(f"   Image: {image_data[upc][:70]}...")
            print()
    
    print()
    print("IMPORTANT NOTE:")
    print("-" * 80)
    print("The CSV now contains image URLs in the 'Product Image URL' column.")
    print()
    print("To VIEW images in Excel/Sheets:")
    print("  1. Open the CSV in Excel or Google Sheets")
    print("  2. For Excel: Use =IMAGE(D2) formula in a new column")
    print("  3. For Google Sheets: Use =IMAGE(D2) formula in a new column")
    print()
    print("Alternatively, I can create an HTML report with embedded images.")

if __name__ == '__main__':
    main()

