import re
import random
from difflib import SequenceMatcher

POKEMON_DB = [
    {
        "name": "Pikachu",
        "aliases": ["pikachu", "pika", "pepachu", "pekachu"],
        "type": "Electric",
        "is_legendary": False,
        "mid": False,
        "sus": False,
        "vibe": "Certified icon. Cheeks, charm, and a lightning tail. Rizz level: off the charts.",
        "counters": "Ground-type Pokémon (e.g., Garchomp, Swampert) are immune to Electric moves and hit back hard with Earthquake.",
    },
    {
        "name": "Charizard",
        "aliases": ["charizard", "charzar", "charizrd", "chazizard", "chazard", "cazard"],
        "type": "Fire / Flying",
        "is_legendary": False,
        "mid": False,
        "sus": False,
        "vibe": "Main character energy. Looks like a dragon, acts like a dragon, isn't a Dragon. Rizz: elite.",
        "counters": "Rock-type moves deal 4x damage! Water and Electric types (e.g., Blastoise, Zapdos) will easily slay it.",
    },
    {
        "name": "Mewtwo",
        "aliases": ["mewtwo", "mew2", "mewtwoo", "miwtu"],
        "type": "Psychic",
        "is_legendary": True,
        "mid": False,
        "sus": True,
        "vibe": "Dark, brooding, and powerful. Mysterious rizz for sure.",
        "counters": "Dark, Ghost, and Bug types (e.g., Tyranitar, Gengar, Scizor). Dark types are immune to its Psychic moves!",
    },
    {
        "name": "Rayquaza",
        "aliases": ["rayquaza", "rayquza", "rayquasa", "rewaza"],
        "type": "Dragon / Flying",
        "is_legendary": True,
        "mid": False,
        "sus": False,
        "vibe": "Sky-high royalty. Absolutely zero mid in this one.",
        "counters": "Ice-type moves deal 4x massive damage! Use Ice types like Mamoswine, Glaceon, or Weavile to counter it.",
    },
    {
        "name": "Arceus",
        "aliases": ["arceus", "arkeus", "arseus"],
        "type": "Normal (Default)",
        "is_legendary": True,
        "mid": False,
        "sus": False,
        "vibe": "Literally created the universe. Infinite rizz, nothing mid about it.",
        "counters": "Fighting-type moves (e.g., Lucario, Conkeldurr). Watch out for its hold items, its type can change!",
    },
    {
        "name": "Ditto",
        "aliases": ["ditto", "dito", "ditoh"],
        "type": "Normal",
        "is_legendary": False,
        "mid": True,
        "sus": True,
        "vibe": "Copy-paste energy. Lowkey mid on its own, rizz depends on who it's copying.",
        "counters": "Substitute users, Taunt users, or Pokémon with high HP/bad stats that ruin its transformed copy.",
    },
    {
        "name": "Gengar",
        "aliases": ["gengar", "gengr"],
        "type": "Ghost / Poison",
        "is_legendary": False,
        "mid": False,
        "sus": True,
        "vibe": "Chaotic troll energy with a grin that is 100% sus... and iconic.",
        "counters": "Dark, Psychic, Ghost, and Ground types (e.g., Alakazam, Tyranitar, Darkrai).",
    },
]

