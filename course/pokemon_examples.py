"""
More examples for each lesson, in the Pokémon world.

POKEMON[lesson_id] = list of examples, in the same format as the ones in lessons.py.
They appear on the page in a "With Pokémon" section, after Cupi's examples.
The ones marked "random": True give a different result every time.
"""

POKEMON = {

"hello": [
{"text": "Every trainer's battle cry:",
 "code": """show("Pikachu, I choose you!")
show("Pika pika")
"""},
{"text": "An introduction, with a note for people:",
 "code": """# Ash introduces himself
show("Hi, my name is Ash")
show("I'm from Pallet Town")
show("And I'm going to be the very best Pokémon Master")
"""},
],

"variables": [
{"text": "A Pokémon's details, each one in its own box:",
 "code": """pokemon = "Pikachu"
type = "electric"
level = 5

show(pokemon, "is an", type, "type")
show("It's at level", level)
"""},
{"text": "Pikachu levels up!",
 "code": """level = 5
show("Level before training:", level)

level = level + 1
show("Level after training:", level)
"""},
{"text": "Variables can also hold longer texts:",
 "code": """trainer = "Misty"
favorite = "Starmie"
city = "Cerulean City"

show(trainer, "lives in", city)
show("Her favorite Pokémon is", favorite)
"""},
],

"texts": [
{"text": "A Pokédex entry made with a text:",
 "code": """name = "Charmander"
type = "fire"
number = 4
show("Pokédex #{number}: {name}, {type} type")
"""},
{"text": "Math inside the text:",
 "code": """name = "Squirtle"
hp = 44
damage = 12
show("{name} took {damage} damage")
show("It has {hp - damage} HP left")
"""},
],

"math": [
{"text": "Shopping at the Poké Mart:",
 "code": """pokeball_price = 200
amount = 5
total = pokeball_price * amount

show("{amount} Poké Balls cost {total} coins")
show("With 1500 coins you have {1500 - total} left over")
"""},
{"text": "Experience and levels: each level needs 100 points.",
 "code": """experience = 1250
per_level = 100

show("It went up {experience // per_level} levels")
show("And it has {experience % per_level} points left over")
"""},
{"text": "A super effective attack does double damage:",
 "code": """power = 40
multiplier = 2
show("Thunder Shock does {power * multiplier} damage")
"""},
],

"reading": [
{"text": "Choose your starter Pokémon. The answers are already in **Answers**:",
 "inputs": "Ash\nPikachu",
 "code": """trainer = read("What's your name? ")
starter = read("Which is your starter Pokémon? ")
show("{trainer} chose {starter}!")
"""},
{"text": "Buying Poké Balls:",
 "inputs": "3",
 "code": """amount = read_num("How many Poké Balls do you want? ")
show("That's {amount * 200} coins, please")
"""},
],

"decisions": [
{"text": "Is it super effective? Change the types and try it:",
 "code": """attack = "water"
defender = "fire"

if attack == "water" and defender == "fire":
    show("It's super effective!")
else if attack == defender:
    show("It's not very effective…")
else:
    show("It's a normal attack")
"""},
{"text": "With `when`, what Professor Oak says about each type:",
 "code": """type = "grass"

when type:
    is "fire":
        show("Strong against grass, weak against water")
    is "water":
        show("Strong against fire, weak against grass")
    is "grass":
        show("Strong against water, weak against fire")
    else:
        show("I don't know that type")
"""},
{"text": "How's its HP?",
 "code": """hp = 8
max_hp = 35

if hp == 0:
    show("It fainted: off to the Pokémon Center!")
else if hp in 1..10:
    show("Careful! It's low on HP")
else:
    show("It's ready to battle")
"""},
],

"loops": [
{"text": "Pikachu is happy:",
 "code": """repeat 3:
    show("Pika!")
show("Pikachuuuu!")
"""},
{"text": "Training from level 14 to 18. At 16, Charmander evolves!",
 "code": """for level in 14..18:
    show("Charmander reached level {level}")
    if level == 16:
        show("   Charmander evolved into Charmeleon!")
"""},
{"text": "A battle: keep attacking until the rival faints.",
 "code": """rival_hp = 30
turn = 0

while rival_hp > 0:
    turn += 1
    rival_hp -= 12
    show("Turn {turn}: the rival has {max(rival_hp, 0)} HP left")
show("The rival fainted!")
"""},
],

"lists": [
{"text": "Ash's team:",
 "code": """team = ["Pikachu", "Bulbasaur", "Charmander"]
team = add(team, "Squirtle")

show("Ash has {len(team)} Pokémon")
for i, p at team:
    show("{i + 1}. {p}")
"""},
{"text": "Have you caught it yet?",
 "code": """caught = ["Pidgey", "Rattata", "Pikachu", "Caterpie"]

show("Pikachu" in caught)
show("Mew" not in caught)
show("The first two:", caught[0..1])
"""},
{"text": "A Pokémon goes to live with Professor Oak:",
 "code": """team = ["Pikachu", "Bulbasaur", "Charmander", "Squirtle"]
team = drop(team, "Bulbasaur")
show(team)
show("Is the team empty?", team is empty)
"""},
],

"dictionaries": [
{"text": "A Pokédex: the type of each Pokémon.",
 "code": """pokedex = ["Pikachu": "electric", "Squirtle": "water", "Bulbasaur": "grass"]

show("Squirtle's type is", pokedex["Squirtle"])

pokedex["Eevee"] = "normal"
for name in keys(pokedex):
    show("{name}: {pokedex[name]}")
"""},
{"text": "Looking up one that isn't there, with a backup value:",
 "code": """pokedex = ["Pikachu": "electric", "Squirtle": "water"]

show(pokedex["Pikachu"] else "unknown")
show(pokedex["Mewtwo"] else "unknown")
show("Mewtwo" in pokedex)
"""},
{"text": "The shop: the price of each item.",
 "code": """shop = ["pokeball": 200, "potion": 300, "greatball": 600]

total = shop["pokeball"] * 3 + shop["potion"]
show("Three Poké Balls and a Potion: {total} coins")
"""},
],

"records": [
{"text": "A Pokémon with all its details:",
 "code": """pika = (name: "Pikachu", type: "electric", level: 5, hp: 35)

show("{pika.name}, level {pika.level}, {pika.type} type")
pika.level += 1
show(pika)
"""},
{"text": "A team: a list of records.",
 "code": """team = [
    (name: "Pikachu", type: "electric", level: 12),
    (name: "Bulbasaur", type: "grass", level: 10),
    (name: "Charmander", type: "fire", level: 11),
]

for p in team:
    show("{p.name} ({p.type}) is at level {p.level}")
"""},
{"text": "A record inside another one: the trainer and their favorite Pokémon.",
 "code": """ash = (
    name: "Ash",
    badges: 8,
    favorite: (name: "Pikachu", level: 25)
)

show("{ash.name} has {ash.badges} badges")
show("His favorite is {ash.favorite.name}, level {ash.favorite.level}")
"""},
],

"functions": [
{"text": "A function that works as a mold for making Pokémon:",
 "code": """fx pokemon(name, type, level = 5):
    return (name: name, type: type, level: level, hp: level * 7)

pika = pokemon("Pikachu", "electric")
charizard = pokemon("Charizard", "fire", level = 36)
show(pika)
show(charizard)
"""},
{"text": "How much damage does an attack do?",
 "code": """fx damage(power, level):
    return power * level // 10

show("Thunder Shock, level 10:", damage(40, 10))
show("Flamethrower, level 36:", damage(90, 36))
"""},
{"text": "A function that decides, with `when`. It compares **two things at once**, the attack and the defender, joined with `and`:",
 "code": """fx multiplier(attack, defender):
    when attack and defender:
        is "water" and "fire", "fire" and "grass", "grass" and "water":
            return 2
        is "fire" and "water", "grass" and "fire", "water" and "grass":
            return 0.5
        else:
            return 1

show(multiplier("water", "fire"))
show(multiplier("fire", "water"))
show(multiplier("electric", "grass"))
"""},
],

"copies": [
{"text": "A clone doesn't change the original:",
 "code": """pika = (name: "Pikachu", hp: 35)
clone = pika
clone.name = "Pikachu clone"
clone.hp = 10

show(pika)
show(clone)
"""},
{"text": "The Pokémon Center heals the Pokémon and gives it back:",
 "code": """fx pokemon_center(p):
    p.hp = p.max_hp
    return p

pika = (name: "Pikachu", hp: 3, max_hp: 35)
pika = pokemon_center(pika)
show("{pika.name} has {pika.hp} HP. Good as new!")
"""},
],

"shortcuts": [
{"text": "The ones ready to battle, in one line:",
 "code": """team = [
    (name: "Pikachu", level: 12, hp: 30),
    (name: "Bulbasaur", level: 8, hp: 0),
    (name: "Charmander", level: 15, hp: 39),
]

ready = [p.name for p in team if p.hp > 0]
show("Ready:", ready)
show("Fainted:", count(team, fx: it.hp == 0))
"""},
{"text": "Sorting the team by level, from highest to lowest:",
 "code": """team = [
    (name: "Pikachu", level: 12),
    (name: "Bulbasaur", level: 8),
    (name: "Charmander", level: 15),
]

for p in reversed(sorted(team, fx: it.level)):
    show("{p.name}: level {p.level}")
"""},
{"text": "Giving everyone one more level, with `map`:",
 "code": """levels = [5, 12, 30]
show(map(levels, fx(n): n + 1))
show([n * 2 for n in levels])
"""},
],

"errors": [
{"text": "Looking up something that isn't in the Pokédex:",
 "code": """pokedex = ["Pikachu": "electric"]

try:
    show(pokedex["Mew"])
except error:
    show("It's not in the Pokédex: {error}")
"""},
{"text": "Checking that HP never goes negative:",
 "expect": "error",
 "code": """hp = 10
damage = 25
hp = hp - damage
assert hp >= 0, "HP can't be negative"
"""},
],

"files": [
{"text": "A Pokédex kept in another file:",
 "files": {"pokedex.cup": 'fx type_of(name):\n    types = ["Pikachu": "electric", "Squirtle": "water", "Charmander": "fire"]\n    return types[name] else "unknown"\n'},
 "code": """use type_of from pokedex

show("Pikachu:", type_of("Pikachu"))
show("Mewtwo:", type_of("Mewtwo"))
"""},
],

"random": [
{"text": "A wild Pokémon appears!", "random": True,
 "code": """wild = pick(["Pidgey", "Rattata", "Caterpie", "Pikachu", "Abra"])
level = roll(2, 10)
show("A wild level {level} {wild} appeared!")
"""},
{"text": "Throwing a Poké Ball: it catches with a 40% chance.", "random": True,
 "code": """luck = roll(1, 100)

if luck <= 40:
    show("All right! You caught the Pokémon")
else:
    show("Oh no! It broke free from the Poké Ball")
"""},
{"text": "A mini battle with random damage.", "random": True,
 "code": """pikachu_hp = 35
rival_hp = 35

while not (pikachu_hp <= 0 or rival_hp <= 0):
    rival_hp -= roll(5, 12)
    pikachu_hp -= roll(5, 12)

if rival_hp <= 0 and pikachu_hp > 0:
    show("Pikachu won!")
else if pikachu_hp <= 0 and rival_hp > 0:
    show("Pikachu lost this time")
else:
    show("A tie! They both fainted")
"""},
],

"project": [
{"text": "Cupi also sells to Pokémon trainers:",
 "code": """prices = ["pokeball": 200, "potion": 300]

orders = [
    (trainer: "Ash", item: "pokeball", amount: 5),
    (trainer: "Misty", item: "potion", amount: 2),
    (trainer: "Brock", item: "greatball", amount: 1),
]

for o in orders:
    price = prices[o.item] else 0
    if price == 0:
        show("{o.trainer}: we don't sell {o.item}")
    else:
        show("{o.trainer} pays {price * o.amount} for {o.amount} {o.item}")
"""},
],
}
