import urllib.request
import json
import time

# Your Apify API token - KEEP THIS PRIVATE!
# You'll need to provide your actual token
APIFY_TOKEN = "YOUR_APIFY_API_TOKEN_HERE"  # Replace with your actual token

# The 10 EAN codes we're testing
test_eans = [
    "0711381332580",  # Stonewall Kitchen Waffle Cookie
    "0849455000032",  # Tumaro's Wraps
    "0858183005059",  # Lillie's Q BBQ Sauce
    "0820581153908",  # Bella Maria Cocktail Mix
    "0819046000420",  # InkaCrops Giant Corn
    "0818617022571",  # SUJA Immunity Shot
    "0186011000182",  # Stella & Chewy's Dog Food
    "0312547171670",  # Benadryl Itch Relief
    "0852466006016",  # Simply Gum Mint
    "0824150401162",  # POM Wonderful Juice
]

def run_apify_ean_extractor():
    """
    Submit the 10 EAN codes to Apify EAN/GTIN Image Extractor
    Actor ID: s-r/ean-product-image-search---extract-images-from-any-ean-gtin
    """
    
    # API endpoint to run the actor
    # Using the tilde format for Apify actors
    actor_id = "s-r~ean-product-image-search---extract-images-from-any-ean-gtin"
    url = f"https://api.apify.com/v2/acts/{actor_id}/runs?token={APIFY_TOKEN}"
    
    # Input for the actor - batch of EAN codes
    input_data = {
        "eanCodes": test_eans  # Batch submission
    }
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    print("=" * 80)
    print("APIFY EAN/GTIN IMAGE EXTRACTOR TEST")
    print("=" * 80)
    print()
    print(f"Submitting {len(test_eans)} EAN codes to Apify...")
    print()
    
    try:
        req = urllib.request.Request(
            url, 
            data=json.dumps(input_data).encode('utf-8'),
            headers=headers,
            method='POST'
        )
        
        with urllib.request.urlopen(req, timeout=30) as response:
            run_data = json.loads(response.read().decode())
            run_id = run_data['data']['id']
            
            print(f"[OK] Actor run started successfully!")
            print(f"Run ID: {run_id}")
            print()
            print("Waiting for run to complete...")
            print("(This may take a few minutes as Apify searches multiple sources)")
            print()
            
            # Wait for the run to complete
            status_url = f"https://api.apify.com/v2/actor-runs/{run_id}?token={APIFY_TOKEN}"
            
            while True:
                time.sleep(5)  # Check every 5 seconds
                
                status_req = urllib.request.Request(status_url)
                with urllib.request.urlopen(status_req, timeout=15) as status_response:
                    status_data = json.loads(status_response.read().decode())
                    status = status_data['data']['status']
                    
                    print(f"Status: {status}")
                    
                    if status == 'SUCCEEDED':
                        print()
                        print("[OK] Run completed successfully!")
                        
                        # Get the dataset items
                        dataset_url = f"https://api.apify.com/v2/actor-runs/{run_id}/dataset/items?token={APIFY_TOKEN}"
                        
                        dataset_req = urllib.request.Request(dataset_url)
                        with urllib.request.urlopen(dataset_req, timeout=15) as dataset_response:
                            results = json.loads(dataset_response.read().decode())
                            
                            # Save results
                            with open('apify_ean_results.json', 'w', encoding='utf-8') as f:
                                json.dump(results, f, indent=2)
                            
                            print(f"Retrieved {len(results)} results")
                            print("Results saved to apify_ean_results.json")
                            
                            # Display summary
                            print()
                            print("=" * 80)
                            print("RESULTS SUMMARY")
                            print("=" * 80)
                            
                            for i, result in enumerate(results, 1):
                                ean = result.get('ean', 'Unknown')
                                images = result.get('images', [])
                                title = result.get('title', 'Unknown')
                                
                                print(f"\n{i}. EAN: {ean}")
                                print(f"   Title: {title}")
                                print(f"   Images found: {len(images)}")
                                if images:
                                    print(f"   First image: {images[0][:80]}...")
                            
                            return results
                            
                    elif status == 'FAILED':
                        print()
                        print("[X] Run failed!")
                        print(f"Error: {status_data['data'].get('statusMessage', 'Unknown error')}")
                        return None
                        
                    elif status in ['RUNNING', 'READY']:
                        continue
                    else:
                        print(f"[!] Unexpected status: {status}")
                        time.sleep(5)
                        
    except Exception as e:
        print(f"[X] Error: {e}")
        return None

if __name__ == "__main__":
    # Check if token is set
    if APIFY_TOKEN == "YOUR_APIFY_TOKEN_HERE":
        print()
        print("=" * 80)
        print("ERROR: Please set your Apify API token in the script")
        print("=" * 80)
        print()
        print("Replace 'YOUR_APIFY_TOKEN_HERE' with your actual Apify token")
        print("You can find your token at: https://console.apify.com/account/integrations")
        print()
    else:
        results = run_apify_ean_extractor()