POKEMON_DB.extend([
    {
        "name": "Bulbasaur",
        "aliases": ["bulbasaur", "bulbasor", "bulbasour", "bulbasar", "bulba"],
        "type": "Grass / Poison",
        "is_legendary": False, "mid": False, "sus": False,
        "vibe": "Chill starter with a plant on its back. Underrated rizz, no cap.",
        "counters": "Fire, Flying, Ice, and Psychic types (e.g., Charizard, Articuno, Alakazam) hit it super effectively.",
    },
    {
        "name": "Squirtle",
        "aliases": ["squirtle", "squirtl", "skwirtle", "squirtel"],
        "type": "Water",
        "is_legendary": False, "mid": False, "sus": False,
        "vibe": "Shades-wearing Squirtle Squad energy. Pure cool factor.",
        "counters": "Grass and Electric types (e.g., Venusaur, Zapdos, Jolteon) are the easiest way to beat it.",
    },
    {
        "name": "Eevee",
        "aliases": ["eevee", "eevi", "eevie"],
        "type": "Normal",
        "is_legendary": False, "mid": False, "sus": False,
        "vibe": "Cute with so many glow-ups (evolutions). Main character potential.",
        "counters": "Fighting types (e.g., Lucario, Machamp) are the main counter since Eevee is weak to Fighting.",
    },
    {
        "name": "Snorlax",
        "aliases": ["snorlax", "snorlx", "snorlaks", "snorlex"],
        "type": "Normal",
        "is_legendary": False, "mid": False, "sus": True,
        "vibe": "Sleeps in the middle of the road and still wins. Lazy king energy.",
        "counters": "Fighting types (e.g., Machamp, Conkeldurr). Don't wake it up unless you're ready.",
    },
    {
        "name": "Lucario",
        "aliases": ["lucario", "lucaro", "lukario", "lucareo"],
        "type": "Fighting / Steel",
        "is_legendary": False, "mid": False, "sus": False,
        "vibe": "Aura-sensing martial artist. Serious sigma rizz.",
        "counters": "Fire, Fighting, and Ground types (e.g., Charizard, Machamp, Garchomp) hit it hard.",
    },
])

STATS = {
    "Pikachu": (320, 9), "Charizard": (534, 9), "Mewtwo": (680, 7),
    "Rayquaza": (680, 8), "Arceus": (720, 10), "Ditto": (288, 3), "Gengar": (500, 8),
}
STATS.update({
    "Bulbasaur": (318, 7), "Squirtle": (314, 8), "Eevee": (325, 8),
    "Snorlax": (540, 6), "Lucario": (525, 8),
})
SPEED = {
    "Pikachu": 90, "Charizard": 100, "Mewtwo": 130, "Rayquaza": 95, "Arceus": 120,
    "Ditto": 48, "Gengar": 110, "Bulbasaur": 45, "Squirtle": 43, "Eevee": 55,
    "Snorlax": 30, "Lucario": 90,
}
for _m in POKEMON_DB:
    _m["bst"], _m["rizz"] = STATS[_m["name"]]
    _m["spd"] = SPEED[_m["name"]]

POKEMON_WORDS = {a for m in POKEMON_DB for a in m["aliases"]}
NAMES = ", ".join(m["name"] for m in POKEMON_DB)

TYPES = {"normal", "fire", "water", "grass", "electric", "ice", "fighting", "poison",
         "ground", "flying", "psychic", "bug", "rock", "ghost", "dragon", "dark",
         "steel", "fairy"}

COUNTER_WORDS = {"counter", "counters", "beat", "defeat", "defit", "kill", "weak",
                 "weakness", "against", "win", "destroy"}
SLANG_WORDS = {"bet", "cap", "slay", "rizz", "sus", "mid", "nocap"}
FOLLOW_UP = {"only", "just", "type", "it", "also"}
OWN_WORDS = {"have", "got", "caught", "use", "own", "love", "favorite"}
STRONG_WORDS = {"strong", "strongest", "stronger", "powerful", "power", "op", "tough", "goat"}
COMPARE_WORDS = {"compare", "better", "vs", "versus", "than", "between"}
SMALLTALK = {"thanks", "thank", "thx", "ty", "lol", "lmao", "haha", "hahaha", "ok", "okay",
             "recommend", "suggest", "list", "show", "most", "later", "other"}
CHOOSE_WORDS = {"choose", "pick", "should", "recommend", "suggest", "starter", "team"}
FAST_WORDS = {"fastest", "fast", "speed", "quick", "faster"}
CUTE_WORDS = {"cute", "cutest", "adorable"}
LEGEND_WORDS = {"legendary", "legend", "mythical"}
GREETINGS = {"hi", "hello", "hey", "sup", "yo", "wsp"}
FILLER = {"what", "that", "this", "with", "have", "pokemon", "about", "tell", "does",
          "want", "like", "into", "from", "your", "know", "think", "good", "best"}
RESERVED = CHOOSE_WORDS | FAST_WORDS | CUTE_WORDS | STRONG_WORDS | COMPARE_WORDS | SMALLTALK | LEGEND_WORDS | COUNTER_WORDS | SLANG_WORDS | FOLLOW_UP | OWN_WORDS | GREETINGS | TYPES | FILLER

SWITCH_RE = re.compile(r"\b(another|other|different|next)\b.*\bpok[eé]mon\b")

