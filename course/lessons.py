"""
The content of the course "Learn to program with Cupcake".

Each lesson has:
  pose:        what Cupi is doing in the drawing
  bubble:      what Cupi says (speech bubble)
  story:       a little story to start
  explanation: the idea, with code examples between ```
  examples:    code that can be run
  exercises:   practice, with automatic checks
  remember:    the most important things, in a few lines

Text format: paragraphs separated by a blank line, lists with "- ",
`code`, **bold** and code blocks between ```.
build.py runs every example and every solution before building the page.
"""

LESSONS = [

# ───────────────────────────────────────────────────────────── 1
{
"id": "hello", "title": "Hi! I'm Cupi",
"pose": "wave", "bubble": "Hi! Let's learn together.",
"story": """
Meet **Cupi**. He's a strawberry cupcake who lives in the display case of a bakery. He has twelve colorful sprinkles, lots of curiosity, and a problem you'll soon discover.

Cupi is going to teach you a programming language that has the same name as him: **Cupcake**. Small, sweet and easy to understand. Programming means writing instructions so the computer does things. And you don't need to know anything beforehand: we start from zero.
""",
"explanation": """
The first instruction is `show`. Whatever you put between the parentheses appears on the screen:

```
show("Hello, world!")
```

Words go **between quotes**. That way the computer knows it's a text to show just as it is.

You can write several instructions, one per line. The computer does them **in order**, from top to bottom.

And if a line starts with `#`, it's a **note for people**. The computer ignores it:

```
# This is a note: the computer doesn't read it
show("This one does get shown")
```
""",
"examples": [
{"text": "Press **Run** and see what happens:",
 "code": """show("Hello, world!")
show("I'm Cupi, and I have twelve sprinkles")
"""},
{"text": "A fun fact: they're called *cupcakes* because they used to be baked in cups. One of the first recipes appeared in a cookbook from **1796**.",
 "code": """# Fun facts about cupcakes
show("They used to be baked in cups")
show("One of the first recipes is from 1796")
"""},
],
"exercises": [
{"task": "Write a program that shows **your name** on one line and **your favorite animal** on another.",
 "starter": "# Write your first program here\n",
 "solution": 'show("My name is Ana")\nshow("My favorite animal is the cat")\n',
 "checks": [
   {"kind": "runs", "text": "The program works"},
   {"kind": "uses", "pattern": r"show\(", "text": "Uses show(…)", "hint": "Write show(\"your text\")"},
   {"kind": "lines", "min": 2, "text": "Shows at least two lines", "hint": "Use show(…) twice, one on each line."},
 ],
 "hints": ["Each show(…) shows one line.", "The text goes between quotes: show(\"My name is Ana\")"]},
],
"remember": [
"`show(\"text\")` shows something on the screen.",
"Texts go between quotes.",
"Instructions run in order, from top to bottom.",
"`#` is for writing notes.",
],
},

# ───────────────────────────────────────────────────────────── 2
{
"id": "variables", "title": "Boxes with names: variables",
"pose": "boxes", "bubble": "I keep everything in labeled boxes!",
"story": """
Cupi is very tidy. Everything he wants to remember goes into **boxes**, and on each box he sticks a **label** with a name. That way, when he needs something, he looks for the label and that's it.
""",
"explanation": """
In programming, those boxes are called **variables**. You create them like this:

```
sprinkles = 12
name = "Cupi"
```

You read it as: “put 12 in a box called `sprinkles`”. The `=` sign means **store**, not “is equal to”.

Afterwards, you use the box's name to get what's inside:

```
show(name, "has", sprinkles, "sprinkles")
```

`show` can show several things at once, separated by commas. It puts them on the same line, with a space between them.

A box can hold **numbers** (`12`, `3.5`) or **texts** (`"Cupi"`). And you can **change** what it holds:

```
sprinkles = 12
sprinkles = sprinkles + 2      # now it holds 14
```

Box names have **no spaces** and can't start with a number: `my_sprinkles`, not `my sprinkles`.
""",
"examples": [
{"text": "Cupi stores his details:",
 "code": """name = "Cupi"
sprinkles = 12
color = "orange"

show(name, "has", sprinkles, "sprinkles")
show("His favorite color is", color)
"""},
{"text": "He got two new sprinkles:",
 "code": """sprinkles = 12
show("Before:", sprinkles)

sprinkles = sprinkles + 2
show("Now:", sprinkles)
"""},
],
"exercises": [
{"task": "Create a variable `name` with your name and a variable `age` with your age. Then show them on one line with `show`.",
 "starter": "# 1. Create the variable for your name\n\n# 2. Create the variable for your age\n\n# 3. Show them\n",
 "solution": 'name = "Ana"\nage = 9\nshow(name, "is", age, "years old")\n',
 "checks": [
   {"kind": "runs", "text": "The program works"},
   {"kind": "uses", "pattern": r"\bname\s*=", "text": "Creates the variable name", "hint": "name = \"Ana\""},
   {"kind": "uses", "pattern": r"\bage\s*=\s*\d", "text": "Creates the variable age with a number", "hint": "age = 9 (no quotes: it's a number)"},
   {"kind": "uses", "pattern": r"show\([^)]*\bname\b[^)]*\bage\b|show\([^)]*\bage\b[^)]*\bname\b", "text": "Shows both with show",
    "hint": "show(name, \"is\", age, \"years old\")"},
 ],
 "hints": ["A variable is created like this: name = value", "To show several things, separate them with commas inside show(…)"]},
],
"remember": [
"A variable is a box with a name: `sprinkles = 12`.",
"`=` means **store**.",
"It can hold numbers or texts, and it can change.",
],
},

# ───────────────────────────────────────────────────────────── 3
{
"id": "texts", "title": "Texts with values",
"pose": "sign", "bubble": "My sign updates itself!",
"story": """
Cupi made a sign for the door of his house: “Here lives Cupi, who has 12 sprinkles”. But every time he gets a new sprinkle, he has to make the sign all over again. What if the sign could **update itself**?
""",
"explanation": """
Inside a text you can put **curly braces** `{ }` with the name of a variable. Cupcake puts its value in that spot:

```
name = "Cupi"
sprinkles = 12
show("Here lives {name}, who has {sprinkles} sprinkles")
```

It shows: `Here lives Cupi, who has 12 sprinkles`.

Inside the braces you can also do **math**:

```
show("Half of his sprinkles is {sprinkles / 2}")
```

And if you ever want to write a real curly brace, put a backslash before it: `\\{`.
""",
"examples": [
{"text": "Cupi's sign:",
 "code": """name = "Cupi"
sprinkles = 12
show("Here lives {name}, who has {sprinkles} sprinkles")
"""},
{"text": "With math inside the braces:",
 "code": """sprinkles = 12
show("Half of his sprinkles is {sprinkles // 2}")
show("If he gets 4 more sprinkles, he'll have {sprinkles + 4}")
"""},
],
"exercises": [
{"task": "Cupi shares `sprinkles = 120` between two cupcakes. Show the text `Each cupcake gets 60 sprinkles`, working out half **inside the braces**.",
 "starter": "sprinkles = 120\n\n# Show how many sprinkles each cupcake gets\n",
 "solution": 'sprinkles = 120\nshow("Each cupcake gets {sprinkles // 2} sprinkles")\n',
 "checks": [
   {"kind": "runs", "text": "The program works"},
   {"kind": "output", "contains": "Each cupcake gets 60 sprinkles", "text": "Shows “Each cupcake gets 60 sprinkles”",
    "hint": "show(\"Each cupcake gets {sprinkles // 2} sprinkles\")"},
   {"kind": "uses", "pattern": r"\{[^}]*sprinkles[^}]*\}", "text": "Does the math inside the braces", "hint": "Write the math between braces: {sprinkles // 2}"},
 ],
 "hints": ["There are two cupcakes: you need to divide by 2.", "// divides without decimals: 120 // 2 gives 60."]},
],
"remember": [
"`\"Hello, {name}\"`: whatever goes between braces is replaced by its value.",
"You can also do math between braces: `{sprinkles + 4}`.",
],
},

# ───────────────────────────────────────────────────────────── 4
{
"id": "math", "title": "Math, math and more math",
"pose": "calculator", "bubble": "How many cupcakes did you say?",
"story": """
Here's Cupi's problem: **his friends have a real sweet tooth**. His best friend, **Argos**, is a little monster with **100 mouths**, and every single one of them is hungry! Cupi wants to give him cupcakes: one for each mouth. And cupcakes cost money. Cupi isn't very good at math, but the computer is.
""",
"explanation": """
Cupcake knows how to do math:

- `+` adds and `-` subtracts
- `*` multiplies (it's the “times”)
- `/` divides
- `//` divides **without decimals**: `7 // 2` gives `3`
- `%` is the **remainder** of a division: `7 % 2` gives `1`
- `**` is “to the power of”: `2 ** 3` gives `8`

Just like in math class, multiplying and dividing happen first, and then adding and subtracting. **Parentheses** change the order:

```
show(2 + 3 * 4)        # 14
show((2 + 3) * 4)      # 20
```
""",
"examples": [
{"text": "How much do the cupcakes for Argos cost?",
 "code": """mouths = 100
price = 3          # each cupcake costs 3 coins

total = mouths * price
show("The cupcakes cost {total} coins")
show("That's {mouths // 2} boxes of two")
"""},
{"text": "The six operations:",
 "code": """show(7 + 2, 7 - 2, 7 * 2)
show(7 / 2, 7 // 2, 7 % 2)
show(2 ** 10)
"""},
],
"exercises": [
{"task": "Argos has a cousin with even more mouths: **250**. Each cupcake costs **4** coins. Work out the total and show it (it should be **1000**).",
 "starter": "mouths = 250\nprice = 4\n\n# Work out the total and show it\n",
 "solution": 'mouths = 250\nprice = 4\n\ntotal = mouths * price\nshow("Total: {total} coins")\n',
 "checks": [
   {"kind": "runs", "text": "The program works"},
   {"kind": "output", "contains": "1000", "text": "Shows 1000", "hint": "total = mouths * price"},
   {"kind": "not_uses", "pattern": r"1000", "text": "The computer works it out (without typing 1000 yourself)",
    "hint": "Use the variables mouths and price: mouths * price"},
 ],
 "hints": ["Multiplying is written with *", "total = mouths * price, and then show(total)"]},
],
"remember": [
"`+ - * /` like in math; `//` divides without decimals; `%` gives the remainder.",
"Parentheses change the order of the math.",
],
},

# ───────────────────────────────────────────────────────────── 5
{
"id": "reading", "title": "Reading what you type",
"pose": "question", "bubble": "And how many mouths do you have?",
"story": """
Until now, Cupi has been talking to himself. Now he wants to **have a conversation**: you type things to him, and he uses what you typed.
""",
"explanation": """
`read` shows a message, waits for the person to type something and press Enter, and stores it:

```
name = read("What's your name? ")
show("Hello, {name}!")
```

The message can be a question, but it doesn't have to be: `read("Type your name: ")` or `read("Press Enter to continue…")` work too.

What the person types is **always a text**. If you want a **number**, to do math with, use `read_num`:

```
age = read_num("How old are you? ")
show("Next year you'll be {age + 1}")
```

And if the person types letters instead of a number, `read_num` patiently asks for the number again.

On this page, the answers are written **before running**, in the **Answers** box, one per line.
""",
"examples": [
{"text": "Cupi asks you questions. The answers are already written in the **Answers** box: change them and run again.",
 "inputs": "Ana\n9",
 "code": """name = read("What's your name? ")
age = read_num("How old are you? ")

show("Hello, {name}!")
show("Next year you'll be {age + 1} years old")
"""},
{"text": "If the answer isn't a number, `read_num` asks again. Here the first answer is `lots`:",
 "inputs": "lots\n100",
 "code": """mouths = read_num("How many mouths do you have? ")
show("{mouths} mouths! You need {mouths // 2} boxes of cupcakes")
"""},
],
"exercises": [
{"task": "Ask **how many mouths** a little monster has and show **how many boxes** it needs (each box holds two cupcakes). With the answer `40`, it should show `20`.",
 "inputs": "40",
 "starter": "# Ask how many mouths it has\n\n# Show how many boxes it needs\n",
 "solution": 'mouths = read_num("How many mouths do you have? ")\nshow("You need {mouths // 2} boxes of cupcakes")\n',
 "checks": [
   {"kind": "runs", "text": "The program works"},
   {"kind": "uses", "pattern": r"read(_num)?\(", "text": "Reads the number with read_num(…)", "hint": "mouths = read_num(\"How many mouths do you have? \")"},
   {"kind": "output", "contains": "20", "text": "With 40 mouths, it shows 20", "hint": "The boxes are mouths // 2"},
 ],
 "hints": ["To read a number: read_num(\"message\")", "mouths = read_num(\"How many mouths do you have? \")"]},
],
"remember": [
"`read(\"message\")` shows the message and gives back what the person types, as text.",
"`read_num(\"message\")` keeps asking until it gets a number.",
"For files: `load(\"file.txt\")` loads and `save(\"file.txt\", text)` saves.",
],
},

# ───────────────────────────────────────────────────────────── 6
{
"id": "decisions", "title": "Deciding: if and else",
"pose": "crossroads", "bubble": "Which way do I go?",
"story": """
Cupi goes out for a walk and reaches a fork in the road: if it's raining, he takes the covered path; if not, he goes through the park. Programs make **decisions** too.
""",
"explanation": """
To decide, you use `if`. The `if` line ends with `:` (a colon), and whatever goes **below it, indented**, happens **only if** the condition is true:

```
if raining:
    show("I'll take the covered path")
```

**Indentation** is the spaces at the start of the line: 4 spaces, or the **Tab** key. It shows what is **inside** the `if`. When a line starts further to the left again, the block is over. What goes inside always goes **on the line below**, indented, even if it's just one instruction.

With `else` you decide what to do otherwise, and with `else if` you can check more cases:

```
if temperature > 30:
    show("It's so hot!")
else if temperature > 15:
    show("It's nice out")
else:
    show("Time to put on a scarf!")
```

**Comparisons** answer `true` or `false`:

- `==` is equal, `!=` is different
- `<` less than, `>` greater than, `<=` less or equal, `>=` greater or equal
- `x in 10..20`: is it between 10 and 20, counting both?

`==` has **two** signs, because a single one is for storing. And to join conditions: `and` (both), `or` (at least one), `not` (the opposite).

**When there are many cases**, `when` lines them up like a list. The first one that matches wins:

```
when color:
    is "pink":
        show("Just like Cupi!")
    is "red":
        show("Like his cherry")
    else:
        show("A new color")
```

Each case says **what to do** after the `:`. The last one, `else`, is for everything else. And if a case needs several lines, they go below it, indented a bit more.

And `not` gives the opposite: `if not raining:` reads “if it's not raining”.
""",
"examples": [
{"text": "Change the temperature and run again:",
 "code": """temperature = 22

if temperature > 30:
    show("It's so hot!")
else if temperature > 15:
    show("It's nice out")
else:
    show("Time to put on a scarf!")
"""},
{"text": "`when` with several cases. With `in` you ask whether it's in a range:",
 "code": """age = 12

when age:
    in 0..5:
        show("Little one")
    in 6..12:
        show("Kid")
    in 13..17:
        show("Teenager")
    else:
        show("Grown-up")

show(age in 10..15)
"""},
],
"exercises": [
{"task": "Cupi has `cupcakes = 100` and Argos has `mouths = 100`. If there's a cupcake for each mouth, show `Let's eat!`. If not, show `Not enough cupcakes`.",
 "starter": "cupcakes = 100\nmouths = 100\n\n# Decide what to show\n",
 "solution": 'cupcakes = 100\nmouths = 100\n\nif cupcakes >= mouths:\n    show("Let\'s eat!")\nelse:\n    show("Not enough cupcakes")\n',
 "checks": [
   {"kind": "runs", "text": "The program works"},
   {"kind": "uses", "pattern": r"\bif\b", "text": "Uses if", "hint": "if cupcakes >= mouths: …"},
   {"kind": "uses", "pattern": r"\belse\b", "text": "Uses else for the other case", "hint": "else:  (lined up with the if)"},
   {"kind": "output", "contains": "Let's eat!", "text": "With 100 and 100, shows “Let's eat!”"},
 ],
 "hints": ["The condition is: cupcakes >= mouths", "if cupcakes >= mouths: … and below it, else: …"]},
{"task": "Using `when`, make it show, depending on the `grade`: from 9 to 10 `Excellent!`, from 6 to 8 `Passed`, and otherwise `Study a bit more`. With `grade = 7` it should show `Passed`.",
 "starter": "grade = 7\n\n# Use when to decide\n",
 "solution": 'grade = 7\n\nwhen grade:\n    in 9..10:\n        show("Excellent!")\n    in 6..8:\n        show("Passed")\n    else:\n        show("Study a bit more")\n',
 "checks": [
   {"kind": "runs", "text": "The program works"},
   {"kind": "uses", "pattern": r"\bwhen\b", "text": "Uses when", "hint": "when grade:  and below it  in 9..10:"},
   {"kind": "output", "contains": "Passed", "text": "With 7, shows “Passed”"},
   {"kind": "no_output", "contains": "Excellent", "text": "Doesn't show “Excellent!”"},
 ],
 "hints": ["Each case: in from..to:  and below it, indented, show(…)", "The last case is: else:  and below it show(\"Study a bit more\")"]},
],
"remember": [
"`if condition: …` happens only if it's true.",
"`else if` checks another case; `else` is everything else.",
"`when value:` with the cases `is …: …`, `in …: …` and `else: …` below it, for many cases.",
"Compare: `== != < > <= >=`, and `x in 1..10` for “between”. Join: `and`, `or`, `not`.",
],
},

# ───────────────────────────────────────────────────────────── 7
{
"id": "loops", "title": "Repeating",
"pose": "laps", "bubble": "One sprinkle, another sprinkle, another…!",
"story": """
Cupi wants to count his sprinkles, but there are so many that he gets tired. Luckily, the computer **loves repeating things**: it can do the same thing a thousand times without getting bored.
""",
"explanation": """
The easiest one: `repeat` repeats something **a number of times**:

```
repeat 3:
    show("Hip, hip, hooray!")
```

`for` repeats **for each number** in a range, and on each round it tells you which one it is. The range `1..5` goes from 1 to 5, **both included**:

```
for i in 1..5:
    show("Sprinkle number {i}")
```

With `by` you can skip ahead in steps, or go backwards:

```
for i in 0..10 by 2:
    show(i)        # 0, 2, 4, 6, 8, 10
for i in 3..1 by -1:
    show(i)        # 3, 2, 1
```

`while` repeats **as long as** something is true:

```
cupcakes = 0
while cupcakes != 3:
    cupcakes += 1
    show("I decorated cupcake {cupcakes}")
```

`cupcakes += 1` is the same as `cupcakes = cupcakes + 1`: “add one to it”.

Be careful: if the condition never changes, it repeats forever! Inside a loop, `break` leaves right away and `continue` jumps to the next round.
""",
"examples": [
{"text": "Hooray!",
 "code": """repeat 3:
    show("Hip, hip, hooray!")
"""},
{"text": "Cupi counts his first sprinkles, and then counts backwards to go into the oven:",
 "code": """for i in 1..5:
    show("Sprinkle number {i}")

for i in 3..1 by -1:
    show("{i}…")
show("Into the oven!")
"""},
{"text": "Cupi decorates cupcakes until he has three:",
 "code": """cupcakes = 0
while cupcakes != 3:
    cupcakes += 1
    show("I decorated cupcake {cupcakes}")
show("Done: {cupcakes} cupcakes")
"""},
],
"exercises": [
{"task": "Show the **7 times table**, from 1 to 10, like this: `7 x 1 = 7`, `7 x 2 = 14`… up to `7 x 10 = 70`.",
 "starter": "# Repeat from 1 to 10\n",
 "solution": 'for i in 1..10:\n    show("7 x {i} = {7 * i}")\n',
 "checks": [
   {"kind": "runs", "text": "The program works"},
   {"kind": "uses", "pattern": r"\bfor\b|\bwhile\b", "text": "Uses a loop", "hint": "for i in 1..10:"},
   {"kind": "output", "contains": "7 x 1 = 7", "text": "Starts with 7 x 1 = 7"},
   {"kind": "output", "contains": "7 x 10 = 70", "text": "Ends with 7 x 10 = 70", "hint": "The range 1..10 includes the 10."},
 ],
 "hints": ["for i in 1..10:", "Below it, indented: show(\"7 x {i} = {7 * i}\")"]},
],
"remember": [
"`repeat 3: …` repeats three times.",
"`for i in 1..5: …` repeats with i = 1, 2, 3, 4, 5. With `by 2`, in steps of two.",
"`while` repeats as long as something is true.",
"`break` leaves; `continue` jumps to the next round.",
],
},

# ───────────────────────────────────────────────────────────── 8
{
"id": "lists", "title": "Lists: lots of things in a row",
"pose": "row", "bubble": "My cupcakes line up in a row!",
"story": """
Have you noticed that in the bakery's display case the cupcakes sit **in a row**? The first, the second, the third… one after another. In programming, that's a **list**.
""",
"explanation": """
A list holds several things in order, between **square brackets** `[ ]`:

```
friends = ["Blip", "Kora", "Zum"]
```

Each thing has a **position**, and counting starts **at 0**:

```
show(friends[0])      # Blip    (the first one)
show(friends[2])      # Zum
show(friends[-1])     # Zum   (the last one)
```

To **slice** out a piece you use `..`, like in ranges:

```
show(friends[0..1])   # ["Blip", "Kora"]
```

Functions for lists:
- `len(list)` counts how many things it has;
- `add(list, x)` adds something at the end;
- `drop(list, x)` removes something;
- `count(list, x)` counts how many times something is in it.

And to ask whether something is in the list, you use `in`:

```
"Kora" in friends          # is Kora in the list?
"Nova" not in friends      # is Nova not in it?
friends is empty           # is it empty?
```

`add` and `drop` **give back a new list**. That's why you store the result: `friends = add(friends, "Nova")`.

And `for` lets you go through a list, one by one. With `at`, you also get the position:

```
for i, friend at friends:
    show("{i}: Hello, {friend}!")
```
""",
"examples": [
{"text": "Cupi's friends:",
 "code": """friends = ["Blip", "Kora", "Zum"]

show(friends[0], "goes first")
show("He has {len(friends)} friends")

friends = add(friends, "Nova")
show(friends)

for friend in friends:
    show("Hello, {friend}!")
"""},
{"text": "Searching and slicing:",
 "code": """cupcakes = ["red", "blue", "green", "yellow", "purple", "red"]

show("blue" in cupcakes, "black" not in cupcakes)
show(cupcakes[1..3])
show("There are {count(cupcakes, "red")} red cupcakes")

for i, c at cupcakes:
    show("{i}: {c}")
"""},
],
"exercises": [
{"task": "Cupi has `fruits = [\"apple\", \"pear\"]`. Add `\"mango\"` to the list and show **how many fruits** there are (it should be 3) and **which one is last**.",
 "starter": 'fruits = ["apple", "pear"]\n\n# Add the mango\n\n# Show how many there are and the last one\n',
 "solution": 'fruits = ["apple", "pear"]\n\nfruits = add(fruits, "mango")\n\nshow(len(fruits), fruits[-1])\n',
 "checks": [
   {"kind": "runs", "text": "The program works"},
   {"kind": "uses", "pattern": r"fruits\s*=\s*add\(", "text": "Adds with add and stores the result", "hint": "fruits = add(fruits, \"mango\")"},
   {"kind": "output", "contains": "3", "text": "Shows 3", "hint": "len(fruits)"},
   {"kind": "output", "contains": "mango", "text": "Shows the mango, which is the last one", "hint": "fruits[-1] is the last one"},
 ],
 "hints": ["fruits = add(fruits, \"mango\")", "show(len(fruits), fruits[-1])"]},
],
"remember": [
"A list goes between square brackets: `[\"a\", \"b\"]`. Counting starts at 0.",
"`len`, `add`, `drop`, `count`. To ask: `x in list`, `x not in list`, `list is empty`.",
"To slice: `list[1..3]`. To know the position: `for i, x at list`.",
"`add` and `drop` give back a new list: store it.",
],
},

# ───────────────────────────────────────────────────────────── 9
{
"id": "dictionaries", "title": "Dictionaries: looking things up by name",
"pose": "book", "bubble": "I look up the word, and find its value.",
"story": """
At the bakery, each cupcake size has a price. Cupi doesn't want to remember “the third one on the list”: he wants to ask “how much is the small size?”. That's what **dictionaries** are for.
""",
"explanation": """
A dictionary is like a list, but each thing has a **key** instead of a position. You write it just like a list, adding `key:` in front of each value:

```
prices = ["small": 3, "medium": 5, "large": 8]
```

You look things up by key:

```
show(prices["medium"])     # 5
```

You can **add** or **change** a value:

```
prices["giant"] = 12
prices["small"] = 4
```

Handy functions:
- `keys(dict)`: the keys;
- `values(dict)`: the values;
- `key in dict`: does it have that key?

If you look up a key that doesn't exist, Cupcake warns you with an error. But if you want a **backup value**, use `else`:

```
price = prices["mini"] else 0     # if there's no mini size, 0
```

An empty dictionary is written `[:]`.
""",
"examples": [
{"text": "The bakery's prices:",
 "code": """prices = ["small": 3, "medium": 5, "large": 8]

show("The medium size costs", prices["medium"])

prices["giant"] = 12
show(keys(prices))
show("mini" in prices)
show(prices["mini"] else "there's no mini size")

for size in keys(prices):
    show("Size {size}: {prices[size]} coins")
"""},
],
"exercises": [
{"task": "Create a dictionary `ages` with two friends and their ages (for example, Blip is 3 and Kora is 5). Then add Zum, who is 4, and show **Zum's age**.",
 "starter": "# Create the dictionary\n\n# Add Zum\n\n# Show Zum's age\n",
 "solution": 'ages = ["Blip": 3, "Kora": 5]\nages["Zum"] = 4\nshow(ages["Zum"])\n',
 "checks": [
   {"kind": "runs", "text": "The program works"},
   {"kind": "uses", "pattern": r"\[\s*\"[^\"]+\"\s*:", "text": "Creates a dictionary with key: value", "hint": "ages = [\"Blip\": 3, \"Kora\": 5]"},
   {"kind": "uses", "pattern": r"ages\[\s*\"Zum\"\s*\]\s*=", "text": "Adds Zum", "hint": "ages[\"Zum\"] = 4"},
   {"kind": "output", "contains": "4", "text": "Shows Zum's age"},
 ],
 "hints": ["A dictionary: [\"key\": value, …]", "ages[\"Zum\"] = 4 and then show(ages[\"Zum\"])"]},
],
"remember": [
"Dictionary: `[\"key\": value]`. Empty: `[:]`.",
"Look up with `dict[\"key\"]` and add with `dict[\"key\"] = value`.",
"`keys`, `values`, `key in dict`. Backup value: `dict[\"x\"] else 0`.",
],
},

# ───────────────────────────────────────────────────────────── 10
{
"id": "records", "title": "Records: cards with fields",
"pose": "card", "bubble": "This is my card!",
"story": """
Argos signed up for the bakers' club, and they gave him a **membership card**: name, mouths, color. Each detail in its own slot. In Cupcake, a card like that is called a **record**.
""",
"explanation": """
A record gathers several details about **one single thing**, each with its own name (its **field**). It goes between parentheses:

```
argos = (name: "Argos", mouths: 100, color: "green")
```

Each field is read with a **dot**:

```
show(argos.name)        # Argos
show(argos.mouths)      # 100
```

And it can be changed:

```
argos.mouths = 102
```

A record **is born with its fields**, and you can't add others to it. If you misspell a field, Cupcake warns you and suggests the right one. That way no data gets lost because of a typo!

**Is there something in that field?** With `has` you ask whether a field has something: a number greater than 0, a text or a list with something in it, or `true`. It always answers `true` or `false`:

```
argos = (name: "Argos", mouths: 100, asleep: false)

if argos has mouths:
    show("Argos is hungry!")

if argos has not asleep:
    show("And he's awake")
```

You can ask about several fields at once with `and` and `or`: `argos has mouths and name`. And if the field doesn't exist, `has` answers `false`.

**Dictionary or record?**
- A **record** describes **one thing**, with fixed fields: Argos's card.
- A **dictionary** is a **collection** that can grow: the shop's prices.
""",
"examples": [
{"text": "Argos's card:",
 "code": """argos = (name: "Argos", mouths: 100, color: "green")

show("{argos.name} is {argos.color}")
argos.mouths = 102
show(argos)
"""},
{"text": "A typo. Run it and see how Cupcake helps you:",
 "expect": "error",
 "code": """argos = (name: "Argos", mouths: 100)
argos.mouhts = 102
"""},
{"text": "A list of records:",
 "code": """club = [
    (name: "Argos", mouths: 100),
    (name: "Blip", mouths: 6),
    (name: "Kora", mouths: 8),
]

for member in club:
    show("{member.name} eats with {member.mouths} mouths")
"""},
{"text": "`has` in a game: who's still standing? With a list, `has` asks whether **anyone** has that field:",
 "code": """cupi = (name: "Cupi", energy: 3, shield: false)
rival = (name: "Glub", energy: 0, shield: true)

if cupi has energy and rival has not energy:
    show("{cupi.name} won the race!")

if rival has shield:
    show("{rival.name} has a shield")

team = [cupi, rival]
if team has energy:
    show("Someone on the team can still play")
"""},
],
"exercises": [
{"task": "Create a record `pet` with the fields `name`, `animal` and `age`. Then it's **its birthday**: add 1 to its age and show the record.",
 "starter": "# Create the pet record\n\n# Add 1 to its age\n\n# Show it\n",
 "solution": 'pet = (name: "Luna", animal: "cat", age: 3)\npet.age = pet.age + 1\nshow(pet)\n',
 "checks": [
   {"kind": "runs", "text": "The program works"},
   {"kind": "uses", "pattern": r"\(\s*name\s*:", "text": "Creates a record with the field name", "hint": "pet = (name: \"Luna\", animal: \"cat\", age: 3)"},
   {"kind": "uses", "pattern": r"pet\.age\s*=", "text": "Changes the age with a dot", "hint": "pet.age = pet.age + 1"},
   {"kind": "output", "contains": "age:", "text": "Shows the record", "hint": "show(pet)"},
 ],
 "hints": ["A record: (field: value, field: value)", "pet.age = pet.age + 1"]},
],
"remember": [
"Record: `(name: \"Argos\", mouths: 100)`.",
"Read and change it with a dot: `argos.mouths`.",
"`argos has mouths` asks whether that field has something; it answers `true` or `false`.",
"It never gets new fields: that's how typos get caught.",
],
},

# ───────────────────────────────────────────────────────────── 11
{
"id": "functions", "title": "Functions: your own instructions",
"pose": "tool", "bubble": "I built my own tool!",
"story": """
Cupi got tired of working out, every single time, how many boxes a friend needs. So he invented his own instruction: he tells it how many mouths someone has, and it answers how many boxes they need. That's a **function**.
""",
"explanation": """
A function is an instruction **that you invent**. You create it with `fx`, like the f(x) from math class:

```
fx boxes(mouths):
    return mouths // 2
```

- `boxes` is its name;
- `mouths`, between parentheses, is the data it **receives**;
- `return` says what it **gives back**.

And you use it like any other instruction:

```
show(boxes(100))     # 50
show(boxes(6))       # 3
```

Without `return`, the function does what it says but gives nothing back (it gives back `none`). If you write a line that only calculates something, like `mouths // 2`, Cupcake warns you that the `return` is missing.

A function can receive several pieces of data, and some can have a **default value**:

```
fx greet(name, greeting = "Hello"):
    show("{greeting}, {name}")

greet("Cupi")                         # Hello, Cupi
greet("Blip", greeting = "Hi there")  # Hi there, Blip
```

Functions also work as a **mold** for making records that are all alike:

```
fx friend(name, mouths):
    return (name: name, mouths: mouths)
```
""",
"examples": [
{"text": "Cupi's tool:",
 "code": """fx boxes(mouths):
    return mouths // 2

show("Argos needs", boxes(100), "boxes")
show("Blip needs", boxes(6), "boxes")
"""},
{"text": "Greetings with a default value:",
 "code": """fx greet(name, greeting = "Hello"):
    show("{greeting}, {name}")

greet("Cupi")
greet("Blip", greeting = "Hi there")
"""},
],
"exercises": [
{"task": "Create a function `cost(mouths, price)` that gives back how much the cupcakes cost (mouths × price). Use it to show the cost for **100 mouths at 3 coins** (it should be 300).",
 "starter": "# Create the cost function\n\n# Use it and show the result\n",
 "solution": 'fx cost(mouths, price):\n    return mouths * price\n\nshow(cost(100, 3))\n',
 "checks": [
   {"kind": "runs", "text": "The program works"},
   {"kind": "uses", "pattern": r"fx\s+cost\s*\(", "text": "Creates the function cost", "hint": "fx cost(mouths, price): …"},
   {"kind": "output", "contains": "300", "text": "Shows 300", "hint": "show(cost(100, 3))"},
 ],
 "hints": ["fx cost(mouths, price):  and below it  return mouths * price", "To use it: show(cost(100, 3))"]},
],
"remember": [
"`fx name(data): …` creates a function.",
"`return` gives back the result. Without `return`, the function gives nothing back.",
"Data can have a default value: `greeting = \"Hello\"`.",
],
},

# ───────────────────────────────────────────────────────────── 12
{
"id": "copies", "title": "Data gets copied",
"pose": "photocopy", "bubble": "There are two Cupis! Well, one is a copy.",
"story": """
Cupi lent his card to Blip so he could see how to fill one in. Blip crossed things out, drew on it, wrote all over it… but Cupi's card stayed perfect! Why? Because Cupi gave him a **photocopy**.
""",
"explanation": """
In Cupcake, when you store something in another variable, or pass it to a function, a **copy** is made. Each name has **its own data**:

```
a = [1, 2]
b = a
b = add(b, 3)
show(a)      # [1, 2]       ← a didn't change
show(b)      # [1, 2, 3]
```

This avoids surprises: nothing changes “behind your back”. (In many other languages, `a` would have changed too, and that's very confusing.)

That's why, if a function **changes** something, it has to **give it back**, and you decide to store it:

```
fx decorate(c):
    c.sprinkles = c.sprinkles + 2
    return c

cupi = decorate(cupi)       # ← store what it gave back
```

If you forget to store the result, the change stays in the copy and gets lost.
""",
"examples": [
{"text": "The photocopies:",
 "code": """cupi = (name: "Cupi", sprinkles: 12)
copy = cupi
copy.sprinkles = 4

show(cupi.sprinkles)      # the original didn't change
show(copy.sprinkles)
"""},
{"text": "A function that changes something and gives it back:",
 "code": """fx decorate(c):
    c.sprinkles = c.sprinkles + 2
    return c

cupi = (name: "Cupi", sprinkles: 12)
decorate(cupi)
show("Without storing:", cupi.sprinkles)

cupi = decorate(cupi)
show("Storing it:", cupi.sprinkles)
"""},
],
"exercises": [
{"task": "This program should show `30`, but it shows `10`. **Fix it**: the result of `heal` isn't being stored.",
 "starter": 'fx heal(monster, amount):\n    monster.hp = monster.hp + amount\n    return monster\n\nkora = (name: "Kora", hp: 10)\nheal(kora, 20)\nshow(kora.hp)\n',
 "solution": 'fx heal(monster, amount):\n    monster.hp = monster.hp + amount\n    return monster\n\nkora = (name: "Kora", hp: 10)\nkora = heal(kora, 20)\nshow(kora.hp)\n',
 "checks": [
   {"kind": "runs", "text": "The program works"},
   {"kind": "uses", "pattern": r"kora\s*=\s*heal\(", "text": "Stores what heal gives back", "hint": "kora = heal(kora, 20)"},
   {"kind": "output", "contains": "30", "text": "Shows 30"},
 ],
 "hints": ["heal gives back the healed little monster, but nobody stores it.", "Change the line to: kora = heal(kora, 20)"]},
],
"remember": [
"Assigning or passing data makes a **copy**.",
"A function that changes something gives it back: `x = change(x)`.",
],
},

# ───────────────────────────────────────────────────────────── 13
{
"id": "shortcuts", "title": "Shortcuts: nameless functions and quick lists",
"pose": "magnifier", "bubble": "I only want the red cupcakes…",
"story": """
Cupi has a mountain of colorful cupcakes and wants **only the red ones**, or to **sort them by size**. He could check them one by one with a `for`… or use some awesome shortcuts.
""",
"explanation": """
**Quick lists.** You can make a new list from another one in a single line:

```
doubles = [n * 2 for n in 1..5]               # [2, 4, 6, 8, 10]
evens = [n for n in 1..10 if n % 2 == 0]      # [2, 4, 6, 8, 10]
```

You read it as: “`n * 2`, for each `n` from 1 to 5”. And with an `if` at the end, only the ones that meet the condition.

**Nameless functions.** Sometimes you need a tiny function, to use just once. You write it with `fx`, but **without a name**:

```
fx(c): c.size
```

You read it as: “given a `c`, give back `c.size`”. It's useful, for example, to tell `sorted` **what** to sort by:

```
in_order = sorted(cupcakes, fx(c): c.size)
```

And if it receives just one piece of data, you don't even need to name it: it's called `it`:

```
in_order = sorted(cupcakes, fx: it.size)
```

`λ` (the Greek letter lambda) is the same as `fx`, in case you like it better: `λ(c): c.size`.

Other functions that accept a nameless function:
- `filter(list, fx: condition)`: keeps the ones that meet it;
- `map(list, fx: change)`: changes each one;
- `count(list, fx: condition)`: counts how many meet it.
""",
"examples": [
{"text": "Quick lists:",
 "code": """show([n * 2 for n in 1..5])
show([n for n in 1..10 if n % 2 == 0])

friends = ["Blip", "Kora", "Zum"]
show([upper(f) for f in friends])
"""},
{"text": "Cupi's cupcakes:",
 "code": """cupcakes = [
    (color: "red", size: 3),
    (color: "blue", size: 1),
    (color: "red", size: 2),
]

reds = [c for c in cupcakes if c.color == "red"]
show("Red:", len(reds))
show("Big:", count(cupcakes, fx: it.size >= 2))

for c in sorted(cupcakes, fx: it.size):
    show("Size {c.size}: {c.color}")
"""},
],
"exercises": [
{"task": "From `numbers = [3, 8, 15, 4, 23, 42]`, make a list `big` with only the ones **greater than 10**, using a quick list, and show it (it should be `[15, 23, 42]`).",
 "starter": "numbers = [3, 8, 15, 4, 23, 42]\n\n# Make the list big\n",
 "solution": "numbers = [3, 8, 15, 4, 23, 42]\n\nbig = [n for n in numbers if n > 10]\nshow(big)\n",
 "checks": [
   {"kind": "runs", "text": "The program works"},
   {"kind": "uses", "pattern": r"\[[^\]]*\bfor\b[^\]]*\bif\b", "text": "Uses a quick list with if", "hint": "[n for n in numbers if n > 10]"},
   {"kind": "output", "contains": "[15, 23, 42]", "text": "Shows [15, 23, 42]"},
 ],
 "hints": ["[n for n in numbers if …]", "The condition is n > 10"]},
],
"remember": [
"Quick list: `[x * 2 for x in list if condition]`.",
"Nameless function: `fx(x): …`, or `fx: it…` if it receives just one piece of data.",
"`sorted(list, fx: it.field)` sorts by a field.",
],
},

# ───────────────────────────────────────────────────────────── 14
{
"id": "errors", "title": "Errors: friends who warn you",
"pose": "bandage", "bubble": "I tripped! But I learned something.",
"story": """
Sometimes Cupi drops a sprinkle: with so many, that's normal! What matters is **getting back up and understanding what happened**. It's the same with programs: errors aren't bad. They're **warnings** that tell you what to fix.
""",
"explanation": """
When something goes wrong, Cupcake stops and tells you **on which line** and **what happened**, and often **how to fix it**. Read it calmly! It's like a friend giving you a heads-up.

**Catching an error.** If you know something might fail, like when someone types letters instead of a number, you can **try** it with `try` and say what to do if it fails with `except`:

```
try:
    age = int(read("Age? "))
except error:
    show("That's not a number")
    age = 0
```

**Raising a warning yourself.** With `raise` you can cause an error on purpose, when something doesn't make sense:

```
if mouths < 0:
    raise "Nobody has negative mouths"
```

**A backup value.** For simple cases, `else` says what to use if something fails, in a single line:

```
age = int(read("Age? ")) else 0
```

**Checking.** `assert` checks that something is true. If it isn't, it stops and shows you the values:

```
assert cupcakes >= 0
```
""",
"examples": [
{"text": "An error on purpose. Run it and read the message calmly:",
 "expect": "error",
 "code": """mouths = 100
show("I have " + mouths + " mouths")
"""},
{"text": "Catching the error. The answer already written is `lots`, which isn't a number:",
 "inputs": "lots",
 "code": """try:
    mouths = int(read("How many mouths do you have? "))
    show("You need {mouths // 2} boxes")
except error:
    show("Oops: {error}")
"""},
],
"exercises": [
{"task": "Ask for the age. If the person **doesn't type a number**, instead of stopping, the program should show `That's not a number`. The test answer is `nine`.",
 "inputs": "nine",
 "starter": 'age = int(read("How old are you? "))\nshow("You are {age} years old")\n',
 "solution": 'try:\n    age = int(read("How old are you? "))\n    show("You are {age} years old")\nexcept error:\n    show("That\'s not a number")\n',
 "checks": [
   {"kind": "runs", "text": "The program doesn't stop with an error", "hint": "Put the code below try:, indented"},
   {"kind": "uses", "pattern": r"\btry\b", "text": "Uses try"},
   {"kind": "output", "contains": "That's not a number", "text": "Shows “That's not a number”", "hint": "except error:  and below it  show(\"That's not a number\")"},
 ],
 "hints": ["try:  (below it, what might fail)   except error:  (below it, what to do)", "Move both lines below try:, indented."]},
],
"remember": [
"Error messages tell you the line, what happened and, often, how to fix it.",
"`try: … except error: …` catches an error; `something else backup` is the short version.",
"`raise \"message\"` warns; `assert condition` checks.",
],
},

# ───────────────────────────────────────────────────────────── 15
{
"id": "files", "title": "Using other files",
"pose": "backpack", "bubble": "I carry my tools in my backpack.",
"story": """
Cupi already has lots of tools: `boxes`, `cost`, `greet`… and he wants to use them in all his programs without writing them again. He keeps them in a separate file, like in a **backpack**, and takes them out when he needs them.
""",
"explanation": """
A Cupcake program is saved in a file that ends in `.cup`. You can put your functions in one file, for example `tools.cup`, and use them from another one with `use`:

```
use boxes, cost from tools
```

You read it as: “use `boxes` and `cost` from `tools`”. After that, you use them as usual: `boxes(100)`.

Other ways:

```
use tools                       # brings everything
use boxes as half from tools    # with a different name
```

On this page, the file `tools.cup` already exists: you can see what's in it below each example.

**`main`: what runs when you run the file.** If a file has a function called `main`, Cupcake runs it at the end, **only when you run that file**. If another file uses it with `use`, its `main` does **not** run. That way you can keep tests in your tools without them getting in the way:

```
fx boxes(mouths):
    return mouths // 2

fx main():
    show(boxes(100))       # only runs if you run this file
```

`main` is optional: a short program doesn't need it.
""",
"examples": [
{"text": "Cupi uses his backpack. Notice that `tools.cup` has a `main` with tests, but it doesn't run, because here we're only using it:",
 "files": {"tools.cup": "fx boxes(mouths):\n    return mouths // 2\n\nfx cost(mouths, price):\n    return mouths * price\n\nfx main():\n    show(\"Test:\", boxes(10))\n"},
 "code": """use boxes, cost from tools

show("Boxes:", boxes(100))
show("Cost:", cost(100, 3))
"""},
],
"exercises": [
{"task": "The file `greetings.cup` has a function `greet(name)`. Use it to greet **Blip**.",
 "files": {"greetings.cup": 'fx greet(name):\n    show("Hello, {name}! Welcome to the club.")\n'},
 "starter": "# Bring greet from greetings\n\n# Greet Blip\n",
 "solution": 'use greet from greetings\n\ngreet("Blip")\n',
 "checks": [
   {"kind": "runs", "text": "The program works"},
   {"kind": "uses", "pattern": r"\buse\b", "text": "Uses use", "hint": "use greet from greetings"},
   {"kind": "output", "contains": "Hello, Blip!", "text": "Greets Blip", "hint": "greet(\"Blip\")"},
 ],
 "hints": ["use greet from greetings", "Then: greet(\"Blip\")"]},
],
"remember": [
"`use a, b from file` brings functions from `file.cup`.",
"`use file` brings everything.",
"`fx main():` runs when you run the file, but not when another file uses it.",
],
},

# ───────────────────────────────────────────────────────────── 16
{
"id": "random", "title": "Games of chance",
"pose": "dice", "bubble": "Let's see what comes up!",
"story": """
Cupi organized a fair at the bakery, with dice games and a prize wheel. But there's a problem: he doesn't know how to program something when **nobody knows what will come up**! Luckily, the computer can play games of luck too.
""",
"explanation": """
Two functions for playing with chance:

- `roll(1, 6)` gives a **random** number between 1 and 6, like a die;
- `pick(list)` chooses **a random item** from a list.

```
die = roll(1, 6)
prize = pick(["a cupcake", "a cap", "a balloon"])
```

Every time you run the program, something different might come up. Try it several times!

With `roll`, `read_num` and `while` you can already make your first real game: guess the number.
""",
"examples": [
{"text": "Cupi's dice. Run it several times:", "random": True,
 "code": """die1 = roll(1, 6)
die2 = roll(1, 6)
show("You rolled {die1} and {die2}")

if die1 == die2:
    show("Doubles! You won an extra cupcake")
"""},
{"text": "The prize wheel:", "random": True,
 "code": """prizes = ["a cupcake", "a cap", "a balloon", "a medal"]
show("You won {pick(prizes)}!")
"""},
{"text": "**Guess the number.** Cupi thinks of a number from 1 to 10, and you get three tries. Write your answers in **Answers** and run:", "random": True,
 "inputs": "5\n3\n8",
 "code": """secret = roll(1, 10)
tries = 0
guessed = false

while not (guessed or tries == 3):
    n = read_num("Which number am I thinking of? ")
    tries += 1
    if n == secret:
        guessed = true
    else if n < secret:
        show("Higher…")
    else:
        show("Lower…")

if guessed:
    show("You guessed it in {tries} tries!")
else:
    show("It was {secret}. Better luck next time!")
"""},
],
"exercises": [
{"task": "Roll **two dice** with `roll` and show the sum, like this: `Sum: 7` (the number changes every time).",
 "starter": "# Roll two dice and show the sum\n",
 "solution": 'die1 = roll(1, 6)\ndie2 = roll(1, 6)\nshow("Sum: {die1 + die2}")\n',
 "checks": [
   {"kind": "runs", "text": "The program works"},
   {"kind": "uses", "pattern": r"roll\(\s*1\s*,\s*6\s*\)[\s\S]*roll\(\s*1\s*,\s*6\s*\)", "text": "Rolls two dice with roll(1, 6)", "hint": "die1 = roll(1, 6) and die2 = roll(1, 6)"},
   {"kind": "output", "contains": "Sum:", "text": "Shows “Sum: …”", "hint": "show(\"Sum: {die1 + die2}\")"},
 ],
 "hints": ["Store each die in a variable: die1 = roll(1, 6)", "show(\"Sum: {die1 + die2}\")"]},
],
"remember": [
"`roll(1, 6)` gives a random number; `pick(list)` chooses a random item.",
"With chance involved, each run can be different.",
],
},

# ───────────────────────────────────────────────────────────── 17
{
"id": "project", "title": "Final project: Cupi's Bakery",
"pose": "trophy", "bubble": "I opened my very own bakery!",
"story": """
After handing out so many cupcakes, Cupi had an idea: **open his own bakery**, for little monsters with a sweet tooth and lots of mouths. Let's program it together, using everything you've learned.
""",
"explanation": """
The bakery needs:
- a list of **customers**, each one a **record** with their name and their mouths;
- a **dictionary** with the price of each size;
- a **function** that works out how much each customer pays;
- a **loop** to serve everyone, and an **if** to give a discount to the ones with lots of mouths.

Everything you've learned, all together!
""",
"examples": [
{"text": "Cupi's Bakery:",
 "code": """prices = ["small": 2, "medium": 3, "large": 5]

customers = [
    (name: "Blip", mouths: 6, size: "small"),
    (name: "Kora", mouths: 8, size: "medium"),
    (name: "Argos", mouths: 100, size: "large"),
]

fx bill(customer):
    total = customer.mouths * prices[customer.size]
    if customer.mouths >= 50:
        total = total - total // 10       # 10% discount
    return total

earnings = 0
for c in customers:
    payment = bill(c)
    show("{c.name} pays {payment} coins for {c.mouths} cupcakes")
    earnings = earnings + payment
show("Today Cupi earned {earnings} coins")
"""},
],
"exercises": [
{"task": "Add a new customer to the list: **Zib**, Argos's cousin, with **100 mouths** and size **medium**. With the discount, Zib should pay **270** coins.",
 "starter": """prices = ["small": 2, "medium": 3, "large": 5]

customers = [
    (name: "Blip", mouths: 6, size: "small"),
    (name: "Kora", mouths: 8, size: "medium"),
]

# Add Zib to the list of customers

fx bill(customer):
    total = customer.mouths * prices[customer.size]
    if customer.mouths >= 50:
        total = total - total // 10
    return total

for c in customers:
    show("{c.name} pays {bill(c)} coins")
""",
 "solution": """prices = ["small": 2, "medium": 3, "large": 5]

customers = [
    (name: "Blip", mouths: 6, size: "small"),
    (name: "Kora", mouths: 8, size: "medium"),
]

customers = add(customers, (name: "Zib", mouths: 100, size: "medium"))

fx bill(customer):
    total = customer.mouths * prices[customer.size]
    if customer.mouths >= 50:
        total = total - total // 10
    return total

for c in customers:
    show("{c.name} pays {bill(c)} coins")
""",
 "checks": [
   {"kind": "runs", "text": "The program works"},
   {"kind": "output", "contains": "Zib pays 270 coins", "text": "Zib pays 270 coins",
    "hint": "customers = add(customers, (name: \"Zib\", mouths: 100, size: \"medium\"))"},
 ],
 "hints": ["To add to a list: list = add(list, new_one)", "The new customer is a record: (name: \"Zib\", mouths: 100, size: \"medium\")"]},
],
"remember": [
"You know how to program now! Variables, decisions, loops, lists, dictionaries, records, functions and errors.",
"Now invent your own program: a game, a to-do list, a calculator… whatever you can imagine.",
],
},
]
