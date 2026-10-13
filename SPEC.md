**English** · [Español](SPEC.es.md)

# Cupcake

**Version 1.0 "Frambuesa"**

A small, comfortable scripting language with **no classes, no objects and no methods**. There are only **data** and **functions**.

Files use the `.cup` extension.

> A cupcake is small, sweet and understood at a glance: one whole serving, no hidden layers. That's what Cupcake wants to be: simple data and small functions, with no hierarchies and nothing hidden.

---

## 1. The ideas

1. **Data is just data.** A record holds fields and nothing else: it has no functions inside and doesn't "know how to do" anything.
2. **Everything that does something is a function.** There is no `list.append(x)`: you write `add(list, x)`.
3. **Data is copied.** If a piece of data changed, you can see it on the line where it was assigned. Nothing changes behind your back.
4. **It reads like a sentence.** `"Pikachu" in team`, `if list is empty`, `age in 10..18`.
5. **Simple.** When you have to choose between a short way and a clear way, clear wins.

---

## 2. A complete program

```
# A small Pokémon team in Cupcake

use describe from pokemon

team = [
    (name: "Pikachu",    type: "electric", hp: 12),
    (name: "Charmander", type: "fire",     hp: 39),
    (name: "Squirtle",   type: "water",    hp: 0),
]

fx heal(p, amount):
    p.hp = min(p.hp + amount, 40)
    return p

alive = [heal(p, 20) for p in team if p.hp > 0]

for p in sorted(alive, fx: it.name):
    show(describe(p))

for p in team:
    when p.hp:
        is 0:
            status = "needs to go to the Pokémon Center"
        in 1..19:
            status = "is weak"
        else:
            status = "is fine"
    show("{p.name} {status}")
```

---

## 3. The basics

```
# A comment

name = "Ash"
age = 10
height = 1.45
ready = true
winner = none
```

| What | How you write it |
|---|---|
| Comment | `# to the end of the line` |
| Numbers | `10`, `1.45` |
| Text | `"Hello"` or `'Hello'` |
| Multi-line text | `"""…"""` |
| Yes, no, nothing | `true`, `false`, `none` |

One variable per line: there is no `a, b = 1, 2`. But `+=`, `-=`, `*=` and `/=` do exist.

### Text with values

**Any text** can hold values inside braces. No `f` in front needed.

```
show("{name} is {age} years old")              # Ash is 10 years old
show("Next year they'll be {age + 1}")         # Next year they'll be 11
show("Their first Pokémon is {team[0].name}")
```

Anything that gives a value can go inside the braces. To write a real brace: `\{`. Braces are only used **inside text**: code blocks use indentation.

---

## 4. Operators

| What | Operators |
|---|---|
| Arithmetic | `+  -  *  /  //  %  **` |
| Compare | `==  !=  <  >  <=  >=` (one at a time: `x > 0 and x < 10`) |
| Logic | `and  or  not` |
| Is it there? | `x in list`, `x not in list` (also dictionaries, text and fields: `"hp" in pika`) |
| Does it have something? | `pika has hp`, `pika has not hp`, `eevee has stone and friendship` |
| What is it? | `x is number`, `x is not empty` |
| Is it between? | `x in 1..10` (includes both ends, decimals too) |
| From… to | `1..10`, `0..10 by 2` |
| Fallback value | `something else value` |

### `in`: is it there?

```
"Pikachu" in team            # is it in the list?
"pokeball" in prices         # does the dictionary have that key?
"chu" in "Pikachu"           # does the text contain those letters?
"hp" in pika                 # does the record have that field?
age in 0..12                 # is it between 0 and 12, both included?
```

With a range without `by`, `in` asks "is it between the two?", decimals too: `5.5 in 0..10` is `true`. With `by` it asks whether it's one of the values in that list: `4 in 0..10 by 2` is `true`, `3 in 0..10 by 2` is `false`.

### `has`: is there something in that field?

`has` looks at the value of a field and answers `true` or `false`:

```
pika = (name: "Pikachu", hp: 35, asleep: false)

pika has hp            # true:  35 is greater than 0
pika has asleep        # false: it's false
pika has age           # false: there's no such field
pika has not asleep    # true
```