SLANG_ONLY = {
    "bet": ["Bet! 🔥 Name a Pokémon and let's talk."],
    "no cap": ["No cap?? Okay, I believe you. Which Pokémon are we talking about?"],
    "cap": ["That's cap! 🧢 Which Pokémon are you talking about so I can fact-check?"],
    "slay": ["Slay! 💅 Now tell me a Pokémon name so I can slay with you."],
    "rizz": ["Rizz check! Tell me a Pokémon and I'll rate its rizz."],
    "mid": ["Mid?! Which Pokémon are you calling mid? Say it to my face."],
    "sus": ["Sus?! Who's being sus? Name the Pokémon."],
}

context = {"last_pokemon": None, "user_name": None}


def tokenize(text):
    return re.findall(r"[a-z0-9']+", text.lower().replace("é", "e"))


def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()


TYPO_VOCAB = {t for t in TYPES if len(t) >= 4} | {"counter", "counters", "defeat",
                                                  "legendary", "weakness", "weakest", "strongest", "pokemon", "fastest"}


def fix_typos(words):
    fixed = []
    for w in words:
        if len(w) >= 4 and w not in RESERVED and w not in POKEMON_WORDS:
            best = max(TYPO_VOCAB, key=lambda v: similarity(w, v))
            if similarity(w, best) >= 0.75:
                w = best
        fixed.append(w)
    return fixed


def match_word(word):
    for mon in POKEMON_DB:
        if word in mon["aliases"]:
            return mon
    if len(word) < 4 or word in RESERVED:
        return None
    best, best_score = None, 0.0
    for mon in POKEMON_DB:
        for alias in mon["aliases"]:
            if len(alias) >= 4:
                score = similarity(word, alias)
                if word[:3] == alias[:3] and word[-1] == alias[-1] and score >= 0.65:
                    score = max(score, 0.7)
                if score > best_score:
                    best, best_score = mon, score
    return best if best_score >= 0.7 else None


def find_all(user_input):
    found = []
    for word in tokenize(user_input):
        mon = match_word(word)
        if mon and mon not in found:
            found.append(mon)
    return found


def find_pokemon(user_input):
    found = find_all(user_input)
    return found[0] if found else None


def detect_slang(text, tokens):
    if "no cap" in text or "nocap" in tokens:
        return "no cap"
    for word in ("cap", "slay", "rizz", "mid", "sus", "bet"):
        if word in tokens:
            return word
    return None


def status_of(mon):
    return "Legendary Pokémon 👑" if mon["is_legendary"] else "Regular Pokémon ⚡"


WEAK_TO = {
    "Pikachu": {"ground"}, "Charizard": {"rock", "water", "electric"},
    "Mewtwo": {"dark", "ghost", "bug"}, "Rayquaza": {"ice", "dragon", "fairy", "rock"},
    "Arceus": {"fighting"}, "Ditto": {"fighting"},
    "Gengar": {"ghost", "dark", "psychic", "ground"},
}


WEAK_TO.update({
    "Bulbasaur": {"fire", "flying", "ice", "psychic"}, "Squirtle": {"grass", "electric"},
    "Eevee": {"fighting"}, "Snorlax": {"fighting"},
    "Lucario": {"fire", "fighting", "ground"},
})


def mon_types(mon):
    return set(re.findall(r"[a-z]+", mon["type"].lower())) & TYPES


def matchup_reply(a, b):
    a_hits = mon_types(a) & WEAK_TO[b["name"]]
    b_hits = mon_types(b) & WEAK_TO[a["name"]]
    an_, bn_ = a["name"], b["name"]
    if a_hits and not b_hits:
        verdict = (f"Yes! {an_}'s {'/'.join(sorted(a_hits)).title()} typing hits {bn_}'s "
                   f"weakness. Type advantage: {an_}. W! 🔥")
    elif b_hits and not a_hits:
        verdict = (f"Nope, {bn_}'s {'/'.join(sorted(b_hits)).title()} typing hits {an_}'s "
                   f"weakness, so {bn_} has the type advantage. L for {an_}. 😬")
    elif a_hits and b_hits:
        verdict = "Both hit each other's weaknesses! It's a wild fight, speed and stats decide. ⚔️"
    else:
        top = max((a, b), key=lambda m: m["bst"])
        if a["bst"] == b["bst"]:
            verdict = "Neither has a type advantage and stats are equal. Total toss-up!"
        else:
            verdict = (f"Neither has a type advantage, so stats decide: "
                       f"{top['name']} ({top['bst']}) edges it. 💪")
    return f"{an_} vs {bn_} ⚔️ {verdict}"


