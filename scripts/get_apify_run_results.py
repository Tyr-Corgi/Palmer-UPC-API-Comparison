import urllib.request
import json
import time
import sys

APIFY_TOKEN = "YOUR_APIFY_API_TOKEN_HERE"  # Replace with your actual token

# Get run ID from command line or from saved file
if len(sys.argv) > 1:
    run_id = sys.argv[1]
else:
    # Load from saved file
    try:
        with open('apify_latest_run.json', 'r') as f:
            data = json.load(f)
            run_id = data['run_id']
    except:
        print("Error: No run ID provided and no saved run found")
        print("Usage: python get_apify_run_results.py [RUN_ID]")
        sys.exit(1)

print("=" * 80)
print("APIFY RUN RESULTS RETRIEVAL")
print("=" * 80)
print()
print(f"Run ID: {run_id}")
print()
print("Checking run status...")
print()

# Check run status
status_url = f"https://api.apify.com/v2/actor-runs/{run_id}?token={APIFY_TOKEN}"

max_wait = 300  # Wait up to 5 minutes
check_interval = 5  # Check every 5 seconds
elapsed = 0

while elapsed < max_wait:
    try:
        req = urllib.request.Request(status_url)
        with urllib.request.urlopen(req, timeout=15) as response:
            status_data = json.loads(response.read().decode())
            status = status_data['data']['status']
            
            print(f"[{elapsed}s] Status: {status}")
            
            if status == 'SUCCEEDED':
                print()
                print("[OK] Run completed successfully!")
                print()
                
                # Get the dataset items
                dataset_url = f"https://api.apify.com/v2/actor-runs/{run_id}/dataset/items?token={APIFY_TOKEN}"
                
                dataset_req = urllib.request.Request(dataset_url)
                with urllib.request.urlopen(dataset_req, timeout=15) as dataset_response:
                    results = json.loads(dataset_response.read().decode())
                    
                    # Save results
                    with open('apify_retest_results.json', 'w', encoding='utf-8') as f:
                        json.dump(results, f, indent=2)
                    
                    print(f"Retrieved {len(results)} results")
                    print("Results saved to apify_retest_results.json")
                    print()
                    print("=" * 80)
                    print("RESULTS SUMMARY")
                    print("=" * 80)
                    print()
                    
                    if len(results) == 0:
                        print("No products found for any of the 5 EAN codes.")
                        print()
                        print("Tested EAN codes:")
                        print("  - 0818617022571 (SUJA Immunity Shot)")
                        print("  - 0186011000182 (Stella & Chewy's Dog Food)")
                        print("  - 0312547171670 (Benadryl Itch Relief)")
                        print("  - 0852466006016 (Simply Gum Mint)")
                        print("  - 0824150401162 (POM Wonderful Juice)")
                    else:
                        for i, result in enumerate(results, 1):
                            ean = result.get('ean', 'Unknown')
                            title = result.get('title', 'Unknown')
                            images = result.get('images', [])
                            image_url = result.get('image_url', 'N/A')
                            
                            print(f"{i}. EAN: {ean}")
                            print(f"   Title: {title}")
                            if images:
                                print(f"   Images: {len(images)}")
                            elif image_url != 'N/A':
                                print(f"   Image URL: {image_url[:60]}...")
                                print(f"   Size: {result.get('width', 'N/A')}x{result.get('height', 'N/A')}px")
                            print()
                    
                    print("=" * 80)
                    sys.exit(0)
                    
            elif status == 'FAILED':
                print()
                print("[X] Run failed!")
                error_msg = status_data['data'].get('statusMessage', 'Unknown error')
                print(f"Error: {error_msg}")
                print()
                break
                
            elif status in ['RUNNING', 'READY']:
                time.sleep(check_interval)
                elapsed += check_interval
            else:
                print(f"[!] Unexpected status: {status}")
                time.sleep(check_interval)
                elapsed += check_interval
                
    except Exception as e:
        print(f"[X] Error checking status: {e}")
        time.sleep(check_interval)
        elapsed += check_interval

if elapsed >= max_wait:
    print()
    print("[!] Timeout: Run is taking longer than expected")
    print(f"Check manually at: https://console.apify.com/actors/runs/{run_id}")
    print()

print("=" * 80)

