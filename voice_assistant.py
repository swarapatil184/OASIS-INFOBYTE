"""
Voice Assistant - Python Project 1 (Beginner Level)
====================================================
A text-based assistant that responds to your commands!
Features:
  - Greetings and responses
  - Tell the time and date
  - Simple web search (opens browser)
  - Tell jokes
  - Basic calculator
  - Exit command

HOW TO RUN:
    python voice_assistant.py

No extra libraries needed — uses only built-in Python!
"""

import datetime
import webbrowser
import random


# =============================================
#   RESPONSES DATABASE
# =============================================

GREETINGS = ["hello", "hi", "hey", "good morning", "good evening", "good afternoon", "howdy"]

GREETING_REPLIES = [
    "Hello! How can I help you today? 😊",
    "Hi there! What can I do for you?",
    "Hey! I'm your Python assistant. Ask me anything!",
    "Good to see you! How can I assist?",
]

JOKES = [
    "Why do programmers prefer dark mode?\n   Because light attracts bugs! 🐛",
    "Why did the Python script break up with Java?\n   Because it couldn't handle the exceptions! 😄",
    "What do you call a sleeping dinosaur?\n   A dino-snore! 😴",
    "Why don't scientists trust atoms?\n   Because they make up everything! ⚛️",
    "What's a computer's favorite snack?\n   Microchips! 💻",
    "Why did the programmer quit his job?\n   Because he didn't get arrays (a raise)! 📊",
]

FAREWELLS = ["bye", "goodbye", "exit", "quit", "see you", "farewell", "stop"]

ABOUT_REPLIES = [
    "I'm a simple Python Voice Assistant built for Project 1!",
    "I'm your friendly Python assistant. I can tell jokes, give time/date, and search the web!",
]


# =============================================
#   HELPER FUNCTIONS
# =============================================

def get_time():
    now = datetime.datetime.now()
    return now.strftime("⏰ Current time: %I:%M %p")


def get_date():
    today = datetime.date.today()
    return today.strftime("📅 Today is: %A, %B %d, %Y")


def web_search(query):
    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    webbrowser.open(search_url)
    return f"🌐 Opening Google search for: '{query}'"


def calculate(expression):
    """Simple calculator — handles basic math safely."""
    try:
        # Only allow safe math characters
        allowed = set("0123456789 +-*/.() ")
        if not all(c in allowed for c in expression):
            return "❌ I can only calculate basic math (+ - * /)"
        result = eval(expression)
        return f"🧮 Result: {expression} = {result}"
    except ZeroDivisionError:
        return "❌ Oops! You can't divide by zero."
    except Exception:
        return "❌ I couldn't calculate that. Try something like: calculate 5 + 3"


def tell_joke():
    return "😄 Here's a joke:\n\n   " + random.choice(JOKES)


def show_help():
    return """
📋 Here's what I can do:
─────────────────────────────────────
  hello / hi          → Greet me
  time                → Get current time
  date                → Get today's date
  joke                → Hear a joke
  search <topic>      → Search the web
  calculate <math>    → Do math (e.g., calculate 5 + 3)
  about               → About this assistant
  help                → Show this menu
  bye / exit          → Quit
─────────────────────────────────────"""


# =============================================
#   MAIN ASSISTANT LOGIC
# =============================================

def process_command(user_input):
    """Takes user input and returns the assistant's response."""
    
    command = user_input.lower().strip()

    # --- Greeting ---
    if any(greet in command for greet in GREETINGS):
        return random.choice(GREETING_REPLIES)

    # --- Time ---
    elif "time" in command:
        return get_time()

    # --- Date ---
    elif "date" in command or "today" in command or "day" in command:
        return get_date()

    # --- Joke ---
    elif "joke" in command or "funny" in command or "laugh" in command:
        return tell_joke()

    # --- Web Search ---
    elif command.startswith("search "):
        query = user_input[7:].strip()
        if query:
            return web_search(query)
        else:
            return "❓ What should I search? Try: search Python tutorials"

    # --- Calculator ---
    elif command.startswith("calculate ") or command.startswith("calc "):
        expression = command.replace("calculate", "").replace("calc", "").strip()
        if expression:
            return calculate(expression)
        else:
            return "❓ What should I calculate? Try: calculate 10 * 5"

    # --- About ---
    elif "about" in command or "who are you" in command or "what are you" in command:
        return random.choice(ABOUT_REPLIES)

    # --- Help ---
    elif "help" in command or "what can you do" in command:
        return show_help()

    # --- Farewell ---
    elif any(word in command for word in FAREWELLS):
        return "EXIT"

    # --- Unknown Command ---
    else:
        return (
            f"🤔 I didn't understand: '{user_input}'\n"
            "   Type 'help' to see what I can do!"
        )


# =============================================
#   MAIN PROGRAM
# =============================================

def main():
    print("=" * 47)
    print("   🤖  Python Voice Assistant  🤖")
    print("       Python Programming - Project 1")
    print("=" * 47)
    print("   Type your command below. Type 'help' to")
    print("   see all commands. Type 'bye' to quit.")
    print("=" * 47)
    print()

    while True:
        try:
            # Get user input
            user_input = input("You: ").strip()

            # Skip empty input
            if not user_input:
                continue

            # Process the command
            response = process_command(user_input)

            # Check if user wants to exit
            if response == "EXIT":
                print("\nAssistant: 👋 Goodbye! Have a great day!")
                break

            # Print the assistant's response
            print(f"\nAssistant: {response}\n")

        except KeyboardInterrupt:
            print("\n\nAssistant: 👋 Goodbye! (Interrupted)")
            break


# Entry point
if __name__ == "__main__":
    main()
