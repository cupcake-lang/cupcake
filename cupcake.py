#!/usr/bin/env python3
"""
Cupcake: a small scripting language with no classes, no objects and no methods.

    cupcake file.cup

This interpreter doesn't use classes either: only functions, dictionaries, lists and tuples,
just like the language it implements.

Parts:
  1. Lexer:      the text becomes a list of pieces (tokens).
  2. Parser:     the pieces become a tree of nodes (dictionaries).
  3. Execution:  the tree is walked.
  4. Builtins:   show, read, add, drop, sorted…
  5. Program:    the command line.
"""
import difflib
import os
import random
import sys

sys.setrecursionlimit(10000)


# ================================================================ errors

def error(message, line=None):
    """Every Cupcake error is an Exception with ("cupcake", message, line)."""
    return Exception("cupcake", message, line)


def is_cupcake_error(ex):
    return len(ex.args) == 3 and ex.args[0] == "cupcake"


def did_you_mean(name, options):
    p = difflib.get_close_matches(name, list(options), 1, 0.6)
    return f" Did you mean '{p[0]}'?" if p else ""


# ================================================================ 1. lexer

KEYWORDS = {
    "true", "false", "none", "and", "or", "not", "in", "has", "is",
    "if", "when", "else", "while", "repeat", "for", "at", "by",
    "break", "continue", "return", "stop",
    "fx", "try", "except", "finally", "raise", "assert",
    "use", "from", "as",
}

# After 'is', these words are types: x is number, list is empty…
TYPES = {"number", "text", "list", "dict", "record", "function", "bool", "empty"}

DOUBLE_OPS = {"..", "=>", "==", "!=", "<=", ">=", "**", "//", "+=", "-=", "*=", "/="}
SINGLE_OPS = set("+-*/%<>=()[]{},:.")

# Words Cupcake used to have and no longer uses: the error shows the new form.
OLD_WORDS = {
    "other": "else  (and 'other if' is 'else if'; 'x other 0' is 'x else 0')",
    "unless": "if not",
    "until": "while not",
    "each": "for x in list",
    "between": "x in 1..10",
    "then": ":  (a colon at the end of the line)",
}

OTHER_WORDS = {
    "def": "fx", "elif": "else if", "lambda": "fx(…): …", "True": "true", "False": "false",
    "None": "none", "print": "show", "input": "read", "ask": "read", "ask_number": "read_num", "read_number": "read_num", "write": "save", "class": None, "pass": "none (a line with none does nothing)", "import": "use",
    "nonlocal": None, "global": None, "del": "drop(…)", "with": None, "yield": None,
    "fn": "fx", "lam": "fx(…): …", "range": "a..b", "elsif": "else if", "switch": "when", "match": "when",
}


def tokenize(source, first_line=1):
    """Returns a list of (kind, value, line). Kinds: num, str, name, kw, op, nl, indent, dedent, eof.
    Indentation marks the blocks: 'indent' opens one and 'dedent' closes it."""
    toks = []
    i, n, line, depth = 0, len(source), first_line, 0
    levels = [0]

    def indentation(i, line):
        """At the start of a line: compares its indentation with the lines above."""
        j, width = i, 0
        while j < n and source[j] in " \t":
            width += 4 if source[j] == "\t" else 1
            j += 1
        if j >= n or source[j] in "\n\r#":           # empty line, or just a comment: doesn't count
            return
        if width > levels[-1]:
            levels.append(width)
            toks.append(("indent", width, line))
        while width < levels[-1]:
            levels.pop()
            toks.append(("dedent", width, line))
        if width != levels[-1]:
            raise error("this line's indentation doesn't match any line above", line)

    indentation(0, line)
    while i < n:
        c = source[i]
        if c == "\n":
            line += 1
            i += 1
            if depth == 0:
                toks.append(("nl", "\n", line - 1))
                indentation(i, line)
            continue
        if c in " \t\r":
            i += 1
            continue
        if c == "#":
            while i < n and source[i] != "\n":
                i += 1
            continue
        if c.isdigit():
            j = i
            while j < n and source[j].isdigit():
                j += 1
            is_decimal = j + 1 < n and source[j] == "." and source[j + 1].isdigit()
            if is_decimal:
                j += 1
                while j < n and source[j].isdigit():
                    j += 1
                toks.append(("num", float(source[i:j]), line))
            else:
                toks.append(("num", int(source[i:j]), line))
            i = j
            continue
        if c == "λ":
            toks.append(("kw", "fx", line))
            i += 1
            continue
        if c.isalpha() or c == "_":
            j = i
            while j < n and (source[j].isalnum() or source[j] == "_"):
                j += 1
            word = source[i:j]
            toks.append(("kw" if word in KEYWORDS else "name", word, line))
            i = j
            continue
        if c in "\"'":
            i, line, parts = read_text(source, i, line)
            toks.append(("str", parts, line))
            continue
        if source[i:i + 2] in DOUBLE_OPS:
            toks.append(("op", source[i:i + 2], line))
            i += 2
            continue
        if c in SINGLE_OPS:
            if c in "([":
                depth += 1
            elif c in ")]":
                depth = max(0, depth - 1)
            toks.append(("op", c, line))
            i += 1
            continue
        raise error(f"I don't understand the symbol '{c}'", line)
    toks.append(("nl", "\n", line))
    for _ in levels[1:]:
        toks.append(("dedent", 0, line))
    toks.append(("eof", None, line))
    return toks


ESCAPES = {"n": "\n", "t": "\t", "\\": "\\", '"': '"', "'": "'", "{": "{", "}": "}"}


def read_text(source, i, line):
    """Reads a quoted text. Returns (position, line, parts); each part is a text
    or ("expr", code, line) for what goes between braces."""
    quote = source[i]
    triple = source[i:i + 3] == quote * 3
    closing = quote * 3 if triple else quote
    i += len(closing)
    start_line = line
    parts, current = [], []
    n = len(source)
    while True:
        if i >= n:
            raise error("this text is missing its closing quote", start_line)
        if source.startswith(closing, i):
            i += len(closing)
            break
        c = source[i]
        if c == "\n":
            if not triple:
                raise error("this text is missing its closing quote (for several lines use \"\"\"…\"\"\")",
                            start_line)
            line += 1
        if c == "\\" and i + 1 < n:
            current.append(ESCAPES.get(source[i + 1], "\\" + source[i + 1]))
            i += 2
            continue
        if c == "{":
            j, level = i + 1, 1
            while j < n and level:
                if source[j] in "\"'":                  # a text inside the braces
                    q = source[j]
                    j += 1
                    while j < n and source[j] != q:
                        j += 2 if source[j] == "\\" else 1
                elif source[j] == "{":
                    level += 1
                elif source[j] == "}":
                    level -= 1
                j += 1
            if level:
                raise error("a brace '}' is missing inside the text", line)
            if current:
                parts.append("".join(current))
                current = []
            parts.append(("expr", source[i + 1:j - 1], line))
            i = j
            continue
        current.append(c)
        i += 1
    if current or not parts:
        parts.append("".join(current))
    return i, line, parts


# ================================================================ 2. parser
# The parser state is a dictionary: {"t": tokens, "i": position}.
# Each tree node is a dictionary with "t" (what it is) and "l" (the line).

def node(t, l, **fields):
    fields["t"] = t
    fields["l"] = l
    return fields


def peek(P, k=0):
    return P["t"][min(P["i"] + k, len(P["t"]) - 1)]


def take(P):
    tok = peek(P)
    P["i"] += 1
    return tok


def is_op(P, value, k=0):
    tok = peek(P, k)
    return tok[0] in ("op", "kw") and tok[1] == value


def accept(P, value):
    if is_op(P, value):
        return take(P)
    return None


def expect(P, value, explanation=None):
    tok = peek(P)
    if is_op(P, value):
        return take(P)
    got = "the end of the line" if tok[0] == "nl" else "the end of the file" if tok[0] == "eof" \
        else f"'{tok[1]}'" if tok[0] != "str" else "a text"
    raise error(explanation or f"expected '{value}' but got {got}", tok[2])


def skip_newlines(P):
    while peek(P)[0] == "nl":
        take(P)


def name(P, what="a name"):
    tok = take(P)
    if tok[0] != "name":
        raise error(f"expected {what} but got '{tok[1]}'", tok[2])
    return tok[1]


def parse_program(source):
    P = {"t": tokenize(source), "i": 0}
    statements = []
    skip_newlines(P)
    while peek(P)[0] != "eof":
        statements.append(statement(P))
        end_of_statement(P)
        skip_newlines(P)
    return statements


BRACES = "Cupcake doesn't use braces for blocks: put ':' at the end of the line and, below it, the indented instructions (4 spaces)"


def end_of_statement(P):
    tok = peek(P)
    if tok[0] in ("nl", "eof", "dedent") or P["t"][P["i"] - 1][0] == "dedent":
        return
    if is_op(P, "{") or is_op(P, "}"):
        raise error(BRACES, tok[2])
    if tok[0] == "name" and tok[1] in OLD_WORDS:
        raise error(f"Cupcake no longer uses '{tok[1]}'. Write:  {OLD_WORDS[tok[1]]}", tok[2])
    raise error(f"there's an extra '{tok[1] if tok[0] != 'str' else 'text'}' at the end of this instruction", tok[2])


