from __future__ import annotations
import re
import random
import time
import sys
import wikipedia
from datetime import datetime
from difflib import get_close_matches


#  typing effect 
def slow_print(text: str, delay: float = 0.03) -> None:
    for c in text:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(delay)
    print()


class Chatbot:
    def __init__(self) -> None:
        # Memory 
        self.memory = {"name": None}

        
        self.intents = [
            (re.compile(r"\b(hi|hello|hey|yo)\b", re.I), self._greet),
            (re.compile(r"\bhow (are|r) (you|u)\b", re.I), self._how_are_you),
            (re.compile(r"\bmy name is\s+([A-Za-z][A-Za-z\-']*)\b", re.I), self._remember_name),
            (re.compile(r"\bwhat is my name\b", re.I), self._recall_name),
            (re.compile(r"\bwhat'?s your name\b|\bwho are you\b", re.I), self._bot_name),
            (re.compile(r"\bwhat time is it\b|\bcurrent time\b|\btime\?\b", re.I), self._time),
            (re.compile(r"\bwhat'?s the date\b|\btoday'?s date\b|\bdate\?\b", re.I), self._date),
            (re.compile(r"\btell me a joke\b|\bjoke\b", re.I), self._joke),
            (re.compile(r"\b(help|commands)\b", re.I), self._help),
            (re.compile(r"\b(thank(s)?|ty)\b", re.I), self._thanks),
            (re.compile(r"\b(bye|exit|quit|goodbye)\b", re.I), self._goodbye),
            (re.compile(r"\b(sad|down|stressed|anxious|depressed)\b", re.I), self._support),
            (re.compile(r"\bcalc (.+)", re.I), self._calculator),
            (re.compile(r"\bdefine (.+)", re.I), self._define),
            (re.compile(r"\bwiki (.+)", re.I), self._wiki),
        ]

        # Known command keywords
        self.commands = [
            "hello", "how are you", "my name is <Name>", "what is my name",
            "what's your name", "time", "date", "joke", "help",
            "thanks", "bye", "calc <expression>", "define <word>", "wiki <topic>"
        ]


        self.greetings = ["Hey there! 👋", "Hello! 😊", "Hi!", "Yo! 😎", "Namaste! 🙏"]
        self.jokes = [
            "😂 Why do programmers prefer dark mode? Because light attracts bugs.",
            "💻 I told my computer I needed a break, and it said 'No problem—I'll go to sleep.'",
            "1️⃣0️⃣ There are 10 kinds of people: those who understand binary and those who don't.",
        ]
        self.how_are_you_responses = [
            "Doing great, thanks for asking! 🌟",
            "All good here, just running some Python code 🐍",
            "Fantastic! How about you? 😃",
            "I’m feeling awesome today 🚀"
        ]
        self.defaults = [
            "I didn’t quite get that 🤔",
            "Could you rephrase that? 😊",
            "Hmm, interesting... tell me more! 😃"
        ]

    def _greet(self, _: re.Match) -> str:
        name = self.memory.get("name")
        base = random.choice(self.greetings)
        return f"{base} {name}!" if name else base

    def _how_are_you(self, _: re.Match) -> str:
        return random.choice(self.how_are_you_responses)

    def _remember_name(self, m: re.Match) -> str:
        name = m.group(1).strip().title()
        self.memory["name"] = name
        return f"Nice to meet you, {name}! 😃"

    def _recall_name(self, _: re.Match) -> str:
        return f"Your name is {self.memory.get('name', 'I don’t know yet 😅')}"

    def _bot_name(self, _: re.Match) -> str:
        return "I'm a tiny Python chatbot 🤖. You can call me PyPal."

    def _time(self, _: re.Match) -> str:
        return datetime.now().strftime("⏰ It's %I:%M %p.")

    def _date(self, _: re.Match) -> str:
        return datetime.now().strftime("📅 Today is %A, %B %d, %Y.")

    def _joke(self, _: re.Match) -> str:
        return random.choice(self.jokes)

    def _help(self, _: re.Match) -> str:
        return "📝 Try: " + ", ".join(self.commands)

    def _thanks(self, _: re.Match) -> str:
        return "You're welcome! 🙌"

    def _goodbye(self, _: re.Match) -> str:
        return "Goodbye! Take care 👋\n__EXIT__"

    def _support(self, _: re.Match) -> str:
        return "🤗 I'm sorry you're feeling that way. Want to talk about it a bit more?"

    # calculator
    def _calculator(self, m: re.Match) -> str:
        expr = m.group(1).strip()
        try:
            if not re.match(r"^[0-9\.\+\-\*\/\(\)\s]+$", expr):
                return "❌ That doesn't look like a math expression."
            result = eval(expr, {"__builtins__": {}})
            return f"🧮 The result of {expr} is {result}"
        except Exception:
            return "❌ Sorry, I couldn't calculate that."

    def _define(self, m: re.Match) -> str:
        word = m.group(1).strip()
        fake_dict = {
            "python": "A powerful programming language 🐍",
            "chatbot": "A program designed to talk with humans 🤖",
            "ai": "Artificial Intelligence, making machines think like humans 🧠"
        }
        return fake_dict.get(word.lower(), f"❓ Sorry, I don’t know the meaning of '{word}'.")

    #  Wikipedia
    def _wiki(self, m: re.Match) -> str:
        topic = m.group(1).strip()
        try:
            summary = wikipedia.summary(topic, sentences=2)
            return f"🌍 Wikipedia says: {summary}"
        except Exception:
            return f"❌ Sorry, I couldn’t fetch info about '{topic}'."

 
    def respond(self, text: str) -> str:
        text = text.strip()
        if not text:
            return "Say something and I'll try to help. Type 'help' for options."

 
        for pattern, handler in self.intents:
            m = pattern.search(text)
            if m:
                return handler(m)

        suggestion = get_close_matches(text.lower(), [c.lower() for c in self.commands], n=1, cutoff=0.6)
        if suggestion:
            return f"🤔 Did you mean: '{suggestion[0]}'?"
        return random.choice(self.defaults)


def chat_loop():
    bot = Chatbot()
    slow_print("PyPal 🤖: Hi! Type 'help' to see what I can do. Type 'bye' to exit.")
    while True:
        try:
            user = input("You: ")
        except (EOFError, KeyboardInterrupt):
            slow_print("\nPyPal 🤖: Goodbye! 👋")
            break

        reply = bot.respond(user)
        if reply.endswith("__EXIT__"):
            slow_print("PyPal 🤖: " + reply.replace("__EXIT__", ""))
            break
        slow_print("PyPal 🤖: " + reply)


if __name__ == "__main__":
    chat_loop()
