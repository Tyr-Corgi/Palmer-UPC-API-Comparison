import urllib.request
import json

APIFY_TOKEN = "YOUR_APIFY_API_TOKEN_HERE"  # Replace with your actual token

# The 5 EAN codes that weren't found in the first Apify test (items 6-10)
remaining_eans = [
    "0818617022571",  # SUJA Immunity Shot
    "0186011000182",  # Stella & Chewy's Dog Food
    "0312547171670",  # Benadryl Itch Relief
    "0852466006016",  # Simply Gum Mint
    "0824150401162",  # POM Wonderful Juice
]

product_names = [
    "SUJA Immunity Shot",
    "Stella & Chewy's Dog Food",
    "Benadryl Itch Relief",
    "Simply Gum Mint",
    "POM Wonderful Juice"
]

print("=" * 80)
print("APIFY EAN/GTIN - RETEST OF ITEMS 6-10")
print("=" * 80)
print()
print("Testing the 5 EAN codes that were not found in the first Apify test:")
print()

for i, (ean, name) in enumerate(zip(remaining_eans, product_names), 6):
    print(f"{i}. EAN {ean} - {name}")

print()
print("=" * 80)
print()

# Try using the Apify web scraper actor directly
# This is the actor ID from the URL you provided
actor_username = "s-r"
actor_name = "ean-product-image-search---extract-images-from-any-ean-gtin"

print("Attempting to start Apify actor run...")
print()

# Method 1: Try POST to start a new run
try:
    url = f"https://api.apify.com/v2/acts/{actor_username}~{actor_name}/runs?token={APIFY_TOKEN}"
    
    # Input format for the EAN extractor
    input_data = {
        "eans": remaining_eans,  # Field name must be 'eans'
        "maxImages": 5,  # Get up to 5 images per EAN
        "timeout": 60
    }
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    print(f"URL: {url}")
    print(f"Input: {len(remaining_eans)} EAN codes")
    print()
    
    req = urllib.request.Request(
        url,
        data=json.dumps(input_data).encode('utf-8'),
        headers=headers,
        method='POST'
    )
    
    print("Submitting request to Apify...")
    
    with urllib.request.urlopen(req, timeout=30) as response:
        result = json.loads(response.read().decode())
        
        print("[OK] Actor run started!")
        print()
        print(f"Run ID: {result['data']['id']}")
        print(f"Status: {result['data']['status']}")
        print(f"Started at: {result['data'].get('startedAt', 'N/A')}")
        print()
        print("The actor is now running. To check results:")
        print(f"1. Wait a few minutes for it to complete")
        print(f"2. Check the Apify console: https://console.apify.com/actors/runs/{result['data']['id']}")
        print(f"3. Or run this command to get results:")
        print(f"   python get_apify_run_results.py {result['data']['id']}")
        print()
        
        # Save the run ID for later retrieval
        with open('apify_latest_run.json', 'w') as f:
            json.dump({
                'run_id': result['data']['id'],
                'eans': remaining_eans,
                'started_at': result['data'].get('startedAt'),
                'status': result['data']['status']
            }, f, indent=2)
        
        print("Run details saved to apify_latest_run.json")
        
except urllib.error.HTTPError as e:
    print(f"[X] HTTP Error {e.code}: {e.reason}")
    print()
    error_body = e.read().decode('utf-8')
    print("Error details:")
    try:
        error_data = json.loads(error_body)
        print(json.dumps(error_data, indent=2))
    except:
        print(error_body)
    print()
    print("=" * 80)
    print()
    print("Trying alternative method: Checking if there's a recent run we can use...")
    print()
    
    # Method 2: Check if we can access existing runs
    try:
        # Try to get actor information
        actor_url = f"https://api.apify.com/v2/acts/{actor_username}~{actor_name}?token={APIFY_TOKEN}"
        req = urllib.request.Request(actor_url)
        
        with urllib.request.urlopen(req, timeout=15) as response:
            actor_data = json.loads(response.read().decode())
            print("[OK] Actor found!")
            print(f"Name: {actor_data['data']['name']}")
            print(f"Description: {actor_data['data'].get('description', 'N/A')[:80]}...")
            print()
            print("Note: You may need to run this actor through the Apify console")
            print(f"Visit: https://console.apify.com/actors/{actor_username}~{actor_name}")
            
    except Exception as e2:
        print(f"[X] Could not access actor: {e2}")
        
except Exception as e:
    print(f"[X] Error: {e}")
    import traceback
    traceback.print_exc()

print()
print("=" * 80)