def block(P):
    """ ':' and a block, below, indented."""
    tok = peek(P)
    if is_op(P, "{"):
        raise error(BRACES, tok[2])
    if tok[0] == "indent" or (tok[0] == "nl" and peek(P, 1)[0] == "indent"):
        raise error("missing ':' at the end of the line above, before the indented block", tok[2])
    if peek(P)[0] == "name" and peek(P)[1] == "then":
        raise error(f"Cupcake no longer uses 'then'. Write:  {OLD_WORDS['then']}", peek(P)[2])
    expect(P, ":", "missing ':' at the end of the line, before the block")
    if peek(P)[0] in ("nl", "eof"):
        L = peek(P)[2]
        skip_newlines(P)
        if peek(P)[0] != "indent":
            raise error("after ':' come the block's instructions, below and indented (4 spaces)", L)
        take(P)
        statements = []
        while peek(P)[0] not in ("dedent", "eof"):
            statements.append(statement(P))
            end_of_statement(P)
            skip_newlines(P)
        accept_dedent(P)
        return statements
    if is_op(P, "}"):
        raise error(BRACES, peek(P)[2])
    raise error("what the block does goes on the next line, indented (4 spaces), not on the same line", peek(P)[2])


def accept_dedent(P):
    if peek(P)[0] == "dedent":
        take(P)


def block_or_header(P):
    return block(P)


def statement(P):
    tok = peek(P)
    L = tok[2]
    if tok[0] == "kw" and tok[1] == "else":
        raise error("this 'else' has no 'if' before it (or it is indented differently from its if)", L)
    if tok[0] == "name" and tok[1] in OLD_WORDS and not (is_op(P, "=", 1) or is_op(P, "(", 1) or is_op(P, ".", 1) or is_op(P, "[", 1)
                                                      or is_op(P, "+=", 1) or is_op(P, "-=", 1)):
        raise error(f"Cupcake no longer uses '{tok[1]}'. Write:  {OLD_WORDS[tok[1]]}", L)
    if tok[0] == "indent":
        raise error("this line is indented too much (is ':' missing on the line above?)", L)
    if is_op(P, "{") or is_op(P, "}"):
        raise error(BRACES, L)
    if tok[0] == "name" and tok[1] in OTHER_WORDS and (
            peek(P, 1)[0] in ("name", "nl") or is_op(P, ":", 1) or tok[1] in ("def", "class", "else", "elif", "fn")):
        replacement = OTHER_WORDS[tok[1]]
        hint = f" Write '{replacement}'." if replacement else " Cupcake doesn't have it."
        raise error(f"'{tok[1]}' is not a Cupcake word.{hint}", L)
    if tok[0] == "kw":
        v = tok[1]
        if v == "fx" and peek(P, 1)[0] == "name":
            take(P)
            n = name(P, "the function's name")
            dont_shadow(n, L)
            parameters = parameter_list(P)
            body = block_or_header(P)
            check_return(body)
            return node("def", L, name=n, params=parameters, body=body)
        if v == "if":
            return if_statement(P)
        if v == "when":
            return when_statement(P)
        if v == "while":
            take(P)
            return node("while", L, cond=expression(P), body=block_or_header(P))
        if v == "repeat":
            take(P)
            return node("repeat", L, times=expression(P), body=block_or_header(P))
        if v == "for":
            take(P)
            var, position, iterable = for_header(P, full_expression=True)
            return node("for", L, var=var, iterable=iterable, position=position, body=block_or_header(P))
        if v == "return":
            take(P)
            value = None if peek(P)[0] in ("nl", "eof", "dedent") else expression(P)
            return node("return", L, value=value)
        if v in ("break", "continue", "stop"):
            take(P)
            return node(v, L)
        if v == "raise":
            take(P)
            return node("raise", L, value=expression(P))
        if v == "assert":
            take(P)
            begin = P["i"]
            cond = expression(P)
            text = text_of(P, begin)
            message = expression(P) if accept(P, ",") else None
            return node("assert", L, cond=cond, text=text, message=message)
        if v == "try":
            return try_statement(P)
        if v == "use":
            return use_statement(P)
    e = expression(P)
    if is_op(P, "=") or is_op(P, "+=") or is_op(P, "-=") or is_op(P, "*=") or is_op(P, "/="):
        op = take(P)[1]
        if e["t"] not in ("name", "index", "field"):
            raise error("you can only assign to a variable, an element ([…]) or a field (.field)", L)
        if e["t"] == "name":
            dont_shadow(e["name"], L)
        value = expression(P)
        if op != "=":
            value = node("bin", L, op=op[0], a=e, b=value)
        return node("assign", L, target=e, value=value)
    return node("expr", L, expr=e)


def text_of(P, begin):
    """Rebuilds the code of an expression, for assert messages."""
    parts = []
    for tok in P["t"][begin:P["i"]]:
        if tok[0] == "str":
            parts.append('"' + "".join(x if isinstance(x, str) else "{" + x[1] + "}" for x in tok[1]) + '"')
        else:
            parts.append(str(tok[1]))
    text = " ".join(parts)
    for a, b in ((" . ", "."), (" ( ", "("), (" )", ")"), ("( ", "("), (" [ ", "["), (" ]", "]"), (" ,", ",")):
        text = text.replace(a, b)
    return text


def if_statement(P, as_value=False):
    L = take(P)[2]
    branches = [(expression(P), block_or_header(P))]
    otherwise = None
    while True:
        saved = P["i"]
        skip_newlines(P)
        tok = peek(P)
        if tok[1] == "elif":
            raise error("in Cupcake, 'elif' is written 'else if'", tok[2])
        if tok[0] == "name" and tok[1] == "other":
            raise error(f"Cupcake no longer uses 'other'. Write:  {OLD_WORDS['other']}", tok[2])
        if not accept(P, "else"):
            P["i"] = saved
            break
        if accept(P, "if"):
            branches.append((expression(P), block_or_header(P)))
            continue
        otherwise = block_or_header(P)
        break
    return node("ifvalue" if as_value else "if", L, branches=branches, otherwise=otherwise)


def case_body(P):
    """What a when case does: ':' and, below, an indented block."""
    return block(P)


def else_body(P):
    return block(P)


def other_in_when(tok):
    return error("in a when, the last case is written 'else:'", tok[2])


def open_cases(P, L):
    """After 'when x': ':' and the cases below, indented. Returns True."""
    if is_op(P, "{"):
        raise error(BRACES, peek(P)[2])
    expect(P, ":", "missing ':' at the end of the when:  when x:")
    if peek(P)[0] not in ("nl", "eof"):
        raise error("the cases of a when go on the lines below, indented:  is 1:", peek(P)[2])
    skip_newlines(P)
    if peek(P)[0] != "indent":
        raise error("the cases of a when go below, indented:  is 1:", L)
    take(P)
    return True


def end_of_cases(P, below):
    if below:
        return peek(P)[0] in ("dedent", "eof")
    return peek(P)[0] in ("nl", "eof", "dedent") or is_op(P, ")") or is_op(P, "]") or is_op(P, ",")


def pair_pattern(P, kind):
    """A pattern of a when case with several things: a type or a value (with is), or a group (with in)."""
    if kind == "is" and ((peek(P)[0] == "name" and peek(P)[1] in TYPES) or is_op(P, "none")):
        return ("type_", take(P)[1])
    return ("value" if kind == "is" else "in", not_(P))


def pair_cases(P, kind, how_many, names, L):
    """'"water" and "fire", "fire" and "grass"': alternatives separated by commas, each with one pattern per thing."""
    alternatives = []
    while True:
        alt = [pair_pattern(P, kind)]
        while accept(P, "and"):
            alt.append(pair_pattern(P, kind))
        if len(alt) != how_many:
            raise error(f"this when compares {how_many} things ({names}): each case needs {how_many} values joined with 'and', "
                        f"like  {kind} {' and '.join(['…'] * how_many)}: …", L)
        alternatives.append(alt)
        if not accept(P, ","):
            return alternatives


def when_statement(P, as_value=False):
    L = take(P)[2]
    # 'when attack and defender:  is "water" and "fire": …' compares several things at once
    begin = P["i"]
    subjects = [not_(P)]
    while accept(P, "and"):
        subjects.append(not_(P))
    if len(subjects) > 1 and (is_op(P, ":") or is_op(P, "{")):
        return multi_when(P, L, subjects, begin, as_value)
    P["i"] = begin
    value = expression(P)
    below = open_cases(P, L)
    cases, otherwise = [], None
    while not end_of_cases(P, below):
        tok = peek(P)
        if tok[0] == "name" and tok[1] == "other":
            raise other_in_when(tok)
        if accept(P, "else"):
            otherwise = else_body(P)
        elif accept(P, "is"):
            negated = bool(accept(P, "not"))
            if (peek(P)[0] == "name" and peek(P)[1] in TYPES) or is_op(P, "none"):
                pattern = ("type_", take(P)[1])
            else:
                values_ = [or_(P)]
                while accept(P, ","):
                    values_.append(or_(P))
                pattern = ("values", values_)
            cases.append((pattern, negated, case_body(P), tok[2]))
        elif accept(P, "in"):
            cases.append((("in", or_(P)), False, case_body(P), tok[2]))
        else:
            raise error("each case of a when starts with 'is', 'in' or 'else':  is \"red\":", tok[2])
        if below:
            skip_newlines(P)
    if below:
        accept_dedent(P)
    return node("whenvalue" if as_value else "when", L, value=value, cases=cases, otherwise=otherwise)


