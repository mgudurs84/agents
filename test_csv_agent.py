#!/usr/bin/env python3
"""
Test the CSV to JSON Agent locally
"""

def test_agent():
    """Test the agent locally before deployment."""
    print("Testing CSV to JSON Agent")
    print("=" * 30)
    
    try:
        from csv_json_converter import root_agent
        
        test_cases = [
            "Hello!",
            """name,age,city
John,25,New York
Jane,30,London
Bob,35,Paris""",
        ]
        
        for i, test in enumerate(test_cases, 1):
            print(f"\n--- Test {i} ---")
            print(f"Input: {test[:50]}{'...' if len(test) > 50 else ''}")
            
            try:
                response = root_agent(test)
                print(f"Response: {response[:200]}{'...' if len(response) > 200 else ''}")
                print("SUCCESS")
            except Exception as e:
                print(f"ERROR: {e}")
        
        print("\nLocal testing complete!")
        
    except ImportError as e:
        print(f"Import failed: {e}")
        print("Run setup_clean.py first")

if __name__ == "__main__":
    test_agent()
