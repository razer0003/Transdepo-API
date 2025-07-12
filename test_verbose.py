"""
Test script for the new verbose levels in gittertalk
"""
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gittertalk import gittertalk, gittertalk_to_string

# Test gittertalk object
test_gt = gittertalk(
    act="flight",
    obj="Flight",
    params={
        "from": "NYC",
        "to": "ABQ",
        "when": "+1",
        "check": "availability"
    }
)

print("Testing gittertalk verbose levels:")
print("Original concept: 'okay so im coming from NYC. i need to get a flight to albuerqerque NM TOMORROW. PLEASE tell me theres one available' (115 chars)")
print()

for level in [1, 2, 3, 4]:
    output = gittertalk_to_string(test_gt, level)
    print(f"Level {level}: {output} ({len(output)} chars)")
    if level == 1:
        print(f"  Current format - {len(output)/115*100:.1f}% of original")
    elif level == 2:
        print(f"  60% target - {len(output)/115*100:.1f}% of original")
    elif level == 3:
        print(f"  40% target - {len(output)/115*100:.1f}% of original")
    elif level == 4:
        print(f"  20% target - {len(output)/115*100:.1f}% of original")
    print()
