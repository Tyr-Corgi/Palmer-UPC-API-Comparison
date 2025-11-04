"""
API Result Validator - Cross-checks API responses against Palmer's master list
This script validates that API-returned product names match our expected products
"""

import csv
import json
from difflib import SequenceMatcher

def load_master_list(csv_file='../palmers-barcodes-master-list-with-upc-check.csv'):
    """Load the master product list and create UPC -> Product Name mapping"""
    upc_to_product = {}
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        
        for row in reader:
            if len(row) > 3:
                upc = row[1].strip()  # Column 1: Item ID (UPC)
                product_name = row[3].strip()  # Column 3: Item Name
                
                if upc and product_name and upc.isdigit() and len(upc) == 12:
                    upc_to_product[upc] = product_name
    
    return upc_to_product

def calculate_similarity(str1, str2):
    """Calculate similarity ratio between two strings (0-1, where 1 is identical)"""
    return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()

def validate_api_response(upc, api_product_name, master_product_name, api_name, threshold=0.3):
    """
    Validate if API response matches our expected product
    
    Args:
        upc: The UPC code
        api_product_name: Product name from API
        master_product_name: Expected product name from master list
        api_name: Name of the API (for reporting)
        threshold: Minimum similarity score (0-1) to consider a match
    
    Returns:
        dict with validation results
    """
    similarity = calculate_similarity(api_product_name, master_product_name)
    
    # Check for major category mismatches (e.g., food vs electronics)
    food_keywords = ['food', 'snack', 'drink', 'juice', 'yogurt', 'protein', 'organic', 
                     'chocolate', 'cookie', 'wrap', 'sauce', 'gum', 'tea', 'coffee']
    electronics_keywords = ['cable', 'connector', 'ethernet', 'rj45', 'usb', 'adapter', 
                           'network', 'computer', 'electronic']
    
    master_lower = master_product_name.lower()
    api_lower = api_product_name.lower()
    
    master_is_food = any(keyword in master_lower for keyword in food_keywords)
    api_is_food = any(keyword in api_lower for keyword in food_keywords)
    
    master_is_electronics = any(keyword in master_lower for keyword in electronics_keywords)
    api_is_electronics = any(keyword in api_lower for keyword in electronics_keywords)
    
    category_mismatch = False
    if (master_is_food and api_is_electronics) or (master_is_electronics and api_is_food):
        category_mismatch = True
    
    # Determine validation status
    if category_mismatch:
        status = 'CRITICAL_MISMATCH'
        message = f"Category mismatch! Expected food/beverage, got electronics (or vice versa)"
    elif similarity >= 0.7:
        status = 'MATCH'
        message = f"Good match (similarity: {similarity:.2%})"
    elif similarity >= threshold:
        status = 'PARTIAL_MATCH'
        message = f"Partial match (similarity: {similarity:.2%}) - Review recommended"
    else:
        status = 'NO_MATCH'
        message = f"Poor match (similarity: {similarity:.2%}) - Likely wrong product"
    
    return {
        'upc': upc,
        'api_name': api_name,
        'expected_product': master_product_name,
        'api_product': api_product_name,
        'similarity_score': similarity,
        'status': status,
        'message': message
    }

def validate_api_results_from_json(json_file, api_name):
    """
    Validate API results from a JSON file
    
    Args:
        json_file: Path to JSON file with API results
        api_name: Name of the API
    
    Returns:
        List of validation results
    """
    # Load master list
    master_list = load_master_list()
    
    # Load API results
    with open(json_file, 'r', encoding='utf-8') as f:
        api_results = json.load(f)
    
    validation_results = []
    
    for result in api_results:
        upc = result.get('upc', '').strip()
        api_product_name = result.get('title', result.get('product_name', '')).strip()
        
        if upc in master_list:
            master_product_name = master_list[upc]
            
            validation = validate_api_response(
                upc, 
                api_product_name, 
                master_product_name, 
                api_name
            )
            validation_results.append(validation)
        else:
            validation_results.append({
                'upc': upc,
                'api_name': api_name,
                'expected_product': 'NOT IN MASTER LIST',
                'api_product': api_product_name,
                'similarity_score': 0,
                'status': 'UPC_NOT_FOUND',
                'message': 'UPC not found in master list'
            })
    
    return validation_results

