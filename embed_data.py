#!/usr/bin/env python3
import json

# Read CSV files
with open('CAPEG_20260216 (1).csv', 'r') as f:
    capacity_data = f.read()

with open('final_gwap_20260125.csv', 'r') as f:
    price_data = f.read()

with open('mru_mo_processed_20260209-20260215.csv', 'r') as f:
    ops_data = f.read()

# Create JavaScript variables
print("const EMBEDDED_DATA = {")
print(f"  capacity: {json.dumps(capacity_data)},")
print(f"  prices: {json.dumps(price_data)},")
print(f"  operations: {json.dumps(ops_data)}")
print("};")
