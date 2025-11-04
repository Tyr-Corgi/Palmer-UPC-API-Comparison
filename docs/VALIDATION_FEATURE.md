# API Validation Feature

## Overview
Automatic cross-checking of API results against Palmer's master product list to detect data quality issues.

## Problem Solved
Previously, we discovered that some APIs return completely wrong products for valid UPCs:
- **Example**: UPC `818290019592` should be "Chobani Coffee Greek Yogurt"
- **Barcode Lookup API returned**: "CAT5 Network Cable" (completely wrong category)
- **UPCitemdb returned**: Same wrong product
- **Apify returned**: Correct product ✅

This validation feature automatically detects these issues during API testing.

## Features

### 1. Similarity Matching
- Compares API-returned product names with expected names from master list
- Uses fuzzy matching algorithm (0-100% similarity)
- **70%+ similarity** = Good match ✅
- **30-70% similarity** = Partial match (review recommended) ⚠️
- **<30% similarity** = No match ❌

### 2. Category Mismatch Detection
Detects critical errors when products are in completely wrong categories:
- Food vs Electronics
- Beverages vs Network Equipment
- Etc.

These are flagged as **CRITICAL_MISMATCH** 🚨

### 3. Validation Status Codes
- **MATCH**: Good match (70%+ similarity)
- **PARTIAL_MATCH**: Acceptable but review recommended (30-70%)
- **NO_MATCH**: Different product (<30% similarity)
- **CRITICAL_MISMATCH**: Wrong product category (food vs electronics, etc.)
- **UPC_NOT_FOUND**: UPC not in master list

## Usage

### Option 1: Standalone Validation Script
```python
from validate_api_results import validate_single_product

# Validate a single API response
result = validate_single_product(
    upc="818290019592",
    api_product_name="Chobani Coffee Greek Yogurt",
    api_name="Apify"
)

print(f"Status: {result['status']}")
print(f"Similarity: {result['similarity_score']:.1%}")
print(f"Message: {result['message']}")
```

### Option 2: Integrated API Testing
```bash
cd scripts
python test_api_with_validation.py
```

This will:
1. Select 10 random products from master list
2. Test them with the API
3. Automatically validate each result
4. Generate a summary report with accuracy metrics

### Option 3: Batch Validation from JSON
```python
from validate_api_results import validate_api_results_from_json, generate_validation_report

# Validate all results from a JSON file
results = validate_api_results_from_json('api_test_results.json', 'API Name')
generate_validation_report(results, 'validation_report.txt')
```

## Example Output

```
================================================================================
PRODUCT 14/15: Chobani Coffee Greek Yogurt
UPC: 818290019592
================================================================================

  Testing Barcode Lookup API...
    API Response: 100 X RJ45 Coupler CAT5 CAT6 Network Cable
    Validation: 🚨 CRITICAL_MISMATCH
    Similarity: 0%
    Category mismatch! Expected food/beverage, got electronics

  Testing Apify...
    API Response: Chobani Yogurt, Reduced Fat, Greek, Blended, Coffee
    Validation: ✅ MATCH
    Similarity: 85%
    Good match

================================================================================
VALIDATION SUMMARY
================================================================================
  ✅ Perfect Matches: 13/15
  ⚠️  Partial Matches: 1/15
  ❌ No Match: 0/15
  🚨 Critical Mismatches: 1/15

  Overall Accuracy: 86.7%

  ⚠️  WARNING: Critical mismatches detected!
     These products are in completely wrong categories.
     Review these results carefully before using this API.
```

## Integration with Existing Scripts

The validation can be added to any existing API test script:

```python
from validate_api_results import validate_single_product

# After getting API response
api_product_name = api_response['title']

# Validate it
validation = validate_single_product(upc, api_product_name, "Your API Name")

if validation['status'] == 'CRITICAL_MISMATCH':
    print(f"⚠️  WARNING: {validation['message']}")
    # Flag for review or skip this result
```

## Files

- **`scripts/validate_api_results.py`**: Core validation logic
- **`scripts/test_api_with_validation.py`**: Integrated testing with validation
- **`docs/VALIDATION_FEATURE.md`**: This documentation

## Benefits

1. **Automatic Quality Control**: Catches bad data before it enters your system
2. **Trust Scoring**: Know which APIs are more reliable
3. **Cost Savings**: Avoid paying for APIs with poor data quality
4. **Decision Support**: Clear metrics for API selection
5. **Early Warning**: Detect database issues in API providers

## Next Steps

1. Run validation on your full API test suite
2. Compare validation scores across APIs
3. Set minimum similarity thresholds for production use
4. Consider rejecting results with CRITICAL_MISMATCH status

## Example: Row 14 Chobani Issue

This feature would have immediately flagged the Row 14 issue:

```
UPC: 818290019592
Expected: Chobani Coffee Greek Yogurt
Barcode Lookup: 100 X RJ45 Coupler CAT5 Network Cable
Status: 🚨 CRITICAL_MISMATCH
Similarity: 0%
Message: Category mismatch! Expected food/beverage, got electronics
```

Instead of manually discovering it by reviewing the HTML report, the validation would automatically alert you during the API test.

