import tiktoken
from gittertalk import gittertalk, gittertalk_to_string
from typing import List, Dict, Tuple

def count_tokens(text: str, model: str = "gpt-3.5-turbo") -> int:
    """Count tokens using OpenAI's tiktoken library"""
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

def test_token_efficiency():
    """Test and prove gittertalk's token efficiency claims"""
    
    # Test cases: (original_human_text, expected_gittertalk_object)
    test_cases = [
        (
            "okay so im coming from NYC. i need to get a flight to albuquerque NM TOMORROW. PLEASE tell me theres one available",
            gittertalk(act="flight", obj="Flight", params={"from": "NYC", "to": "ABQ", "when": "+1", "check": "availability"})
        ),
        (
            "I want to book a hotel room in Paris for next week, preferably something nice but not too expensive",
            gittertalk(act="hotel", obj="Hotel", params={"location": "Paris", "when": "+7", "type": "mid-range"})
        ),
        (
            "Can you tell me what's happening with Tesla stock today? I need the latest news and analysis",
            gittertalk(act="news", obj="Tesla", params={"type": "stock", "when": "today", "detail": "analysis"})
        ),
        (
            "I'm really stressed out from work. Can you tell me a funny joke to cheer me up?",
            gittertalk(act="joke", obj="entertainment", params={"mood": "stressed", "purpose": "cheer_up"})
        ),
        (
            "I need to find a rental car in Los Angeles for this weekend, something economical would be great",
            gittertalk(act="car", obj="rental", params={"location": "LAX", "when": "weekend", "type": "economy"})
        )
    ]
    
    print("=" * 80)
    print("GITTERTALK TOKEN EFFICIENCY ANALYSIS")
    print("=" * 80)
    
    total_original_tokens = 0
    total_level_tokens = {1: 0, 2: 0, 3: 0, 4: 0}
    
    for i, (original_text, gt_obj) in enumerate(test_cases, 1):
        print(f"\n--- Test Case {i} ---")
        print(f"Original: \"{original_text}\"")
        
        original_tokens = count_tokens(original_text)
        total_original_tokens += original_tokens
        print(f"Original tokens: {original_tokens}")
        
        for level in [1, 2, 3, 4]:
            gittertalk_str = gittertalk_to_string(gt_obj, level)
            level_tokens = count_tokens(gittertalk_str)
            total_level_tokens[level] += level_tokens
            
            reduction = ((original_tokens - level_tokens) / original_tokens) * 100
            print(f"Level {level}: \"{gittertalk_str}\" ({level_tokens} tokens, {reduction:.1f}% reduction)")
    
    print("\n" + "=" * 80)
    print("OVERALL EFFICIENCY SUMMARY")
    print("=" * 80)
    
    for level in [1, 2, 3, 4]:
        total_reduction = ((total_original_tokens - total_level_tokens[level]) / total_original_tokens) * 100
        efficiency_target = {1: "Current", 2: "60%", 3: "40%", 4: "20%"}[level]
        
        print(f"Level {level} ({efficiency_target} target):")
        print(f"  Total original tokens: {total_original_tokens}")
        print(f"  Total gittertalk tokens: {total_level_tokens[level]}")
        print(f"  Actual reduction: {total_reduction:.1f}%")
        print(f"  Tokens saved: {total_original_tokens - total_level_tokens[level]}")
        print()
    
    # Verify the 80% claim
    level_4_reduction = ((total_original_tokens - total_level_tokens[4]) / total_original_tokens) * 100
    claim_verified = level_4_reduction >= 80.0
    
    print("=" * 80)
    print("CLAIM VERIFICATION")
    print("=" * 80)
    print(f"README Claim: 'Token usage by up to 80% (Level 4 verbosity)'")
    print(f"Actual Level 4 reduction: {level_4_reduction:.1f}%")
    print(f"Claim verified: {'✅ YES' if claim_verified else '❌ NO'}")
    
    if not claim_verified:
        print(f"Recommendation: Update README to claim 'up to {level_4_reduction:.0f}%' reduction")
    
    return {
        'original_tokens': total_original_tokens,
        'level_tokens': total_level_tokens,
        'reductions': {level: ((total_original_tokens - tokens) / total_original_tokens) * 100 
                      for level, tokens in total_level_tokens.items()},
        'claim_verified': claim_verified
    }

def test_pipeline_efficiency():
    """Test efficiency in a full pipeline context"""
    print("\n" + "=" * 80)
    print("PIPELINE EFFICIENCY ANALYSIS")
    print("=" * 80)
    
    # Simulate a multi-stage pipeline where gittertalk is passed between stages
    original_request = "I need to book a flight from New York to Los Angeles tomorrow morning, check if business class is available"
    gt_obj = gittertalk(
        act="flight", 
        obj="booking", 
        params={"from": "NYC", "to": "LAX", "when": "+1", "time": "morning", "class": "business", "check": "availability"}
    )
    
    print(f"Original request: \"{original_request}\"")
    print(f"Original tokens: {count_tokens(original_request)}")
    print()
    
    # Simulate passing this through 5 pipeline stages
    stages = ["Feeder", "Interpreter", "Router", "Department", "Response Generator"]
    
    for level in [1, 2, 3, 4]:
        gittertalk_str = gittertalk_to_string(gt_obj, level)
        gittertalk_tokens = count_tokens(gittertalk_str)
        
        # Calculate tokens if we passed original text vs gittertalk through pipeline
        original_pipeline_tokens = count_tokens(original_request) * len(stages)
        gittertalk_pipeline_tokens = gittertalk_tokens * len(stages)
        
        pipeline_savings = original_pipeline_tokens - gittertalk_pipeline_tokens
        pipeline_reduction = (pipeline_savings / original_pipeline_tokens) * 100
        
        print(f"Level {level} Pipeline Efficiency:")
        print(f"  Gittertalk: \"{gittertalk_str}\"")
        print(f"  Original text × 5 stages: {original_pipeline_tokens} tokens")
        print(f"  Gittertalk × 5 stages: {gittertalk_pipeline_tokens} tokens")
        print(f"  Pipeline savings: {pipeline_savings} tokens ({pipeline_reduction:.1f}% reduction)")
        print()

if __name__ == "__main__":
    # You'll need to install tiktoken first
    print("Installing tiktoken for token counting...")
    print("Run: pip install tiktoken")
    print()
    
    try:
        results = test_token_efficiency()
        test_pipeline_efficiency()
    except ImportError:
        print("Please install tiktoken: pip install tiktoken")