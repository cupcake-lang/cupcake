"""
El puente entre la página del curso y el intérprete de Cupcake.

  ejecutar(fuente, entradas, archivos)          → {"estado", "salida", "error", "linea"}
  comprobar(fuente, entradas, checks, archivos) → lo mismo, más "resultados" y "todo_bien"

«archivos» son otros archivos .cup que el programa puede usar con «use» (para la lección de use).
Se usa igual en la computadora (construir.py) y en el navegador (Pyodide).
"""
import contextlib
import io
import os
import re
import sys
import tempfile

import cupcake


def ejecutar(fuente, entradas="", archivos=None):
    carpeta = tempfile.mkdtemp(prefix="cup_")
    for nombre, contenido in (archivos or {}).items():
        with open(os.path.join(carpeta, nombre), "w", encoding="utf-8") as f:
            f.write(contenido)
    salida = io.StringIO()
    stdin_original = sys.stdin
    sys.stdin = io.StringIO(entradas)
    try:
        with contextlib.redirect_stdout(salida):
            resultado = cupcake.ejecutar_texto(fuente, carpeta)
    finally:
        sys.stdin = stdin_original
    if resultado is None:
        return {"estado": "ok", "salida": salida.getvalue(), "error": None, "linea": None}
    return {"estado": "error", "salida": salida.getvalue(), "error": resultado[0], "linea": resultado[1]}


def un_check(r, fuente, c):
    tipo = c["tipo"]
    if tipo == "ejecuta":
        return r["estado"] == "ok"
    if tipo == "salida":
        return c["contiene"] in r["salida"]
    if tipo == "no_salida":
        return c["contiene"] not in r["salida"]
    if tipo == "usa":
        return re.search(c["patron"], fuente) is not None
    if tipo == "no_usa":
        return re.search(c["patron"], fuente) is None
    if tipo == "lineas":
        return len([l for l in r["salida"].split("\n") if l.strip()]) >= c["minimo"]
    if tipo == "error":
        return r["estado"] == "error" and c["contiene"] in (r["error"] or "")
    raise ValueError(f"comprobación desconocida: {tipo}")


def comprobar(fuente, entradas, checks, archivos=None):
    r = ejecutar(fuente, entradas, archivos)
    resultados = []
    for c in checks:
        try:
            ok = un_check(r, fuente, c)
        except Exception:
            ok = False
        resultados.append({"ok": ok, "texto": c["texto"], "pista": "" if ok else c.get("pista", "")})
    r["resultados"] = resultados
    r["todo_bien"] = all(x["ok"] for x in resultados)
    return r