| If the field is… | `has` gives… |
|---|---|
| `true` / `false` | the same |
| a number | `true` if it's greater than 0 |
| a text, list or dictionary | `true` if it's not empty |
| `none`, or the field doesn't exist | `false` |

You can combine several fields with `and` and `or`: `eevee has stone and friendship`. With a **list** of records, it asks whether **any** of them has it: `team has hp` ("do I still have anyone who can fight?").

To compare, use the dot: `pika.level >= 36`. If the field name is misspelled, Cupcake tells you: "Did you mean 'hp'?".

### `is`: what kind of data is it

After `is` comes a **type**: `number`, `text`, `bool`, `list`, `dict`, `record`, `function`, `none` or `empty` (an empty list, dictionary or text).

```
if answer is number:
    …
if team is empty:
    show("You have no Pokémon")
```

To compare **values**, use `==`: `color == "red"`. (Inside a `when`, cases are written `is "red":`.)

### `else` as a fallback value

If the left side **fails**, you get the right side:

```
age = int(read("Age? ")) else 0
price = prices["mini"] else 0
```

---

## 5. Making decisions

Blocks use **indentation**: the line that opens a block ends with `:`, and the lines inside go below it, 4 more spaces in. The block ends when the indentation goes back. There are no semicolons: each statement ends at the line break.

```
if age >= 10:
    show("You can be a trainer")
else if age > 5:
    show("Almost")
else:
    show("Not yet")
```

`else:` lines up with its `if`. The body **always goes on the line below**, indented, even if it's a single statement. The condition doesn't need parentheses, though they're allowed. For a block that does nothing, write `none`. For the opposite of a condition: `if not raining:`.

Lines inside `( )` or `[ ]` can continue on the next line, whatever the indentation. If the indentation doesn't match, or the `:` is missing, Cupcake tells you on which line.

### `if` and `when` don't give a value

The value is stored inside each case. That way it's clear which variable changes and where:

```
if hp > 0:
    status = "alive"
else:
    status = "fainted"
```

`status = if …` gives an error that explains how to write it.

### `when`: choosing by a value

```
when color:
    is "red":
        show("Like Raspberry's cherry!")
    in ["orange", "yellow"]:
        show("Warm colors")
    else:
        show("A new color")
```

- `is value`: equal to that value (or to one of several: `is "a", "b"`);
- `is type`: of that type (`is number`, `is empty`…);
- `in group`: inside a list or a range (`in 0..9`);
- `else`: if none of them match.

What each case does goes below, indented further. The **first** case that matches wins. To store a value, store it inside each case:

```
when age:
    in 0..9:
        stage = "child"
    in 10..17:
        stage = "teenager"
    else:
        stage = "adult"
```

**Several things at once.** Join them with `and`, and each case has one value for each, also joined with `and`. The comma still means "or":

```
fx multiplier(attack, defender):
    when attack and defender:
        is "water" and "fire", "fire" and "grass", "grass" and "water":
            return 2
        is "fire" and "water", "grass" and "fire", "water" and "grass":
            return 0.5
        else:
            return 1
```

Types and groups work too: `is number and text`, `in 0..5 and 6..10`. `is not` negates the whole case.

---

## 6. Repeating

```
repeat 3:
    show("Hooray!")

while counter < 3:
    counter += 1

while cupcakes != mouths:
    cupcakes += 1

for p in team:
    show(p.name)

for i, p at team:            # i is the position: 0, 1, 2…
    show("{i}: {p.name}")

for i at team:               # just the positions
    show(i)

for i in 1..4:               # 1, 2, 3, 4
    show(i)
```

- `for x in group:` walks through **what's there**. `for i, x at list:` walks through **the positions**, and also gives you what's at each one (the position comes first).

- `break` leaves the loop; `continue` skips to the next round.
- `stop` ends the program.

### From… to: `..`

`a..b` goes from `a` to `b`, **including both**. With `by`, in steps:

```
1..4            # 1, 2, 3, 4
0..10 by 2      # 0, 2, 4, 6, 8, 10
5..1 by -1      # 5, 4, 3, 2, 1
```

---

## 7. Lists and dictionaries: square brackets

Square brackets are for **collections**: things that grow and are looked up with `[ ]`.

### Lists

