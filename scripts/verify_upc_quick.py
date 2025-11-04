import csv
import time
import urllib.request
import urllib.error
import json
import sys

def lookup_upc_free(upc_code):
    """
    Lookup UPC using multiple free APIs with fallbacks
    Returns: (found: bool, product_name: str, source: str)
    """
    
    # Method 1: Try UPCitemdb (free trial, no API key needed for basic lookups)
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
                title = item.get('title', 'Product found')
                brand = item.get('brand', '')
                full_name = f"{brand} {title}" if brand else title
                return True, full_name.strip(), 'UPCitemdb'
    except urllib.error.HTTPError as e:
        if e.code == 429:  # Rate limit
            return None, 'Rate limit reached', 'UPCitemdb'
    except Exception as e:
        pass
    
    # Method 2: Try OpenFoodFacts (free, no API key)
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
                name = product.get('product_name', '')
                brand = product.get('brands', '')
                if name:
                    full_name = f"{brand} {name}" if brand else name
                    return True, full_name.strip(), 'OpenFoodFacts'
    except Exception as e:
        pass
    
    return False, '', 'Not found'

def main():
    input_file = 'palmers-barcodes-master-list-with-upc-check.csv'
    output_file = 'palmers-barcodes-master-list-verified-sample.csv'
    
    # Quick test mode - first 50 UPCs
    NUM_TO_TEST = 50
    
    print("=" * 70)
    print("UPC Database Verification Tool - Quick Test Mode")
    print("=" * 70)
    print(f"Testing first {NUM_TO_TEST} valid UPC codes")
    print()
    
    # Read all rows and identify UPCs to verify
    print("Reading input file...")
    upc_rows = []
    all_rows = []
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            
            for i, row in enumerate(reader, 1):
                if row and len(row) > 1:
                    all_rows.append(row)
                    # Check if this row has "YES" in the Valid UPC Format column
                    if row[0] == 'YES':
                        upc_code = row[1]  # Item ID column
                        upc_rows.append((i, upc_code, row))
        
        print(f"Total items: {len(all_rows)}")
        print(f"Valid UPC codes found: {len(upc_rows)}")
        print(f"Testing first: {min(NUM_TO_TEST, len(upc_rows))}")
        print()
        
        # Test only first N UPCs
        upc_rows = upc_rows[:NUM_TO_TEST]
        
        print("Starting verification...")
        print("-" * 70)
        
        # Verify UPCs
        verification_results = {}
        found_count = 0
        not_found_count = 0
        rate_limited = False
        
        for i, (row_num, upc_code, row_data) in enumerate(upc_rows, 1):
            percentage = (i / len(upc_rows)) * 100
            print(f"[{i}/{len(upc_rows)} - {percentage:.0f}%] {upc_code}...", end=' ')
            
            found, product_name, source = lookup_upc_free(upc_code)
            
            if found is None:  # Rate limited
                print(f"RATE LIMITED: {product_name}")
                rate_limited = True
                verification_results[upc_code] = (False, '', 'Rate limited')
                not_found_count += 1
                time.sleep(5)
            elif found:
                print(f"FOUND: {product_name[:50]}")
                verification_results[upc_code] = (True, product_name, source)
                found_count += 1
            else:
                print(f"NOT FOUND")
                verification_results[upc_code] = (False, '', 'Not found')
                not_found_count += 1
            
            # Rate limiting - be respectful to free APIs
            time.sleep(1.2)
        
        print()
        print("=" * 70)
        print("Verification Complete!")
        print("=" * 70)
        print(f"Total verified: {len(verification_results)}")
        print(f"Found in database: {found_count} ({found_count/len(verification_results)*100:.1f}%)")
        print(f"Not found: {not_found_count} ({not_found_count/len(verification_results)*100:.1f}%)")
        print()
        
        # Write results to new CSV
        print(f"Creating output file: {output_file}")
        
        with open(input_file, 'r', encoding='utf-8') as f_in:
            with open(output_file, 'w', encoding='utf-8', newline='') as f_out:
                reader = csv.reader(f_in)
                writer = csv.writer(f_out)
                
                # Write header with new columns
                header = next(reader)
                new_header = ['Verified in DB', 'Database Product Name', 'Source'] + header[1:]
                writer.writerow(new_header)
                
                # Write data rows
                for row in reader:
                    if row and len(row) > 1:
                        upc_code = row[1]  # Item ID
                        
                        if upc_code in verification_results:
                            found, product_name, source = verification_results[upc_code]
                            verified = 'YES' if found else 'NO'
                            new_row = [verified, product_name, source] + row[1:]
                        elif row[0] == 'YES':
                            # Valid UPC format but not verified in this quick test
                            new_row = ['NOT TESTED', '', ''] + row[1:]
                        else:
                            # Not a valid UPC format
                            new_row = ['NO', 'Invalid UPC format', ''] + row[1:]
                        
                        writer.writerow(new_row)
        
        print(f"Complete! Output saved to: {output_file}")
        print()
        
        if rate_limited:
            print("WARNING: Some requests were rate-limited.")
        
        # Show verified products
        if found_count > 0:
            print(f"\nSuccessfully verified {found_count} products:")
            print("-" * 70)
            for upc, (found, name, source) in verification_results.items():
                if found:
                    print(f"  {upc}: {name}")
        
        print()
        print("Next Steps:")
        print("  - Review the sample results in the output file")
        print("  - If results look good, you can run full verification on all 9,394 UPCs")
        print("  - Full verification will take ~2-3 hours due to API rate limits")
        
    except FileNotFoundError:
        print(f"Error: Could not find file '{input_file}'")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()

