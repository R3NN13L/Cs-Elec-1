import re
import random
from difflib import SequenceMatcher

POKEMON_DB = [
    {
        "name": "Pikachu",
        "aliases": ["pikachu", "pika", "pepachu", "pekachu", "picjahu", "pichaku", "pikatu"],
        "type": "Electric",
        "generation": 1,
        "is_legendary": False,
        "mid": False,
        "sus": False,
        "bst": 320,
        "spd": 90,
        "vibe": "Certified icon. Cheeks, charm, and a lightning tail. Rizz level: off the charts.",
        "counters": "Ground-type Pokémon are immune to Electric moves and hit back hard."
    },
    {
        "name": "Charizard",
        "aliases": ["charizard", "charzar", "charizrd", "chazizard", "chazard", "cazard", "charsard"],
        "type": "Fire / Flying",
        "generation": 1,
        "is_legendary": False,
        "mid": False,
        "sus": False,
        "bst": 534,
        "spd": 100,
        "vibe": "Main character energy. Looks like a dragon, acts like a dragon, isn't a Dragon.",
        "counters": "Rock-type moves deal 4x damage. Water and Electric types also hit it hard."
    },
    {
        "name": "Bulbasaur",
        "aliases": ["bulbasaur", "bulba", "bulbasor", "bulbasour", "bulbasar"],
        "type": "Grass / Poison",
        "generation": 1,
        "is_legendary": False,
        "mid": False,
        "sus": False,
        "bst": 318,
        "spd": 45,
        "vibe": "Chill starter with a plant on its back. Underrated rizz, no cap.",
        "counters": "Fire, Flying, Ice, and Psychic types."
    },
    {
        "name": "Squirtle",
        "aliases": ["squirtle", "squirtl", "skwirtle", "squirtel"],
        "type": "Water",
        "generation": 1,
        "is_legendary": False,
        "mid": False,
        "sus": False,
        "bst": 314,
        "spd": 43,
        "vibe": "Shades-wearing Squirtle Squad energy. Pure cool factor.",
        "counters": "Grass and Electric types."
    },
    {
        "name": "Mewtwo",
        "aliases": ["mewtwo", "mew2", "mewtwoo", "miwtu"],
        "type": "Psychic",
        "generation": 1,
        "is_legendary": True,
        "mid": False,
        "sus": True,
        "bst": 680,
        "spd": 130,
        "vibe": "Dark, brooding, and powerful. Mysterious rizz for sure.",
        "counters": "Dark, Ghost, and Bug types."
    },
    {
        "name": "Eevee",
        "aliases": ["eevee", "eevi", "eevie"],
        "type": "Normal",
        "generation": 1,
        "is_legendary": False,
        "mid": False,
        "sus": False,
        "bst": 325,
        "spd": 55,
        "vibe": "Cute with so many glow-ups. Main character potential.",
        "counters": "Fighting types."
    },
    {
        "name": "Snorlax",
        "aliases": ["snorlax", "snorlx", "snorlaks", "snorlex"],
        "type": "Normal",
        "generation": 1,
        "is_legendary": False,
        "mid": False,
        "sus": True,
        "bst": 540,
        "spd": 30,
        "vibe": "Sleeps in the middle of the road and still wins. Lazy king energy.",
        "counters": "Fighting types."
    },
    {
        "name": "Gengar",
        "aliases": ["gengar", "gengr"],
        "type": "Ghost / Poison",
        "generation": 1,
        "is_legendary": False,
        "mid": False,
        "sus": True,
        "bst": 500,
        "spd": 110,
        "vibe": "Chaotic troll energy with a grin that is 100% sus.",
        "counters": "Dark, Psychic, Ghost, and Ground types."
    },
    {
        "name": "Lucario",
        "aliases": ["lucario", "lucaro", "lukario", "lucareo", "lukaryo"],
        "type": "Fighting / Steel",
        "generation": 4,
        "is_legendary": False,
        "mid": False,
        "sus": False,
        "bst": 525,
        "spd": 90,
        "vibe": "Aura-sensing martial artist. Serious sigma rizz.",
        "counters": "Fire, Fighting, and Ground types."
    },
    {
        "name": "Arceus",
        "aliases": ["arceus", "arkeus", "arseus"],
        "type": "Normal",
        "generation": 4,
        "is_legendary": True,
        "mid": False,
        "sus": False,
        "bst": 720,
        "spd": 120,
        "vibe": "Literally created the universe. Infinite rizz.",
        "counters": "Fighting-type moves."
    },
    {
        "name": "Rayquaza",
        "aliases": ["rayquaza", "rayquza", "rayquasa", "rewaza"],
        "type": "Dragon / Flying",
        "generation": 3,
        "is_legendary": True,
        "mid": False,
        "sus": False,
        "bst": 680,
        "spd": 95,
        "vibe": "Sky-high royalty. Absolutely zero mid.",
        "counters": "Ice, Dragon, Fairy, and Rock types."
    },
    {
        "name": "Garchomp",
        "aliases": ["garchomp", "garchom", "garchomp"],
        "type": "Dragon / Ground",
        "generation": 4,
        "is_legendary": False,
        "mid": False,
        "sus": False,
        "bst": 600,
        "spd": 102,
        "vibe": "Land shark energy. Fast, strong, and built different.",
        "counters": "Ice, Dragon, and Fairy types."
    },
    {
        "name": "Tyranitar",
        "aliases": ["tyranitar", "tyranitar"],
        "type": "Rock / Dark",
        "generation": 2,
        "is_legendary": False,
        "mid": False,
        "sus": False,
        "bst": 600,
        "spd": 61,
        "vibe": "Walking natural disaster. Huge aura.",
        "counters": "Fighting, Ground, Steel, Water, Grass, Bug, Fairy, and other types."
    },
    {
        "name": "Greninja",
        "aliases": ["greninja", "grenija", "grininja"],
        "type": "Water / Dark",
        "generation": 6,
        "is_legendary": False,
        "mid": False,
        "sus": False,
        "bst": 530,
        "spd": 122,
        "vibe": "Ninja frog with insane speed and style.",
        "counters": "Electric, Grass, Fighting, Bug, and Fairy types."
    },
    {
        "name": "Gardevoir",
        "aliases": ["gardevoir", "gardevoirr", "gardevior"],
        "type": "Psychic / Fairy",
        "generation": 3,
        "is_legendary": False,
        "mid": False,
        "sus": False,
        "bst": 518,
        "spd": 80,
        "vibe": "Elegant psychic fairy with serious power.",
        "counters": "Ghost, Poison, and Steel types."
    },
    {
        "name": "Blaziken",
        "aliases": ["blaziken", "blaziken"],
        "type": "Fire / Fighting",
        "generation": 3,
        "is_legendary": False,
        "mid": False,
        "sus": False,
        "bst": 530,
        "spd": 80,
        "vibe": "Kickboxing chicken with legendary energy.",
        "counters": "Water, Ground, Flying, Psychic, and Fairy types."
    },
    {
        "name": "Sceptile",
        "aliases": ["sceptile", "septile", "sceptil"],
        "type": "Grass",
        "generation": 3,
        "is_legendary": False,
        "mid": False,
        "sus": False,
        "bst": 530,
        "spd": 120,
        "vibe": "Fast grass lizard with main character energy.",
        "counters": "Fire, Ice, Poison, Flying, and Bug types."
    },
    {
        "name": "Infernape",
        "aliases": ["infernape", "infernap", "infernape"],
        "type": "Fire / Fighting",
        "generation": 4,
        "is_legendary": False,
        "mid": False,
        "sus": False,
        "bst": 534,
        "spd": 108,
        "vibe": "Monkey with fire fists. Straight heat.",
        "counters": "Water, Ground, Flying, Psychic, and Fairy types."
    },
    {
        "name": "Metagross",
        "aliases": ["metagross", "metagros", "metagross"],
        "type": "Steel / Psychic",
        "generation": 3,
        "is_legendary": False,
        "mid": False,
        "sus": False,
        "bst": 600,
        "spd": 70,
        "vibe": "Four-brain supercomputer with insane physical power.",
        "counters": "Fire, Ground, Ghost, and Dark types."
    },
    {
        "name": "Salamence",
        "aliases": ["salamence", "salamens", "salamence"],
        "type": "Dragon / Flying",
        "generation": 3,
        "is_legendary": False,
        "mid": False,
        "sus": False,
        "bst": 600,
        "spd": 100,
        "vibe": "Dragon powerhouse with wings and attitude.",
        "counters": "Ice, Rock, Dragon, and Fairy types."
    },
    {
        "name": "Gyarados",
        "aliases": ["gyarados", "gyaradoss", "gyarado"],
        "type": "Water / Flying",
        "generation": 1,
        "is_legendary": False,
        "mid": False,
        "sus": False,
        "bst": 540,
        "spd": 81,
        "vibe": "Magikarp glow-up taken to the extreme.",
        "counters": "Electric and Rock types."
    },
    {
        "name": "Jolteon",
        "aliases": ["jolteon", "joltean", "joltion"],
        "type": "Electric",
        "generation": 1,
        "is_legendary": False,
        "mid": False,
        "sus": False,
        "bst": 525,
        "spd": 130,
        "vibe": "Electric speed demon. Very fast, very spicy.",
        "counters": "Ground types."
    },
    {
        "name": "Umbreon",
        "aliases": ["umbreon", "umbrean", "umbrion"],
        "type": "Dark",
        "generation": 2,
        "is_legendary": False,
        "mid": False,
        "sus": False,
        "bst": 525,
        "spd": 65,
        "vibe": "Dark Eeveelution with maximum mysterious aura.",
        "counters": "Fighting, Bug, and Fairy types."
    },
    {
        "name": "Heracross",
        "aliases": ["heracross", "heracros"],
        "type": "Bug / Fighting",
        "generation": 2,
        "is_legendary": False,
        "mid": False,
        "sus": False,
        "bst": 500,
        "spd": 85,
        "vibe": "Horned beetle that throws hands.",
        "counters": "Flying, Fire, Psychic, and Fairy types."
    },
    {
        "name": "Espeon",
        "aliases": ["espeon", "espean", "espeon"],
        "type": "Psychic",
        "generation": 2,
        "is_legendary": False,
        "mid": False,
        "sus": False,
        "bst": 525,
        "spd": 110,
        "vibe": "Psychic Eeveelution with elegant speed.",
        "counters": "Dark, Ghost, and Bug types."
    },
    {
        "name": "Dragonite",
        "aliases": ["dragonite", "dragonaite", "dragonit"],
        "type": "Dragon / Flying",
        "generation": 1,
        "is_legendary": False,
        "mid": False,
        "sus": False,
        "bst": 600,
        "spd": 80,
        "vibe": "Friendly-looking dragon that can absolutely throw down.",
        "counters": "Ice, Rock, Dragon, and Fairy types."
    },
    {
        "name": "Lapras",
        "aliases": ["lapras", "laprus", "lapress"],
        "type": "Water / Ice",
        "generation": 1,
        "is_legendary": False,
        "mid": False,
        "sus": False,
        "bst": 535,
        "spd": 60,
        "vibe": "Chill sea Pokémon with tank energy.",
        "counters": "Electric, Grass, Fighting, and Rock types."
    },
    {
        "name": "Scizor",
        "aliases": ["scizor", "scisor", "scizur"],
        "type": "Bug / Steel",
        "generation": 2,
        "is_legendary": False,
        "mid": False,
        "sus": False,
        "bst": 500,
        "spd": 65,
        "vibe": "Metal mantis with giant claws and serious aura.",
        "counters": "Fire types are extremely effective."
    },
    {
        "name": "Machamp",
        "aliases": ["machamp", "macham", "machamp"],
        "type": "Fighting",
        "generation": 1,
        "is_legendary": False,
        "mid": False,
        "sus": False,
        "bst": 505,
        "spd": 55,
        "vibe": "Four arms, zero fear. Certified gym monster.",
        "counters": "Flying, Psychic, and Fairy types."
    },
    {
        "name": "Zoroark",
        "aliases": ["zoroark", "zoroarkk", "zoroak"],
        "type": "Dark",
        "generation": 5,
        "is_legendary": False,
        "mid": False,
        "sus": True,
        "bst": 510,
        "spd": 105,
        "vibe": "Illusion master with sneaky main-character energy.",
        "counters": "Fighting, Bug, and Fairy types."
    }
]

