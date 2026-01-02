
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

models_to_check = ["models/gemini-3-flash-preview", "models/gemini-2.5-flash", "models/gemini-3.0-fast"]

print("Checking specific models...")
for m_name in models_to_check:
    try:
        model = genai.GenerativeModel(m_name)
        # Just checking if we can instantiate, or maybe list it
        # The best way is to check if it's in list_models, but I already did that.
        # Let's try to get info if possible, or just rely on the previous list.
        print(f"Checking {m_name}...")
        # There isn't a direct 'get_model' that throws if not found easily without listing.
        # But I can check against the list again carefully.
        found = False
        for m in genai.list_models():
            if m.name == m_name or m.name == m_name.replace("models/", ""):
                found = True
                print(f"✅ Found: {m.name}")
                break
        if not found:
            print(f"❌ Not found in list: {m_name}")
            
    except Exception as e:
        print(f"Error checking {m_name}: {e}")
