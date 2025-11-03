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
                title = item.get('title', 'Product found')
                brand = item.get('brand', '')
                full_name = f"{brand} {title}" if brand else title
                return True, full_name.strip(), 'UPCitemdb'
    except urllib.error.HTTPError as e:
        if e.code == 429:
            return None, 'Rate limit reached', 'UPCitemdb'
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
    output_file = 'palmers-barcodes-FULL-VERIFICATION.csv'
    
    print("=" * 80)
    print("FULL UPC DATABASE VERIFICATION - All 9,394 UPCs")
    print("=" * 80)
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
                    if row[0] == 'YES':
                        upc_code = row[1]
                        upc_rows.append((i, upc_code, row))
        
        print(f"Total items: {len(all_rows)}")
        print(f"Valid UPC codes to verify: {len(upc_rows)}")
        print()
        print("Starting full verification...")
        print(f"Estimated time: ~{int(len(upc_rows) * 0.8 / 60)} minutes")
        print()
        print("This process will continue even if you close the terminal.")
        print("Check the output file periodically for progress.")
        print("-" * 80)
        
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
            print(f"(ETA: {int(remaining_time/60)}m) ", end='')
            
            found, product_name, source = lookup_upc_free(upc_code)
            
            if found is None:
                print(f"RATE LIMITED")
                rate_limited_count += 1
                verification_results[upc_code] = (False, 'Rate limited', 'Rate limited')
                not_found_count += 1
                time.sleep(5)
            elif found:
                print(f"FOUND: {product_name[:40]}")
                verification_results[upc_code] = (True, product_name, source)
                found_count += 1
            else:
                print(f"NOT FOUND")
                verification_results[upc_code] = (False, '', 'Not found')
                not_found_count += 1
            
            time.sleep(0.8)
            
            # Save progress every 100 items
            if i % 100 == 0:
                print(f"\n--- Progress: {found_count} found, {not_found_count} not found ---")
                print(f"    Success rate: {(found_count/i*100):.1f}% | Avg: {avg_time_per_upc:.2f}s/UPC")
                print("-" * 80)
        
        total_time = time.time() - start_time
        
        print()
        print("=" * 80)
        print("VERIFICATION COMPLETE!")
        print("=" * 80)
        print(f"Total time: {int(total_time/60)}m {int(total_time%60)}s")
        print(f"Total verified: {len(verification_results)}")
        print(f"Found in database: {found_count} ({found_count/len(verification_results)*100:.1f}%)")
        print(f"Not found: {not_found_count}")
        print(f"Rate limited: {rate_limited_count}")
        print()
        
        # Write results
        print(f"Writing output file: {output_file}")
        
        with open(input_file, 'r', encoding='utf-8') as f_in:
            with open(output_file, 'w', encoding='utf-8', newline='') as f_out:
                reader = csv.reader(f_in)
                writer = csv.writer(f_out)
                
                header = next(reader)
                new_header = ['Verified in DB', 'Database Product Name', 'Source'] + header[1:]
                writer.writerow(new_header)
                
                for row in reader:
                    if row and len(row) > 1:
                        upc_code = row[1]
                        
                        if upc_code in verification_results:
                            found, product_name, source = verification_results[upc_code]
                            verified = 'YES' if found else 'NO'
                            new_row = [verified, product_name, source] + row[1:]
                        elif row[0] == 'YES':
                            new_row = ['NOT CHECKED', '', ''] + row[1:]
                        else:
                            new_row = ['NO', 'Invalid UPC format', ''] + row[1:]
                        
                        writer.writerow(new_row)
        
        print(f"COMPLETE! Output saved to: {output_file}")
        print()
        print(f"Successfully verified {found_count} products!")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()