GENERATION_NAMES = {
    1: "Generation 1",
    2: "Generation 2",
    3: "Generation 3",
    4: "Generation 4",
    5: "Generation 5",
    6: "Generation 6"
}

POKEMON_WORDS = {a for p in POKEMON_DB for a in p["aliases"]}
NAMES = ", ".join(p["name"] for p in POKEMON_DB)

TYPES = {
    "normal", "fire", "water", "grass", "electric", "ice", "fighting",
    "poison", "ground", "flying", "psychic", "bug", "rock", "ghost",
    "dragon", "dark", "steel", "fairy"
}

COUNTER_WORDS = {
    "counter", "counters", "beat", "defeat", "defit", "kill",
    "weak", "weakness", "against", "win", "destroy", "fight",
    "battle", "defeated"
}

COMPARE_WORDS = {"compare", "better", "vs", "versus", "than", "between"}
OWN_WORDS = {"have", "got", "caught", "use", "own", "love", "my", "using"}
STRONG_WORDS = {"strong", "strongest", "stronger", "powerful", "power", "op", "tough", "goat"}
FAST_WORDS = {"fastest", "fast", "speed", "quick", "faster"}
CUTE_WORDS = {"cute", "cutest", "adorable"}
NEG_WORDS = {"trash", "bad", "garbage", "overrated", "useless", "ugly", "terrible"}
POS_WORDS = {"great", "awesome", "amazing", "goated", "cool", "nice", "beautiful"}
LEGEND_WORDS = {"legendary", "legend", "mythical"}
GREETINGS = {"hi", "hello", "hey", "sup", "yo", "wsp"}
SLANG_WORDS = {"bet", "cap", "slay", "rizz", "sus", "mid", "nocap"}

