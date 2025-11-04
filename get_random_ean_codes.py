import csv
import random

# Read the master list
with open('palmers-barcodes-master-list-with-upc-check.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)
    
    # Get all rows with valid UPCs
    all_rows = []
    for row in reader:
        if row and len(row) > 1:
            upc = row[1].strip()
            # Check if it's a valid UPC (12 digits)
            if upc.isdigit() and len(upc) == 12:
                all_rows.append(row)
    
    # Get 5 random rows
    random_rows = random.sample(all_rows, 5)
    
    print("=" * 80)
    print("5 Random Products with EAN-13 Codes")
    print("=" * 80)
    print()
    
    for i, row in enumerate(random_rows, 1):
        upc = row[1].strip()
        ean13 = "0" + upc  # Convert UPC-A to EAN-13 by adding leading 0
        item_name = row[5] if len(row) > 5 else "Unknown"
        dept_name = row[4] if len(row) > 4 else "Unknown"
        
        print(f"{i}. {item_name}")
        print(f"   Department: {dept_name}")
        print(f"   UPC-A:  {upc}")
        print(f"   EAN-13: {ean13}")
        print()
    
    print("=" * 80)