def article(word):
    return "an" if word[0].lower() in "aeiou" else "a"


def ranked():
    return sorted(POKEMON_DB, key=lambda m: m["bst"], reverse=True)


def strength_reply(mon):
    bst = mon["bst"]
    if bst >= 680:
        verdict = "Certified powerhouse 💪"
    elif bst >= 500:
        verdict = "Pretty strong, no cap 💪"
    elif bst >= 400:
        verdict = "Decent, but not the strongest."
    else:
        verdict = "Low on raw stats, but it can still slay with strategy."
    return (f"{mon['name']}'s total base stats are {bst} "
            f"(rank {ranked().index(mon) + 1} of {len(POKEMON_DB)}). {verdict}")


def pick_best(pool):
    return max(pool, key=lambda m: (m["bst"], m["spd"]))


def reasons(mon):
    order = ranked()
    weak_set = sorted(WEAK_TO[mon["name"]])
    weak = ", ".join(w.title() for w in weak_set)
    only = "only " if len(weak_set) == 1 else ""
    return (f"{mon['bst']} base stats (rank {order.index(mon) + 1} of {len(order)}), "
            f"speed {mon['spd']}, and it's {only}weak to {weak}. {mon['vibe']}")


def choose_reply(best, pool, label):
    others = sorted((m for m in pool if m is not best), key=lambda m: -m["bst"])
    msg = f"My pick for {label}: **{best['name']}**! 🔥\nWhy: {reasons(best)}"
    if others:
        msg += f"\nRunner-up: {others[0]['name']} ({others[0]['bst']} stats)."
    if label == "starter":
        msg += "\n(Charmander isn't in my database, but Charizard is its final form!)"
    context["last_pokemon"] = best
    return msg


def dream_team():
    order = ranked()
    team = [order[0]]
    while len(team) < 3:
        used = set().union(*(WEAK_TO[t["name"]] for t in team))
        rest = [m for m in order if m not in team]
        team.append(min(rest, key=lambda m: (len(WEAK_TO[m["name"]] & used), -m["bst"])))
    weak = sorted(set().union(*(WEAK_TO[m["name"]] for m in team)))
    return ("My dream team: " + ", ".join(m["name"] for m in team)
            + " 💪\nI picked high stats with few shared weaknesses. "
            + f"Team weak to: {', '.join(w.title() for w in weak)}.")


