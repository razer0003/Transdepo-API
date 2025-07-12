from gittertalk import gittertalk, gittertalk_to_string

# Create a test gittertalk object
gt = gittertalk(
    act="flight",
    obj="Flight", 
    params={
        "from": "NYC",
        "to": "ABQ", 
        "when": "+1",
        "check": "availability"
    }
)

print("Testing verbose levels:")
for level in [1, 2, 3, 4]:
    result = gittertalk_to_string(gt, level)
    print(f"Level {level}: {result} ({len(result)} chars)")
