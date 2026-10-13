"""
Construye curso.html: «Aprende a programar con Cupcake».

    python3 construir.py

Antes de escribir la página comprueba todo el contenido con el intérprete de verdad:
  - cada ejemplo termina como se espera (bien, o con el error que se quiere mostrar);
  - cada solución pasa todas sus comprobaciones;
  - cada código inicial NO las pasa.
Si algo falla, no se escribe la página.
"""
import html
import json
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path[:0] = [RAIZ, AQUI]

import puente  # noqa: E402
from ejemplos_pokemon import POKEMON  # noqa: E402
from lecciones import LECCIONES  # noqa: E402

# La Galería Pokémon: programas completos de la carpeta ejemplos/
GALERIA = [
    ("pokedex", "La Pokédex", "Busca un Pokémon y muestra su ficha, con un consejo según su tipo.", "Pikachu\nmewtwo\nSquirtle", False),
    ("combate", "Un combate por turnos", "Pikachu contra Squirtle, con tipos, daño al azar y efectividad.", "", True),
    ("captura", "Atrapar un Pokémon", "Un Pokémon salvaje aparece y tienes tres Poké Balls.", "", True),
    ("tienda_pokemon", "La Tienda Pokémon", "Elige cuántas cosas compras y mira si te alcanza el dinero.", "3\n2", False),
    ("evolucion", "Evoluciones", "Cada Pokémon evoluciona al llegar a cierto nivel.", "", False),
    ("entrenamiento", "Entrenamiento", "Gana experiencia en cada combate y sube de nivel.", "", False),
    ("equipo", "El equipo", "Cura a los que pueden pelear y avisa quién necesita ayuda (usa otro archivo).", "", False),
]

PYODIDE_CDN = "https://cdn.jsdelivr.net/npm/pyodide@0.26.4/"


# ---------------------------------------------------------------- texto → HTML

def en_linea(t):
    t = html.escape(t, quote=False)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    return t


def bloques(texto):
    """Párrafos, listas con «- » y bloques de código entre ```."""
    partes = []
    trozos = re.split(r"```\n(.*?)\n```", texto.strip(), flags=re.S)
    for k, trozo in enumerate(trozos):
        if k % 2 == 1:
            partes.append(f'<pre class="codigo-fijo" data-cup>{html.escape(trozo)}</pre>')
            continue
        for bloque in trozo.strip().split("\n\n"):
            lineas = [l.strip() for l in bloque.strip().splitlines() if l.strip()]
            if not lineas:
                continue
            if all(l.startswith("- ") for l in lineas):
                partes.append("<ul>" + "".join(f"<li>{en_linea(l[2:])}</li>" for l in lineas) + "</ul>")
            elif lineas[0].startswith("- ") is False and any(l.startswith("- ") for l in lineas):
                inicio = [l for l in lineas if not l.startswith("- ")]
                items = [l for l in lineas if l.startswith("- ")]
                partes.append(f"<p>{en_linea(' '.join(inicio))}</p>")
                partes.append("<ul>" + "".join(f"<li>{en_linea(l[2:])}</li>" for l in items) + "</ul>")
            else:
                partes.append(f"<p>{en_linea(' '.join(lineas))}</p>")
    return "\n".join(partes)


# ---------------------------------------------------------------- comprobar

def preparar_ejemplos(lista, quien, problemas):
    salida = []
    for i, e in enumerate(lista, start=1):
        r = puente.ejecutar(e["codigo"], e.get("entradas", ""), e.get("archivos"))
        esperado = e.get("espera", "ok")
        if r["estado"] != esperado:
            problemas.append(f"[{quien}] ejemplo {i}: terminó en «{r['estado']}», se esperaba «{esperado}»\n"
                             f"{r['salida']}{r['error'] or ''}")
        salida.append({"texto": en_linea(e["texto"]), "codigo": e["codigo"], "entradas": e.get("entradas", ""),
                       "archivos": e.get("archivos") or {}, "pre": r, "azar": e.get("azar", False)})
    return salida


