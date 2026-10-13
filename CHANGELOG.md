# Changelog

## 1.0 "Frambuesa" — 2026

The first public version of Cupcake.

- Blocks with `:` and indentation. The body always goes on the next line.
- Decide with `if`, `else if`, `else`; several cases with `when` (`is`, `in`, `else`), also with several things at once (`when attack and defender:`).
- Repeat with `for x in list:`, `for i, x at list:` (position first), `while` and `repeat`.
- `in` asks whether something is there, also in ranges with decimals (`x in 0..10`).
- `has` asks whether a field has something: `pika has hp`, `eevee has stone and friendship`, and with lists, whether anyone has it.
- Functions give values back with `return`; one-line anonymous functions (`fx: it.hp`) give their value.
- `fx main():` runs only when you run that file, not when another file loads it with `use`.
- `read` and `read_num` read what the person types; `load` and `save` work with files.
- Fallback value: `int(text) else 0`.
- Friendly errors that show the right form when you write something from another language or from older versions.
- A VS Code extension and a course for learning from scratch.
