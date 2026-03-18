#!/usr/bin/env python3
"""
Discover available Gemini API models for your account.
This helps find the correct model name to use.
"""

import os
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    print("ERROR: GOOGLE_API_KEY not set in .env file")
    print("Please add: GOOGLE_API_KEY=your_key_here")
    exit(1)

print("=" * 70)
print("  Gemini API - Available Models Discovery")
print("  This lists all models available for your API key")
print("=" * 70)
print()

try:
    client = genai.Client(api_key=GOOGLE_API_KEY)

    print("Fetching available models...")
    print()

    # List available models
    models = client.models.list()

    print("AVAILABLE MODELS:")
    print("-" * 70)

    available_models = []
    for model in models:
        model_name = model.name
        # Extract just the model ID
        if "/" in model_name:
            model_id = model_name.split("/")[-1]
        else:
            model_id = model_name

        available_models.append(model_id)
        print(f"  {model_id}")

    print()
    print("=" * 70)
    print()

    if available_models:
        print("RECOMMENDATIONS:")
        print()

        # Find best model for free tier
        if "gemini-2.0-flash-lite" in available_models:
            print("✅ Best for free tier:")
            print("   model = 'gemini-2.0-flash-lite'")
        elif "gemini-2.0-flash" in available_models:
            print("✅ Good option:")
            print("   model = 'gemini-2.0-flash'")
        elif "gemini-1.5-flash" in available_models:
            print("✅ Good option:")
            print("   model = 'gemini-1.5-flash'")
        elif "gemini-pro" in available_models:
            print("✅ Classic option:")
            print("   model = 'gemini-pro'")
        else:
            print("✅ Use any of the above models")
            print(f"   model = '{available_models[0]}'")

        print()
        print("UPDATE YOUR CODE:")
        print()
        print("In telegram_bot.py, line 197-200, change:")
        print("  response = client.models.generate_content(")
        print("      model='YOUR_MODEL_NAME',")
        print("      contents=full_prompt,")
        print("  )")

    else:
        print("ERROR: No models found!")
        print("Check your API key and quota at: https://ai.dev/rate-limit")

except Exception as e:
    print(f"ERROR: {str(e)}")
    print()
    print("Possible solutions:")
    print("1. Verify GOOGLE_API_KEY is correct in .env")
    print("2. Check quota: https://ai.dev/rate-limit")
    print("3. Check API status: https://ai.google.dev/gemini-api")
    print("4. Regenerate API key if needed")

print()
