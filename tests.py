"""
Cupcake tests: each case is a program and what it must show (or the error it must give).

    python3 tests.py
"""
import contextlib
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cupcake  # noqa: E402

# (name, code, input for read, expected output)   — or  ("error", part of the message)
CASES = [
("hello", 'show("Hello, world")', "", "Hello, world\n"),
("variables and texts with values", '''
name = "Ash"
age = 10
show("{name} is {age} years old")
show("Next year they will be {age + 1}")
''', "", "Ash is 10 years old\nNext year they will be 11\n"),
("escaped brace", r'show("use \{ to open")', "", "use { to open\n"),
("multi-line text", '''
name = "Misty"
show("""Hello, {name}.
Welcome.""")
''', "", "Hello, Misty.\nWelcome.\n"),
("true false none", '''
show(true, false, none)
winner = none
show(winner == none)
''', "", "true false none\ntrue\n"),
("if else if else", """
fx level(age):
    if age >= 10:
        return "trainer"
    else if age > 5:
        return "almost"
    else:
        return "not yet"
show(level(12), level(7), level(3))
""", "", "trainer almost not yet\n"),
("else on the next line", """
ready = false
if ready:
    show("Let's go")
else:
    show("Wait")
""", "", "Wait\n"),
("block with empty lines and comments", """
if true:

    # a comment inside the block
    show("ok")
""", "", "ok\n"),
("braces give a hint", 'if true {\n    show(1)\n}', "", ("error", "Cupcake doesn't use braces for blocks")),
("missing colon", 'if true\n    show(1)', "", ("error", "missing ':'")),
("too much indentation", 'show(1)\n    show(2)', "", ("error", "indented too much")),
("empty block with none", 'if true:\n    none\nfx nothing():\n    return none\nshow(nothing())', "", "none\n"),
("while, break and continue", """
i = 0
while true:
    i = i + 1
    if i == 2:
        continue
    if i > 4:
        break
    show(i)
""", "", "1\n3\n4\n"),
("ranges include the last one", """
for i in 1..4:
    show(i)
show(1..3)
""", "", "1\n2\n3\n4\n[1, 2, 3]\n"),
("slicing lists", '''
team = ["Pikachu", "Charmander", "Squirtle", "Bulbasaur", "Eevee"]
show(team[0], team[-1])
show(team[1..3])
show(team[2..])
show(team[..1])
show(team[-2..])
''', "", 'Pikachu Eevee\n["Charmander", "Squirtle", "Bulbasaur"]\n["Squirtle", "Bulbasaur", "Eevee"]\n'
         '["Pikachu", "Charmander"]\n["Bulbasaur", "Eevee"]\n'),
("dictionaries", """
prices = ["pokeball": 200, "potion": 300]
prices["greatball"] = 600
show(prices["potion"], len(prices))
show(keys(prices))
empty = [:]
show(empty, "pokeball" in prices)
badges = [1: "Boulder", 2: "Cascade"]
show(badges[2])
""", "", '300 3\n["pokeball", "potion", "greatball"]\n[:] true\nCascade\n'),
("comprehensions", """
show([i * 2 for i in 1..5])
team = [(name: "Pikachu", hp: 12), (name: "Squirtle", hp: 0)]
show([p.name for p in team if p.hp > 0])
show([p.name: p.hp for p in team])
""", "", '[2, 4, 6, 8, 10]\n["Pikachu"]\n["Pikachu": 12, "Squirtle": 0]\n'),
("records", '''
pika = (name: "Pikachu", type: "electric", hp: 35)
show(pika.name)
pika.hp = 30
show(pika)
''', "", 'Pikachu\n(name: "Pikachu", type: "electric", hp: 30)\n'),
("record on several lines", '''
pika = (
    name: "Pikachu",
    hp: 35
)
show(pika.hp)
''', "", "35\n"),
("a record doesn't get new fields", '''
pika = (name: "Pikachu", health: 35)
pika.healht = 10
''', "", ("error", "has no field 'healht'. Did you mean 'health'?")),
("record: reading a missing field", '''
pika = (name: "Pikachu", hp: 35)
show(pika.nam)
''', "", ("error", "Did you mean 'name'?")),
("a function as a mold", """
fx pokemon(name, type, hp = 35):
    return (name: name, type: type, hp: hp)
pika = pokemon("Pikachu", "electric")
charm = pokemon("Charmander", "fire", hp = 39)
show(pika.hp, charm.hp)
""", "", "35 39\n"),
("data is copied", '''
a = [1, 2]
b = a
b = add(b, 3)
b[0] = 99
show(a, b)
pika = (name: "Pikachu", hp: 35)
clone = pika
clone.hp = 10
show(pika.hp, clone.hp)
''', "", "[1, 2] [99, 2, 3]\n35 10\n"),
("a function doesn't change what's outside", """
fx heal(p, amount):
    p.hp = p.hp + amount
    return p
pika = (name: "Pikachu", hp: 10)
heal(pika, 5)
show(pika.hp)
pika = heal(pika, 5)
show(pika.hp)
""", "", "10\n15\n"),
("anonymous functions: fx(…):, λ and it", """
team = [(name: "Squirtle", hp: 0), (name: "Pikachu", hp: 12), (name: "Charmander", hp: 39)]
alive = filter(team, fx(p): p.hp > 0)
show([p.name for p in sorted(alive, λ(p): p.name)])
plus = fx(a, b): a + b
show(plus(2, 3))
show(map([1, 2, 3], fx: it * 10))
show(reduce([1, 2, 3, 4], fx(a, b): a + b, 0))
""", "", '["Charmander", "Pikachu"]\n5\n[10, 20, 30]\n10\n'),
("returning a record", """
fx divide_with_remainder(a, b):
    return (quotient: a // b, remainder: a % b)
r = divide_with_remainder(17, 5)
show(r.quotient, r.remainder)
""", "", "3 2\n"),
("list builtins", '''
team = ["Pikachu", "Charmander"]
team = add(team, "Eevee")
team = drop(team, "Charmander")
show(team, len(team), first(team), last(team))
show(sorted([3, 1, 2]), reversed([1, 2, 3]))
show(sum([1, 2, 3]), min(4, 2, 8), max([4, 2, 8]))
''', "", '["Pikachu", "Eevee"] 2 Pikachu Eevee\n[1, 2, 3] [3, 2, 1]\n6 2 8\n'),
("text builtins", '''
show(upper("hello"), lower("HELLO"), strip("  x  "))
show(split("a,b,c", ","), join(["a", "b"], "-"), replace("cat", "c", "b"))
show(int("42") + 1, float("1.5"), str(10) + "!")
''', "", 'HELLO hello x\n["a", "b", "c"] a-b bat\n43 1.5 10!\n'),
("try, except, finally", """
try:
    age = int("abc")
except error:
    show("Failed: {error}")
finally:
    show("Done")
""", "", "Failed: 'abc' is not a whole number\nDone\n"),
("raise caught", """
fx validate(age):
    if age < 0:
        raise "Age can't be negative"
    return age
try:
    validate(-1)
except e:
    show(e)
""", "", "Age can't be negative\n"),
("assert with values", """
fx heal(p, amount):
    assert amount > 0
    return p
heal((hp: 1), -5)
""", "", ("error", "assert failed: amount > 0\n  amount is -5")),
("assert with a message", '''
hp = -3
assert hp >= 0, "hp can't be negative"
''', "", ("error", "hp can't be negative")),
("read", '''
name = read("Name? ")
age = int(read("Age? "))
show("Hi, {name}. Next year you'll be {age + 1}.")
''', "Ash\n10\n", "Name? Ash\nAge? 10\nHi, Ash. Next year you'll be 11.\n"),
("in and not in", '''
team = ["Pikachu", "Eevee"]
show("Pikachu" in team, "Mew" not in team, "chu" in "Pikachu")
''', "", "true true true\n"),
("functions in any order", """
show(double(21))
fx double(x):
    return x * 2
""", "", "42\n"),
("recursion", """
fx factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
show(factorial(10))
""", "", "3628800\n"),
("+=", '''
x = 5
x += 3
show(x)
''', "", "8\n"),
# -- friendly errors
("method: append", 'team = ["a"]\nteam.append("b")', "",
 ("error", "Cupcake has no methods: '.append(…)' doesn't exist. Write:  team = add(team, \"b\")")),
("method: upper", 'name = "ash"\nshow(name.upper())', "", ("error", "Write:  upper(name)")),
("word from another language: def", "def greet(x): none", "", ("error", "'def' is not a Cupcake word. Write 'fx'.")),
("word from another language: print", 'print("hello")', "", ("error", "'print' is not a Cupcake word. Write 'show'.")),
("word from another language: True", "x = True", "", ("error", "'True' is not a Cupcake word. Write 'true'.")),
("misspelled name", 'team = []\nshow(teamm)', "", ("error", "'teamm' doesn't exist. Did you mean 'team'?")),
("adding text and a number", 'show("Age: " + 10)', "", ("error", "can't add a text and a number")),
("dividing by zero", "show(1 / 0)", "", ("error", "can't divide by zero")),
("position that doesn't exist", 'l = [1, 2]\nshow(l[5])', "", ("error", "the list has 2 elements (0 to 1); position 5 doesn't exist")),
("dictionary with a dot", 'd = ["a": 1]\nshow(d.a)', "", ("error", 'a dictionary is read with brackets:  dict["a"]')),
("record with quotes", 'r = ("name": "x")', "", ("error", "in a record, fields go without quotes")),
("record with braces (old form)", 'r = {name: "x"}', "", ("error", "A record is written with parentheses")),
("grouping parentheses still work", 'show((2 + 3) * 4)', "", "20\n"),
("unclosed text", 'show("hello)', "", ("error", "missing its closing quote")),
("indentation that doesn't match", 'if true:\n    show(1)\n  show(2)\n', "", ("error", "doesn't match any line above")),
("misspelled parameter name", 'fx f(name):\n    return none\nf(nme = "x")', "", ("error", "Did you mean 'name'?")),
("int of a text that isn't a number", 'int("hello")', "", ("error", "'hello' is not a whole number")),
("return outside a function", "return 5", "", ("error", "'return' only makes sense inside a function")),
# -- Cupcake 1.0
("a one-line function needs return", """
fx double(x):
    return x * 2
show(double(21))
""", "", "42\n"),
("fx: it", """
team = [(name: "Pikachu", hp: 12), (name: "Squirtle", hp: 0)]
show(count(team, fx: it.hp > 0))
show(count([1, 2, 2, 3], 2))
""", "", "1\n2\n"),
("in with dictionaries and texts", """
team = ["Pikachu", "Eevee"]
show("Pikachu" in team, "Mew" not in team, "chu" in "Pikachu")
prices = ["pokeball": 200]
show("pokeball" in prices, "potion" not in prices)
""", "", "true true true\ntrue true\n"),
("repeat", """
repeat 3:
    show("Hooray!")
""", "", "Hooray!\nHooray!\nHooray!\n"),
("while instead of until", """
shoes = 0
while shoes != 3:
    shoes += 1
show(shoes)
""", "", "3\n"),
("if not instead of unless", """
rain = true
if not rain:
    show("To the park")
else:
    show("Home")
""", "", "Home\n"),
("is: types and empty", """
show(5 is number, "a" is text, [] is empty, [1] is not empty, none is none, (a: 1) is record)
team = []
if team is empty:
    show("You have no Pokémon")
""", "", "true true true true true true\nYou have no Pokémon\n"),
("storing a value inside each branch", """
hp = 0
if hp > 0:
    state = "alive"
else:
    state = "fainted"
show(state)
if 5 > 3:
    show("yes")
else if 5 > 1:
    show("almost")
else:
    show("no")
""", "", "fainted\nyes\n"),
("if doesn't give a value", 'x = if true:\n    1', "", ("error", "'if' doesn't give a value")),
("when doesn't give a value", 'x = when 1:\n    is 1:\n        2', "", ("error", "'when' doesn't give a value")),
("when with is, in and else", """
fx stage(age):
    when age:
        in 0..9:
            return "child"
        in 10..17:
            return "teen"
        else:
            return "adult"
show(stage(5), stage(12), stage(40))
color = "red"
when color:
    is "red":
        show("Like Cupi's cherry!")
    in ["orange", "yellow"]:
        show("Warm")
    else:
        show("Other")
when 3.5:
    is text:
        show("text")
    is number:
        show("number")
""", "", "child teen adult\nLike Cupi's cherry!\nnumber\n"),
("when with several things joined by and", """
fx multiplier(attack, defender):
    when attack and defender:
        is "water" and "fire", "fire" and "grass":
            return 2
        is "fire" and "water":
            return 0.5
        else:
            return 1
show(multiplier("water", "fire"), multiplier("fire", "grass"), multiplier("fire", "water"), multiplier("water", "water"))
x = 3
when x and "hello":
    is text and text:
        show("wrong")
    is number and text:
        show("number and text")
when x and x * 2:
    in 0..2 and 0..9:
        show("wrong")
    in 0..5 and 6..10:
        show("small and medium")
when x > 1 and x:
    is true and 3:
        show("good")
    else:
        show("wrong")
""", "", "2 2 0.5 1\nnumber and text\nsmall and medium\ngood\n"),
("when with and: a value is missing", """
when 1 and 2:
    is 1:
        show(1)
""", "", ("error", "each case needs 2 values joined with 'and'")),
("in with a range: between the two, decimals too", """
age = 12
show(age in 10..18, age in 13..18)
show(5.5 in 0..10, 10 in 0..10, 11 in 0..10, "a" in 0..10)
show(3 in 0..10 by 2, 4 in 0..10 by 2)
when 2.5:
    in 0..3:
        show("small")
""", "", "true false\ntrue true false false\nfalse true\nsmall\n"),
("between no longer exists", 'show(5 between 1 and 9)', "", ("error", "Cupcake no longer uses 'between'")),
("chained comparison", 'show(0 < 5 < 9)', "", ("error", "compare one thing at a time")),
("else as a fallback", """
prices = ["pokeball": 200]
show(prices["mini"] else 0)
show(int("hello") else -1)
show(prices["pokeball"] else 0)
""", "", "0\n-1\n200\n"),
("ranges with by", """
show(0..10 by 2)
show(5..1 by -1)
""", "", "[0, 2, 4, 6, 8, 10]\n[5, 4, 3, 2, 1]\n"),
("for at", """
for i, p at ["a", "b"]:
    show(i, p)
for i at "xy":
    show(i)
show(["{i}{x}" for i, x at ["a", "b"]], [x for x in [1, 2, 3] if x > 1])
""", "", "0 a\n1 b\n0\n1\n[\"0a\", \"1b\"] [2, 3]\n"),
("for: the position goes first", 'for x in [1] at i:\n    none', "", ("error", "the position goes first")),
("for: two names with in", 'for i, x in [1]:\n    none', "", ("error", "with two names use at")),
("stop", """
show("before")
stop
show("after")
""", "", "before\n"),
("roll and pick", """
d = roll(1, 6)
show(d in 1..6, pick(["x"]))
""", "", "true x\n"),
("read_num asks again", """
age = read_num("Age? ")
show(age + 1)
""", "nine\n9\n", "Age? nine\n'nine' is not a number. Try again.\nAge? 9\n10\n"),
("return inside if and when", """
fx mult(a, d):
    when a:
        is "water":
            if d == "fire":
                return 2
            return 1
        else:
            return 1
fx sign(x):
    if x > 0:
        return "positive"
    else if x < 0:
        return "negative"
    return "zero"
show(mult("water", "fire"), mult("water", "grass"), sign(-3), sign(0))
""", "", "2 1 negative zero\n"),
("a function without return gives none", 'fx f():\n    show("hello")\nshow(f())', "", "hello\nnone\n"),
("missing return", 'fx double(x):\n    x * 2', "", ("error", "For the function to give it back, write return")),
("block on the same line", 'if true: show(1)', "", ("error", "goes on the next line")),
("when case on the same line", 'when 1:\n    is 1: show(1)', "", ("error", "goes on the next line")),
("inline anonymous fx gives its value", 'show(map([1, 2], fx: it * 10), map([1, 2], fx(n): n + 1))', "", "[10, 20] [2, 3]\n"),
("anonymous fx with a block uses return", 'f = fx(n):\n    return n * 3\nshow(f(2))', "", "6\n"),
("old words: other", 'if true:\n    none\nother:\n    none', "", ("error", "Cupcake no longer uses 'other'")),
("old fallback with other", 'x = int("a") other 0', "", ("error", "Cupcake no longer uses 'other'")),
("unless", 'unless true:\n    none', "", ("error", "Cupcake no longer uses 'unless'")),
("until", 'until true:\n    none', "", ("error", "Cupcake no longer uses 'until'")),
("each", 'for each p in [1]:\n    none', "", ("error", "Cupcake no longer uses 'each'")),
("then", 'if true then\n    none', "", ("error", "Cupcake no longer uses 'then'")),
("lonely else", "else:\n    show(1)", "", ("error", "this 'else' has no 'if' before it")),
("other in a when", "when 1:\n    is 1:\n        none\n    other:\n        none", "", ("error", "the last case is written 'else:'")),
("is with a value outside a when", 'c = "red"\nshow(c is "red")', "", ("error", "To compare values use ==")),
("has: fields of a record", """
pika = (name: "Pikachu", hp: 35, asleep: false, level: 0)
show(pika has hp, pika has asleep, pika has level, pika has age, pika has not asleep)
eevee = (stone: true, friendship: 220, level: 0)
show(eevee has stone and friendship, eevee has stone and level, eevee has level or friendship)
rival = (hp: 0)
show(pika has hp and rival has hp, pika has hp or rival has hp)
if pika has hp and level:
    show("wrong")
else:
    show("good")
""", "", "true false false false true\ntrue false true\nfalse true\ngood\n"),
("has: anyone in the list?", """
team = [(name: "A", hp: 0), (name: "B", hp: 12)]
show(team has hp, team has not hp, [(hp: 0)] has hp)
""", "", "true false false\n"),
("has: errors", 'show([1, 2] has hp)', "", ("error", "this list has things without fields")),
("has: a field comes next", 'show(["a"] has "a")', "", ("error", "after 'has' comes a field name")),
("has: misspelled field", 'p = (health: 3)\nshow(p has healht)', "", ("error", "Did you mean 'health'?")),
("in with records: does it have the field?", 'p = (hp: 3)\nshow("hp" in p, "age" in p, "age" not in p)', "", "true false true\n"),
("empty record", 'x = ()', "", ("error", "a record needs at least one field")),
("don't hide builtins", 'count = 3', "", ("error", "'count' is already a Cupcake function")),
("main runs at the end", 'fx main():\n    show("in main", double(2))\nfx double(x):\n    return x * 2\nshow("on top")', "", "on top\nin main 4\n"),
("main takes no values", 'fx main(x):\n    none', "", ("error", "main takes no values")),
("old word: fn", "fn f(x): none", "", ("error", "Write 'fx'")),
("old arrow", "f = fx(x) => x", "", ("error", "Cupcake no longer uses '=>'")),
]


def run(code, stdin_text):
    output = io.StringIO()
    original_stdin = sys.stdin
    sys.stdin = io.StringIO(stdin_text)
    try:
        with contextlib.redirect_stdout(output):
            result = cupcake.run_text(code.strip("\n") + "\n")
    finally:
        sys.stdin = original_stdin
    return output.getvalue(), result


def main():
    failures = 0
    for name, code, stdin_text, expected in CASES:
        output, result = run(code, stdin_text)
        if isinstance(expected, tuple):
            ok = result is not None and expected[1] in result[0]
            got = result[0] if result else f"(no error) {output!r}"
        else:
            ok = result is None and output == expected
            got = output if result is None else f"ERROR: {result[0]} (line {result[1]})"
        if not ok:
            failures += 1
            print(f"FAIL  {name}\n  expected: {expected!r}\n  got:      {got!r}\n")
    print(f"{len(CASES) - failures} of {len(CASES)} tests pass")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
