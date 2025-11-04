# Remove corrupted fake data from lines 1924-2346
import os

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
# Go up one level to project root
project_root = os.path.dirname(script_dir)
html_file = os.path.join(project_root, 'API_Compare_Chart.html')

print(f"Reading from: {html_file}")

with open(html_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Original file has {len(lines)} lines")

# Keep lines 1-1923 and skip 1924-2346, then add rest
new_lines = lines[:1923] + lines[2346:]

with open(html_file, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Successfully removed corrupted lines 1924-2346")
print(f"New file has {len(new_lines)} lines")
print(f"Removed {len(lines) - len(new_lines)} lines")

