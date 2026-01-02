import google.generativeai as genai

api_key = "AIzaSyAbNvAQbKDRc-mKSU4ULR34AXs5o-yiQyI"

try:
    genai.configure(api_key=api_key)
    print(f"Testing API key: {api_key[:10]}...")
    
    print("Listing available models:")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
            
    print("\nSuccess! The API key is valid.")
    
except Exception as e:
    print(f"\nError: {e}")