def generate_validation_report(validation_results, output_file='validation_report.txt'):
    """Generate a human-readable validation report"""
    
    # Categorize results
    critical = [r for r in validation_results if r['status'] == 'CRITICAL_MISMATCH']
    no_match = [r for r in validation_results if r['status'] == 'NO_MATCH']
    partial = [r for r in validation_results if r['status'] == 'PARTIAL_MATCH']
    matches = [r for r in validation_results if r['status'] == 'MATCH']
    not_found = [r for r in validation_results if r['status'] == 'UPC_NOT_FOUND']
    
    report = []
    report.append("=" * 80)
    report.append("API VALIDATION REPORT")
    report.append("=" * 80)
    report.append("")
    report.append(f"Total Products Validated: {len(validation_results)}")
    report.append(f"  Perfect Matches: {len(matches)}")
    report.append(f"  Partial Matches: {len(partial)}")
    report.append(f"  No Match: {len(no_match)}")
    report.append(f"  CRITICAL Mismatches: {len(critical)}")
    report.append(f"  UPC Not Found: {len(not_found)}")
    report.append("")
    
    if critical:
        report.append("=" * 80)
        report.append("CRITICAL MISMATCHES (WRONG PRODUCT CATEGORY)")
        report.append("=" * 80)
        for r in critical:
            report.append(f"\nUPC: {r['upc']}")
            report.append(f"  Expected: {r['expected_product']}")
            report.append(f"  API ({r['api_name']}): {r['api_product']}")
            report.append(f"  Similarity: {r['similarity_score']:.2%}")
            report.append(f"  Status: {r['message']}")
    
    if no_match:
        report.append("\n" + "=" * 80)
        report.append("NO MATCH (DIFFERENT PRODUCTS)")
        report.append("=" * 80)
        for r in no_match:
            report.append(f"\nUPC: {r['upc']}")
            report.append(f"  Expected: {r['expected_product']}")
            report.append(f"  API ({r['api_name']}): {r['api_product']}")
            report.append(f"  Similarity: {r['similarity_score']:.2%}")
    
    if partial:
        report.append("\n" + "=" * 80)
        report.append("PARTIAL MATCHES (REVIEW RECOMMENDED)")
        report.append("=" * 80)
        for r in partial:
            report.append(f"\nUPC: {r['upc']}")
            report.append(f"  Expected: {r['expected_product']}")
            report.append(f"  API ({r['api_name']}): {r['api_product']}")
            report.append(f"  Similarity: {r['similarity_score']:.2%}")
    
    report_text = "\n".join(report)
    
    # Print to console
    print(report_text)
    
    # Save to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report_text)
    
    print(f"\nValidation report saved to: {output_file}")
    
    return report_text

def validate_single_product(upc, api_product_name, api_name):
    """
    Quick validation for a single product
    
    Args:
        upc: UPC code (12 digits)
        api_product_name: Product name from API
        api_name: Name of the API
    
    Returns:
        Validation result dict
    """
    master_list = load_master_list()
    
    if upc not in master_list:
        return {
            'status': 'UPC_NOT_FOUND',
            'message': f'UPC {upc} not found in master list'
        }
    
    master_product_name = master_list[upc]
    return validate_api_response(upc, api_product_name, master_product_name, api_name)

# Example usage
if __name__ == "__main__":
    print("API Result Validator")
    print("=" * 80)
    print()
    
    # Example: Validate a single product
    print("Example 1: Single Product Validation")
    print("-" * 40)
    
    # The problem UPC from Row 14 (Chobani)
    result = validate_single_product(
        upc="818290019592",
        api_product_name="100 X RJ45 Coupler CAT5 CAT6 5E 8P8C Network Ethernet Connector Adapter Joiner",
        api_name="Barcode Lookup API"
    )
    
    print(f"UPC: {result['upc']}")
    print(f"Expected: {result['expected_product']}")
    print(f"API Returned: {result['api_product']}")
    print(f"Status: {result['status']}")
    print(f"Message: {result['message']}")
    print()
    
    # Example: Validate from JSON file (you would need to provide the file)
    print("Example 2: Batch Validation from JSON")
    print("-" * 40)
    print("To validate API results from a JSON file, use:")
    print("  results = validate_api_results_from_json('your_api_results.json', 'API Name')")
    print("  generate_validation_report(results)")