def multi_when(P, L, subjects, begin, as_value):
    names = " and ".join(name_of(s) or "…" for s in subjects)
    below = open_cases(P, L)
    cases, otherwise = [], None
    while not end_of_cases(P, below):
        tok = peek(P)
        if tok[0] == "name" and tok[1] == "other":
            raise other_in_when(tok)
        if accept(P, "else"):
            otherwise = else_body(P)
        elif tok[0] == "kw" and tok[1] in ("is", "in"):
            kind = take(P)[1]
            negated = kind == "is" and bool(accept(P, "not"))
            alternatives = pair_cases(P, kind, len(subjects), names, tok[2])
            cases.append((("pairs", alternatives), negated, case_body(P), tok[2]))
        else:
            raise error(f"each case of a when starts with 'is', 'in' or 'else':  is {' and '.join(['…'] * len(subjects))}: …", tok[2])
        if below:
            skip_newlines(P)
    if below:
        accept_dedent(P)
    return node("whenvalue" if as_value else "when", L, value=None, subjects=subjects, cases=cases, otherwise=otherwise)


def try_statement(P):
    L = take(P)[2]
    body = block_or_header(P)
    var = handler = finally_ = None
    saved = P["i"]
    skip_newlines(P)
    if accept(P, "except"):
        if peek(P)[0] == "name":
            var = take(P)[1]
        handler = block_or_header(P)
        saved = P["i"]
        skip_newlines(P)
    if accept(P, "finally"):
        finally_ = block_or_header(P)
    else:
        P["i"] = saved
    if handler is None and finally_ is None:
        raise error("after try comes 'except' or 'finally'", L)
    return node("try", L, body=body, var=var, handler=handler, finally_=finally_)


def use_statement(P):
    L = take(P)[2]
    names = []
    while True:
        n = name(P, "the name of what you want to use")
        alias = name(P, "the new name") if accept(P, "as") else n
        names.append((n, alias))
        if not accept(P, ","):
            break
    if accept(P, "from"):
        module = name(P, "the file name")
        return node("use", L, module=module, names=names)
    if len(names) > 1 or names[0][0] != names[0][1]:
        raise error("missing 'from':  use heal, describe from pokemon", L)
    return node("use", L, module=names[0][0], names=None)


def parameter_list(P):
    expect(P, "(")
    params = []
    while not is_op(P, ")"):
        n = name(P, "a parameter name")
        dont_shadow(n, peek(P)[2])
        default = expression(P) if accept(P, "=") else None
        params.append((n, default))
        if not accept(P, ","):
            break
    expect(P, ")")
    return params


# -- expressions, from lowest to highest priority

def expression(P):
    e = or_(P)
    # 'else' as a fallback: if the left side fails, the right side is used.
    while is_op(P, "else") and not is_op(P, ":", 1) and not is_op(P, "if", 1):
        L = take(P)[2]
        e = node("fallback", L, a=e, b=or_(P))
    return e


def anonymous_fx(P, L):
    """fx(p): … or fx: … (with 'it'): a function without a name."""
    params = parameter_list(P) if is_op(P, "(") else [("it", None)]
    if is_op(P, "=>"):
        raise error("Cupcake no longer uses '=>'. Write:  fx(p): p.hp > 0", peek(P)[2])
    if is_op(P, ":") and peek(P, 1)[0] not in ("nl", "eof"):     # fx: it.hp   → gives that value
        take(P)
        return node("anon", L, params=params, body=expression(P), lam=True)
    body = block_or_header(P)
    check_return(body)
    return node("anon", L, params=params, body=body, lam=False)


def or_(P):
    a = and_(P)
    while is_op(P, "or"):
        L = take(P)[2]
        a = node("or", L, a=a, b=and_(P))
    return a


def and_(P):
    a = not_(P)
    while is_op(P, "and"):
        L = take(P)[2]
        a = node("and", L, a=a, b=not_(P))
    return a


def not_(P):
    if is_op(P, "not"):
        L = take(P)[2]
        return node("not", L, a=not_(P))
    return comparison(P)


COMPARISONS = ("==", "!=", "<", ">", "<=", ">=")


def comparison(P):
    a = range_(P)
    tok = peek(P)
    L = tok[2]
    if tok[0] == "op" and tok[1] in COMPARISONS:
        t = take(P)
        e = node("bin", t[2], op=t[1], a=a, b=range_(P))
        if peek(P)[0] == "op" and peek(P)[1] in COMPARISONS:
            raise error("compare one thing at a time:  x > 0 and x < 10  (or, for a range:  x in 0..10)", L)
        return e
    if is_op(P, "in"):
        take(P)
        return node("in", L, a=a, b=range_(P))
    if is_op(P, "not") and is_op(P, "in", 1):
        take(P)
        take(P)
        return node("not", L, a=node("in", L, a=a, b=range_(P)))
    if is_op(P, "has"):
        take(P)
        negated = bool(accept(P, "not"))
        if peek(P)[0] != "name":
            raise error("after 'has' comes a field name:  pika has hp. "
                        "To ask whether something is in a list or a text, use in:  \"Pikachu\" in team", L)
        e = node("has", L, obj=a, fields=has_fields(P))
        return node("not", L, a=e) if negated else e
    if is_op(P, "is"):
        take(P)
        negated = bool(accept(P, "not"))
        if (peek(P)[0] == "name" and peek(P)[1] in TYPES) or is_op(P, "none"):
            e = node("is_type", L, a=a, type_=take(P)[1])
        else:
            raise error("outside a when, 'is' is for types (x is number, x is empty). "
                        "To compare values use ==:  color == \"red\"", L)
        return node("not", L, a=e) if negated else e
    if peek(P)[0] == "name" and peek(P)[1] == "between":
        raise error(f"Cupcake no longer uses 'between'. Write:  {OLD_WORDS['between']}", L)
    return a


END_OF_FIELDS = (":", ")", ",", "]", "else")


def has_fields(P):
    """After has: a field, or several joined with and / or:  pika has stone and friendship.
    An 'and' continues the list only if what follows is another bare field (not  'and rival has hp')."""
    def term():
        return ("field", name(P, "a field name"))

    def next_is_field():
        if not (is_op(P, "and") or is_op(P, "or")) or peek(P, 1)[0] != "name":
            return False
        after = peek(P, 2)
        return after[0] in ("nl", "eof", "dedent") or (after[0] in ("op", "kw") and after[1] in END_OF_FIELDS + ("and", "or"))

    tree = term()
    while next_is_field():
        op = take(P)[1]
        tree = ("and" if op == "and" else "or", tree, term())
    return tree


def range_ends(P):
    return is_op(P, "]") or is_op(P, ")") or is_op(P, ",") or peek(P)[0] in ("nl", "eof") or is_op(P, ":") or is_op(P, "by") or is_op(P, "at")


def for_header(P, full_expression):
    """for p in list  ·  for i, p at list  ·  for i at list.  Returns (variable, position, iterable)."""
    if peek(P)[0] == "name" and peek(P)[1] == "each":
        raise error(f"Cupcake no longer uses 'each'. Write:  {OLD_WORDS['each']}", peek(P)[2])
    names = [name(P, "the name of the loop variable")]
    if accept(P, ","):
        names.append(name(P, "the name of the loop variable"))
    for n in names:
        dont_shadow(n, peek(P)[2])
    read_with = expression if full_expression else or_
    if accept(P, "in"):
        if len(names) == 2:
            raise error(f"with two names use at:  for {names[0]}, {names[1]} at …", peek(P)[2])
        iterable = read_with(P)
        if is_op(P, "at"):
            raise error(f"the position goes first:  for position, {names[0]} at …", peek(P)[2])
        return names[0], None, iterable
    if accept(P, "at"):
        iterable = read_with(P)
        if len(names) == 1:
            return None, names[0], iterable
        return names[1], names[0], iterable
    raise error("after the variable comes 'in' (each thing) or 'at' (the positions):  for p in team", peek(P)[2])


def range_(P):
    if is_op(P, ".."):                                   # ..b: only inside [ ]
        L = take(P)[2]
        return node("range", L, a=None, b=sum_expr(P), step=None)
    a = sum_expr(P)
    if is_op(P, ".."):
        L = take(P)[2]
        b = None if range_ends(P) else sum_expr(P)
        step = sum_expr(P) if accept(P, "by") else None
        return node("range", L, a=a, b=b, step=step)
    return a


def sum_expr(P):
    a = product(P)
    while peek(P)[0] == "op" and peek(P)[1] in ("+", "-"):
        tok = take(P)
        a = node("bin", tok[2], op=tok[1], a=a, b=product(P))
    return a


def product(P):
    a = unary(P)
    while peek(P)[0] == "op" and peek(P)[1] in ("*", "/", "//", "%"):
        tok = take(P)
        a = node("bin", tok[2], op=tok[1], a=a, b=unary(P))
    return a


def unary(P):
    if peek(P)[0] == "op" and peek(P)[1] in ("-", "+"):
        tok = take(P)
        return node("neg" if tok[1] == "-" else "pos", tok[2], a=unary(P))
    return power(P)