WEAK_TO = {
    "Pikachu": {"ground"},
    "Charizard": {"rock", "water", "electric"},
    "Bulbasaur": {"fire", "flying", "ice", "psychic"},
    "Squirtle": {"grass", "electric"},
    "Mewtwo": {"dark", "ghost", "bug"},
    "Eevee": {"fighting"},
    "Snorlax": {"fighting"},
    "Gengar": {"ghost", "dark", "psychic", "ground"},
    "Lucario": {"fire", "fighting", "ground"},
    "Arceus": {"fighting"},
    "Rayquaza": {"ice", "dragon", "fairy", "rock"},
    "Garchomp": {"ice", "dragon", "fairy"},
    "Tyranitar": {"fighting", "ground", "steel", "water", "grass", "bug", "fairy"},
    "Greninja": {"electric", "grass", "fighting", "bug", "fairy"},
    "Gardevoir": {"ghost", "poison", "steel"},
    "Blaziken": {"water", "ground", "flying", "psychic", "fairy"},
    "Sceptile": {"fire", "ice", "poison", "flying", "bug"},
    "Infernape": {"water", "ground", "flying", "psychic", "fairy"},
    "Metagross": {"fire", "ground", "ghost", "dark"},
    "Salamence": {"ice", "rock", "dragon", "fairy"},
    "Gyarados": {"electric", "rock"},
    "Jolteon": {"ground"},
    "Umbreon": {"fighting", "bug", "fairy"},
    "Heracross": {"flying", "fire", "psychic", "fairy"},
    "Espeon": {"dark", "ghost", "bug"},
    "Dragonite": {"ice", "rock", "dragon", "fairy"},
    "Lapras": {"electric", "grass", "fighting", "rock"},
    "Scizor": {"fire"},
    "Machamp": {"flying", "psychic", "fairy"},
    "Zoroark": {"fighting", "bug", "fairy"}
}

