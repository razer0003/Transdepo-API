#!/usr/bin/env python3
"""
Quick test of token efficiency with updated abbreviations
"""
import tiktoken
from gittertalk import gittertalk, gittertalk_to_string

def count_tokens(text: str, model: str = "gpt-3.5-turbo") -> int:
    """Count tokens using OpenAI's tiktoken library"""
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

def test_updated_abbreviations():
    """Test token efficiency with our updated defined abbreviations"""
    
    # Test route example (the one you were asking about)
    original_text = "what highway to take to get from zanesville ohio to get to columbus ohio"
    route_obj = gittertalk(act="route", obj="Route", params={"from": "Zanesville", "to": "Columbus"})
    
    print("UPDATED ABBREVIATION TEST")
    print("=" * 60)
    print(f"Original: \"{original_text}\"")
    print(f"Original tokens: {count_tokens(original_text)}")
    print()
    
    for level in [1, 2, 3, 4]:
        gittertalk_str = gittertalk_to_string(route_obj, level)
        level_tokens = count_tokens(gittertalk_str)
        original_tokens = count_tokens(original_text)
        reduction = ((original_tokens - level_tokens) / original_tokens) * 100
        
        print(f"Level {level}: \"{gittertalk_str}\"")
        print(f"  Tokens: {level_tokens} (vs {original_tokens} original)")
        print(f"  Reduction: {reduction:.1f}%")
        print()
    
    # Test a few of the original test cases to see if they still work
    print("ORIGINAL TEST CASES WITH NEW ABBREVIATIONS")
    print("=" * 60)
    
    test_cases = [
        (
            "I need to get a flight to albuquerque NM TOMORROW",
            gittertalk(act="flight", obj="Flight", params={"to": "ABQ", "when": "+1"})
        ),
        (
            "I want to book a hotel room in Paris for next week",
            gittertalk(act="hotel", obj="Hotel", params={"location": "Paris", "when": "+7"})
        ),
        (
            "Can you tell me a funny joke?",
            gittertalk(act="joke", obj="entertainment", params={})
        )
    ]
    
    for i, (original_text, gt_obj) in enumerate(test_cases, 1):
        print(f"\n--- Test Case {i} ---")
        print(f"Original: \"{original_text}\"")
        original_tokens = count_tokens(original_text)
        print(f"Original tokens: {original_tokens}")
        
        for level in [2, 3, 4]:  # Skip level 1 for brevity
            gittertalk_str = gittertalk_to_string(gt_obj, level)
            level_tokens = count_tokens(gittertalk_str)
            reduction = ((original_tokens - level_tokens) / original_tokens) * 100
            print(f"  Level {level}: \"{gittertalk_str}\" ({level_tokens} tokens, {reduction:.1f}% reduction)")

if __name__ == "__main__":
    try:
        test_updated_abbreviations()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
