import csv
import random

# Read the verified file and extract UPCs
upcs = []
with open('palmers-barcodes-master-list-verified-500.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        # Check if there's a valid UPC in the row (look for 12-digit numbers)
        for key, value in row.items():
            if value and len(str(value)) == 12 and str(value).isdigit():
                upcs.append(str(value))
                break

# Get 5 random UPCs (different from the ones we already tested)
already_tested = [
    "711381332580", "849455000032", "858183005059", "820581153908", "819046000420",
    "818617022571", "186011000182", "312547171670", "852466006016", "824150401162"
]

available_upcs = [u for u in upcs if u not in already_tested]

if len(available_upcs) < 5:
    print(f"Warning: Only {len(available_upcs)} unique UPCs available")
    selected_upcs = available_upcs
else:
    random.seed(123)  # Different seed for different selection
    selected_upcs = random.sample(available_upcs, 5)

print("Selected 5 new random UPCs:")
print("=" * 80)
for i, upc in enumerate(selected_upcs, 1):
    print(f"{i}. {upc}")

# Save to file
with open('additional_5_upcs.txt', 'w') as f:
    for upc in selected_upcs:
        f.write(upc + '\n')

print("\n" + "=" * 80)
print(f"Saved {len(selected_upcs)} UPCs to additional_5_upcs.txt")

