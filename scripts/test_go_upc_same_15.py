"""
Test Go-UPC API with the same 15 EAN codes used in the main comparison
"""

import urllib.request
import urllib.error
import json
import time

# Go-UPC API Key
GO_UPC_API_KEY = "c74e46d117cd569c11ae68c88bae8f00c11f66b9ca5f662dd397550a4ea5d7ce"

# The exact 15 EAN/UPC codes from our API comparison
test_products = [
    {"upc": "711381332580", "ean": "0711381332580", "name": "Stonewall Kitchen Maple Brown Butter Waffle Cookie", "size": "1.1 OZ"},
    {"upc": "849455000032", "ean": "0849455000032", "name": "Tumaro's Multi Grain Wraps", "size": "11.2 OZ"},
    {"upc": "858183005059", "ean": "0858183005059", "name": "Lillie's Q Ivory Barbeque", "size": "16 OZ"},
    {"upc": "820581153908", "ean": "0820581153908", "name": "Bella Maria Spanish Mix", "size": "3.5 OZ"},
    {"upc": "819046000420", "ean": "0819046000420", "name": "Inka Giant Corn Chile Picante", "size": "4.0 Ounce"},
    {"upc": "818617022571", "ean": "0818617022571", "name": "Suja Immunity Rebound Shot", "size": "2 Fl Oz"},
    {"upc": "186011000182", "ean": "0186011000182", "name": "S&C D FZD DNR PAT LMB 14OZ", "size": "14 Oz"},
    {"upc": "312547171670", "ean": "0312547171670", "name": "Benadryl Extra Strength Itch Stopping Cream", "size": "1 Oz"},
    {"upc": "852466006016", "ean": "0852466006016", "name": "Simply Gum Natural Mint Gum", "size": ""},
    {"upc": "824150401162", "ean": "0824150401162", "name": "POM Wonderful Pomegranate Juice", "size": "16 Ounce"},
    {"upc": "753656710990", "ean": "0753656710990", "name": "Think Thin Chunky Chocolate Pe", "size": ""},
    {"upc": "742676400592", "ean": "0742676400592", "name": "Trot Dancing Leaves Green Tea", "size": ""},
    {"upc": "810089955197", "ean": "0810089955197", "name": "Collagen Creamer,original", "size": ""},
    {"upc": "818290019592", "ean": "0818290019592", "name": "Chobani Coffee Greek Yogurt", "size": ""},
    {"upc": "850017604032", "ean": "0850017604032", "name": "Drumroll Chocolate Glazed Donuts", "size": ""}
]

def test_go_upc_api(upc):
    """Test Go-UPC API with a single UPC"""
    url = f"https://go-upc.com/api/v1/code/{upc}"
    
    try:
        req = urllib.request.Request(url)
        req.add_header('Authorization', f'Bearer {GO_UPC_API_KEY}')
        
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            
            return {
                'success': True,
                'data': data
            }
    
    except urllib.error.HTTPError as e:
        error_body = e.read().decode() if e.fp else ""
        return {
            'success': False,
            'error': f'HTTP {e.code}: {e.reason}',
            'details': error_body
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def main():
    """Run Go-UPC API tests on the same 15 products"""
    print("=" * 80)
    print("GO-UPC API TEST - SAME 15 PRODUCTS AS MAIN COMPARISON")
    print("=" * 80)
    print()
    print(f"API Key: {GO_UPC_API_KEY[:20]}...")
    print(f"Testing: 15 products")
    print(f"Remaining calls after test: ~{150 - 15} calls")
    print()
    
    results = []
    
    for i, product in enumerate(test_products, 1):
        print(f"\n{'=' * 80}")
        print(f"PRODUCT {i}/15: {product['name']}")
        print(f"UPC: {product['upc']} | EAN: {product['ean']}")
        if product['size']:
            print(f"Size: {product['size']}")
        print(f"{'=' * 80}")
        
        # Test with UPC
        print("\n  Testing with UPC...")
        result = test_go_upc_api(product['upc'])
        
        if result['success']:
            data = result['data']
            product_info = data.get('product', {})
            
            print(f"    Status: Success")
            print(f"    Product Name: {product_info.get('name', 'N/A')}")
            print(f"    Brand: {product_info.get('brand', 'N/A')}")
            print(f"    Category: {product_info.get('category', 'N/A')}")
            
            images = product_info.get('images', [])
            print(f"    Images: {len(images)} available")
            if images:
                print(f"    First Image: {images[0]}")
            
            results.append({
                'upc': product['upc'],
                'ean': product['ean'],
                'expected_name': product['name'],
                'expected_size': product['size'],
                'api_name': product_info.get('name', ''),
                'brand': product_info.get('brand', ''),
                'category': product_info.get('category', ''),
                'description': product_info.get('description', ''),
                'images': images,
                'image_count': len(images),
                'success': True
            })
        else:
            print(f"    Status: Failed")
            print(f"    Error: {result['error']}")
            if 'details' in result:
                print(f"    Details: {result['details']}")
            
            results.append({
                'upc': product['upc'],
                'ean': product['ean'],
                'expected_name': product['name'],
                'expected_size': product['size'],
                'error': result['error'],
                'success': False
            })
        
        # Small delay to avoid rate limiting
        if i < len(test_products):
            time.sleep(0.5)
    
    # Save results
    output_file = '../json-data/go_upc_15_products_test.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n{'=' * 80}")
    print("TEST SUMMARY")
    print(f"{'=' * 80}")
    
    successful = sum(1 for r in results if r['success'])
    failed = len(results) - successful
    
    total_images = sum(r.get('image_count', 0) for r in results if r['success'])
    products_with_images = sum(1 for r in results if r['success'] and r.get('image_count', 0) > 0)
    
    print(f"  Total Tests: {len(results)}")
    print(f"  Successful: {successful} ({successful/len(results)*100:.1f}%)")
    print(f"  Failed: {failed}")
    print(f"  Products with Images: {products_with_images}/{successful}")
    print(f"  Total Images: {total_images}")
    print(f"\n  Results saved to: {output_file}")
    print()
    
    # Show which products failed (if any)
    if failed > 0:
        print(f"{'=' * 80}")
        print("FAILED PRODUCTS:")
        print(f"{'=' * 80}")
        for r in results:
            if not r['success']:
                print(f"  - {r['expected_name']} (UPC: {r['upc']})")
                print(f"    Error: {r['error']}")

if __name__ == "__main__":
    main()

