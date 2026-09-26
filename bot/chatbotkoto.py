import random
import re
import sys

# Fix for Windows console UnicodeEncodeError with emojis
try:
    sys.stdout.reconfigure(encoding="utf-8")
except AttributeError:
    pass

BOT_PERSONALITY = {
    "W_RIZZ": [
        "Damn, that's giving me butterflies! Total slay, no cap! 💅",
        "Sheesh! So smooth, you can totally send that right away! 🔥",
        "Oh look, we got a Rizz God over here! Smooth, they're definitely gonna swoon, bet!",
    ],
    "MID_RIZZ": [
        "It's okay, but kinda basic. Feels like you just pulled it off TikTok, ngl.",
        "It has potential, but it feels a bit short on drama and confidence.",
        "Hmm, pretty mid vibes. Not quite swoon-worthy, but not embarrassing either.",
    ],
    "L_RIZZ": [
        "Yikes, bestie! Do not send that, it's majorly cringe and sus! 😭",
        "Major L Rizz! If you say that, they might just block you out of nowhere, no cap.",
        "Oof, I'm almost crying for you bestie... delete that right now!",
    ],
}

# Hiwalay na ang Classic Pick-up Lines at Rizz Jokes
PICKUP_SETS = [
    {
        "set_name": "Classic & Smooth Pick-up Lines",
        "options": [
            {
                "line": "Are you coffee? Because you make my heart beat faster. ☕",
                "next_followups": [
                    "Your next chat: 'Seriously, when are we going on a coffee date?' 😉",
                    "If they reply: 'But coffee tastes even better when I'm with you.' ☕❤️",
                ],
            },
            {
                "line": "Do you have a map? I keep getting lost in your eyes. 👀",
                "next_followups": [
                    "When they reply: 'Don't worry, at least I found you.' ✨",
                    "Your next line: 'Looks like I've wandered into your heart too.' 🗺️",
                ],
            },
            {
                "line": "Are you from Pandi? Because my world revolves around you. 🌍",
                "next_followups": [
                    "Next line: 'No matter where I go, I always find my way back to you.' 🏠",
                    "If they react with haha: 'For real, this ain't just a basic pickup line!' 💯",
                ],
            },
        ],
    }
]

JOKE_SETS = [
    {
        "set_name": "Rizz Jokes & Ice Breakers",
        "options": [
            {
                "line": "What fish is the luckiest? It's 'Tilapia'... because ti-choose (tilapi-piliin) you every single day! 🐟",
                "next_followups": [
                    "Follow it up with: 'That's why you're my favorite choice every day!' 🥰",
                    "If they laugh: 'See, came with a side of kilig!' 💅",
                ],
            },
            {
                "line": "What kind of gun doesn't hurt? 'Guns'... Guns-to (Gusto) you, slay! 🔥",
                "next_followups": [
                    "Follow with: 'Bang! Straight to your heart.' 💘",
                    "If they reply with an emoji: 'Let me take you out so you don't have to look for anyone else.' 🍔",
                ],
            },
            {
                "line": "Are you head lice? Because you just won't get out of my brain! 🧠",
                "next_followups": [
                    "Follow with: 'No matter what I do, you're all I think about.' 💭",
                    "If they call it corny: 'Corny maybe, but it only gets like this for you.' ❤️",
                ],
            },
        ],
    }
]

BOOST_WORDS = [
    "cute",
    "eyes",
    "smile",
    "star",
    "angel",
    "coffee",
    "sweet",
    "beautiful",
    "pretty",
    "gorgeous",
    "handsome",
    "love",
    "heaven",
    "look like",
]

CRINGE_WORDS = [
    "discord",
    "kitten",
    "feet",
    "sigma",
    "alpha",
    "skibidi",
    "uwu",
    "mewing",
]


def is_asking_for_joke(text):
    text_lower = text.lower()
    return any(w in text_lower for w in ["joke", "jokes", "funny", "tawa"])


def is_asking_for_pickup(text):
    text_lower = text.lower()
    return any(
        w in text_lower for w in ["pickup", "pick-up", "rizz", "suggestion"]
    )


