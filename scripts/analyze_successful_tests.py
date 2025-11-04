import csv

def analyze_test_file(filename, test_name):
    """Analyze a successful test file"""
    
    verified_yes = 0
    not_found = 0
    invalid_format = 0
    rate_limited = 0
    verified_products = []
    sources = {'UPCitemdb': 0, 'OpenFoodFacts': 0, 'Not found': 0}
    
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            verified = row.get('Verified in DB', row.get('Verified in Database', ''))
            product_name = row.get('Database Product Name', '')
            source = row.get('Data Source', row.get('Source', ''))
            
            if verified == 'YES':
                verified_yes += 1
                verified_products.append({
                    'upc': row.get('﻿Item ID', row.get('Item ID', '')),
                    'name': product_name,
                    'source': source,
                    'item_name': row.get('Item Name', '')
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
    print(f"{test_name}")
    print("=" * 70)
    print()
    print(f"Total items processed: {total:,}")
    print(f"  - Invalid UPC format: {invalid_format:,}")
    print(f"  - Valid UPCs checked: {valid_upcs_checked:,}")
    print()
    print(f"Valid UPC Results:")
    print(f"  + Verified in database: {verified_yes:,}")
    print(f"  - Not found in database: {not_found:,}")
    print(f"  ! Rate limited: {rate_limited:,}")
    print()
    
    if valid_upcs_checked > 0:
        success_rate = (verified_yes / valid_upcs_checked) * 100
        print(f"Success rate: {success_rate:.1f}%")
        print()
        
        if verified_yes > 0:
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
    print()
    return verified_yes, not_found, rate_limited, verified_products

if __name__ == '__main__':
    print("\n")
    
    # Analyze the sample test
    v1, nf1, rl1, products1 = analyze_test_file(
        'palmers-barcodes-master-list-verified-sample.csv',
        'SAMPLE TEST RESULTS'
    )
    
    # Analyze the 500 test
    v2, nf2, rl2, products2 = analyze_test_file(
        'palmers-barcodes-master-list-verified-500.csv',
        '500 UPC TEST RESULTS'
    )
    
    print("=" * 70)
    print("COMPARISON SUMMARY")
    print("=" * 70)
    print()
    print(f"Sample Test:")
    print(f"  Verified: {v1}, Not Found: {nf1}, Rate Limited: {rl1}")
    print()
    print(f"500 UPC Test:")
    print(f"  Verified: {v2}, Not Found: {nf2}, Rate Limited: {rl2}")
    print()
    print(f"Total Successful Verifications: {v1 + v2}")
    print("=" * 70)