def preparar():
    problemas, lecciones = [], []
    for n, l in enumerate(LECCIONES, start=1):
        pokemon = preparar_ejemplos(POKEMON.get(l["id"], []), l["id"] + " (Pokémon)", problemas)
        ejemplos = []
        for i, e in enumerate(l["ejemplos"], start=1):
            r = puente.ejecutar(e["codigo"], e.get("entradas", ""), e.get("archivos"))
            esperado = e.get("espera", "ok")
            if r["estado"] != esperado:
                problemas.append(f"[{l['id']}] ejemplo {i}: terminó en «{r['estado']}», se esperaba «{esperado}»\n"
                                 f"{r['salida']}{r['error'] or ''}")
            ejemplos.append({"texto": en_linea(e["texto"]), "codigo": e["codigo"], "entradas": e.get("entradas", ""),
                             "archivos": e.get("archivos") or {}, "pre": r, "azar": e.get("azar", False)})
        ejercicios = []
        for i, x in enumerate(l["ejercicios"], start=1):
            entradas, archivos = x.get("entradas", ""), x.get("archivos")
            sol = puente.comprobar(x["solucion"], entradas, x["checks"], archivos)
            if not sol["todo_bien"]:
                fallan = [c["texto"] for c in sol["resultados"] if not c["ok"]]
                problemas.append(f"[{l['id']}] ejercicio {i}: la solución no pasa {fallan}\n{sol['salida']}{sol['error'] or ''}")
            if puente.comprobar(x["inicial"], entradas, x["checks"], archivos)["todo_bien"]:
                problemas.append(f"[{l['id']}] ejercicio {i}: el código inicial ya pasa las comprobaciones")
            ejercicios.append({"enunciado": en_linea(x["enunciado"]), "inicial": x["inicial"], "solucion": x["solucion"],
                               "entradas": entradas, "archivos": archivos or {}, "checks": x["checks"],
                               "pistas": [en_linea(p) for p in x.get("pistas", [])]})
        lecciones.append({"id": l["id"], "n": n, "titulo": l["titulo"], "cupi": l["cupi"],
                          "bocadillo": l["bocadillo"], "historia": bloques(l["historia"]),
                          "explicacion": bloques(l["explicacion"]), "ejemplos": ejemplos, "pokemon": pokemon,
                          "ejercicios": ejercicios, "recuerda": [en_linea(r) for r in l["recuerda"]]})
    galeria = []
    modulo_pokemon = open(os.path.join(RAIZ, "ejemplos", "pokemon.cup"), encoding="utf-8").read()
    for archivo, titulo, descripcion, entradas, azar in GALERIA:
        codigo = open(os.path.join(RAIZ, "ejemplos", archivo + ".cup"), encoding="utf-8").read()
        archivos = {"pokemon.cup": modulo_pokemon} if "from pokemon" in codigo else {}
        r = puente.ejecutar(codigo, entradas, archivos)
        if r["estado"] != "ok":
            problemas.append(f"[galería] {archivo}.cup: {r['error']}")
        galeria.append({"titulo": titulo, "descripcion": descripcion, "codigo": codigo, "entradas": entradas,
                        "archivos": archivos, "pre": r, "azar": azar, "texto": en_linea(descripcion)})
    return lecciones, galeria, problemas


def json_seguro(x):
    return json.dumps(x, ensure_ascii=False).replace("</", "<\\/").replace("<!--", "<\\!--")


def main():
    lecciones, galeria, problemas = preparar()
    if problemas:
        print("No se escribió la página. Problemas en el contenido:\n")
        print("\n\n".join(problemas))
        return 1
    fuentes = {
        "cupcake.py": open(os.path.join(RAIZ, "cupcake.py"), encoding="utf-8").read(),
        "puente.py": open(os.path.join(AQUI, "puente.py"), encoding="utf-8").read(),
    }
    plantilla = open(os.path.join(AQUI, "plantilla.html"), encoding="utf-8").read()
    pagina = (plantilla
              .replace("/*DATOS*/null", json_seguro({"lecciones": lecciones, "galeria": galeria, "pyodide": PYODIDE_CDN}))
              .replace("/*FUENTES*/null", json_seguro(fuentes)))
    salida = os.path.join(AQUI, "curso.html")
    open(salida, "w", encoding="utf-8").write(pagina)
    n_ej = sum(len(l["ejemplos"]) + len(l["pokemon"]) for l in lecciones)
    n_pr = sum(len(l["ejercicios"]) for l in lecciones)
    print(f"{salida}  ({len(pagina) // 1024} KB)")
    print(f"  {len(lecciones)} lecciones, {n_ej} ejemplos, {n_pr} ejercicios, {len(galeria)} programas en la galería; todo comprobado.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
