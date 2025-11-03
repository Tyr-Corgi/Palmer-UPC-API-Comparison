import csv

def analyze_verification_results(filename):
    """Analyze the verification results and display statistics"""
    
    verified_yes = 0
    not_found = 0
    invalid_format = 0
    rate_limited = 0
    verified_products = []
    sources = {'UPCitemdb': 0, 'OpenFoodFacts': 0}
    
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            verified = row['Verified in DB']
            product_name = row['Database Product Name']
            source = row['Source']
            
            if verified == 'YES':
                verified_yes += 1
                verified_products.append({
                    'upc': row['﻿Item ID'],
                    'name': product_name,
                    'source': source,
                    'item_name': row['Item Name']
                })
                if source in sources:
                    sources[source] += 1
            elif product_name == 'Invalid UPC format':
                invalid_format += 1
            elif 'Rate limit' in product_name or 'Rate limit' in source:
                rate_limited += 1
            else:
                not_found += 1
    
    total = verified_yes + not_found + invalid_format + rate_limited
    valid_upcs_checked = verified_yes + not_found + rate_limited
    
    print("=" * 70)
    print("UPC VERIFICATION RESULTS")
    print("=" * 70)
    print()
    print(f"Total items processed: {total:,}")
    print(f"  - Invalid UPC format: {invalid_format:,}")
    print(f"  - Valid UPC format checked: {valid_upcs_checked:,}")
    print()
    print(f"Valid UPC Results:")
    print(f"  + Verified in database: {verified_yes:,}")
    print(f"  - Not found in database: {not_found:,}")
    print(f"  ! Rate limited: {rate_limited:,}")
    print()
    
    if verified_yes > 0:
        success_rate = (verified_yes / valid_upcs_checked) * 100
        print(f"Success rate: {success_rate:.1f}%")
        print()
        
        print("Data Sources:")
        for source, count in sources.items():
            if count > 0:
                print(f"  • {source}: {count:,} products")
        print()
        
        print(f"Sample of verified products (showing first 10):")
        print("-" * 70)
        for i, product in enumerate(verified_products[:10], 1):
            print(f"{i}. UPC: {product['upc']}")
            print(f"   Store Item: {product['item_name']}")
            print(f"   Database Name: {product['name']}")
            print(f"   Source: {product['source']}")
            print()
    
    print("=" * 70)

if __name__ == '__main__':
    analyze_verification_results('palmers-barcodes-FULL-VERIFICATION.csv')

