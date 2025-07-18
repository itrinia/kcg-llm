#!/usr/bin/env python3
"""
Interactive test script for the retail chatbot
"""

from retail_chatbot import setup_database, create_agent

def test_chatbot():
    print("Testing Retail Chatbot Components...")
    print("=" * 50)
    
    # Test database setup
    print("1. Testing database setup...")
    db_result = setup_database()
    print(f"   Database setup: {'✓ Success' if db_result else '✗ Failed'}")
    
    # Test agent creation
    print("\n2. Testing agent creation...")
    agent = create_agent()
    if agent:
        print("   ✓ Agent created successfully")
        
        # Test a simple question
        print("\n3. Testing a simple question...")
        try:
            response = agent.invoke({"input": "Which product category had the highest order demand in March 2016?"})
            print("   ✓ Question answered successfully!")
            print(f"   Answer: {response['output']}")
        except Exception as e:
            print(f"   ✗ Error answering question: {e}")
    else:
        print("   ✗ Agent creation failed")
    
    print("\n" + "=" * 50)
    print("Test completed!")

if __name__ == "__main__":
    test_chatbot() 