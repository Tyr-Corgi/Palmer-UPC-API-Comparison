import csv
import random

# Read the master list
upcs = []
with open('palmers-barcodes-master-list.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        upc = row.get('UPC', '').strip()
        if upc and len(upc) >= 12:
            upcs.append(upc)

# Get 5 random UPCs
random.seed(42)  # For reproducibility
selected_upcs = random.sample(upcs, 5)

print("Selected 5 random UPCs:")
print("=" * 80)
for i, upc in enumerate(selected_upcs, 1):
    print(f"{i}. {upc}")

# Save to file
with open('additional_5_upcs.txt', 'w') as f:
    for upc in selected_upcs:
        f.write(upc + '\n')

print("\n" + "=" * 80)
print("Saved to additional_5_upcs.txt")

