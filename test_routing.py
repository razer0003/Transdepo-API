"""
Test script to verify department routing logic
"""
import asyncio
from feeder import feeder_process
from interpreter import interpreter_process
from departments import handle_department

async def test_request(request, fallback_mode="strict", verbose=2):
    print(f"\n=== Testing: '{request}' (fallback: {fallback_mode}) ===")
    
    try:
        # 1. Feeder step
        structured = await feeder_process(request)
        print(f"Structured: {structured}")
        
        # 2. Interpreter step
        gittertalk, department = await interpreter_process(structured, verbose)
        print(f"Department: {department}")
        print(f"Gittertalk: {gittertalk}")
        
        # 3. Department step
        result = await handle_department(department, gittertalk, fallback_mode)
        print(f"Result: {result}")
        
    except Exception as e:
        print(f"Error: {e}")

async def main():
    # Test cases that should hit specific departments
    await test_request("Book a flight to NYC", "strict")
    await test_request("Tell me a joke", "strict") 
    await test_request("What's the latest news about AI?", "strict")
    
    # Test cases that should hit fallback in strict mode
    await test_request("What is the best video game of 2024?", "strict")
    await test_request("Help me with my homework", "strict")
    
    # Test cases with adaptive mode
    await test_request("What is the best video game of 2024?", "adaptive")

if __name__ == "__main__":
    asyncio.run(main())
