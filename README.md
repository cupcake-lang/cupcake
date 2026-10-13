<p align="center"><b>English</b> · <a href="README.es.md">Español</a></p>

<p align="center">
  <img src="logo/cupcake.svg" width="120" alt="Cupcake logo">
</p>

<h1 align="center">Cupcake</h1>

<p align="center">
  A small, friendly scripting language with <b>no classes, no objects and no methods</b>.<br>
  Just <b>data</b> and <b>functions</b>, with friendly errors that tell you how to fix them.<br>
  <i>Version 1.0 "Frambuesa"</i>
</p>

---

```
# Raspberry's Bakery
prices = ["small": 2, "medium": 3, "large": 5]

fx bill(mouths, size):
    total = mouths * (prices[size] else 0)
    if mouths >= 50:
        total -= total // 10          # 10% discount
    return total

fx main():
    name = read("What's your name? ")
    argos = (name: "Argos", mouths: 100, happy: true)

    if argos has mouths and happy:
        show("Hi, {name}! Argos pays {bill(argos.mouths, "small")} coins")

    for i, flavor at ["strawberry", "chocolate", "vanilla"]:
        show("{i}. {flavor}")
```

## Why Cupcake

- **It reads the way you think.** `:` and indentation. `if`, `else if`, `else`, `when`, `for`, `while`.
- **No classes or methods.** Data is lists `[1, 2]`, dictionaries `["a": 1]` and records `(name: "Mint", hp: 3)`. Everything else is a function: `add(list, x)`, never `list.append(x)`.
- **Data is copied.** `b = a` makes a copy: nothing changes behind your back.
- **One way to do each thing.** No shortcuts to memorize.
- **Friendly errors.** They tell you the line, what happened and how to fix it. If you write something from another language (`def`, `print`, `elif`, `list.append(x)`), Cupcake tells you how to write it.

## At a glance

| What | Cupcake |
|---|---|
| Show and read | `show("Hello")`, `name = read("Name: ")`, `age = read_num("Age: ")` |
| Text with values | `"Hello, {name}"` |
| Decide | `if … :` / `else if … :` / `else:` |
| Several cases | `when color:` and below it `is "red":`, `in 0..9:`, `is number:`, `else:` |
| Repeat | `for p in team:`, `for i, p at team:`, `while …:`, `repeat 3:` |
| Ranges | `1..10` (includes 10), `0..10 by 2`, `x in 0..10` |
| Functions | `fx double(x):` and below it `return x * 2` |
| Anonymous functions | `sorted(team, fx: it.hp)` |
| Is it there? | `"Pikachu" in team` |
| Does it have something? | `pika has hp`, `eevee has stone and friendship`, `team has hp` |
| What is it? | `x is number`, `list is empty` |
| Fallback value | `int(text) else 0` |
| Errors | `try:` / `except error:` / `finally:`, `raise "message"`, `assert x > 0` |
| Other files | `use heal from pokemon` |
| On run | `fx main():` runs only when you run that file |

The full reference is in [SPEC.md](SPEC.md).

## Try it

All you need is **Python 3.8 or newer**.

```
git clone https://github.com/cupcake-lang/cupcake.git
cd cupcake
python3 cupcake.py examples/hello.cup
```

Without a file, it opens a console where you type and see the result right away:

```
python3 cupcake.py
```

To use it as a command (`cupcake file.cup`) on Linux or macOS:

```
chmod +x cupcake.py
ln -s "$PWD/cupcake.py" ~/.local/bin/cupcake
```

[`examples/`](examples) has complete programs: a Pokédex, a turn-based battle, a shop and more.

## VS Code

The [`vscode-cupcake/`](vscode-cupcake) folder has an extension with colors, automatic indentation and snippets. To install it:

```
python3 vscode-cupcake/pack.py
code --install-extension vscode-cupcake/cupcake-1.0.0.vsix
```

## The course

[`course/`](course) has a course for learning to program from scratch with Cupcake, for adults and kids alike: a journey through the Kingdom of Cupcake, with 17 places, lots of Pokémon examples and a gallery of complete programs. Every example runs and every challenge checks itself, right in the browser. It comes in English and in Spanish.

**Take the course online:** [in English](https://cupcake-lang.github.io/cupcake/) · [en español](https://cupcake-lang.github.io/cupcake/es/)

To build it yourself:

```
python3 course/build.py
```

Then open `course/en/course.html` (English) or `course/es/course.html` (Spanish) in your browser.

## Tests

```
python3 tests.py
```

## How it's made

The interpreter is a single file, and it **doesn't use classes either**: only functions, dictionaries, lists and tuples, just like the language it implements.

## License

[MIT](LICENSE) © 2026 Jesús Denizard