```
team = ["Pikachu", "Charmander", "Squirtle", "Bulbasaur", "Eevee"]

team[0]           # "Pikachu"  (counting starts at 0)
team[-1]          # "Eevee"    (the last one)
team[1..3]        # ["Charmander", "Squirtle", "Bulbasaur"]
team[2..]         # from position 2 to the end
team[..1]         # from the start to position 1
```

### Dictionaries

**Put `key:` in front of each value and the list becomes a dictionary.**

```
prices = ["pokeball": 200, "potion": 300]
badges = [1: "Boulder", 2: "Cascade"]
empty = [:]

prices["pokeball"]             # 200
prices["greatball"] = 600      # a dictionary can grow
```

### List comprehensions

With `key:` in front, they make a dictionary.

```
names = [p.name for p in team if p.hp > 0]
doubles = [i * 2 for i in 1..5]                # [2, 4, 6, 8, 10]
hps = [p.name: p.hp for p in team]             # dictionary
```

---

## 8. Records: parentheses

Parentheses with fields are **records**: data with a fixed shape, read with a dot.

```
pika = (name: "Pikachu", type: "electric", hp: 35)

show(pika.name)            # Pikachu
pika.hp = 30               # you can change a field
```

**A record is born with its fields and doesn't get new ones**:

```
pika.hpp = 10
```
```
Error in file.cup, line 2:
    pika.hpp = 10
  the record has no field 'hpp'. Did you mean 'hp'? A record is born with its fields and doesn't get new ones.
```

To make many records with the same shape, a function works as the mold:

```
fx pokemon(name, type, hp = 35):
    return (name: name, type: type, hp: hp)

pika = pokemon("Pikachu", "electric")
charm = pokemon("Charmander", "fire", hp = 39)
```

Each symbol has just one job:

