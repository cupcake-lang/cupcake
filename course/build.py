"""
Builds the course in each language: en/course.html (the official one) and es/course.html.

    python3 build.py          # both
    python3 build.py es       # only one

Before writing the page it checks all the content with the real interpreter:
  - every example ends as expected (fine, or with the error it wants to show);
  - every solution passes all its checks;
  - every starter code does NOT pass them.
If anything fails, the page is not written.
"""
import html
import importlib.util
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path[:0] = [ROOT, HERE]

import bridge  # noqa: E402
from ui import UI  # noqa: E402

LANGUAGES = ("en", "es")

# The Pokémon Gallery: complete programs (file, title, description, inputs, uses randomness).
# English: the examples/ folder. Spanish: es/gallery/.
GALLERY = {"en": [
    ("pokedex", "The Pokédex", "Look up a Pokémon and show its card, with a tip based on its type.", "Pikachu\nmewtwo\nSquirtle", False),
    ("battle", "A turn-based battle", "Pikachu against Squirtle, with types, random damage and effectiveness.", "", True),
    ("catch", "Catch a Pokémon", "A wild Pokémon appears and you have three Poké Balls.", "", True),
    ("shop", "The Poké Mart", "Choose how many things you buy and see if you have enough money.", "3\n2", False),
    ("evolution", "Evolutions", "Each Pokémon evolves when it reaches a certain level.", "", False),
    ("training", "Training", "Earn experience in every battle and level up.", "", False),
    ("team", "The team", "Heal the ones that can still fight and warn who needs help (uses another file).", "", False),
], "es": [
    ("pokedex", "La Pokédex", "Busca un Pokémon y muestra su ficha, con un consejo según su tipo.", "Pikachu\nmewtwo\nSquirtle", False),
    ("combate", "Un combate por turnos", "Pikachu contra Squirtle, con tipos, daño al azar y efectividad.", "", True),
    ("captura", "Atrapar un Pokémon", "Un Pokémon salvaje aparece y tienes tres Poké Balls.", "", True),
    ("tienda_pokemon", "La Tienda Pokémon", "Elige cuántas cosas compras y mira si te alcanza el dinero.", "3\n2", False),
    ("evolucion", "Evoluciones", "Cada Pokémon evoluciona al llegar a cierto nivel.", "", False),
    ("entrenamiento", "Entrenamiento", "Gana experiencia en cada combate y sube de nivel.", "", False),
    ("equipo", "El equipo", "Cura a los que pueden pelear y avisa quién necesita ayuda (usa otro archivo).", "", False),
]}

PYODIDE_CDN = "https://cdn.jsdelivr.net/npm/pyodide@0.26.4/"


# ---------------------------------------------------------------- text → HTML

def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    return t


def blocks(text):
    """Paragraphs, lists with "- " and code blocks between ```."""
    parts = []
    pieces = re.split(r"```\n(.*?)\n```", text.strip(), flags=re.S)
    for k, piece in enumerate(pieces):
        if k % 2 == 1:
            parts.append(f'<pre class="code-static" data-cup>{html.escape(piece)}</pre>')
            continue
        for block in piece.strip().split("\n\n"):
            lines = [l.strip() for l in block.strip().splitlines() if l.strip()]
            if not lines:
                continue
            if all(l.startswith("- ") for l in lines):
                parts.append("<ul>" + "".join(f"<li>{inline(l[2:])}</li>" for l in lines) + "</ul>")
            elif lines[0].startswith("- ") is False and any(l.startswith("- ") for l in lines):
                lead = [l for l in lines if not l.startswith("- ")]
                items = [l for l in lines if l.startswith("- ")]
                parts.append(f"<p>{inline(' '.join(lead))}</p>")
                parts.append("<ul>" + "".join(f"<li>{inline(l[2:])}</li>" for l in items) + "</ul>")
            else:
                parts.append(f"<p>{inline(' '.join(lines))}</p>")
    return "\n".join(parts)


# ---------------------------------------------------------------- checking

def prepare_examples(items, who, problems):
    out = []
    for i, e in enumerate(items, start=1):
        r = bridge.run(e["code"], e.get("inputs", ""), e.get("files"))
        expected = e.get("expect", "ok")
        if r["status"] != expected:
            problems.append(f"[{who}] example {i}: ended in \"{r['status']}\", expected \"{expected}\"\n"
                            f"{r['output']}{r['error'] or ''}")
        out.append({"text": inline(e["text"]), "code": e["code"], "inputs": e.get("inputs", ""),
                    "files": e.get("files") or {}, "pre": r, "random": e.get("random", False)})
    return out