def power(P):
    a = postfix(P)
    if is_op(P, "**"):
        L = take(P)[2]
        return node("bin", L, op="**", a=a, b=unary(P))
    return a


METHOD_HINTS = {
    "append": "add", "remove": "drop", "sort": "sorted", "reverse": "reversed", "pop": "drop",
    "upper": "upper", "lower": "lower", "strip": "strip", "split": "split", "replace": "replace",
    "keys": "keys", "values": "values", "items": "keys", "get": "dict[key] else value", "join": "join", "insert": "add",
    "extend": "+", "count": "count", "index": "in", "format": "\"{…}\"", "startswith": "in", "endswith": "in",
}
CHANGE_THE_DATA = {"append", "remove", "sort", "reverse", "pop", "insert", "extend"}


def postfix(P):
    e = primary(P)
    while True:
        tok = peek(P)
        if is_op(P, "("):
            take(P)
            positional, named = [], []
            while not is_op(P, ")"):
                if peek(P)[0] == "name" and is_op(P, "=", 1):
                    n = take(P)[1]
                    take(P)
                    named.append((n, expression(P)))
                else:
                    if named:
                        raise error("values without a name go before the ones with a name", peek(P)[2])
                    positional.append(expression(P))
                if not accept(P, ","):
                    break
            expect(P, ")", "the ')' of this call is missing")
            e = node("call", tok[2], f=e, args=positional, named=named)
        elif is_op(P, "["):
            take(P)
            position = expression(P)
            expect(P, "]")
            e = node("index", tok[2], obj=e, idx=position)
        elif is_op(P, "."):
            take(P)
            field = name(P, "a field name")
            if is_op(P, "(") and peek(P)[2] == tok[2]:
                raise error(method_message(e, field, args_as_text(P)), tok[2])
            e = node("field", tok[2], obj=e, field=field)
        else:
            return e


def args_as_text(P):
    """The code between the parentheses of a call, to suggest it in a message."""
    begin, level, j = P["i"], 0, P["i"]
    while j < len(P["t"]):
        v = P["t"][j]
        if v[0] == "op" and v[1] in "([":
            level += 1
        elif v[0] == "op" and v[1] in ")]":
            level -= 1
            if level == 0:
                break
        elif v[0] in ("nl", "eof"):
            break
        j += 1
    saved = P["i"]
    P["i"] = j
    text = text_of(P, begin + 1)
    P["i"] = saved
    return text


def method_message(obj, method, args):
    who = obj["name"] if obj["t"] == "name" else "datum"
    func = METHOD_HINTS.get(method, method)
    inner = f"{who}, {args}" if args else who
    if method in CHANGE_THE_DATA:
        example = f"{who} = {func}({inner})"
    elif method == "join":
        example = f"join(list, {who})"
    else:
        example = f"{func}({inner})" if func.isidentifier() else func
    return f"Cupcake has no methods: '.{method}(…)' doesn't exist. Write:  {example}"


def primary(P):
    tok = take(P)
    type_, v, L = tok
    if type_ == "num":
        return node("lit", L, value=v)
    if type_ == "str":
        return text_node(v, L)
    if type_ == "kw" and v in ("true", "false", "none"):
        return node("lit", L, value={"true": True, "false": False, "none": None}[v])
    if type_ == "kw" and v == "fx":
        return anonymous_fx(P, L)
    if type_ == "kw" and v in ("if", "when"):
        raise error(f"'{v}' doesn't give a value. Store the value inside each case:\n"
                    f"    message = \"\"\n    {v} …:\n        message = \"…\"", L)
    if type_ == "name":
        if v in OTHER_WORDS and OTHER_WORDS[v] and (v[0].isupper() or v in ("lam", "lambda")):
            raise error(f"'{v}' is not a Cupcake word. Write '{OTHER_WORDS[v]}'.", L)
        return node("name", L, name=v)
    if type_ == "op" and v == "=>":
        raise error("Cupcake no longer uses '=>'. A function without a name is written:  fx(p): p.hp > 0", L)
    if type_ == "op" and v == "(":
        if is_op(P, ")"):
            raise error("a record needs at least one field:  (name: \"Pikachu\")", L)
        if peek(P)[0] in ("name", "str") and is_op(P, ":", 1):      # (field: value, …) is a record
            return record(P, L)
        e = expression(P)
        expect(P, ")", "the closing ')' is missing")
        return e
    if type_ == "op" and v == "[":
        return list_or_dict(P, L)
    if type_ == "op" and v == "{":
        raise error("Cupcake doesn't use braces. A record is written with parentheses:  "
                    "(name: \"Pikachu\", hp: 35)", L)
    what = "the end of the line" if type_ == "nl" else "the end of the file" if type_ == "eof" else f"'{v}'"
    raise error(f"I didn't expect {what} here", L)


def text_node(parts, L):
    if all(isinstance(p, str) for p in parts):
        return node("lit", L, value="".join(parts))
    pieces = []
    for p in parts:
        if isinstance(p, str):
            pieces.append(p)
        else:
            sub = {"t": tokenize(p[1], p[2]), "i": 0}
            e = expression(sub)
            if peek(sub)[0] not in ("nl", "eof"):
                raise error(f"I don't understand what's between the braces: '{{{p[1]}}}'", p[2])
            pieces.append(e)
    return node("text", L, pieces=pieces)


def list_or_dict(P, L):
    if is_op(P, ":") and is_op(P, "]", 1):
        take(P)
        take(P)
        return node("dict", L, pairs=[])
    if accept(P, "]"):
        return node("list", L, items=[])
    first_ = expression(P)
    if accept(P, ":"):                                # dictionary
        value = expression(P)
        if is_op(P, "for"):
            return comprehension(P, L, key=first_, value=value)
        pairs = [(first_, value)]
        while accept(P, ","):
            if is_op(P, "]"):
                break
            k = expression(P)
            expect(P, ":", "in a dictionary each value has its key:  [\"a\": 1, \"b\": 2]")
            pairs.append((k, expression(P)))
        expect(P, "]", "the closing bracket ']' is missing")
        return node("dict", L, pairs=pairs)
    if is_op(P, "for"):
        return comprehension(P, L, key=None, value=first_)
    items = [first_]
    while accept(P, ","):
        if is_op(P, "]"):
            break
        items.append(expression(P))
    expect(P, "]", "the closing bracket ']' is missing")
    return node("list", L, items=items)


def comprehension(P, L, key, value):
    expect(P, "for")
    var, position, iterable = for_header(P, full_expression=False)
    cond = or_(P) if accept(P, "if") else None
    expect(P, "]", "the closing bracket ']' is missing")
    return node("comp", L, key=key, value=value, var=var, position=position, iterable=iterable, cond=cond)


def record(P, L):
    """(field: value, field: value): the '(' was already read."""
    fields = []
    while not is_op(P, ")"):
        tok = peek(P)
        if tok[0] == "str":
            raise error("in a record, fields go without quotes:  (name: \"Pikachu\"). "
                        "If you want keys with quotes, that's a dictionary:  [\"name\": \"Pikachu\"]", tok[2])
        n = name(P, "a field name")
        expect(P, ":", f"in a record, each field has a colon:  ({n}: value)")
        if any(n == c for c, _ in fields):
            raise error(f"the field '{n}' is repeated", tok[2])
        fields.append((n, expression(P)))
        if not accept(P, ","):
            break
    expect(P, ")", "the record is missing its closing ')'")
    return node("record", L, fields=fields)


# ================================================================ 3. execution
# How Cupcake values are stored:
#   numbers, texts, True/False, None  → the same
#   list                               → list
#   dictionary                         → dict
#   record                            → ("record", dict)     ← its shape doesn't change
#   function                          → ("function", dict)
#   builtin function                  → a host function

def is_record(v):
    return isinstance(v, tuple) and len(v) == 2 and v[0] == "record"


def is_function(v):
    return (isinstance(v, tuple) and len(v) == 2 and v[0] == "function") or callable(v)


def copy(v):
    """Data is copied: each name has its own data."""
    if isinstance(v, list):
        return [copy(x) for x in v]
    if isinstance(v, dict):
        return {k: copy(x) for k, x in v.items()}
    if is_record(v):
        return ("record", {k: copy(x) for k, x in v[1].items()})
    return v


def type_of(v):
    if v is None:
        return "none"
    if isinstance(v, bool):
        return "a yes/no (true or false)"
    if isinstance(v, (int, float)):
        return "a number"
    if isinstance(v, str):
        return "a text"
    if isinstance(v, list):
        return "a list"
    if isinstance(v, dict):
        return "a dictionary"
    if is_record(v):
        return "a record"
    return "a function"


def display(v, inner=False):
    if v is None:
        return "none"
    if v is True:
        return "true"
    if v is False:
        return "false"
    if isinstance(v, str):
        if not inner:
            return v
        return '"' + v.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n") + '"'
    if isinstance(v, float):
        return repr(v)
    if isinstance(v, list):
        return "[" + ", ".join(display(x, True) for x in v) + "]"
    if isinstance(v, dict):
        if not v:
            return "[:]"
        return "[" + ", ".join(f"{display(k, True)}: {display(x, True)}" for k, x in v.items()) + "]"
    if is_record(v):
        return "(" + ", ".join(f"{k}: {display(x, True)}" for k, x in v[1].items()) + ")"
    if isinstance(v, tuple) and v[0] == "function":
        return f"<function {v[1]['name']}>"
    if callable(v):
        return f"<function {v.__name__.rstrip('_')}>"
    return str(v)