| | `:` and indentation | Square brackets `[ ]` | Parentheses `( )` |
|---|---|---|---|
| What they are | **code**: blocks of `if`, `for`, `fx`… | **collections**: lists and dictionaries | **named data**: records (and a function's inputs) |
| Example | `if x:` (and below it, indented) | `[1, 2]`, `["a": 1]` | `(name: "Pikachu")` |
| How you read them | — | `list[0]`, `dict["key"]` | `record.field` |
| Do they grow? | — | yes | no: they're born with their fields |

---

## 9. Functions: `fx`

```
fx greet(name, greeting = "Hello"):
    show("{greeting}, {name}")

greet("Ash")
greet("Misty", greeting = "Good afternoon")
```

`return` gives back a value, and **you always write it**. A function without `return` gives back `none`. If a line in the function only computes something and doesn't use it (`x * 2`), Cupcake tells you the `return` is missing:

```
fx double(x):
    return x * 2
```

To give back several values, return a record:

```
fx divide_with_remainder(a, b):
    return (quotient: a // b, remainder: a % b)

r = divide_with_remainder(17, 5)
show(r.quotient, r.remainder)      # 3 2
```

Order doesn't matter: you can use a function before you write it.

### Functions without a name: `fx(…): …`

`fx` without a name is an anonymous function. `λ` is the same as `fx`. If it's on the same line, it **gives the value of what it holds**, without `return`. It's the only exception to "the block goes below", because it usually sits inside parentheses.

```
alive = filter(team, fx(p): p.hp > 0)
by_name = sorted(team, λ(p): p.name)
plus = fx(a, b): a + b
```

If it takes **just one input**, you can leave out the name: it's called `it`:

```
alive = filter(team, fx: it.hp > 0)
```

### A function doesn't change anything outside it

There is no `global` or `nonlocal`. A function takes data and gives back data.

---

## 10. Data is copied

Assigning or passing data makes a **copy**. Each name has its own data.

```
a = [1, 2]
b = a
b = add(b, 3)
show(a)      # [1, 2]
show(b)      # [1, 2, 3]
```

That's why a function that changes something **returns it**, and the caller decides whether to keep it:

```
pika = heal(pika, 20)
```

---

## 11. No methods

The dot is only for a record's fields. Everything that does something is a function, with **the main data first**.

```
team.append("Eevee")
```
```
Error in file.cup, line 2:
    team.append("Eevee")
  Cupcake has no methods: '.append(…)' doesn't exist. Write:  team = add(team, "Eevee")
```

---

## 12. Showing, reading and files

```
name = read("What's your name? ")
show("Hello,", name)

age = read_num("How old are you? ")
```

- `show(…)` shows whatever you give it; if there are several things, it separates them with a space.
- `read("prompt")` shows the prompt, waits for the person to type something, and gives it back as **text**. The prompt doesn't have to be a question: `read("Press Enter to continue…")`.
- `read_num("prompt")` keeps asking **until it gets a number**, and gives it back as a number.
- `load("file.txt")` loads a file and gives back its text; `save("file.txt", text)` saves it.

---

## 13. Errors: `try`, `except`, `finally`, `raise`, `assert`

```
try:
    age = int(read("Age? "))
except error:
    show("That's not a number: {error}")
    age = 0
finally:
    show("Done")
```

- `error` is a text that explains what went wrong. You choose the name, and you can leave it out: `except: …`.
- `finally` always runs, whether there was an error or not. It's optional.
- For simple cases, the fallback value is enough: `int(read("Age? ")) else 0`.

To cause an error on purpose:

```
if age < 0:
    raise "Age can't be negative"
```

To check something that should always be true:

```
assert amount > 0
assert p.hp >= 0, "hp can't be negative"
```

If it isn't true, the program stops and tells you what failed and what each thing was worth:

```
Error in file.cup, line 2:
    assert amount > 0
  assert failed: amount > 0
  amount is 0
```

---

## 14. Other files: `use`

```
use heal, describe from pokemon        # brings just those two
use heal as cure from pokemon          # under another name
use pokemon                            # brings everything
```

`pokemon` is the file `pokemon.cup` in the same folder. You use the functions directly by name: `heal(pika)`, never `pokemon.heal(pika)`.

### `main`: what runs when you run the file

`main` is optional. If a file has `fx main():`, Cupcake runs it at the end, **only when you run that file**. If another file brings it in with `use`, its `main` doesn't run:

```
# tools.cup
fx double(x):
    return x * 2

fx main():
    show(double(4))       # a test: only runs with  cupcake tools.cup
```

`main` takes no inputs.

---

## 15. Built-in functions

All in English, with the main data first.

There are no methods: you always write `name(data, …)`, never `data.name(…)`.

| Group | Functions |
|---|---|
| Showing and reading | `show`, `read`, `read_num` |
| Numbers | `abs`, `round`, `min`, `max`, `sum` |
| Conversion | `int`, `float`, `str`, `bool` |
| Lists | `len`, `add`, `drop`, `sorted`, `reversed`, `filter`, `map`, `reduce`, `count`, `first`, `last` |
| Text | `len`, `upper`, `lower`, `strip`, `split`, `join`, `replace` |
| Dictionaries | `keys`, `values`, `drop` |
| Random | `roll(1, 6)`: a random whole number; `pick(list)`: a random element |
| Files | `load`, `save` |

- `sorted(list, key)` takes a function that says what to sort by: `sorted(team, fx: it.hp)`.
- `count(list, x)` counts how many times `x` appears; `count(list, fx: …)` counts how many match something.

---

## 16. Reserved words

```
true  false  none  and  or  not  in  has  is
if  else  when  while  repeat  for  at  by
break  continue  return  stop
fx  λ
try  except  finally  raise  assert
use  from  as
```

---

## 17. What Cupcake leaves out, on purpose

| Doesn't have | Because |
|---|---|
| `class`, inheritance, `self`, methods | there are only data and functions |
| `global`, `nonlocal` | a function doesn't change anything outside it |
| tuples | lists and records are enough |
| `a, b = 1, 2` | one variable per line |
| `pass` | `none` |
| the pipe `\|>` | step by step, with names, is preferred |
| `del` | to remove something: `drop(…)` |
| `with` | it relies on objects; files are read with `load(…)` |
| `yield`, `async`, `await`, `type` | advanced: maybe in a later version |

---

## 18. How it's built

- An interpreter: `cupcake file.cup`. Without a file, it opens a console.
- **The interpreter doesn't use classes either:** only functions and data, true to the language it implements.
- Error messages that say what happened and how to fix it. If you write a word from another language (`def`, `elif`, `print`…), it tells you the Cupcake one.
- A VS Code extension with syntax colors for `.cup`.