def general_reply(text, tokens, refers_back):
    order = ranked()

    if tokens & {"thanks", "thank", "thx", "ty"}:
        return "You're welcome! W convo. 🔥 Wanna talk about another Pokémon?"
    if tokens & {"lol", "lmao", "haha", "hahaha"}:
        return "💀 fr fr. Anyway, which Pokémon are we talking about next?"
    if "later" in tokens or tokens & {"bye", "goodbye", "cya"}:
        return "Peace out! ✌️ Come back anytime, no cap."
    if tokens & {"ok", "okay"} and len(tokens) <= 2:
        return "Bet. Name a Pokémon whenever you're ready. 😎"
    if re.search(r"who are you|what can you do|what are you|\bhelp\b", text):
        return ("I'm a Pokémon Gen Z bot! Ask me about a Pokémon's type, counters, strength, "
                "rizz, or if it's mid, sus or legendary. No cap! 🔥")

    m = re.search(r"do you know (?:about )?(\w+)", text)
    if m and m.group(1) not in {"any", "all", "pokemon", "a", "the", "some", "about"}:
        return (f"Hmm, I don't know '{m.group(1)}' yet 😅 That's not in my database. "
                f"I only know: {NAMES}.")
    if re.search(r"are you sure|for real|really\b", text):
        last = context["last_pokemon"]
        extra = f" {last['name']} is {article(last['type'])} {last['type']} type." if last else ""
        return f"100% sure, no cap! ✅{extra}"

    if "why" in tokens and len(tokens) <= 2 and not context["last_pokemon"]:
        return "Why what? 😅 Tell me a Pokémon first, then ask me why."
    if tokens & FAST_WORDS and not refers_back:
        fast = sorted(POKEMON_DB, key=lambda m: -m["spd"])[:3]
        return ("Fastest on speed stat: " + ", ".join(f"{m['name']} ({m['spd']})" for m in fast)
                + f". {fast[0]['name']} moves first, no cap! ⚡")
    if tokens & CUTE_WORDS:
        return "Cutest? Eevee and Pikachu, easy. 🥹 Squirtle with the shades is a close third!"

    types = sorted(tokens & TYPES)
    wants_choice = bool(tokens & (CHOOSE_WORDS | {"best"})) and not tokens & COUNTER_WORDS
    if wants_choice and "team" in tokens:
        return dream_team()
    if wants_choice:
        pool, label = POKEMON_DB, "overall"
        if tokens & LEGEND_WORDS:
            pool, label = [m for m in POKEMON_DB if m["is_legendary"]], "legendary"
        elif "starter" in tokens:
            pool, label = [m for m in POKEMON_DB if m["name"] in ("Bulbasaur", "Squirtle")], "starter"
        elif types:
            pool = [m for m in POKEMON_DB if set(types) & mon_types(m)]
            label = "/".join(t.title() for t in types) + " type"
        if not pool:
            return f"I don't have any {label} Pokémon yet. 😅 Try asking for another type!"
        best = pick_best(pool)
        if tokens & {"recommend", "suggest"} and label == "overall":
            best = random.choice(order[:5])
        return choose_reply(best, pool, label)
    if types and "pokemon" in tokens and not refers_back and not tokens & COUNTER_WORDS:
        pool = [m for m in POKEMON_DB if set(types) & mon_types(m)]
        label = "/".join(t.title() for t in types)
        if pool:
            return f"{label}-type Pokémon I know: " + ", ".join(m["name"] for m in pool) + ". Pick one! 🔥"
        return f"I don't have any {label}-type Pokémon yet. 😅"

    if tokens & LEGEND_WORDS and not refers_back:
        legends = [m for m in order if m["is_legendary"]]
        return "Legendary squad 👑: " + ", ".join(f"{m['name']} ({m['bst']})" for m in legends)
    if "rizz" in tokens and tokens & {"most", "best", "who", "which", "highest"}:
        top = max(POKEMON_DB, key=lambda m: m["rizz"])
        return f"{top['name']} has the most rizz ({top['rizz']}/10)! 😎 {top['vibe']}"
    if tokens & STRONG_WORDS and not (context["last_pokemon"] and refers_back):
        top = order[:3]
        return ("Want a strong one? Top 3 by base stats: "
                + ", ".join(f"{m['name']} ({m['bst']})" for m in top)
                + f". {top[0]['name']} is the GOAT, no cap! 🔥")
    if tokens & {"weak", "weakest"} and "pokemon" in tokens and not refers_back:
        low = order[::-1][:2]
        return ("Weakest on stats: " + ", ".join(f"{m['name']} ({m['bst']})" for m in low)
                + ". But don't sleep on them, strategy can still slay! 😤")
    if tokens & {"favorite", "fav"}:
        m = random.choice(POKEMON_DB)
        return f"My fave? {m['name']}! {m['vibe']} 🔥"
    if "list" in tokens or re.search(r"\ball\b.*pokemon|do you know", text):
        return f"Here's my squad: {NAMES}. Pick one! 🔥"
    return None