# -- environments: {"vars": {...}, "parent": environment or None, "folder": path}

def environment(parent=None, folder=None):
    return {"vars": {}, "parent": parent, "folder": folder if folder is not None else (parent or {}).get("folder", ".")}


def lookup(env, n, L):
    e = env
    while e is not None:
        if n in e["vars"]:
            return e["vars"][n]
        e = e["parent"]
    visible = set()
    e = env
    while e is not None:
        visible |= set(e["vars"])
        e = e["parent"]
    if n in OTHER_WORDS and OTHER_WORDS[n]:
        raise error(f"'{n}' is not a Cupcake word. Write '{OTHER_WORDS[n]}'.", L)
    raise error(f"'{n}' doesn't exist.{did_you_mean(n, visible)}", L)


def execute_program(statements, env):
    # The file's functions are registered first: the order they are written in doesn't matter.
    for s in statements:
        if s["t"] == "def":
            env["vars"][s["name"]] = ("function", {"name": s["name"], "params": s["params"],
                                                    "body": s["body"], "env": env, "lam": False})
    signal = execute_block(statements, env)
    if signal is not None:
        word = {"return": "return", "break": "break", "continue": "continue"}[signal[0]]
        raise error(f"'{word}' only makes sense inside "
                    f"{'a function' if word == 'return' else 'a loop'}", signal[2])


def execute_block(statements, env):
    """Returns None, or a signal: ("return", value, line), ("break", None, line), ("continue", None, line)."""
    for s in statements:
        signal = execute(s, env)
        if signal is not None:
            return signal
    return None


def execute(s, env):
    t = s["t"]
    if t == "expr":
        evaluate(s["expr"], env)
        return None
    if t == "assign":
        assign(s["target"], evaluate(s["value"], env), env, s["l"])
        return None
    if t == "def":
        env["vars"][s["name"]] = ("function", {"name": s["name"], "params": s["params"],
                                                "body": s["body"], "env": env, "lam": False})
        return None
    if t == "if":
        for cond, body in s["branches"]:
            if truthy(evaluate(cond, env)):
                return execute_block(body, env)
        if s["otherwise"] is not None:
            return execute_block(s["otherwise"], env)
        return None
    if t == "while":
        loops = 0
        while truthy(evaluate(s["cond"], env)):
            loops += 1
            if loops > 10_000_000:
                raise error("the loop ran more than ten million times; did you forget to change the condition?", s["l"])
            signal = execute_block(s["body"], env)
            if signal is not None:
                if signal[0] == "break":
                    break
                if signal[0] == "return":
                    return signal
        return None
    if t == "repeat":
        times = evaluate(s["times"], env)
        if not isinstance(times, int) or isinstance(times, bool) or times < 0:
            raise error(f"repeat needs a whole number (how many times), and got {display(times, True)}", s["l"])
        for _ in range(times):
            signal = execute_block(s["body"], env)
            if signal is not None:
                if signal[0] == "break":
                    break
                if signal[0] == "return":
                    return signal
        return None
    if t == "when":
        body = choose_case(s, env)
        return None if body is None else execute_block(body, env)
    if t == "stop":
        raise Exception("cupcake-stop")
    if t == "for":
        for position, element in enumerate(iterable_of(evaluate(s["iterable"], env), s["l"], s.get("position"))):
            if s["var"]:
                env["vars"][s["var"]] = copy(element)
            if s.get("position"):
                env["vars"][s["position"]] = position
            signal = execute_block(s["body"], env)
            if signal is not None:
                if signal[0] == "break":
                    break
                if signal[0] == "return":
                    return signal
        return None
    if t == "return":
        return ("return", None if s["value"] is None else evaluate(s["value"], env), s["l"])
    if t in ("break", "continue"):
        return (t, None, s["l"])
    if t == "raise":
        v = evaluate(s["value"], env)
        raise error(display(v), s["l"])
    if t == "assert":
        if not truthy(evaluate(s["cond"], env)):
            if s["message"] is not None:
                message = display(evaluate(s["message"], env))
            else:
                message = f"assert failed: {s['text']}"
            details = values_of(s["cond"], env)
            if details:
                message += "\n" + "\n".join(f"  {k} is {v}" for k, v in details)
            raise error(message, s["l"])
        return None
    if t == "try":
        try:
            signal = execute_block(s["body"], env)
        except Exception as ex:
            if not is_cupcake_error(ex) or s["handler"] is None:
                if s["finally_"] is not None:
                    execute_block(s["finally_"], env)
                raise
            if s["var"]:
                env["vars"][s["var"]] = ex.args[1]
            try:
                signal = execute_block(s["handler"], env)
            finally:
                if s["finally_"] is not None:
                    execute_block(s["finally_"], env)
            return signal
        if s["finally_"] is not None:
            other = execute_block(s["finally_"], env)
            if other is not None:
                return other
        return signal
    if t == "use":
        use_module(s, env)
        return None
    raise error(f"unknown instruction: {t}", s["l"])


def block_value(body, env, L):
    """A one-line block is worth what that line is worth."""
    if not body:
        return None
    if is_single_value(body):
        return line_value(body[0], env)
    raise error("each block must have a single value", L)


def is_single_value(body):
    """Does the block have a single line that gives a value (an expression, or a whole if / when)?"""
    return len(body) == 1 and body[0]["t"] in ("expr", "if", "when")


def single_value_blocks(s):
    """An if or when whose blocks all have a single line that gives a value."""
    if s["t"] == "if":
        blocks = [c for _, c in s["branches"]] + ([s["otherwise"]] if s["otherwise"] is not None else [])
    else:
        blocks = [c for _, _, c, _ in s["cases"]] + ([s["otherwise"]] if s["otherwise"] is not None else [])
    return all(not b or (is_single_value(b) and (b[0]["t"] == "expr" or single_value_blocks(b[0]))) for b in blocks)


def line_value(s, env):
    if s["t"] == "expr":
        return evaluate(s["expr"], env)
    if s["t"] == "if":
        for cond, body in s["branches"]:
            if truthy(evaluate(cond, env)):
                return block_value(body, env, s["l"])
        return block_value(s["otherwise"], env, s["l"]) if s["otherwise"] is not None else None
    body = choose_case(s, env)
    return None if body is None else block_value(body, env, s["l"])


def is_of_type(v, type_):
    if type_ == "number":
        return isinstance(v, (int, float)) and not isinstance(v, bool)
    if type_ == "text":
        return isinstance(v, str)
    if type_ == "list":
        return isinstance(v, list)
    if type_ == "dict":
        return isinstance(v, dict)
    if type_ == "record":
        return is_record(v)
    if type_ == "function":
        return is_function(v)
    if type_ == "bool":
        return isinstance(v, bool)
    if type_ == "none":
        return v is None
    if type_ == "empty":
        return isinstance(v, (list, dict, str)) and len(v) == 0
    return False


def choose_case(s, env):
    """The block of the first matching case of a when (or the else, or none)."""
    if s.get("subjects"):
        vs = [evaluate(x, env) for x in s["subjects"]]

        def fits(v, pattern, L):
            kind, datum = pattern
            if kind == "type_":
                return is_of_type(v, datum)
            if kind == "value":
                return v == evaluate(datum, env)
            return is_in(v, datum, env, L)

        for (_, alternatives), negated, body, L in s["cases"]:
            matches = any(all(fits(v, pt, L) for v, pt in zip(vs, alt)) for alt in alternatives)
            if matches != negated:
                return body
        return s["otherwise"]
    v = evaluate(s["value"], env)
    for (kind, datum), negated, body, L in s["cases"]:
        if kind == "type_":
            matches = is_of_type(v, datum)
        elif kind == "values":
            matches = any(v == evaluate(x, env) for x in datum)
        else:
            matches = is_in(v, datum, env, L)
        if matches != negated:
            return body
    return s["otherwise"]


def values_of(e, env):
    """The names and fields in a condition, with their values (for assert messages)."""
    seen, output = set(), []

    def walk(x):
        if not isinstance(x, dict):
            return
        if x.get("t") in ("name", "field", "index"):
            text = name_of(x)
            if text and text not in seen:
                seen.add(text)
                try:
                    output.append((text, display(evaluate(x, env), True)))
                except Exception:
                    pass
            if x["t"] != "name":
                return
        for v in x.values():
            if isinstance(v, dict):
                walk(v)
            elif isinstance(v, list):
                for and_ in v:
                    walk(and_)

    walk(e)
    return output


def name_of(x):
    if x["t"] == "name":
        return x["name"]
    if x["t"] == "field":
        base = name_of(x["obj"])
        return base and f"{base}.{x['field']}"
    if x["t"] == "index" and x["idx"]["t"] == "lit":
        base = name_of(x["obj"])
        return base and f"{base}[{display(x['idx']['value'], True)}]"
    return None


def truthy(v):
    if is_record(v):
        return True
    return bool(v)


def iterable_of(v, L, with_position=None):
    if with_position and not isinstance(v, (list, str)):
        raise error(f"'at' gives the positions of a list or a text, and this is {type_of(v)}", L)
    if isinstance(v, (list, str)):
        return list(v)
    if isinstance(v, dict):
        return list(v.keys())
    if is_record(v):
        raise error("a record can't be looped over with for; to see its fields, show it with show(…)", L)
    raise error(f"for needs a list, a text or a dictionary, and got {type_of(v)}", L)


