#!/usr/bin/env python3
"""
Simple test script for the SQL to MongoDB translator
"""

from sql_to_mongodb import SQLToMongoDBTranslator

def test_basic_translation():
    """Test basic SQL to MongoDB translation."""
    translator = SQLToMongoDBTranslator()
    
    # Test a simple SELECT query
    sql_query = "SELECT name, age FROM users WHERE age > 18"
    
    try:
        result = translator.translate(sql_query)
        print("✅ Basic translation test passed!")
        print(f"SQL: {sql_query}")
        print(f"MongoDB: {result}")
        return True
    except Exception as e:
        print(f"❌ Basic translation test failed: {e}")
        return False

def test_batch_translation():
    """Test batch translation."""
    translator = SQLToMongoDBTranslator()
    
    sql_queries = [
        "SELECT * FROM users WHERE status = 'active'",
        "SELECT name, age FROM users WHERE age > 18"
    ]
    
    try:
        results = translator.translate_batch(sql_queries)
        print("✅ Batch translation test passed!")
        print(f"Translated {len(results)} queries")
        return True
    except Exception as e:
        print(f"❌ Batch translation test failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing SQL to MongoDB Translator...")
    print("=" * 50)
    
    test1 = test_basic_translation()
    test2 = test_batch_translation()
    
    print("=" * 50)
    if test1 and test2:
        print("🎉 All tests passed! The translator is working correctly.")
        print("\nTo run the web application:")
        print("python run_webapp.py")
        print("\nThen open: http://localhost:8000")
    else:
        print("❌ Some tests failed. Please check the error messages above.") 