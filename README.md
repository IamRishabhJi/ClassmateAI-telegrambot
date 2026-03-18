# ClassMate AI Telegram Bot

Welcome to **ClassMate AI** – your personal study buddy for Punjab Technical University (PTU) and school students! This project is designed to make learning, revision, and exam prep easier, friendlier, and more interactive right inside Telegram.

---

## 🚀 What is ClassMate AI?
ClassMate AI is a Telegram chatbot that uses Google Gemini's latest AI models to answer questions, explain concepts, solve maths, help with assignments, and more. It supports English and Hinglish, and is tailored for PTU students but useful for anyone who wants clear, step-by-step help.

**Key Features:**
- 8 learning modes (General, Educational, Maths, Coding, Hinglish, Assignment, Exam Prep, Doubt Solver)
- 2/4/8-mark question answer modes for exam-style responses
- Step-by-step maths solutions
- Hinglish (Hindi+English) support
- Assignment and exam-ready answers
- Conversation history per user
- Friendly, simple language – never intimidating!

---

## 🛠️ Quick Start

1. **Clone this repo:**
   ```bash
   git clone <this-repo-url>
   cd AI-TelegramBot
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Get your API keys:**
   - **Google Gemini API Key:** [Get it here](https://aistudio.google.com/app/apikey)
   - **Telegram Bot Token:** Message [@BotFather](https://t.me/BotFather) on Telegram, create a new bot, and copy the token.
4. **Create a `.env` file:**
   ```env
   GOOGLE_API_KEY=your_google_key_here
   TELEGRAM_BOT_TOKEN=your_telegram_token_here
   ```
5. **Run the bot:**
   ```bash
   python telegram_bot.py
   ```
6. **Open Telegram, find your bot, and send `/start`!**

---

## 💡 How to Use
- Use `/mode` to pick your learning style (General, Educational, Maths, etc.)
- Ask any question – from maths to coding to theory
- For exam-style answers, pick 2-mark, 4-mark, or 8-mark mode
- Use `/help` for a guide to all features
- Use `/clear` to reset your conversation

---

## 🧑‍💻 For Developers

**Main Files:**
- `telegram_bot.py` – Main bot logic, Telegram integration, mode handling
- `prompts.py` – All prompt engineering, modes, roles, output formats, and language rules
- `requirements.txt` – Python dependencies
- `discover_models.py` – See all Gemini models available to your API key
- `verify_integration.py` – Test script to check if everything is set up right

**Prompt Engineering:**
- Easily add new modes, roles, or output formats in `prompts.py`
- All prompts are written to sound human, friendly, and exam-focused
- Supports both English and Hinglish (auto-detects language)

**Customization:**
- Add your own learning modes or answer styles in `prompts.py`
- Tweak the bot’s welcome/help messages in `telegram_bot.py`
- Use `.env` to keep your API keys safe

---

## 📁 Project Structure
- `telegram_bot.py` – Telegram bot logic
- `prompts.py` – Prompt templates and logic
- `requirements.txt` – Dependencies
- `main.py` – Minimal Gemini API test
- `discover_models.py` – List available Gemini models
- `verify_integration.py` – Integration test script
- `README.md` – You’re reading it!
- `README_COMPLETE.md`, `QUICKSTART.md`, `QUICK_REFERENCE.md`, `SETUP.md` – Extra docs

---

## 🙏 Credits
Made with ❤️ by Rishabh for PTU students and anyone who loves learning. Contributions, suggestions, and feedback are always welcome!

---

## 📬 Need Help?
- Open an issue on GitHub
- Or just ping your bot with `/help` for instant guidance

Happy learning! 🎓
