# Palmer's UPC/EAN Product Database Project

## 📊 Quick Access

### **[API Compare Chart](API_Compare_Chart.html)** 
**Main deliverable** - Comprehensive comparison of 3 UPC/EAN APIs with 15 test products showing images, data quality, and pricing analysis.

---

## Project Overview

This project validates Palmer's product UPC codes against external databases and evaluates API services for product image and data retrieval.

## Key Findings

### API Performance Summary
- **Barcode Lookup API**: 93.3% accuracy (14/15 products correct)
- **Apify EAN/GTIN**: 93.3% accuracy (14/15 products correct) + High-resolution images
- **UPCitemdb**: 86.7% accuracy (13/15 products correct) + Multiple images per product

### Data Quality Issue Identified
- **Row 14** (Chobani Coffee Greek Yogurt - UPC 818290019592): Incorrectly identified as network cable by Barcode Lookup API and UPCitemdb. Only Apify correctly identified this product.
- See [`docs/DATA_QUALITY_ISSUE_ROW_14.md`](docs/DATA_QUALITY_ISSUE_ROW_14.md) for detailed analysis.

---

## Project Structure

```
PerPound/
├── API_Compare_Chart.html          # 📊 MAIN CHART - Open this for full API comparison
├── README.md                        # This file
│
├── api-reports/                     # All generated HTML reports
│   ├── API_Comparison_Table.html
│   ├── Barcode_Lookup_API_Test_Results.html
│   ├── EAN_Test_Results_10_Products.html
│   ├── Palmers_Verified_Products_with_Images.html
│   └── UPC_API_PRICING_TABLE.html
│
├── docs/                            # Documentation and analysis
│   ├── DATA_QUALITY_ISSUE_ROW_14.md
│   ├── UPC_API_PRICING_COMPARISON.md
│   ├── VERIFICATION_SUMMARY.md
│   └── UPC_Pattern_Analysis_Report.md
│
├── scripts/                         # All Python scripts
│   ├── verify_upc_incremental.py   # Main UPC verification script
│   ├── test_*_api.py               # API testing scripts
│   └── get_*.py                    # Data retrieval scripts
│
├── json-data/                       # API test results and data
│   ├── api_comparison_results.json
│   ├── all_product_details.json
│   └── *_test_results.json
│
└── csv-data/                        # Product CSV files
    ├── palmers-barcodes-master-list.csv
    ├── palmers-barcodes-master-list-with-upc-check.csv
    └── palmers-barcodes-verified-with-images.csv
```

---

## Master Product List

**Location**: `palmers-barcodes-master-list-with-upc-check.csv`
- **Total Products**: ~25,400
- **Valid UPCs**: 9,394

---

## API Pricing Summary

| API | Plan | Cost | Features |
|-----|------|------|----------|
| **Barcode Lookup** | Professional | $9.99/month | 100,000 calls/month, 1 image per product |
| **Apify** | Pay-as-you-go | ~$0.01 per item | High-res images (1000x1000px), batch processing |
| **UPCitemdb** | Sustainable | $10/month | 20,000 lookups/day, multiple images |

See [`docs/UPC_API_PRICING_COMPARISON.md`](docs/UPC_API_PRICING_COMPARISON.md) for detailed pricing analysis.

---

## How to Use

### View the API Comparison
1. Open [`API_Compare_Chart.html`](API_Compare_Chart.html) in your browser
2. Review the 15 test products with side-by-side API comparisons
3. Check row numbers on the left for easy navigation
4. Note data quality warnings where APIs returned incorrect data

### Run UPC Verification
```bash
cd scripts
python verify_upc_incremental.py
```

### Test a Specific API
```bash
cd scripts
# Edit the script to add your API key
python test_barcode_lookup_api.py
```

---

## Contact

For questions about this analysis, contact the project team.

---

**Last Updated**: November 4, 2025

