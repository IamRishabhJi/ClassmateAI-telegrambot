import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from google import genai
import prompts  # Import the prompts module

# Load environment variables from .env file if it exists
load_dotenv()

# Get API keys from environment variables
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Validate that required tokens are set
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY environment variable not set")
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN environment variable not set")

# Initialize Genai client with API key
client = genai.Client(api_key=GOOGLE_API_KEY)

# Default user mode settings
DEFAULT_MODE = "general"
DEFAULT_ROLE = "ptu_tutor"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    welcome_message = """
╔══════════════════════════════════════════════╗
║    🎓 Welcome to ClassMate AI! 🤖          ║
║   Made by Rishabh • For PTU Students        ║
╚══════════════════════════════════════════════╝

I'm here to help you learn! I can:
✅ Answer any question clearly
✅ Explain tough topics simply
✅ Help with assignments
✅ Prepare for exams
✅ Solve maths problems step-by-step
✅ Answer in English or Hinglish

**Commands:**
/start - Show this message
/mode - Choose your learning mode
/help - Get help
/clear - Reset conversation

**Just type your question and I'll help!**
    """
    await update.message.reply_text(welcome_message)

    # Initialize user data
    context.user_data["mode"] = DEFAULT_MODE
    context.user_data["role"] = DEFAULT_ROLE
    context.user_data["conversation"] = []