def is_question(text):
    text_lower = text.lower().strip()
    if any(w in text_lower for w in ["angel", "eyes", "heaven", "star", "are you"]):
        return False
    if "?" in text:
        return True
    return any(re.search(p, text_lower) for p in [r"^\b(why|how|what|who|where|when)\b"])


def evaluate_line(line):
    line_lower = line.lower()
    score = 50
    words = line.split()

    if len(words) < 3:
        score -= 20
    elif 4 <= len(words) <= 12:
        score += 15
    else:
        score -= 10

    for word in BOOST_WORDS:
        if word in line_lower:
            score += 20

    for word in CRINGE_WORDS:
        if word in line_lower:
            score -= 30

    score += random.randint(-5, 5)
    return max(0, min(100, score))


def main():
    print("=" * 60)
    print("        🔥 SMART GEN Z RIZZ & CHAT BOT 🔥        ")
    print("=" * 60)

    state = "IDLE"
    current_options = []

    while True:
        user_input = input("You: ").strip()
        input_lower = user_input.lower()

        if input_lower in ["exit", "quit", "bye"]:
            print(
                "\nBot: Later bestie, catch you on the flip side! Stay rizzing, no cap! 👋"
            )
            break

        if not user_input:
            print("Bot: Why you so quiet, sus! Say something.\n")
            continue

        if state == "WAITING_SELECTION":
            if user_input in ["1", "2", "3"]:
                idx = int(user_input) - 1
                selected = current_options[idx]

                print(f'\nBot: Let\'s go! You picked: "{selected["line"]}" 🔥')
                print(
                    "Bot: Here are some follow-up lines you can use right after:"
                )

                for i, next_line in enumerate(
                    selected["next_followups"], start=1
                ):
                    print(f"    {i}. {next_line}")

                print(
                    "\nBot: Want more? Type 'joke' or 'pickup' anytime!\n"
                )
                state = "IDLE"
                continue
            else:
                print(
                    "Bot: Just pick 1, 2, or 3 from the choices above!\n"
                )
                continue

        # 1. INTENT: JOKE
        if is_asking_for_joke(user_input):
            chosen_set = random.choice(JOKE_SETS)
            current_options = chosen_set["options"]
            print(
                f"\nBot: Bet! Here are some funny [{chosen_set['set_name']}] for you:"
            )
            for i, opt in enumerate(current_options, start=1):
                print(f' {i}. "{opt["line"]}"')
            print(
                "\nBot: Pick 1, 2, or 3 and I'll give you the follow-up lines! 👇\n"
            )
            state = "WAITING_SELECTION"
            continue

        # 2. INTENT: PICKUP LINES / RIZZ
        if is_asking_for_pickup(user_input) or input_lower in ["more", "other"]:
            chosen_set = random.choice(PICKUP_SETS)
            current_options = chosen_set["options"]
            print(
                f"\nBot: Bet! Here are top-tier [{chosen_set['set_name']}] for you:"
            )
            for i, opt in enumerate(current_options, start=1):
                print(f' {i}. "{opt["line"]}"')
            print(
                "\nBot: Pick 1, 2, or 3 and I'll give you the follow-up lines! 👇\n"
            )
            state = "WAITING_SELECTION"
            continue

        if is_question(user_input):
            print(
                "\nBot: Good question! But for real, your day would be way better if you asked for a joke or a pick-up line. Try typing 'joke' or 'rizz'!\n"
            )
            continue

        # 3. DEFAULT: EVALUATE CUSTOM LINE
        score = evaluate_line(user_input)

        if score >= 70:
            tier_key = "W_RIZZ"
        elif score >= 40:
            tier_key = "MID_RIZZ"
        else:
            tier_key = "L_RIZZ"

        opinion = random.choice(BOT_PERSONALITY[tier_key])

        print(f"\nBot: {opinion}")
        print(f"Bot: [Score: {score}/100] Drop another one, bet!\n")


if __name__ == "__main__":
    main()