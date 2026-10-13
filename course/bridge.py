"""
The bridge between the course page and the Cupcake interpreter.

  run(source, inputs, files)           → {"status", "output", "error", "line"}
  check(source, inputs, checks, files) → the same, plus "results" and "all_passed"

"files" are other .cup files the program can import (for the lesson about files).
It is used the same way on the computer (build.py) and in the browser (Pyodide).
"""
import contextlib
import io
import os
import re
import sys
import tempfile

import cupcake


def run(source, inputs="", files=None):
    folder = tempfile.mkdtemp(prefix="cup_")
    for name, content in (files or {}).items():
        with open(os.path.join(folder, name), "w", encoding="utf-8") as f:
            f.write(content)
    output = io.StringIO()
    original_stdin = sys.stdin
    sys.stdin = io.StringIO(inputs)
    try:
        with contextlib.redirect_stdout(output):
            result = cupcake.run_text(source, folder)
    finally:
        sys.stdin = original_stdin
    if result is None:
        return {"status": "ok", "output": output.getvalue(), "error": None, "line": None}
    return {"status": "error", "output": output.getvalue(), "error": result[0], "line": result[1]}


def check_one(r, source, c):
    kind = c["kind"]
    if kind == "runs":
        return r["status"] == "ok"
    if kind == "output":
        return c["contains"] in r["output"]
    if kind == "no_output":
        return c["contains"] not in r["output"]
    if kind == "uses":
        return re.search(c["pattern"], source) is not None
    if kind == "not_uses":
        return re.search(c["pattern"], source) is None
    if kind == "lines":
        return len([l for l in r["output"].split("\n") if l.strip()]) >= c["min"]
    if kind == "error":
        return r["status"] == "error" and c["contains"] in (r["error"] or "")
    raise ValueError(f"unknown check: {kind}")


def check(source, inputs, checks, files=None):
    r = run(source, inputs, files)
    results = []
    for c in checks:
        try:
            ok = check_one(r, source, c)
        except Exception:
            ok = False
        results.append({"ok": ok, "text": c["text"], "hint": "" if ok else c.get("hint", "")})
    r["results"] = results
    r["all_passed"] = all(x["ok"] for x in results)
    return r
