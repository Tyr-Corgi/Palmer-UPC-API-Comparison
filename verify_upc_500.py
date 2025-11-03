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
    output_file = 'palmers-barcodes-master-list-verified-500.csv'
    
    # Test 500 UPCs
    NUM_TO_TEST = 500
    
    print("=" * 70)
    print("UPC Database Verification Tool - 500 Sample Test")
    print("=" * 70)
    print(f"Testing {NUM_TO_TEST} valid UPC codes")
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
        print(f"Testing: {min(NUM_TO_TEST, len(upc_rows))}")
        print()
        
        # Test first N UPCs
        upc_rows = upc_rows[:NUM_TO_TEST]
        
        print("Starting verification...")
        print(f"Estimated time: ~{int(NUM_TO_TEST * 0.8 / 60)} minutes")
        print("-" * 70)
        
        start_time = time.time()
        
        # Verify UPCs
        verification_results = {}
        found_count = 0
        not_found_count = 0
        rate_limited_count = 0
        
        for i, (row_num, upc_code, row_data) in enumerate(upc_rows, 1):
            percentage = (i / len(upc_rows)) * 100
            elapsed = time.time() - start_time
            avg_time_per_upc = elapsed / i if i > 0 else 0
            remaining_time = avg_time_per_upc * (len(upc_rows) - i)
            
            print(f"[{i}/{len(upc_rows)} - {percentage:.1f}%] {upc_code}... ", end='')
            print(f"(~{int(remaining_time/60)}m {int(remaining_time%60)}s left) ", end='')
            
            found, product_name, source = lookup_upc_free(upc_code)
            
            if found is None:  # Rate limited
                print(f"RATE LIMITED")
                rate_limited_count += 1
                verification_results[upc_code] = (False, 'Rate limited', 'Rate limited')
                not_found_count += 1
                time.sleep(5)  # Wait longer if rate limited
            elif found:
                print(f"FOUND: {product_name[:40]}")
                verification_results[upc_code] = (True, product_name, source)
                found_count += 1
            else:
                print(f"NOT FOUND")
                verification_results[upc_code] = (False, '', 'Not found')
                not_found_count += 1
            
            # Adaptive rate limiting - start at 0.8 seconds
            time.sleep(0.8)
            
            # Progress summary every 100 items
            if i % 100 == 0:
                print(f"\n--- Progress Update ---")
                print(f"  Found: {found_count}, Not found: {not_found_count}, Rate limited: {rate_limited_count}")
                print(f"  Success rate: {(found_count/i*100):.1f}%")
                print(f"  Avg time per UPC: {avg_time_per_upc:.2f}s")
                print("-" * 70)
        
        total_time = time.time() - start_time
        
        print()
        print("=" * 70)
        print("Verification Complete!")
        print("=" * 70)
        print(f"Total time: {int(total_time/60)}m {int(total_time%60)}s")
        print(f"Total verified: {len(verification_results)}")
        print(f"Found in database: {found_count} ({found_count/len(verification_results)*100:.1f}%)")
        print(f"Not found: {not_found_count} ({not_found_count/len(verification_results)*100:.1f}%)")
        print(f"Rate limited: {rate_limited_count}")
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
                            # Valid UPC format but not verified in this test
                            new_row = ['NOT TESTED', '', ''] + row[1:]
                        else:
                            # Not a valid UPC format
                            new_row = ['NO', 'Invalid UPC format', ''] + row[1:]
                        
                        writer.writerow(new_row)
        
        print(f"Complete! Output saved to: {output_file}")
        print()
        
        if rate_limited_count > 0:
            print(f"WARNING: {rate_limited_count} requests were rate-limited.")
            print("Consider increasing delay for full run.")
        
        # Show sample of verified products
        if found_count > 0:
            print(f"\nSample of verified products (showing first 10):")
            print("-" * 70)
            sample_count = 0
            for upc, (found, name, source) in verification_results.items():
                if found and sample_count < 10:
                    print(f"  {upc}: {name[:60]}")
                    sample_count += 1
        
        print()
        print("Performance Analysis:")
        print("-" * 70)
        print(f"Average time per UPC: {total_time/len(verification_results):.2f}s")
        if rate_limited_count == 0:
            print("No rate limiting detected - can potentially run faster!")
            full_estimate = (9394 * (total_time/len(verification_results))) / 60
            print(f"Estimated time for all 9,394 UPCs: ~{int(full_estimate)} minutes")
        else:
            print(f"Rate limiting detected - need to maintain current speed or slower")
        
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