context = {
    "last_pokemon": None,
    "user_name": None
}

TYPO_VOCAB = TYPES | {
    "counter", "counters", "defeat", "legendary", "weakness",
    "weakest", "strongest", "pokemon", "fastest", "generation"
}

def tokenize(text):
    return re.findall(r"[a-z0-9']+", text.lower().replace("é", "e"))

def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

def fix_typos(words):
    fixed = []

    for word in words:
        if len(word) >= 4 and word not in POKEMON_WORDS:
            best = max(TYPO_VOCAB, key=lambda x: similarity(word, x))

            if similarity(word, best) >= 0.75:
                word = best

        fixed.append(word)

    return fixed

def match_word(word):
    for p in POKEMON_DB:
        if word in p["aliases"]:
            return p

    if len(word) < 4:
        return None

    best = None
    best_score = 0

    for p in POKEMON_DB:
        for alias in p["aliases"]:
            if len(alias) >= 4:
                score = similarity(word, alias)

                if word[:3] == alias[:3]:
                    score += 0.1

                if score > best_score:
                    best = p
                    best_score = score

    if best_score >= 0.68:
        return best

    return None

def find_all(text):
    found = []

    for word in tokenize(text):
        p = match_word(word)

        if p and p not in found:
            found.append(p)

    return found

