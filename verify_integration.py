#!/usr/bin/env python3
"""
Verification script to test ClassMate AI integration
Tests prompts.py and telegram_bot.py together
"""

import sys
import os

# Add the directory to path
sys.path.insert(0, os.path.dirname(__file__))

print("=" * 60)
print("   ClassMate AI - Integration Verification Script")
print("   Made by Rishabh - For PTU Students")
print("=" * 60)
print()

# Test 1: Check if required modules are installed
print("[Test 1] Checking required modules...")
try:
    import telegram
    print("  OK: python-telegram-bot installed")
except ImportError:
    print("  ERROR: python-telegram-bot NOT installed")
    sys.exit(1)

try:
    from google import genai
    print("  OK: google-genai installed")
except ImportError:
    print("  ERROR: google-genai NOT installed")
    sys.exit(1)

try:
    import dotenv
    print("  OK: python-dotenv installed")
except ImportError:
    print("  ERROR: python-dotenv NOT installed")
    sys.exit(1)

# Test 2: Check if .env file exists
print("\n[Test 2] Checking environment setup...")
if os.path.exists(".env"):
    print("  OK: .env file exists")
else:
    print("  WARNING: .env file not found (you'll need to create it)")

# Test 3: Check if prompts.py is loadable
print("\n[Test 3] Checking prompts.py...")
try:
    import prompts
    print("  OK: prompts.py imported successfully")

    # Check key functions
    options = prompts.list_all_options()
    print(f"  OK: Available modes: {', '.join(options['modes'])}")
    print(f"  OK: Available roles: {', '.join(options['roles'])}")
    print(f"  OK: Available formats: {', '.join(options['output_formats'])}")
except ImportError as e:
    print(f"  ERROR: Error importing prompts: {e}")
    sys.exit(1)

# Test 4: Test prompt building
print("\n[Test 4] Testing prompt generation...")
try:
    # Test general prompt
    general_prompt = prompts.get_system_prompt("general")
    print(f"  OK: General prompt: {len(general_prompt)} characters")

    # Test math prompt
    math_prompt = prompts.get_math_prompt("Integration")
    print(f"  OK: Math prompt: {len(math_prompt)} characters")

    # Test educational prompt
    edu_prompt = prompts.get_educational_prompt("Operating Systems")
    print(f"  OK: Educational prompt: {len(edu_prompt)} characters")

    # Test full prompt builder
    full_prompt = prompts.build_full_prompt(
        mode="educational",
        role="ptu_tutor",
        output_format="concept"
    )
    print(f"  OK: Full prompt: {len(full_prompt)} characters")
except Exception as e:
    print(f"  ERROR: Error generating prompts: {e}")
    sys.exit(1)

# Test 5: Check telegram_bot.py syntax
print("\n[Test 5] Checking telegram_bot.py syntax...")
try:
    with open("telegram_bot.py", "r", encoding="utf-8") as f:
        code = f.read()
    compile(code, "telegram_bot.py", "exec")
    print("  OK: telegram_bot.py syntax is valid")
except SyntaxError as e:
    print(f"  ERROR: Syntax error in telegram_bot.py: {e}")
    sys.exit(1)
except Exception as e:
    print(f"  ERROR: {e}")
    sys.exit(1)

# Test 6: Test few-shot examples
print("\n[Test 6] Testing few-shot examples...")
try:
    general_qa = prompts.get_few_shot_prompt("general_qa")
    print(f"  OK: General Q&A examples: {len(general_qa)} examples")

    hinglish_qa = prompts.get_few_shot_prompt("hinglish_qa")
    print(f"  OK: Hinglish Q&A examples: {len(hinglish_qa)} examples")

    math_qa = prompts.get_few_shot_prompt("math_qa")
    print(f"  OK: Math Q&A examples: {len(math_qa)} examples")
except Exception as e:
    print(f"  ERROR: Error with few-shot examples: {e}")
    sys.exit(1)

# Test 7: Test role-based prompts
print("\n[Test 7] Testing role-based prompts...")
try:
    roles = ["ptu_tutor", "math_teacher", "coding_mentor", "exam_coach", "assignment_helper", "doubt_solver"]
    for role in roles:
        role_prompt = prompts.get_role_prompt(role)
        print(f"  OK: {role}: {len(role_prompt)} characters")
except Exception as e:
    print(f"  ERROR: Error with role prompts: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("  ALL TESTS PASSED SUCCESSFULLY!")
print("=" * 60)
print()

print("[NEXT STEPS]")
print("  1. Create .env file with your API keys:")
print("     GOOGLE_API_KEY=your_key_here")
print("     TELEGRAM_BOT_TOKEN=your_token_here")
print("  2. Run: python telegram_bot.py")
print("  3. Find your bot on Telegram")
print("  4. Send /start to begin!")
print()
print("[FEATURES READY]")
print("  - 8 different learning modes")
print("  - 6 specialized roles")
print("  - Chain-of-thought reasoning")
print("  - Few-shot prompting")
print("  - Conversation history")
print("  - Hinglish support")
print("  - PTU exam-focused answers")
print()