def assign(target, value, env, L):
    value = copy(value)
    t = target["t"]
    if t == "name":
        if target["name"] in OTHER_WORDS and OTHER_WORDS[target["name"]] and target["name"][0].isupper():
            raise error(f"'{target['name']}' is not a Cupcake word. Write '{OTHER_WORDS[target['name']]}'.", L)
        env["vars"][target["name"]] = value
        return
    container = evaluate(target["obj"], env)          # not copied: the variable's own data is changed
    if t == "field":
        if not is_record(container):
            raise error(f"only records have fields, and this is {type_of(container)}", L)
        fields = container[1]
        if target["field"] not in fields:
            raise error(f"the record has no field '{target['field']}'.{did_you_mean(target['field'], fields)} "
                        f"A record is born with its fields and doesn't get new ones.", L)
        fields[target["field"]] = value
        return
    position = evaluate(target["idx"], env)
    if isinstance(container, list):
        if not isinstance(position, int) or isinstance(position, bool):
            raise error("a list position is a whole number", L)
        if not -len(container) <= position < len(container):
            raise error(f"the list has {len(container)} elements; position {position} doesn't exist", L)
        container[position] = value
    elif isinstance(container, dict):
        container[position] = value
    elif is_record(container):
        raise error(f"a record is changed with a dot:  record.{position if isinstance(position, str) else 'field'} = …", L)
    else:
        raise error(f"can't change an element of {type_of(container)}", L)


OPERATIONS = {
    "+": lambda a, b: a + b, "-": lambda a, b: a - b, "*": lambda a, b: a * b,
    "/": lambda a, b: a / b, "//": lambda a, b: a // b, "%": lambda a, b: a % b,
    "**": lambda a, b: a ** b,
    "==": lambda a, b: a == b, "!=": lambda a, b: a != b,
    "<": lambda a, b: a < b, ">": lambda a, b: a > b, "<=": lambda a, b: a <= b, ">=": lambda a, b: a >= b,
}
OPERATION_NAMES = {"+": "add", "-": "subtract", "*": "multiply", "/": "divide", "//": "divide",
                     "%": "take the remainder of", "**": "raise", "<": "compare", ">": "compare",
                     "<=": "compare", ">=": "compare"}


def operate(op, a, b, L):
    if op == "in":
        if isinstance(b, (list, dict)):
            return a in b
        if isinstance(b, str):
            if not isinstance(a, str):
                raise error(f"to search inside a text you need another text, and got {type_of(a)}", L)
            return a in b
        if is_record(b):
            if not isinstance(a, str):
                raise error("to ask whether a record has a field, use its name as text:  \"hp\" in pika", L)
            return a in b[1]
        raise error(f"'in' looks inside a list, a text or a dictionary, not in {type_of(b)}", L)
    if op in ("==", "!="):
        return OPERATIONS[op](a, b)
    number = lambda x: isinstance(x, (int, float)) and not isinstance(x, bool)
    if op == "+" and isinstance(a, str) != isinstance(b, str):
        raise error(f"can't add a text and {type_of(b if isinstance(a, str) else a)}. "
                    f"To join them, put them in a text:  \"…{{value}}…\"", L)
    if op in ("+", "*") and (isinstance(a, list) or isinstance(b, list)):
        if op == "+" and isinstance(a, list) and isinstance(b, list):
            return copy(a) + copy(b)
        if op == "*" and isinstance(a, list) and isinstance(b, int):
            return copy(a) * b
        raise error(f"can't {OPERATION_NAMES[op]} a list and {type_of(b)}. "
                    f"To add something to a list:  add(list, x)", L)
    allowed = (number(a) and number(b)) or (isinstance(a, str) and isinstance(b, str) and op in ("+", "<", ">", "<=", ">=")) \
        or (isinstance(a, str) and isinstance(b, int) and op == "*")
    if not allowed:
        raise error(f"can't {OPERATION_NAMES.get(op, 'operate on')} {type_of(a)} and {type_of(b)}", L)
    try:
        return OPERATIONS[op](a, b)
    except ZeroDivisionError:
        raise error("can't divide by zero", L) from None
    except OverflowError:
        raise error("the number is too big", L) from None


def evaluate(e, env):
    t = e["t"]
    L = e["l"]
    if t == "lit":
        return e["value"]
    if t == "name":
        return lookup(env, e["name"], L)
    if t == "text":
        return "".join(p if isinstance(p, str) else display(evaluate(p, env)) for p in e["pieces"])
    if t == "bin":
        return operate(e["op"], evaluate(e["a"], env), evaluate(e["b"], env), L)
    if t == "and":
        a = evaluate(e["a"], env)
        return evaluate(e["b"], env) if truthy(a) else a
    if t == "or":
        a = evaluate(e["a"], env)
        return a if truthy(a) else evaluate(e["b"], env)
    if t == "not":
        return not truthy(evaluate(e["a"], env))
    if t in ("neg", "pos"):
        a = evaluate(e["a"], env)
        if not isinstance(a, (int, float)) or isinstance(a, bool):
            raise error(f"the {'-' if t == 'neg' else '+'} sign goes with numbers, not with {type_of(a)}", L)
        return -a if t == "neg" else a
    if t == "list":
        return [copy(evaluate(x, env)) for x in e["items"]]
    if t == "dict":
        return {valid_key(evaluate(k, env), L): copy(evaluate(v, env)) for k, v in e["pairs"]}
    if t == "record":
        return ("record", {n: copy(evaluate(v, env)) for n, v in e["fields"]})
    if t == "range":
        if e["a"] is None or e["b"] is None:
            raise error("an open range (like 2.. or ..3) only works inside [ ], to slice a list", L)
        a, b = evaluate(e["a"], env), evaluate(e["b"], env)
        step = 1 if e.get("step") is None else evaluate(e["step"], env)
        if not all(isinstance(x, int) and not isinstance(x, bool) for x in (a, b, step)):
            raise error("a range goes from one whole number to another:  1..10  (and the step is whole too:  by 2)", L)
        if step == 0:
            raise error("the step of a range can't be 0", L)
        return list(range(a, b + 1, step)) if step > 0 else list(range(a, b - 1, step))
    if t == "comp":
        local = environment(env)
        if e["key"] is None:
            output = []
        else:
            output = {}
        for position, x in enumerate(iterable_of(evaluate(e["iterable"], env), L, e.get("position"))):
            if e["var"]:
                local["vars"][e["var"]] = copy(x)
            if e.get("position"):
                local["vars"][e["position"]] = position
            if e["cond"] is not None and not truthy(evaluate(e["cond"], local)):
                continue
            if e["key"] is None:
                output.append(copy(evaluate(e["value"], local)))
            else:
                output[valid_key(evaluate(e["key"], local), L)] = copy(evaluate(e["value"], local))
        return output
    if t == "field":
        obj = evaluate(e["obj"], env)
        if is_record(obj):
            if e["field"] not in obj[1]:
                raise error(f"the record has no field '{e['field']}'.{did_you_mean(e['field'], obj[1])}", L)
            return obj[1][e["field"]]
        if isinstance(obj, dict):
            raise error(f"a dictionary is read with brackets:  dict[\"{e['field']}\"]", L)
        raise error(f"only records have fields, and this is {type_of(obj)}", L)
    if t == "index":
        return index_into(evaluate(e["obj"], env), e["idx"], env, L)
    if t == "call":
        f = evaluate(e["f"], env)
        args = [evaluate(a, env) for a in e["args"]]
        named = [(n, evaluate(v, env)) for n, v in e["named"]]
        return call(f, args, named, L)
    if t == "anon":
        return ("function", {"name": "fx", "params": e["params"], "body": e["body"], "env": env, "lam": e.get("lam", False)})
    if t == "in":
        return is_in(evaluate(e["a"], env), e["b"], env, L)
    if t == "has":
        return has_value(evaluate(e["obj"], env), e["fields"], L)
    if t == "ifvalue":
        for cond, body in e["branches"]:
            if truthy(evaluate(cond, env)):
                return block_value(body, env, L)
        return block_value(e["otherwise"], env, L) if e["otherwise"] is not None else None
    if t == "whenvalue":
        body = choose_case(e, env)
        return None if body is None else block_value(body, env, L)
    if t == "fallback":
        try:
            return evaluate(e["a"], env)
        except Exception as ex:
            if not is_cupcake_error(ex):
                raise
            return evaluate(e["b"], env)
    if t == "is_type":
        return is_of_type(evaluate(e["a"], env), e["type_"])
    if t == "between":
        v = evaluate(e["a"], env)
        return operate("<=", evaluate(e["low"], env), v, L) and operate("<=", v, evaluate(e["high"], env), L)
    raise error(f"unknown expression: {t}", L)


def is_in(v, node_b, env, L):
    """x in group. With a range without 'by' (0..10) it means 'between the two, both included', decimals too."""
    if node_b["t"] == "range" and node_b.get("step") is None and node_b["a"] is not None and node_b["b"] is not None:
        a, b = evaluate(node_b["a"], env), evaluate(node_b["b"], env)
        if not all(isinstance(x, (int, float)) and not isinstance(x, bool) for x in (a, b)):
            raise error("a range goes from one number to another:  0..10", L)
        if not isinstance(v, (int, float)) or isinstance(v, bool):
            return False
        return min(a, b) <= v <= max(a, b)
    return operate("in", v, evaluate(node_b, env), L)