def mon_types(p):
    return set(p["type"].lower().split(" / "))

def article(word):
    return "an" if word[0].lower() in "aeiou" else "a"

def ranked():
    return sorted(POKEMON_DB, key=lambda p: p["bst"], reverse=True)

def status_of(p):
    return "Legendary Pokémon 👑" if p["is_legendary"] else "Regular Pokémon ⚡"

def detect_slang(text, tokens):
    if "no cap" in text or "nocap" in tokens:
        return "no cap"

    for word in ("cap", "slay", "rizz", "mid", "sus", "bet"):
        if word in tokens:
            return word

    return None

def matchup(a, b):
    a_hits = mon_types(a) & WEAK_TO[b["name"]]
    b_hits = mon_types(b) & WEAK_TO[a["name"]]

    if a_hits and not b_hits:
        return 1

    if b_hits and not a_hits:
        return -1

    if a["bst"] > b["bst"]:
        return 1

    if b["bst"] > a["bst"]:
        return -1

    if a["spd"] > b["spd"]:
        return 1

    if b["spd"] > a["spd"]:
        return -1

    return 0

def battle_result(attackers, defenders):
    attack_score = 0
    defense_score = 0

    for a in attackers:
        for d in defenders:
            result = matchup(a, d)

            if result == 1:
                attack_score += 3
            elif result == -1:
                defense_score += 3
            else:
                attack_score += 1
                defense_score += 1

    attack_score += sum(p["bst"] / 100 for p in attackers)
    defense_score += sum(p["bst"] / 100 for p in defenders)

    if len(attackers) > len(defenders):
        attack_score += (len(attackers) - len(defenders)) * 2

    if len(defenders) > len(attackers):
        defense_score += (len(defenders) - len(attackers)) * 2

    difference = attack_score - defense_score

    if difference >= 8:
        return "YOU COMPLETELY WIN! 🔥💀"

    if difference >= 3:
        return "YOU WIN! 🔥"

    if difference >= 0.8:
        return "YOU WIN, BUT IT'S CLOSE! ⚔️"

    if difference > -0.8:
        return "EXTREMELY CLOSE BATTLE! ⚔️🔥"

    if difference > -3:
        return "YOU LOSE, BUT IT'S CLOSE! 😬"

    if difference > -8:
        return "YOU LOSE! 💀"

    return "YOU COMPLETELY LOSE! 💀☠️"

def team_battle_reply(attackers, defenders):
    lines = []

    for a in attackers:
        for d in defenders:
            result = matchup(a, d)

            if result == 1:
                lines.append(
                    f"{a['name']} vs {d['name']} ⚔️ Advantage: {a['name']} 🔥"
                )
            elif result == -1:
                lines.append(
                    f"{a['name']} vs {d['name']} ⚔️ Advantage: {d['name']} 😬"
                )
            else:
                lines.append(
                    f"{a['name']} vs {d['name']} ⚔️ Even matchup"
                )

    attacker_total = sum(p["bst"] for p in attackers)
    defender_total = sum(p["bst"] for p in defenders)

    attacker_names = " + ".join(p["name"] for p in attackers)
    defender_names = " + ".join(p["name"] for p in defenders)

    result = battle_result(attackers, defenders)

    return (
        "\n".join(lines)
        + "\n\n"
        + f"{len(attackers)}v{len(defenders)} BATTLE\n"
        + f"{attacker_names} vs {defender_names}\n"
        + f"Your team stats: {attacker_total}\n"
        + f"Opponent team stats: {defender_total}\n"
        + f"🏆 {result}"
    )