def generate_response(user_input, mon):
    text = user_input.lower().replace("é", "e")
    tokens = set(fix_typos(tokenize(text)))
    mons = find_all(text)
    mon = mon or (mons[0] if mons else None)

    m = re.search(r"my n\w{2,3}e is (\w+)|call me (\w+)", user_input, re.IGNORECASE)
    if m:
        name_ = (m.group(1) or m.group(2)).capitalize()
        context["user_name"] = name_
        return f"Yo {name_}! Nice to meet you, bet! 🔥 Which Pokémon do you have or want to talk about?"
    if re.search(r"what.?s my n\w{2,3}e|what is my n\w{2,3}e|who am i", text):
        if context["user_name"]:
            return f"You're {context['user_name']}, no cap! 😎"
        return "I don't know yet! Tell me: 'my name is ...' 😅"

    if SWITCH_RE.search(text):
        context["last_pokemon"] = None
        return f"Bet! Who do you want to talk about next? We have {NAMES}! 🔥"

    slang = detect_slang(text, tokens)
    wants_counter = bool(tokens & COUNTER_WORDS)
    claimed_types = [t for t in TYPES if t in tokens]
    refers_back = bool(tokens & {"this", "that", "it", "he", "she", "its"})

    if len(mons) >= 2 and tokens & COMPARE_WORDS:
        a, b = sorted(mons[:2], key=lambda m: m["bst"], reverse=True)
        context["last_pokemon"] = a
        if a["bst"] == b["bst"]:
            return (f"{a['name']} vs {b['name']}: tie on stats ({a['bst']} each)! "
                    f"Type matchups decide this one. ⚔️")
        return (f"{a['name']} takes the W! 💪 ({a['bst']} vs {b['name']}'s {b['bst']} base stats). "
                f"Type matchups can still flip it though.\nWhy: {reasons(a)}")

    if len(mons) >= 2 and wants_counter and not tokens & {"counter", "counters", "how"}:
        context["last_pokemon"] = mons[1]
        return matchup_reply(mons[0], mons[1])

    if len(mons) >= 2 and slang in ("sus", "mid", "rizz") and tokens & {"more", "most", "which", "who"}:
        a, b = mons[:2]
        if slang == "rizz":
            w = a if a["rizz"] >= b["rizz"] else b
            return f"{w['name']} has more rizz ({a['name']} {a['rizz']}/10 vs {b['name']} {b['rizz']}/10) 😎"
        hits = [m for m in (a, b) if m[slang]]
        if len(hits) == 1:
            return f"{hits[0]['name']} is definitely more {slang}. 👀 {hits[0]['vibe']}"
        if len(hits) == 2:
            return f"Both {a['name']} and {b['name']} are {slang}, no cap. 💀"
        return f"Neither is {slang}, both are W. ✅"

    if len(mons) >= 2 and tokens & {"choose", "pick", "should", "or", "which"} and not tokens & OWN_WORDS:
        best = pick_best(mons)
        others = [m for m in mons if m is not best]
        context["last_pokemon"] = best
        return (f"I'd choose **{best['name']}**! 🔥\nWhy: {reasons(best)}\n"
                f"{', '.join(m['name'] for m in others)} is solid too ({others[0]['bst']} stats), "
                f"but it can't beat that.")

    if len(mons) >= 2 and not tokens & COMPARE_WORDS:
        if wants_counter:
            context["last_pokemon"] = mons[0]
            lines = [f"👉 **{m['name']}** ({m['type']}): {m['counters']}" for m in mons]
            return "Here's how to beat each one:\n" + "\n".join(lines) + "\nSlay that battle!"
        if tokens & OWN_WORDS or not slang:
            context["last_pokemon"] = mons[0]
            names = ", ".join(m["name"] for m in mons[:-1]) + f" and {mons[-1]['name']}"
            lines = [f"• {m['name']}: {m['type']} ({'Legendary 👑' if m['is_legendary'] else 'Regular ⚡'}, "
                     f"{m['bst']} stats)" for m in mons]
            weak = sorted(set().union(*(WEAK_TO[m["name"]] for m in mons)))
            top = max(mons, key=lambda m: m["bst"])
            return (f"Slay, you got {names}! 🔥\n" + "\n".join(lines)
                    + f"\nWatch out: your team is weak to {', '.join(w.title() for w in weak)}."
                    + f"\nTop dog: {top['name']} ({top['bst']}). Absolute W team!")

    if not mon:
        general = general_reply(text, tokens, refers_back)
        if general:
            return general

    if not mon and context["last_pokemon"] and (
            wants_counter or slang or claimed_types or tokens & FOLLOW_UP
            or tokens & LEGEND_WORDS or tokens & STRONG_WORDS
            or "why" in tokens or tokens & FAST_WORDS):
        mon = context["last_pokemon"]
    elif mon:
        context["last_pokemon"] = mon

    if not mon:
        if slang:
            return random.choice(SLANG_ONLY[slang])
        return (f"That sounds a bit sus... I couldn't tell which Pokémon you mean. "
                f"Try one of these: {NAMES}!")

    name, ptype, status = mon["name"], mon["type"], status_of(mon)
    an = article(ptype)

    if tokens & LEGEND_WORDS:
        if mon["is_legendary"]:
            return f"No cap, {name} is a Legendary Pokémon! 👑 Type: **{ptype}**. {mon['vibe']}"
        return (f"Cap! 🧢 {name} is NOT legendary, it's a Regular Pokémon ⚡ "
                f"({ptype} type). Still a W though.")

    if "why" in tokens and not wants_counter and not claimed_types:
        return f"Why {name}? {reasons(mon)}"

    if tokens & FAST_WORDS:
        rank = sorted(POKEMON_DB, key=lambda m: -m["spd"]).index(mon) + 1
        return f"{name}'s base speed is {mon['spd']} (rank {rank} of {len(POKEMON_DB)}). ⚡"

    if claimed_types and tokens & {"only", "just"}:
        return (f"Not only {claimed_types[0].title()}! Here's the full list for {name}: "
                f"{mon['counters']}")

    if claimed_types and not wants_counter:
        if any(t in ptype.lower() for t in claimed_types):
            opener = random.choice(["No cap, you're right!", "Facts! Slay!", "W knowledge, no cap!"])
            return f"{opener} {name} is {an} **{ptype}** type ({status})."
        return (f"Cap! 🧢 {name} is NOT {claimed_types[0].title()} type. "
                f"It's strictly **{ptype}** ({status}).")

    if wants_counter:
        return (f"Wanna defeat {name}? Easy! It's {an} {ptype} type ({status}).\n"
                f"👉 **Best Counter:** {mon['counters']} Slay that battle!")

    if tokens & STRONG_WORDS:
        return strength_reply(mon)

    if tokens & {"better", "think"}:
        return f"Respect the take! 🤝 {strength_reply(mon)}"

    if slang == "mid":
        if mon["mid"]:
            return f"Lowkey... yeah, {name} can be mid. 😬 {mon['vibe']}"
        return f"Mid?! {name} is NOT mid. That's cap! 🧢 {mon['vibe']}"
    if slang == "rizz":
        return f"Rizz check on {name} ({mon['rizz']}/10): {mon['vibe']} 😎"
    if slang == "slay":
        return f"{name} really did slay! 💅 It's {an} **{ptype}** type ({status})."
    if slang == "sus":
        if mon["sus"]:
            return f"Okay yeah, {name} is kinda sus. 👀 {mon['vibe']}"
        return f"{name} isn't sus, it's a straight W. ✅ {mon['vibe']}"
    if slang == "cap":
        return f"Cap?! 🧢 Fact check: {name} is {an} **{ptype}** type ({status})."
    if slang == "no cap":
        return f"No cap?? Then we're on the same page. {name} is {an} **{ptype}** type. {mon['vibe']}"
    if slang == "bet":
        return f"Bet! Ask me how to beat {name}, what type it is, or its rizz. 🔥"

    if tokens & OWN_WORDS:
        return f"Oh, that's a good Pokémon! {name} is a solid {ptype} type ({status}). Absolute W! 🔥"

    return (f"Oh, {name}? That's {an} **{ptype}** type ({status}).\n"
            f"👉 **Best Counter:** {mon['counters']} Zero cap!")


def main():
    print("=" * 60)
    print("⚡ POKÉMON CHATBOT (Gen Z Edition) ⚡")
    print("Try: 'how to defit rewaza', 'is ditto mid?', 'gengar can beat charizard?'")
    print("Type 'exit' to quit.")
    print("=" * 60)

    while True:
        user_input = input("\nYou: ").strip()
        if not user_input:
            continue
        if user_input.lower() in ("exit", "quit", "bye"):
            who = context["user_name"] or "bro"
            print(f"Chatbot: Bye {who}! Slay your Pokémon journey, no cap! 👋")
            break

        matched = find_pokemon(user_input)

        if not matched and set(tokenize(user_input)) & GREETINGS:
            who = f" {context['user_name']}" if context["user_name"] else ""
            print(f"Chatbot: Yo{who}! Tell me what Pokémon you have, love, or want to defeat! Bet! 🔥")
            continue

        print(f"Chatbot: {generate_response(user_input, matched)}")


if __name__ == "__main__":
    main()