def has_something(v):
    """What 'has' counts as having something: a number greater than 0, a non-empty text or list, true."""
    if isinstance(v, bool):
        return v
    if isinstance(v, (int, float)):
        return v > 0
    if isinstance(v, (str, list, dict)):
        return len(v) > 0
    return v is not None


def has_value(obj, fields, L):
    """pika has hp · eevee has stone and friendship · team has hp (does anyone?)."""
    def fields_of(x):
        return x[1] if is_record(x) else x

    def matches(x, tree):
        if tree[0] == "field":
            data = fields_of(x)
            if tree[1] not in data:
                return False
            return has_something(data[tree[1]])
        a = matches(x, tree[1])
        if tree[0] == "and":
            return a and matches(x, tree[2])
        return a or matches(x, tree[2])

    def check_names(known, tree):
        if tree[0] == "field":
            if tree[1] not in known:
                close = difflib.get_close_matches(tree[1], list(known), 1, 0.7)   # only typos
                if close:
                    raise error(f"there's no field '{tree[1]}'. Did you mean '{close[0]}'?", L)
        else:
            check_names(known, tree[1])
            check_names(known, tree[2])

    if is_record(obj) or isinstance(obj, dict):
        check_names(set(fields_of(obj)), fields)
        return matches(obj, fields)
    if isinstance(obj, list):
        if any(not (is_record(x) or isinstance(x, dict)) for x in obj):
            raise error("'has' asks about fields, and this list has things without fields. "
                        "To know whether something is in the list, use in:  x in list", L)
        known = set()
        for x in obj:
            known |= set(fields_of(x))
        check_names(known, fields)
        return any(matches(x, fields) for x in obj)
    raise error(f"'has' asks about the fields of a record (pika has hp), and this is {type_of(obj)}. "
                f"To search inside a text, use in:  \"chu\" in name", L)


def dont_shadow(n, L):
    if n in BUILTINS:
        raise error(f"'{n}' is already a Cupcake function. Use another name, so you don't hide it", L)


def check_return(body):
    """In a function, a line that only computes a value does nothing: it's probably missing return."""
    for s in body:
        t = s["t"]
        if t == "expr" and s["expr"]["t"] != "call" and not (s["expr"]["t"] == "lit" and s["expr"]["value"] is None):
            raise error("this line computes a value but does nothing with it. "
                        "For the function to give it back, write return:  return …", s["l"])
        for key in ("body", "otherwise", "handler", "finally_"):
            if isinstance(s.get(key), list) and s["t"] != "def":
                check_return(s[key])
        for _, b in s.get("branches", []):
            check_return(b)
        for case in s.get("cases", []):
            check_return(case[2])


def valid_key(k, L):
    if isinstance(k, (list, dict)) or is_record(k):
        raise error("a dictionary key is a text or a number", L)
    return k


def index_into(obj, idx_node, env, L):
    if idx_node["t"] == "range":                         # slicing: list[1..3]
        if not isinstance(obj, (list, str)):
            raise error(f"only lists and texts can be sliced, not {type_of(obj)}", L)
        a = 0 if idx_node["a"] is None else evaluate(idx_node["a"], env)
        b = None if idx_node["b"] is None else evaluate(idx_node["b"], env)
        if not isinstance(a, int) or (b is not None and not isinstance(b, int)):
            raise error("slicing uses whole numbers:  list[1..3]", L)
        end = None if b is None or b == -1 else b + 1     # the last one is included
        return copy(obj[a:end])
    i = evaluate(idx_node, env)
    if isinstance(obj, (list, str)):
        if not isinstance(i, int) or isinstance(i, bool):
            raise error(f"the position is a whole number, and got {type_of(i)}", L)
        if not -len(obj) <= i < len(obj):
            what = "the list" if isinstance(obj, list) else "the text"
            raise error(f"{what} has {len(obj)} elements (0 to {len(obj) - 1}); position {i} doesn't exist", L)
        return obj[i]
    if isinstance(obj, dict):
        if i not in obj:
            raise error(f"the dictionary has no key {display(i, True)}."
                        f"{did_you_mean(str(i), [str(k) for k in obj]) if isinstance(i, str) else ''}", L)
        return obj[i]
    if is_record(obj):
        raise error(f"a record is read with a dot:  record.{i if isinstance(i, str) else 'field'}", L)
    raise error(f"can't look up a position in {type_of(obj)}", L)


def call(f, args, named, L):
    if callable(f):
        try:
            return f(*args, **dict(named))
        except TypeError as ex:
            if is_cupcake_error(ex):
                raise
            raise error(f"{f.__name__.rstrip('_')}() got values it didn't expect ({ex})", L) from None
        except Exception as ex:
            if is_cupcake_error(ex):
                if ex.args[2] is None:
                    raise error(ex.args[1], L) from None
                raise
            raise error(f"{f.__name__.rstrip('_')}(): {ex}", L) from None
    if not (isinstance(f, tuple) and f[0] == "function"):
        raise error(f"this is not a function, it's {type_of(f)}: it can't be called with ( )", L)
    data = f[1]
    params = data["params"]
    local = environment(data["env"])
    if len(args) > len(params):
        raise error(f"{data['name']}() takes {len(params)} value(s) and you gave it {len(args)}", L)
    for (n, _), v in zip(params, args):
        local["vars"][n] = copy(v)
    param_names = [n for n, _ in params]
    for n, v in named:
        if n not in param_names:
            raise error(f"{data['name']}() has no value called '{n}'.{did_you_mean(n, param_names)}", L)
        if n in local["vars"]:
            raise error(f"{data['name']}(): the value '{n}' arrived twice", L)
        local["vars"][n] = copy(v)
    for n, default in params:
        if n not in local["vars"]:
            if default is None:
                raise error(f"{data['name']}() needs the value '{n}'", L)
            local["vars"][n] = copy(evaluate(default, data["env"]))
    if data["lam"]:
        return evaluate(data["body"], local)
    for s in data["body"]:
        if s["t"] == "def":
            local["vars"][s["name"]] = ("function", {"name": s["name"], "params": s["params"],
                                                      "body": s["body"], "env": local, "lam": False})
    signal = execute_block(data["body"], local)
    if signal is None:
        return None
    if signal[0] == "return":
        return signal[1]
    raise error(f"'{signal[0]}' only makes sense inside a loop", signal[2])


# -- other files: use

MODULES = {}            # path → variables of the already executed file
LOADING = set()


def use_module(s, env):
    path_ = os.path.join(env["folder"], s["module"] + ".cup")
    if not os.path.exists(path_):
        raise error(f"I can't find the file '{s['module']}.cup' in the program's folder", s["l"])
    path_ = os.path.abspath(path_)
    if path_ in LOADING:
        raise error(f"'{s['module']}.cup' uses itself in a circle", s["l"])
    if path_ not in MODULES:
        LOADING.add(path_)
        try:
            source = open(path_, encoding="utf-8").read()
            mod_env = environment(GLOBAL, os.path.dirname(path_))
            try:
                execute_program(parse_program(source), mod_env)
            except Exception as ex:
                if is_cupcake_error(ex):
                    raise error(f"in {s['module']}.cup, line {ex.args[2]}: {ex.args[1]}", s["l"]) from None
                raise
            MODULES[path_] = mod_env["vars"]
        finally:
            LOADING.discard(path_)
    variables = MODULES[path_]
    if s["names"] is None:
        for n, v in variables.items():
            env["vars"][n] = v
        return
    for n, alias in s["names"]:
        if n not in variables:
            raise error(f"'{s['module']}.cup' has no '{n}'.{did_you_mean(n, variables)}", s["l"])
        env["vars"][alias] = variables[n]


# ================================================================ 4. builtin functions
# All take the main value first. The ones that "change" something return a new copy.

def need_list(v, who):
    if not isinstance(v, list):
        raise error(f"{who}() needs a list, and got {type_of(v)}")
    return v


def need_text(v, who):
    if not isinstance(v, str):
        raise error(f"{who}() needs a text, and got {type_of(v)}")
    return v


def need_function(v, who):
    if not is_function(v):
        raise error(f"{who}() needs a function, like  fx: it > 0")
    return v


def show(*values_):
    print(" ".join(display(v) for v in values_))


def read(prompt=""):
    """Shows a prompt and returns what the person types (always a text)."""
    try:
        answer = input(display(prompt))
    except EOFError:
        raise error("read() was waiting for someone to type something, and nothing came") from None
    if not sys.stdin.isatty():          # with no person typing, the answer is shown
        print(answer)
    return answer


def len_(v):
    if is_record(v):
        raise error("len() doesn't count a record's fields")
    if not isinstance(v, (list, str, dict)):
        raise error(f"len() counts the elements of a list, a text or a dictionary, not of {type_of(v)}")
    return len(v)


def add(list_, x):
    return copy(need_list(list_, "add")) + [copy(x)]


