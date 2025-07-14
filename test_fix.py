#!/usr/bin/env python3
"""
Quick test script to verify the gittertalk fixes
"""
import asyncio
from interpreter import interpreter_process
from departments import handle_department
from gittertalk import gittertalk_to_string

async def test_workflow():
    # Test the workflow that was failing
    structured_prompt = "Intent: find route, Object: highway directions, Parameters: from Zanesville Ohio to Columbus Ohio"
    
    print("Testing Workflow with different verbose levels:")
    print("=" * 60)
    
    for level in [1, 2, 4]:  # Updated to test only supported levels
        print(f"\nVerbose Level {level}:")
        print("-" * 30)
        
        try:
            # Step 1: Interpreter process
            gittertalk_obj, department = await interpreter_process(structured_prompt, level)
            
            # Step 2: Convert to string for display
            gittertalk_str = gittertalk_to_string(gittertalk_obj, level)
            
            print(f"Gittertalk object: act='{gittertalk_obj.act}', obj='{gittertalk_obj.obj}', params={gittertalk_obj.params}")
            print(f"Gittertalk string: '{gittertalk_str}'")
            print(f"Department: {department}")
            
            # Step 3: Department processing (simplified)
            # Note: We're not actually calling the department to avoid API calls in testing
            print("✓ Parsing successful")
            
        except Exception as e:
            print(f"✗ Error: {e}")

if __name__ == "__main__":
    print("Note: This test will not make actual API calls to avoid costs.")
    print("It only tests the parsing and formatting logic.")
    print()
    
    # Test just the parsing logic without API calls
    from gittertalk import gittertalk
    
    # Test Level 2 parsing
    print("Testing Level 2 parsing:")
    test_gt_2 = gittertalk(act="route", obj="directions", params={"from": "Zanesville", "to": "Columbus"})
    level_2_str = gittertalk_to_string(test_gt_2, 2)
    print(f"Level 2 output: '{level_2_str}'")
    
    # Test Level 4 parsing  
    print("\nTesting Level 4 parsing:")
    test_gt_4 = gittertalk(act="route", obj="directions", params={"from": "Zanesville", "to": "Columbus"})
    level_4_str = gittertalk_to_string(test_gt_4, 4)
    print(f"Level 4 output: '{level_4_str}'")
    
    print("\n" + "=" * 60)
    print("If you want to test the full workflow, run the FastAPI server")
    print("and make a POST request to /process with verbose=1, verbose=2, or verbose=4")
