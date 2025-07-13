#!/usr/bin/env python3
"""
Complete token efficiency test - measures both string compression AND pipeline efficiency
"""
import tiktoken
from gittertalk import gittertalk, gittertalk_to_string

def count_tokens(text: str, model: str = "gpt-3.5-turbo") -> int:
    """Count tokens using OpenAI's tiktoken library"""
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

def test_complete_workflow():
    """Test ACTUAL workflow token efficiency: user→AI vs user→gittertalk→AI"""
    
    print("COMPLETE WORKFLOW TOKEN EFFICIENCY TEST")
    print("=" * 80)
    print("Comparing:")
    print("  Scenario A: user_prompt → AI_response")
    print("  Scenario B: user_prompt → gittertalk → AI_response")
    print("=" * 80)
    
    test_cases = [
        {
            "user_prompt": "what highway to take to get from zanesville ohio to columbus ohio",
            "gittertalk_obj": gittertalk(act="route", obj="Route", params={"from": "Zanesville", "to": "Columbus"}),
            "expected_ai_prompt": "You are a Travel Assistant AI. Help with route planning from Zanesville to Columbus Ohio. Provide highway directions and travel advice."
        },
        {
            "user_prompt": "I need to book a flight from NYC to Los Angeles tomorrow morning",
            "gittertalk_obj": gittertalk(act="flight", obj="Flight", params={"from": "New York", "to": "Los Angeles", "when": "+1", "time": "morning"}),
            "expected_ai_prompt": "You are a Travel Assistant AI. Help with flight booking from NYC to Los Angeles for tomorrow morning. Provide booking suggestions and availability."
        },
        {
            "user_prompt": "Can you tell me a funny joke to cheer me up after this stressful work day?",
            "gittertalk_obj": gittertalk(act="joke", obj="entertainment", params={"mood": "stressed", "purpose": "cheer_up"}),
            "expected_ai_prompt": "You are a Comedy Assistant AI. Tell a funny joke to cheer up someone who is stressed from work."
        }
    ]
    
    total_scenario_a_tokens = 0
    total_scenario_b_tokens = {2: 0, 3: 0, 4: 0}
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n--- Test Case {i} ---")
        print(f"User prompt: \"{case['user_prompt']}\"")
        
        # Scenario A: Direct user prompt to AI
        user_tokens = count_tokens(case['user_prompt'])
        ai_prompt_tokens = count_tokens(case['expected_ai_prompt'])
        scenario_a_total = user_tokens + ai_prompt_tokens
        total_scenario_a_tokens += scenario_a_total
        
        print(f"\nScenario A (Direct):")
        print(f"  User prompt: {user_tokens} tokens")
        print(f"  AI prompt: {ai_prompt_tokens} tokens")
        print(f"  Total: {scenario_a_total} tokens")
        
        # Scenario B: User prompt → gittertalk → AI
        for level in [2, 3, 4]:
            gittertalk_str = gittertalk_to_string(case['gittertalk_obj'], level)
            gittertalk_tokens = count_tokens(gittertalk_str)
            
            # Simulate department AI prompt with gittertalk
            dept_prompt = f"You are a Travel Assistant AI. Process this request: {gittertalk_str}"
            dept_prompt_tokens = count_tokens(dept_prompt)
            
            scenario_b_total = user_tokens + gittertalk_tokens + dept_prompt_tokens
            total_scenario_b_tokens[level] += scenario_b_total
            
            savings = scenario_a_total - scenario_b_total
            reduction = (savings / scenario_a_total) * 100 if scenario_a_total > 0 else 0
            
            print(f"\nScenario B (Level {level}):")
            print(f"  User prompt: {user_tokens} tokens")
            print(f"  Gittertalk: \"{gittertalk_str}\" ({gittertalk_tokens} tokens)")
            print(f"  Dept AI prompt: {dept_prompt_tokens} tokens")
            print(f"  Total: {scenario_b_total} tokens")
            print(f"  Savings: {savings} tokens ({reduction:.1f}% reduction)")
    
    print("\n" + "=" * 80)
    print("OVERALL WORKFLOW EFFICIENCY")
    print("=" * 80)
    
    print(f"Scenario A (Direct) Total: {total_scenario_a_tokens} tokens")
    
    for level in [2, 3, 4]:
        total_savings = total_scenario_a_tokens - total_scenario_b_tokens[level]
        total_reduction = (total_savings / total_scenario_a_tokens) * 100
        
        print(f"\nScenario B (Level {level}) Total: {total_scenario_b_tokens[level]} tokens")
        print(f"  Total savings: {total_savings} tokens")
        print(f"  Total reduction: {total_reduction:.1f}%")
        
        if total_reduction > 0:
            print(f"  ✅ Level {level} saves tokens in full workflow")
        else:
            print(f"  ❌ Level {level} uses MORE tokens in full workflow")

def test_string_compression_only():
    """Test JUST string compression (what current tests do)"""
    
    print("\n" + "=" * 80)
    print("STRING COMPRESSION TEST (Current Test)")
    print("=" * 80)
    print("This tests: original_text vs gittertalk_string")
    print("(This is what the current token_efficiency_test.py does)")
    print("=" * 80)
    
    original_text = "what highway to take to get from zanesville ohio to columbus ohio"
    route_obj = gittertalk(act="route", obj="Route", params={"from": "Zanesville", "to": "Columbus"})
    
    original_tokens = count_tokens(original_text)
    print(f"\nOriginal: \"{original_text}\" ({original_tokens} tokens)")
    
    for level in [2, 3, 4]:
        gittertalk_str = gittertalk_to_string(route_obj, level)
        gittertalk_tokens = count_tokens(gittertalk_str)
        reduction = ((original_tokens - gittertalk_tokens) / original_tokens) * 100
        
        print(f"Level {level}: \"{gittertalk_str}\" ({gittertalk_tokens} tokens, {reduction:.1f}% reduction)")

if __name__ == "__main__":
    try:
        test_complete_workflow()
        test_string_compression_only()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