async def mode_select(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show mode selection buttons"""
    keyboard = [
        [InlineKeyboardButton("📚 General Q&A", callback_data="mode_general"),
         InlineKeyboardButton("🎓 Educational", callback_data="mode_educational")],
        [InlineKeyboardButton("📐 Maths Help", callback_data="mode_math"),
         InlineKeyboardButton("💻 Coding", callback_data="mode_coding")],
        [InlineKeyboardButton("🔤 Hinglish (Hindi)", callback_data="mode_hinglish"),
         InlineKeyboardButton("📝 Assignment", callback_data="mode_assignment")],
        [InlineKeyboardButton("📋 Exam Prep", callback_data="mode_exam"),
         InlineKeyboardButton("❓ Doubt Solver", callback_data="mode_doubt")],
        [InlineKeyboardButton("⭐ 2-Mark Q", callback_data="mode_2mark"),
         InlineKeyboardButton("⭐⭐ 4-Mark Q", callback_data="mode_4mark"),
         InlineKeyboardButton("⭐⭐⭐ 8-Mark Q", callback_data="mode_8mark")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🎯 **Choose your learning mode:**",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )


async def mode_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle mode selection"""
    query = update.callback_query
    await query.answer()

    mode_map = {
        "mode_general": ("general", "ptu_tutor", "General Mode - I'll answer all questions!"),
        "mode_educational": ("educational", "ptu_tutor", "🎓 Educational Mode - I'll explain topics simply!"),
        "mode_math": ("math", "math_teacher", "📐 Maths Mode - I'll solve problems step-by-step!"),
        "mode_coding": ("general", "coding_mentor", "💻 Coding Mode - I'll help with code!"),
        "mode_hinglish": ("hinglish", "doubt_solver", "🔤 Hinglish Mode - Dekh, main Hindi + English mein jawab dunga!"),
        "mode_assignment": ("assignment", "assignment_helper", "📝 Assignment Mode - I'll help you write good answers!"),
        "mode_exam": ("detailed", "exam_coach", "📋 Exam Prep Mode - I'll prepare you for exams!"),
        "mode_doubt": ("general", "doubt_solver", "❓ Doubt Solver - No doubt is too small!"),
        "mode_2mark": ("2mark", "ptu_tutor", "⭐ 2-Mark Mode - Short & precise answers!"),
        "mode_4mark": ("4mark", "ptu_tutor", "⭐⭐ 4-Mark Mode - Balanced & detailed answers!"),
        "mode_8mark": ("8mark", "ptu_tutor", "⭐⭐⭐ 8-Mark Mode - Comprehensive & detailed answers!"),
    }

    mode, role, message = mode_map.get(query.data, (DEFAULT_MODE, DEFAULT_ROLE, "Mode updated!"))

    context.user_data["mode"] = mode
    context.user_data["role"] = role
    context.user_data["conversation"] = []  # Reset conversation for new mode

    await query.edit_message_text(text=f"✅ {message}\n\nNow ask me anything!")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    help_message = """
📚 **ClassMate AI - Help Guide**

🎓 **What I Can Do:**
• Answer questions from any subject
• Explain hard topics in simple words
• Give step-by-step solutions
• Help with assignments
• Prepare you for exams
• Answer in English or Hinglish

🎯 **How to Use:**
1. Type `/mode` to choose your learning style
2. Ask any question
3. I'll give clear, easy-to-understand answers
4. Use `/clear` to start fresh

📋 **Available Modes:**
• **General** - Quick answers to any question
• **Educational** - Learn with examples
• **Maths** - Problems solved step-by-step
• **Coding** - Code help with explanations
• **Hinglish** - Hindi + English mix
• **Assignment** - Write better assignments
• **Exam Prep** - Get exam-ready answers
• **Doubt Solver** - Ask anything!
• **2-Mark Q** - Short answers (60-80 words)
• **4-Mark Q** - Medium answers (150-200 words)
• **8-Mark Q** - Detailed answers (300-400 words)

🎓 **Made by Rishabh • For PTU Students**
    """
    await update.message.reply_text(help_message, parse_mode="Markdown")


async def clear_context(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Clear conversation context"""
    context.user_data["conversation"] = []
    await update.message.reply_text("✅ Conversation cleared! Fresh start for you!")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle regular messages and generate AI responses"""
    user_message = update.message.text
    user_id = update.message.from_user.id
    username = update.message.from_user.first_name or "Student"

    # Show typing indicator
    await update.message.chat.send_action("typing")

    try:
        # Initialize user data if not exists
        if "mode" not in context.user_data:
            context.user_data["mode"] = DEFAULT_MODE
        if "role" not in context.user_data:
            context.user_data["role"] = DEFAULT_ROLE
        if "conversation" not in context.user_data:
            context.user_data["conversation"] = []

        mode = context.user_data.get("mode", DEFAULT_MODE)
        role = context.user_data.get("role", DEFAULT_ROLE)

        # Determine the subject if it's math mode
        is_math = mode == "math"

        # Build the system prompt based on selected mode and role
        system_prompt = prompts.build_full_prompt(
            mode=mode,
            role=role,
            use_chain_of_thought=True,
            is_math=is_math,
            subject=None
        )

        # Prepare conversation history
        conversation = context.user_data.get("conversation", [])

        # Build messages for API call
        messages = [
            {"role": "user", "content": system_prompt}  # System prompt as first user message
        ]

        # Add previous conversation history (limited to last 5 exchanges)
        for msg in conversation[-10:]:
            messages.append(msg)

        # Add current message
        messages.append({"role": "user", "content": user_message})

        # Generate response using Gemini with system prompt
        full_prompt = f"{system_prompt}\n\nStudent ({username}): {user_message}"

        response = client.models.generate_content(
            model="gemini-2.5-flash",  # Latest model - available March 2026!
            contents=full_prompt,
        )

        bot_response = response.text

        # Store in conversation history
        conversation.append({"role": "user", "content": user_message})
        conversation.append({"role": "assistant", "content": bot_response})
        context.user_data["conversation"] = conversation[-20:]  # Keep last 20 messages

        # Telegram has a 4096 character limit per message
        if len(bot_response) > 4096:
            # Split message into chunks
            for i in range(0, len(bot_response), 4096):
                await update.message.reply_text(bot_response[i:i+4096])
        else:
            await update.message.reply_text(bot_response)

    except Exception as e:
        error_message = f"❌ Error: {str(e)[:100]}"
        print(f"Error for user {user_id} ({username}): {str(e)}")
        await update.message.reply_text(error_message)


def main():
    """Start the bot"""
    print("╔════════════════════════════════════════╗")
    print("║  🚀 Starting ClassMate AI Bot...      ║")
    print("║  Made by Rishabh • For PTU Students   ║")
    print("╚════════════════════════════════════════╝")

    # Create the Application
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("mode", mode_select))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("clear", clear_context))

    # Add callback handler for mode selection
    application.add_handler(CallbackQueryHandler(mode_callback))

    # Add message handler for all text messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Bot is running! Send /start to begin...")
    # Run the bot
    application.run_polling()


if __name__ == "__main__":
    main()