def generation_reply(text, mons):
    lower = text.lower()

    gen_match = re.search(
        r"(?:gen|generation)\s*(?:number\s*)?([1-6])",
        lower
    )

    if gen_match:
        gen = int(gen_match.group(1))
        pokemon = [p["name"] for p in POKEMON_DB if p["generation"] == gen]

        if pokemon:
            return (
                f"Generation {gen} Pokémon I know ({len(pokemon)}):\n"
                + "\n".join(f"• {name}" for name in pokemon)
            )

        return f"I don't have Pokémon from Generation {gen} in my database yet."

    if mons and re.search(r"\b(gen|generation)\b", lower):
        p = mons[0]

        return (
            f"{p['name']} is from Generation {p['generation']} "
            f"({GENERATION_NAMES[p['generation']]}). 🔥\n"
            f"Type: {p['type']}"
        )

    return None

def find_target(text, mons):
    lower = text.lower()

    keywords = [
        "using",
        "with",
        "against",
        "defeat",
        "beat",
        "fight",
        "destroy",
        "kill"
    ]

    for keyword in keywords:
        if keyword in lower:
            after = lower.split(keyword, 1)[1]
            candidates = find_all(after)

            if candidates:
                return candidates[-1]

    if len(mons) >= 2:
        return mons[-1]

    return None

def is_battle_question(text, mons):
    if len(mons) < 2:
        return False

    lower = text.lower()

    battle_phrases = [
        "can i",
        "can we",
        "can my",
        "defeat",
        "beat",
        "fight",
        "against",
        "using",
        "with",
        "destroy",
        "kill"
    ]

    return any(x in lower for x in battle_phrases)

def general_reply(text, tokens, mons):
    if re.search(
        r"how are you|how r u|how's it going|hows it going|what's up|whats up",
        text
    ):
        return "Doing slay, thanks for asking! 😎 Got a Pokémon in mind?"

    if tokens & CUTE_WORDS:
        top = sorted(POKEMON_DB, key=lambda p: p["name"] in ("Eevee", "Pikachu"), reverse=True)
        return "Cutest picks: Eevee and Pikachu. 🥹"

    if tokens & FAST_WORDS:
        top = sorted(POKEMON_DB, key=lambda p: p["spd"], reverse=True)[:5]
        return (
            "Fastest Pokémon I know: "
            + ", ".join(f"{p['name']} ({p['spd']})" for p in top)
            + " ⚡"
        )

    if tokens & STRONG_WORDS:
        top = ranked()[:5]

        return (
            "Strongest by base stats:\n"
            + "\n".join(f"• {p['name']} ({p['bst']})" for p in top)
        )

    if tokens & LEGEND_WORDS:
        legends = [p for p in POKEMON_DB if p["is_legendary"]]

        return (
            "Legendary Pokémon 👑:\n"
            + "\n".join(f"• {p['name']} — Gen {p['generation']}" for p in legends)
        )

    if "list" in tokens or "all pokemon" in text:
        return (
            f"I know {len(POKEMON_DB)} Pokémon:\n"
            + "\n".join(
                f"• {p['name']} — Gen {p['generation']} — {p['type']}"
                for p in POKEMON_DB
            )
        )

    if re.search(r"who are you|what can you do|help", text):
        return (
            "I'm a Pokémon Gen Z bot! 🔥 "
            "Ask me about types, generations, counters, strength, "
            "rizz, or team battles."
        )

    return None