def drop(collection, x):
    if isinstance(collection, dict):
        if x not in collection:
            raise error(f"drop(): the dictionary has no key {display(x, True)}")
        return {k: copy(v) for k, v in collection.items() if k != x}
    list_ = copy(need_list(collection, "drop"))
    if x not in list_:
        raise error(f"drop(): {display(x, True)} is not in the list")
    list_.remove(x)
    return list_


def sorted_(list_, key=None):
    list_ = need_list(list_, "sorted")
    try:
        if key is None:
            return copy(sorted(list_))
        need_function(key, "sorted")
        return copy(sorted(list_, key=lambda x: call(key, [x], [], None)))
    except TypeError:
        raise error("sorted() can't sort things of different kinds (for example, texts and numbers together)") from None


def reversed_(v):
    if isinstance(v, str):
        return v[::-1]
    return copy(need_list(v, "reversed"))[::-1]


def filter_(list_, f):
    need_function(f, "filter")
    return [copy(x) for x in need_list(list_, "filter") if truthy(call(f, [x], [], None))]


def map_(list_, f):
    need_function(f, "map")
    return [copy(call(f, [x], [], None)) for x in need_list(list_, "map")]


def reduce(list_, f, begin):
    need_function(f, "reduce")
    acc = copy(begin)
    for x in need_list(list_, "reduce"):
        acc = call(f, [acc, x], [], None)
    return acc


def first(list_):
    if not need_list(list_, "first"):
        raise error("first(): the list is empty")
    return copy(list_[0])


def last(list_):
    if not need_list(list_, "last"):
        raise error("last(): the list is empty")
    return copy(list_[-1])


def numbers(values_, who):
    if len(values_) == 1 and isinstance(values_[0], list):
        values_ = values_[0]
    if not values_:
        raise error(f"{who}() needs at least one number")
    for v in values_:
        if not isinstance(v, (int, float, str)) or isinstance(v, bool):
            raise error(f"{who}() compares numbers (or texts), and got {type_of(v)}")
    return values_


def min_(*values_):
    return min(numbers(values_, "min"))


def max_(*values_):
    return max(numbers(values_, "max"))


def sum_(list_):
    total = 0
    for v in need_list(list_, "sum"):
        if not isinstance(v, (int, float)) or isinstance(v, bool):
            raise error(f"sum() adds numbers, and the list has {type_of(v)}")
        total += v
    return total


def abs_(x):
    if not isinstance(x, (int, float)) or isinstance(x, bool):
        raise error(f"abs() needs a number, and got {type_of(x)}")
    return abs(x)


def round_(x, decimals=0):
    if not isinstance(x, (int, float)) or isinstance(x, bool):
        raise error(f"round() needs a number, and got {type_of(x)}")
    return round(x) if decimals == 0 else round(x, decimals)


def int_(x):
    if isinstance(x, bool):
        return int(x)
    if isinstance(x, (int, float)):
        return int(x)
    if isinstance(x, str):
        try:
            return int(x.strip())
        except ValueError:
            raise error(f"'{x}' is not a whole number") from None
    raise error(f"int() converts texts or numbers, not {type_of(x)}")


def float_(x):
    if isinstance(x, (int, float)) and not isinstance(x, bool):
        return float(x)
    if isinstance(x, str):
        try:
            return float(x.strip())
        except ValueError:
            raise error(f"'{x}' is not a number") from None
    raise error(f"float() converts texts or numbers, not {type_of(x)}")


def str_(x):
    return display(x)


def bool_(x):
    return truthy(x)


def upper(t):
    return need_text(t, "upper").upper()


def lower(t):
    return need_text(t, "lower").lower()


def strip(t):
    return need_text(t, "strip").strip()


def split(t, separator=None):
    return need_text(t, "split").split(separator)


def join(list_, separator=""):
    return need_text(separator, "join").join(display(x) for x in need_list(list_, "join"))


def replace(t, old, new):
    return need_text(t, "replace").replace(need_text(old, "replace"), need_text(new, "replace"))


def need_dict(d, who):
    if not isinstance(d, dict):
        extra = " (a record has no keys: its fields are read with a dot)" if is_record(d) else ""
        raise error(f"{who}() needs a dictionary, and got {type_of(d)}{extra}")
    return d


def keys(d):
    return copy(list(need_dict(d, "keys").keys()))


def values(d):
    return copy(list(need_dict(d, "values").values()))


def count(list_, what):
    list_ = need_list(list_, "count")
    if is_function(what):
        return sum(1 for x in list_ if truthy(call(what, [x], [], None)))
    return sum(1 for x in list_ if x == what)


def roll(start, stop_at):
    if not all(isinstance(x, int) and not isinstance(x, bool) for x in (start, stop_at)):
        raise error("roll() needs two whole numbers:  roll(1, 6)")
    if start > stop_at:
        raise error(f"roll({start}, {stop_at}): the first must be less than or equal to the second")
    return random.randint(start, stop_at)


def pick(list_):
    if not need_list(list_, "pick"):
        raise error("pick(): the list is empty")
    return copy(random.choice(list_))


def read_num(prompt=""):
    """Like read, but keeps asking until it gets a number."""
    while True:
        answer = read(prompt).strip()
        try:
            return int(answer)
        except ValueError:
            try:
                return float(answer)
            except ValueError:
                print(f"'{answer}' is not a number. Try again.")


PROGRAM_FOLDER = ["."]


def load(path_):
    """Loads a text file."""
    try:
        with open(os.path.join(PROGRAM_FOLDER[0], need_text(path_, "load")), encoding="utf-8") as f:
            return f.read()
    except OSError:
        raise error(f"load(): couldn't load '{path_}'") from None


def save(path_, text):
    """Saves a text to a file."""
    try:
        with open(os.path.join(PROGRAM_FOLDER[0], need_text(path_, "save")), "w", encoding="utf-8") as f:
            f.write(display(text))
    except OSError:
        raise error(f"save(): couldn't save '{path_}'") from None


BUILTINS = {
    "show": show, "read": read, "len": len_, "add": add, "drop": drop, "sorted": sorted_, "reversed": reversed_,
    "filter": filter_, "map": map_, "reduce": reduce, "first": first, "last": last,
    "min": min_, "max": max_, "sum": sum_, "abs": abs_, "round": round_,
    "int": int_, "float": float_, "str": str_, "bool": bool_,
    "upper": upper, "lower": lower, "strip": strip, "split": split, "join": join, "replace": replace,
    "keys": keys, "values": values, "load": load, "save": save,
    "count": count, "roll": roll, "pick": pick, "read_num": read_num,
}

GLOBAL = environment(None, ".")
GLOBAL["vars"].update(BUILTINS)


# ================================================================ 5. program

def run_text(source, folder="."):
    """Runs a program. Returns None if all went well, or (message, line) if there was an error."""
    PROGRAM_FOLDER[0] = folder
    MODULES.clear()
    env = environment(GLOBAL, folder)
    try:
        execute_program(parse_program(source), env)
        main_fx = env["vars"].get("main")
        if is_function(main_fx):                     # main runs when the file is executed (not when it's loaded with use)
            if main_fx[1]["params"]:
                raise error("main takes no values:  fx main():")
            call(main_fx, [], [], None)
    except Exception as ex:
        if ex.args == ("cupcake-stop",):
            return None
        if is_cupcake_error(ex):
            return ex.args[1], ex.args[2]
        if isinstance(ex, RecursionError):
            return "a function called itself too many times (is a stop condition missing?)", None
        raise
    except KeyboardInterrupt:
        return "stopped with Ctrl+C", None
    return None


def report(file_name, source, result):
    message, line = result
    lines = source.split("\n")
    print(f"\nError in {file_name}" + (f", line {line}:" if line else ":"), file=sys.stderr)
    if line and 1 <= line <= len(lines):
        print(f"    {lines[line - 1].strip()}", file=sys.stderr)
    print(f"  {message}", file=sys.stderr)


def repl():
    print("Cupcake: type code and press Enter. To exit: Ctrl+D")
    env = environment(GLOBAL, ".")
    pending = ""
    while True:
        try:
            line = input("... " if pending else ">>> ")
        except EOFError:
            print()
            return
        pending += line + "\n"
        open_ = pending.count("[") > pending.count("]") or pending.count("(") > pending.count(")")
        with_block = any(l.split("#")[0].rstrip().endswith(":") for l in pending.split("\n"))
        if open_ or (with_block and line.strip()):       # a block ends with an empty line
            continue
        source, pending = pending, ""
        try:
            statements = parse_program(source)
            if len(statements) == 1 and statements[0]["t"] == "expr":
                v = evaluate(statements[0]["expr"], env)
                if v is not None:
                    print(display(v, True))
            else:
                execute_program(statements, env)
        except Exception as ex:
            if ex.args == ("cupcake-stop",):
                return
            if not is_cupcake_error(ex):
                raise
            print(f"Error: {ex.args[1]}")


def main(argv):
    if len(argv) < 2:
        repl()
        return 0
    path_ = argv[1]
    if not path_.endswith(".cup") and not os.path.exists(path_) and os.path.exists(path_ + ".cup"):
        path_ += ".cup"
    try:
        source = open(path_, encoding="utf-8").read()
    except OSError:
        print(f"I can't find the file '{path_}'.", file=sys.stderr)
        return 1
    result = run_text(source, os.path.dirname(os.path.abspath(path_)))
    if result is not None:
        report(os.path.basename(path_), source, result)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