def load(lang, name):
    spec = importlib.util.spec_from_file_location(f"{name}_{lang}", os.path.join(HERE, lang, name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def prepare(lang):
    LESSONS = load(lang, "lessons").LESSONS
    POKEMON = load(lang, "pokemon_examples").POKEMON
    problems, lessons = [], []
    for n, l in enumerate(LESSONS, start=1):
        examples = prepare_examples(l["examples"], l["id"], problems)
        pokemon = prepare_examples(POKEMON.get(l["id"], []), l["id"] + " (Pokémon)", problems)
        exercises = []
        for i, x in enumerate(l["exercises"], start=1):
            inputs, files = x.get("inputs", ""), x.get("files")
            sol = bridge.check(x["solution"], inputs, x["checks"], files)
            if not sol["all_passed"]:
                failing = [c["text"] for c in sol["results"] if not c["ok"]]
                problems.append(f"[{l['id']}] exercise {i}: the solution does not pass {failing}\n"
                                f"{sol['output']}{sol['error'] or ''}")
            if bridge.check(x["starter"], inputs, x["checks"], files)["all_passed"]:
                problems.append(f"[{l['id']}] exercise {i}: the starter code already passes the checks")
            exercises.append({"task": inline(x["task"]), "starter": x["starter"], "solution": x["solution"],
                              "inputs": inputs, "files": files or {}, "checks": x["checks"],
                              "hints": [inline(h) for h in x.get("hints", [])]})
        lessons.append({"id": l["id"], "n": n, "title": l["title"], "pose": l["pose"], "place": l.get("place", ""),
                        "bubble": l["bubble"], "story": blocks(l["story"]),
                        "explanation": blocks(l["explanation"]), "examples": examples, "pokemon": pokemon,
                        "exercises": exercises, "remember": [inline(r) for r in l["remember"]]})
    gallery = []
    folder = os.path.join(ROOT, "examples") if lang == "en" else os.path.join(HERE, lang, "gallery")
    pokemon_module = open(os.path.join(folder, "pokemon.cup"), encoding="utf-8").read()
    for name, title, description, inputs, random in GALLERY[lang]:
        code = open(os.path.join(folder, name + ".cup"), encoding="utf-8").read()
        files = {"pokemon.cup": pokemon_module} if "from pokemon" in code else {}
        r = bridge.run(code, inputs, files)
        if r["status"] != "ok":
            problems.append(f"[gallery] {name}.cup: {r['error']}")
        gallery.append({"title": title, "description": description, "code": code, "inputs": inputs,
                        "files": files, "pre": r, "random": random, "text": inline(description)})
    return lessons, gallery, problems


def safe_json(x):
    return json.dumps(x, ensure_ascii=False).replace("</", "<\\/").replace("<!--", "<\\!--")


def main(argv):
    status = 0
    for lang in [a for a in argv[1:] if a in LANGUAGES] or LANGUAGES:
        status |= build(lang)
    return status


def build(lang):
    lessons, gallery, problems = prepare(lang)
    if problems:
        print(f"[{lang}] The page was not written. Problems in the content:\n")
        print("\n\n".join(problems))
        return 1
    sources = {
        "cupcake.py": open(os.path.join(ROOT, "cupcake.py"), encoding="utf-8").read(),
        "bridge.py": open(os.path.join(HERE, "bridge.py"), encoding="utf-8").read(),
    }
    template = open(os.path.join(HERE, "template.html"), encoding="utf-8").read()
    page = (template
            .replace("/*DATA*/null", safe_json({"lessons": lessons, "gallery": gallery, "pyodide": PYODIDE_CDN, "lang": lang}))
            .replace("/*UI*/null", safe_json(UI[lang]))
            .replace('<html lang="en">', f'<html lang="{lang}">')
            .replace("/*SOURCES*/null", safe_json(sources)))
    target = os.path.join(HERE, lang, "course.html")
    open(target, "w", encoding="utf-8").write(page)
    n_examples = sum(len(l["examples"]) + len(l["pokemon"]) for l in lessons)
    n_exercises = sum(len(l["exercises"]) for l in lessons)
    print(f"{target}  ({len(page) // 1024} KB)")
    print(f"  {len(lessons)} lessons, {n_examples} examples, {n_exercises} exercises, "
          f"{len(gallery)} programs in the gallery; all checked.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