def generate_response(user_input):
    text = user_input.lower().replace("é", "e")
    tokens = set(fix_typos(tokenize(text)))
    mons = find_all(text)

    name_match = re.search(
        r"my n\w{2,4}e is (\w+)|call me (\w+)",
        user_input,
        re.I
    )

    if name_match:
        name = (
            name_match.group(1)
            or name_match.group(2)
        ).capitalize()

        context["user_name"] = name

        return (
            f"Yo {name}! Nice to meet you, bet! 🔥 "
            "Which Pokémon do you have?"
        )

    if re.search(
        r"what.?s my n\w{2,4}e|what is my n\w{2,4}e|who am i",
        text
    ):
        if context["user_name"]:
            return f"You're {context['user_name']}, no cap! 😎"

        return "I don't know yet! Tell me: 'my name is ...' 😅"

    gen_response = generation_reply(text, mons)

    if gen_response:
        return gen_response

    if is_battle_question(text, mons):
        target = find_target(text, mons)

        if target:
            attackers = [p for p in mons if p is not target]

            if attackers:
                context["last_pokemon"] = target
                return team_battle_reply(attackers, [target])

    if len(mons) >= 2 and tokens & COMPARE_WORDS:
        return team_battle_reply([mons[0]], [mons[1]])

    if not mons:
        general = general_reply(text, tokens, mons)

        if general:
            return general

        slang = detect_slang(text, tokens)

        if slang == "bet":
            return "Bet! 🔥 Name a Pokémon and let's talk."

        if slang == "rizz":
            return "Rizz check! Tell me a Pokémon and I'll rate it. 😎"

        if slang == "mid":
            return "Mid?! Which Pokémon are you calling mid? 👀"

        if slang == "sus":
            return "Sus?! Name the Pokémon. 👀"

        return f"I couldn't tell which Pokémon you mean. Try: {NAMES}"

    p = mons[0]
    context["last_pokemon"] = p

    if tokens & LEGEND_WORDS:
        if p["is_legendary"]:
            return (
                f"Yes! {p['name']} is Legendary 👑. "
                f"Type: {p['type']}. Gen {p['generation']}."
            )

        return (
            f"Nope! {p['name']} is not Legendary. "
            f"It's a regular Pokémon from Gen {p['generation']}."
        )

    if tokens & STRONG_WORDS:
        return (
            f"{p['name']} has {p['bst']} base stats and "
            f"{p['spd']} speed. {p['vibe']}"
        )

    if tokens & FAST_WORDS:
        return (
            f"{p['name']}'s base speed is {p['spd']}. ⚡ "
            f"It is from Generation {p['generation']}."
        )

    if tokens & COUNTER_WORDS:
        return (
            f"Wanna defeat {p['name']}? "
            f"It's {article(p['type'])} {p['type']} type.\n"
            f"👉 Best Counter: {p['counters']}"
        )

    if "rizz" in tokens:
        return f"Rizz check on {p['name']}: {p['vibe']} 😎"

    if "mid" in tokens:
        if p["mid"]:
            return f"Lowkey yeah, {p['name']} can be mid. 😬"
        return f"{p['name']} is NOT mid. That's cap! 🧢"

    if "sus" in tokens:
        if p["sus"]:
            return f"Okay yeah, {p['name']} is kinda sus. 👀"
        return f"{p['name']} isn't sus. Straight W. ✅"

    if tokens & POS_WORDS:
        return f"Facts! {p['name']} is a W. 🔥 {p['vibe']}"

    if tokens & NEG_WORDS:
        return f"Cap! 🧢 {p['name']} isn't trash. It has {p['bst']} base stats."

    return (
        f"Oh, {p['name']}? That's {article(p['type'])} "
        f"**{p['type']}** type ({status_of(p)}).\n"
        f"Generation: {p['generation']}.\n"
        f"👉 Best Counter: {p['counters']}"
    )

def main():
    print("=" * 60)
    print("⚡ POKÉMON CHATBOT (Gen Z Edition) ⚡")
    print(f"I know {len(POKEMON_DB)} Pokémon.")
    print("Try: 'what gen is pikachu?'")
    print("Try: 'what pokemon are in gen 3?'")
    print("Try: 'i have pikachu and charizard can i defeat arceus'")
    print("Type 'exit' to quit.")
    print("=" * 60)

    while True:
        user_input = input("\nYou: ").strip()

        if not user_input:
            continue

        if user_input.lower() in ("exit", "quit", "bye"):
            who = context["user_name"] or "bro"
            print(
                f"Chatbot: Bye {who}! "
                "Slay your Pokémon journey, no cap! 👋"
            )
            break

        print(f"Chatbot: {generate_response(user_input)}")

if __name__ == "__main__":
    main()
