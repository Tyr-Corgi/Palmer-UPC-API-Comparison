import csv
from collections import defaultdict

def analyze_upc_patterns():
    """Analyze patterns in verified vs not found UPCs"""
    
    input_file = 'palmers-barcodes-master-list-verified-500.csv'
    
    verified_upcs = []
    not_found_upcs = []
    
    print("=" * 80)
    print("UPC PATTERN ANALYSIS - Verified vs Not Found")
    print("=" * 80)
    print()
    
    # Read the verified results
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        
        for row in reader:
            if len(row) > 3:
                status = row[0]
                db_product = row[1]
                source = row[2]
                upc = row[3]
                dept = row[4] if len(row) > 4 else ''
                item_name = row[5] if len(row) > 5 else ''
                
                if status == 'YES':
                    verified_upcs.append({
                        'upc': upc,
                        'dept': dept,
                        'item_name': item_name,
                        'db_product': db_product,
                        'source': source
                    })
                elif status == 'NO' and source == 'Not found':
                    not_found_upcs.append({
                        'upc': upc,
                        'dept': dept,
                        'item_name': item_name
                    })
    
    print(f"Verified UPCs: {len(verified_upcs)}")
    print(f"Not Found UPCs: {len(not_found_upcs)}")
    print()
    
    # Pattern 1: UPC Prefix Analysis (first 6 digits = manufacturer)
    print("=" * 80)
    print("PATTERN 1: UPC PREFIXES (First 6 digits = Manufacturer Code)")
    print("=" * 80)
    print()
    
    verified_prefixes = defaultdict(list)
    not_found_prefixes = defaultdict(list)
    
    for item in verified_upcs:
        prefix = item['upc'][:6] if len(item['upc']) >= 6 else item['upc']
        verified_prefixes[prefix].append(item)
    
    for item in not_found_upcs[:100]:  # Sample first 100
        prefix = item['upc'][:6] if len(item['upc']) >= 6 else item['upc']
        not_found_prefixes[prefix].append(item)
    
    print("VERIFIED UPC Prefixes (Manufacturers):")
    print("-" * 80)
    for prefix, items in sorted(verified_prefixes.items(), key=lambda x: -len(x[1])):
        print(f"  {prefix}xxx: {len(items)} products - {items[0]['db_product'][:50]}")
    
    print()
    print("NOT FOUND UPC Prefixes (Top 10 most common):")
    print("-" * 80)
    for prefix, items in sorted(not_found_prefixes.items(), key=lambda x: -len(x[1]))[:10]:
        print(f"  {prefix}xxx: {len(items)} products - {items[0]['item_name'][:50]}")
    
    # Pattern 2: Department Analysis
    print()
    print("=" * 80)
    print("PATTERN 2: DEPARTMENT DISTRIBUTION")
    print("=" * 80)
    print()
    
    verified_depts = defaultdict(int)
    not_found_depts = defaultdict(int)
    
    for item in verified_upcs:
        verified_depts[item['dept']] += 1
    
    for item in not_found_upcs:
        not_found_depts[item['dept']] += 1
    
    print("VERIFIED by Department:")
    print("-" * 80)
    for dept, count in sorted(verified_depts.items(), key=lambda x: -x[1]):
        print(f"  {dept}: {count} products")
    
    print()
    print("NOT FOUND by Department (Top 10):")
    print("-" * 80)
    for dept, count in sorted(not_found_depts.items(), key=lambda x: -x[1])[:10]:
        total = verified_depts.get(dept, 0) + count
        print(f"  {dept}: {count} not found (out of {total} total)")
    
    # Pattern 3: UPC Range Analysis
    print()
    print("=" * 80)
    print("PATTERN 3: UPC NUMBER RANGES")
    print("=" * 80)
    print()
    
    verified_ranges = defaultdict(int)
    not_found_ranges = defaultdict(int)
    
    for item in verified_upcs:
        if item['upc'].isdigit():
            range_key = int(item['upc'][:2])  # First 2 digits
            verified_ranges[range_key] += 1
    
    for item in not_found_upcs:
        if item['upc'].isdigit():
            range_key = int(item['upc'][:2])
            not_found_ranges[range_key] += 1
    
    print("VERIFIED UPCs by Starting Digits:")
    print("-" * 80)
    for range_key, count in sorted(verified_ranges.items()):
        print(f"  {range_key}xxxxxxxxxx: {count} products")
    
    print()
    print("NOT FOUND UPCs by Starting Digits (Top 15):")
    print("-" * 80)
    for range_key, count in sorted(not_found_ranges.items(), key=lambda x: -x[1])[:15]:
        print(f"  {range_key}xxxxxxxxxx: {count} products")
    
    # Pattern 4: Source Analysis for Verified
    print()
    print("=" * 80)
    print("PATTERN 4: DATA SOURCE BREAKDOWN (Verified UPCs)")
    print("=" * 80)
    print()
    
    sources = defaultdict(int)
    for item in verified_upcs:
        sources[item['source']] += 1
    
    for source, count in sorted(sources.items(), key=lambda x: -x[1]):
        print(f"  {source}: {count} products ({count/len(verified_upcs)*100:.1f}%)")
    
    # Pattern 5: Specific Examples
    print()
    print("=" * 80)
    print("PATTERN 5: EXAMPLES FOR COMPARISON")
    print("=" * 80)
    print()
    
    print("VERIFIED Examples:")
    print("-" * 80)
    for i, item in enumerate(verified_upcs[:10], 1):
        print(f"{i}. UPC: {item['upc']}")
        print(f"   Item: {item['item_name'][:60]}")
        print(f"   Database: {item['db_product'][:60]}")
        print()
    
    print("NOT FOUND Examples:")
    print("-" * 80)
    for i, item in enumerate(not_found_upcs[:10], 1):
        print(f"{i}. UPC: {item['upc']}")
        print(f"   Item: {item['item_name'][:60]}")
        print()
    
    # Pattern 6: Key Insights
    print()
    print("=" * 80)
    print("KEY INSIGHTS & PATTERNS")
    print("=" * 80)
    print()
    
    # Find prefixes unique to verified
    verified_only_prefixes = set(verified_prefixes.keys()) - set(not_found_prefixes.keys())
    common_prefixes = set(verified_prefixes.keys()) & set(not_found_prefixes.keys())
    
    print("1. MANUFACTURER PATTERNS:")
    print(f"   - {len(verified_prefixes)} unique manufacturer codes in VERIFIED")
    print(f"   - {len(not_found_prefixes)} unique manufacturer codes in NOT FOUND (sample)")
    if verified_only_prefixes:
        print(f"   - {len(verified_only_prefixes)} manufacturer codes ONLY found in verified set")
    
    print()
    print("2. COMMON VERIFIED MANUFACTURER CODES:")
    print("   (These manufacturers have high success rates)")
    for prefix in list(verified_only_prefixes)[:10]:
        if prefix in verified_prefixes:
            items = verified_prefixes[prefix]
            print(f"   - {prefix}: {items[0]['db_product'][:50]}")
    
    print()
    print("3. RECOMMENDATION:")
    print("   Based on patterns, UPCs from these manufacturers are more likely to verify:")
    top_verified = sorted(verified_prefixes.items(), key=lambda x: -len(x[1]))[:5]
    for prefix, items in top_verified:
        print(f"   - {prefix}xxx ({len(items)} verified)")

if __name__ == '__main__':
    analyze_upc_patterns()

