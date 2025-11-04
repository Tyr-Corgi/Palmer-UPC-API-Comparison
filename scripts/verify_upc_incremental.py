import csv
import time
import urllib.request
import urllib.error
import json
import sys
import os
from datetime import datetime

def lookup_upc_free(upc_code):
    """
    Lookup UPC using multiple free APIs with fallbacks
    Returns: (found: bool, product_name: str, source: str)
    """
    
    # Method 1: Try OpenFoodFacts (more lenient rate limits)
    try:
        url = f"https://world.openfoodfacts.org/api/v0/product/{upc_code}.json"
        headers = {
            'User-Agent': 'PalmersUPCScanner/1.0 (Non-commercial research)'
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
    except urllib.error.HTTPError as e:
        if e.code == 429:
            return None, 'Rate limit reached', 'OpenFoodFacts'
    except Exception as e:
        pass
    
    # Method 2: Try UPCitemdb (stricter rate limits, use as fallback)
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
    
    return False, '', 'Not found'

def load_progress(progress_file):
    """Load previously verified UPCs from progress file"""
    verified_upcs = {}
    if os.path.exists(progress_file):
        try:
            with open(progress_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    upc = row['UPC']
                    found = row['Found'] == 'True'
                    product_name = row['Product Name']
                    source = row['Source']
                    verified_upcs[upc] = (found, product_name, source)
        except Exception as e:
            print(f"Warning: Could not load progress file: {e}")
    return verified_upcs

def save_progress(progress_file, verification_results):
    """Save verification results incrementally"""
    with open(progress_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['UPC', 'Found', 'Product Name', 'Source'])
        for upc, (found, product_name, source) in verification_results.items():
            writer.writerow([upc, found, product_name, source])

def main():
    input_file = 'palmers-barcodes-master-list-with-upc-check.csv'
    output_file = 'palmers-barcodes-master-list-verified.csv'
    progress_file = 'verification_progress.csv'
    
    print("=" * 70)
    print("UPC Database Verification Tool (with Incremental Save)")
    print("=" * 70)
    print()
    
    # Load existing progress
    print("Checking for previous progress...")
    verification_results = load_progress(progress_file)
    if verification_results:
        print(f"Found {len(verification_results)} previously verified UPCs")
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
                        # Skip if already verified
                        if upc_code not in verification_results:
                            upc_rows.append((i, upc_code, row))
        
        total_valid_upcs = len([r for r in all_rows if r[0] == 'YES'])
        already_done = len(verification_results)
        remaining = len(upc_rows)
        
        print(f"Total items: {len(all_rows)}")
        print(f"Total valid UPC codes: {total_valid_upcs}")
        print(f"Already verified: {already_done}")
        print(f"Remaining to verify: {remaining}")
        print()
        
        if remaining == 0:
            print("All UPCs already verified! Creating final output file...")
        else:
            # Ask user for verification approach
            print("Verification Options:")
            print(f"  1. Quick test (first 10 remaining UPCs)")
            print(f"  2. Sample verification (100 random UPCs)")
            print(f"  3. Small batch (500 UPCs - recommended)")
            print(f"  4. Full verification (all {remaining} remaining UPCs)")
            print()
            print("NOTE: Free APIs have strict rate limits:")
            print("  - OpenFoodFacts: ~10 requests/minute (conservative)")
            print("  - UPCitemdb trial: ~100 requests/day")
            print("  - Script uses 7-second delays to respect limits")
            print()
            
            choice = input("Enter your choice (1/2/3/4): ").strip()
            
            if choice == '1':
                upc_rows = upc_rows[:10]
                print(f"\nVerifying first {len(upc_rows)} UPCs...")
            elif choice == '2':
                import random
                random.shuffle(upc_rows)
                upc_rows = upc_rows[:100]
                print(f"\nVerifying random sample of {len(upc_rows)} UPCs...")
            elif choice == '3':
                upc_rows = upc_rows[:500]
                estimated_time = (len(upc_rows) * 7) / 60
                print(f"\nVerifying {len(upc_rows)} UPCs...")
                print(f"Estimated time: {estimated_time:.0f} minutes")
            elif choice == '4':
                estimated_time = (len(upc_rows) * 7) / 60
                print(f"\nVerifying all {len(upc_rows)} UPCs...")
                print(f"Estimated time: {estimated_time:.0f} minutes ({estimated_time/60:.1f} hours)")
                confirm = input("Continue? (yes/no): ").strip().lower()
                if confirm != 'yes':
                    print("Cancelled.")
                    return
            else:
                print("Invalid choice. Exiting.")
                return
            
            print()
            print("Starting verification...")
            print("Progress is saved every 10 UPCs - you can safely interrupt and resume")
            print("-" * 70)
            
            # Verify UPCs
            found_count = sum(1 for f, _, _ in verification_results.values() if f)
            not_found_count = len(verification_results) - found_count
            rate_limited_count = 0
            consecutive_rate_limits = 0
            
            for i, (row_num, upc_code, row_data) in enumerate(upc_rows, 1):
                percentage = (i / len(upc_rows)) * 100
                print(f"[{i}/{len(upc_rows)} - {percentage:.1f}%] Checking {upc_code}...", end=' ')
                
                found, product_name, source = lookup_upc_free(upc_code)
                
                if found is None:  # Rate limited
                    print(f"⚠ {product_name} - Backing off...")
                    verification_results[upc_code] = (False, product_name, source)
                    rate_limited_count += 1
                    consecutive_rate_limits += 1
                    
                    # If we hit rate limits multiple times, wait longer
                    if consecutive_rate_limits > 3:
                        wait_time = 30 * consecutive_rate_limits
                        print(f"   Multiple rate limits detected. Waiting {wait_time} seconds...")
                        time.sleep(wait_time)
                    else:
                        time.sleep(15)  # Standard backoff
                        
                elif found:
                    print(f"✓ FOUND: {product_name[:60]}... [{source}]")
                    verification_results[upc_code] = (True, product_name, source)
                    found_count += 1
                    consecutive_rate_limits = 0
                else:
                    print(f"✗ Not in database")
                    verification_results[upc_code] = (False, '', 'Not found')
                    not_found_count += 1
                    consecutive_rate_limits = 0
                
                # Respect API rate limits - use 7 second delay
                # This gives us ~8.5 requests/minute (under the 10/min limit)
                time.sleep(7)
                
                # Save progress every 10 items
                if i % 10 == 0:
                    save_progress(progress_file, verification_results)
                    print(f"\n  Progress saved! {found_count} found, {not_found_count} not found, {rate_limited_count} rate limited")
                    print("-" * 70)
            
            # Final save
            save_progress(progress_file, verification_results)
            
            print()
            print("=" * 70)
            print("Verification Complete!")
            print("=" * 70)
            print(f"Total verified: {len(verification_results)}")
            print(f"Found in database: {found_count}")
            print(f"Not found: {not_found_count}")
            print(f"Rate limited: {rate_limited_count}")
            if found_count + not_found_count > 0:
                print(f"Success rate: {(found_count/(found_count + not_found_count)*100):.1f}%")
            print()
        
        # Write results to final CSV
        print(f"Creating final output file: {output_file}")
        
        with open(input_file, 'r', encoding='utf-8') as f_in:
            with open(output_file, 'w', encoding='utf-8', newline='') as f_out:
                reader = csv.reader(f_in)
                writer = csv.writer(f_out)
                
                # Write header with new columns
                header = next(reader)
                new_header = ['Verified in DB', 'Database Product Name', 'Data Source'] + header[1:]
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
                            # Valid UPC format but not verified yet
                            new_row = ['NOT CHECKED', '', ''] + row[1:]
                        else:
                            # Not a valid UPC format
                            new_row = ['NO', 'Invalid UPC format', ''] + row[1:]
                        
                        writer.writerow(new_row)
        
        print(f"✓ Output saved to: {output_file}")
        print()
        
        # Show some examples of found products
        found_products = [(upc, name, src) for upc, (f, name, src) in verification_results.items() if f]
        if found_products:
            print(f"\nSample of verified products (showing up to 10):")
            for i, (upc, name, source) in enumerate(found_products[:10], 1):
                print(f"  {i}. UPC {upc}: {name} [{source}]")
        
        print()
        print(f"Progress file saved at: {progress_file}")
        print("You can resume verification later if interrupted.")
        
    except FileNotFoundError:
        print(f"Error: Could not find file '{input_file}'")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nInterrupted by user!")
        print(f"Progress has been saved to: {progress_file}")
        print("Run this script again to resume from where you left off.")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()

