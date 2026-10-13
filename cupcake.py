#!/usr/bin/env python3
"""
Cupcake: un lenguaje de scripting como Python, sin clases, sin objetos y sin métodos.

    cupcake archivo.cup

Este intérprete tampoco usa clases: solo funciones, diccionarios, listas y tuplas,
igual que el lenguaje que implementa.

Partes:
  1. Léxico:      el texto se convierte en una lista de piezas (tokens).
  2. Sintaxis:    las piezas se convierten en un árbol de nodos (diccionarios).
  3. Ejecución:   se recorre el árbol.
  4. Integradas:  show, read, add, drop, sorted…
  5. Programa:    la línea de comandos.
"""
import difflib
import os
import random
import sys

sys.setrecursionlimit(10000)


# ================================================================ errores

def error(mensaje, linea=None):
    """Todos los errores de Cupcake son un Exception con ("cupcake", mensaje, linea)."""
    return Exception("cupcake", mensaje, linea)


def es_error_cupcake(ex):
    return len(ex.args) == 3 and ex.args[0] == "cupcake"


def parecido(nombre, opciones):
    p = difflib.get_close_matches(nombre, list(opciones), 1, 0.6)
    return f" ¿Quisiste decir «{p[0]}»?" if p else ""


# ================================================================ 1. léxico

PALABRAS = {
    "true", "false", "none", "and", "or", "not", "in", "has", "is",
    "if", "when", "else", "while", "repeat", "for", "at", "by",
    "break", "continue", "return", "stop",
    "fx", "try", "except", "finally", "raise", "assert",
    "use", "from", "as",
}

# Después de «is», estas palabras son tipos: x is number, lista is empty…
TIPOS = {"number", "text", "list", "dict", "record", "function", "bool", "empty"}

DOBLES = {"..", "=>", "==", "!=", "<=", ">=", "**", "//", "+=", "-=", "*=", "/="}
SIMPLES = set("+-*/%<>=()[]{},:.")

# Palabras que Cupcake tuvo antes y ya no usa: se avisa con la forma nueva.
VIEJAS = {
    "other": "else  (y «other if» es «else if»; «x other 0» es «x else 0»)",
    "unless": "if not",
    "until": "while not",
    "each": "for x in lista",
    "between": "x in 1..10",
    "then": ":  (los dos puntos al final de la línea)",
}

PALABRAS_DE_PYTHON = {
    "def": "fx", "elif": "else if", "lambda": "fx(…): …", "True": "true", "False": "false",
    "None": "none", "print": "show", "input": "read", "ask": "read", "ask_number": "read_num", "read_number": "read_num", "write": "save", "class": None, "pass": "none (una línea con none no hace nada)", "import": "use",
    "nonlocal": None, "global": None, "del": "drop(…)", "with": None, "yield": None,
    "fn": "fx", "lam": "fx(…): …", "range": "a..b", "elsif": "else if", "switch": "when", "match": "when",
}


def tokenizar(fuente, linea_inicial=1):
    """Devuelve una lista de (tipo, valor, línea). Tipos: num, str, name, kw, op, nl, indent, dedent, eof.
    La sangría marca los bloques: «indent» abre uno y «dedent» lo cierra."""
    toks = []
    i, n, linea, profundidad = 0, len(fuente), linea_inicial, 0
    niveles = [0]

    def sangria(i, linea):
        """Al empezar una línea: compara su sangría con la de las de arriba."""
        j, ancho = i, 0
        while j < n and fuente[j] in " \t":
            ancho += 4 if fuente[j] == "\t" else 1
            j += 1
        if j >= n or fuente[j] in "\n\r#":           # línea vacía o solo una nota: no cuenta
            return
        if ancho > niveles[-1]:
            niveles.append(ancho)
            toks.append(("indent", ancho, linea))
        while ancho < niveles[-1]:
            niveles.pop()
            toks.append(("dedent", ancho, linea))
        if ancho != niveles[-1]:
            raise error("la sangría de esta línea no coincide con la de ninguna línea de arriba", linea)

    sangria(0, linea)
    while i < n:
        c = fuente[i]
        if c == "\n":
            linea += 1
            i += 1
            if profundidad == 0:
                toks.append(("nl", "\n", linea - 1))
                sangria(i, linea)
            continue
        if c in " \t\r":
            i += 1
            continue
        if c == "#":
            while i < n and fuente[i] != "\n":
                i += 1
            continue
        if c.isdigit():
            j = i
            while j < n and fuente[j].isdigit():
                j += 1
            es_decimal = j + 1 < n and fuente[j] == "." and fuente[j + 1].isdigit()
            if es_decimal:
                j += 1
                while j < n and fuente[j].isdigit():
                    j += 1
                toks.append(("num", float(fuente[i:j]), linea))
            else:
                toks.append(("num", int(fuente[i:j]), linea))
            i = j
            continue
        if c == "λ":
            toks.append(("kw", "fx", linea))
            i += 1
            continue
        if c.isalpha() or c == "_":
            j = i
            while j < n and (fuente[j].isalnum() or fuente[j] == "_"):
                j += 1
            palabra = fuente[i:j]
            toks.append(("kw" if palabra in PALABRAS else "name", palabra, linea))
            i = j
            continue
        if c in "\"'":
            i, linea, partes = leer_texto(fuente, i, linea)
            toks.append(("str", partes, linea))
            continue
        if fuente[i:i + 2] in DOBLES:
            toks.append(("op", fuente[i:i + 2], linea))
            i += 2
            continue
        if c in SIMPLES:
            if c in "([":
                profundidad += 1
            elif c in ")]":
                profundidad = max(0, profundidad - 1)
            toks.append(("op", c, linea))
            i += 1
            continue
        raise error(f"no entiendo el símbolo «{c}»", linea)
    toks.append(("nl", "\n", linea))
    for _ in niveles[1:]:
        toks.append(("dedent", 0, linea))
    toks.append(("eof", None, linea))
    return toks


ESCAPES = {"n": "\n", "t": "\t", "\\": "\\", '"': '"', "'": "'", "{": "{", "}": "}"}


def leer_texto(fuente, i, linea):
    """Lee un texto entre comillas. Devuelve (posición, línea, partes); cada parte es un texto
    o ("expr", código, línea) para lo que va entre llaves."""
    comilla = fuente[i]
    triple = fuente[i:i + 3] == comilla * 3
    cierre = comilla * 3 if triple else comilla
    i += len(cierre)
    linea_inicio = linea
    partes, actual = [], []
    n = len(fuente)
    while True:
        if i >= n:
            raise error("falta cerrar las comillas de este texto", linea_inicio)
        if fuente.startswith(cierre, i):
            i += len(cierre)
            break
        c = fuente[i]
        if c == "\n":
            if not triple:
                raise error("falta cerrar las comillas de este texto (para varias líneas usa \"\"\"…\"\"\")",
                            linea_inicio)
            linea += 1
        if c == "\\" and i + 1 < n:
            actual.append(ESCAPES.get(fuente[i + 1], "\\" + fuente[i + 1]))
            i += 2
            continue
        if c == "{":
            j, nivel = i + 1, 1
            while j < n and nivel:
                if fuente[j] in "\"'":                  # un texto dentro de las llaves
                    q = fuente[j]
                    j += 1
                    while j < n and fuente[j] != q:
                        j += 2 if fuente[j] == "\\" else 1
                elif fuente[j] == "{":
                    nivel += 1
                elif fuente[j] == "}":
                    nivel -= 1
                j += 1
            if nivel:
                raise error("falta cerrar una llave «}» dentro del texto", linea)
            if actual:
                partes.append("".join(actual))
                actual = []
            partes.append(("expr", fuente[i + 1:j - 1], linea))
            i = j
            continue
        actual.append(c)
        i += 1
    if actual or not partes:
        partes.append("".join(actual))
    return i, linea, partes


# ================================================================ 2. sintaxis
# El estado del lector es un diccionario: {"t": tokens, "i": posición}.
# Cada nodo del árbol es un diccionario con "t" (qué es) y "l" (la línea).

def nodo(t, l, **campos):
    campos["t"] = t
    campos["l"] = l
    return campos


def ver(P, k=0):
    return P["t"][min(P["i"] + k, len(P["t"]) - 1)]


def tomar(P):
    tok = ver(P)
    P["i"] += 1
    return tok


def es(P, valor, k=0):
    tok = ver(P, k)
    return tok[0] in ("op", "kw") and tok[1] == valor


def acepta(P, valor):
    if es(P, valor):
        return tomar(P)
    return None


def espera(P, valor, explicacion=None):
    tok = ver(P)
    if es(P, valor):
        return tomar(P)
    llego = "el final de la línea" if tok[0] == "nl" else "el final del archivo" if tok[0] == "eof" \
        else f"«{tok[1]}»" if tok[0] != "str" else "un texto"
    raise error(explicacion or f"se esperaba «{valor}» y llegó {llego}", tok[2])


def saltar_lineas(P):
    while ver(P)[0] == "nl":
        tomar(P)


def nombre(P, que="un nombre"):
    tok = tomar(P)
    if tok[0] != "name":
        raise error(f"se esperaba {que} y llegó «{tok[1]}»", tok[2])
    return tok[1]


def programa(fuente):
    P = {"t": tokenizar(fuente), "i": 0}
    sentencias = []
    saltar_lineas(P)
    while ver(P)[0] != "eof":
        sentencias.append(sentencia(P))
        fin_de_sentencia(P)
        saltar_lineas(P)
    return sentencias


LLAVES = "Cupcake no usa llaves para los bloques: escribe «:» al final de la línea y, debajo, las instrucciones con sangría (4 espacios)"


def fin_de_sentencia(P):
    tok = ver(P)
    if tok[0] in ("nl", "eof", "dedent") or P["t"][P["i"] - 1][0] == "dedent":
        return
    if es(P, "{") or es(P, "}"):
        raise error(LLAVES, tok[2])
    if tok[0] == "name" and tok[1] in VIEJAS:
        raise error(f"Cupcake ya no usa «{tok[1]}». Se escribe:  {VIEJAS[tok[1]]}", tok[2])
    raise error(f"sobra «{tok[1] if tok[0] != 'str' else 'un texto'}» al final de esta instrucción", tok[2])


def bloque(P):
    """«:» y un bloque: en la misma línea (una sola instrucción) o debajo, con sangría."""
    tok = ver(P)
    if es(P, "{"):
        raise error(LLAVES, tok[2])
    if tok[0] == "indent" or (tok[0] == "nl" and ver(P, 1)[0] == "indent"):
        raise error("falta «:» al final de la línea de arriba, antes del bloque con sangría", tok[2])
    if ver(P)[0] == "name" and ver(P)[1] == "then":
        raise error(f"Cupcake ya no usa «then». Se escribe:  {VIEJAS['then']}", ver(P)[2])
    espera(P, ":", "falta «:» al final de la línea, antes del bloque")
    if ver(P)[0] in ("nl", "eof"):
        L = ver(P)[2]
        saltar_lineas(P)
        if ver(P)[0] != "indent":
            raise error("después de «:» van las instrucciones del bloque, debajo y con sangría (4 espacios)", L)
        tomar(P)
        sentencias = []
        while ver(P)[0] not in ("dedent", "eof"):
            sentencias.append(sentencia(P))
            fin_de_sentencia(P)
            saltar_lineas(P)
        acepta_dedent(P)
        return sentencias
    if es(P, "}"):
        raise error(LLAVES, ver(P)[2])
    raise error("lo que hace el bloque va en la línea de abajo, con sangría (4 espacios), no en la misma línea", ver(P)[2])


def acepta_dedent(P):
    if ver(P)[0] == "dedent":
        tomar(P)


def bloque_o_cabecera(P):
    return bloque(P)


def sentencia(P):
    tok = ver(P)
    L = tok[2]
    if tok[0] == "kw" and tok[1] == "else":
        raise error("este «else» no tiene un «if» antes (o está con otra sangría que su if)", L)
    if tok[0] == "name" and tok[1] in VIEJAS and not (es(P, "=", 1) or es(P, "(", 1) or es(P, ".", 1) or es(P, "[", 1)
                                                      or es(P, "+=", 1) or es(P, "-=", 1)):
        raise error(f"Cupcake ya no usa «{tok[1]}». Se escribe:  {VIEJAS[tok[1]]}", L)
    if tok[0] == "indent":
        raise error("esta línea tiene sangría de más (¿falta «:» en la línea de arriba?)", L)
    if es(P, "{") or es(P, "}"):
        raise error(LLAVES, L)
    if tok[0] == "name" and tok[1] in PALABRAS_DE_PYTHON and (
            ver(P, 1)[0] in ("name", "nl") or es(P, ":", 1) or tok[1] in ("def", "class", "else", "elif", "fn")):
        cambio = PALABRAS_DE_PYTHON[tok[1]]
        pista = f" Se escribe «{cambio}»." if cambio else " Cupcake no lo tiene."
        raise error(f"«{tok[1]}» no es una palabra de Cupcake.{pista}", L)
    if tok[0] == "kw":
        v = tok[1]
        if v == "fx" and ver(P, 1)[0] == "name":
            tomar(P)
            n = nombre(P, "el nombre de la función")
            no_tapar(n, L)
            parametros = lista_parametros(P)
            cuerpo = bloque_o_cabecera(P)
            revisar_return(cuerpo)
            return nodo("def", L, nombre=n, params=parametros, cuerpo=cuerpo)
        if v == "if":
            return sentencia_if(P)
        if v == "when":
            return sentencia_when(P)
        if v == "while":
            tomar(P)
            return nodo("while", L, cond=expresion(P), cuerpo=bloque_o_cabecera(P))
        if v == "repeat":
            tomar(P)
            return nodo("repeat", L, veces=expresion(P), cuerpo=bloque_o_cabecera(P))
        if v == "for":
            tomar(P)
            var, indice, iterable = cabeza_for(P, o_completo=True)
            return nodo("for", L, var=var, iterable=iterable, indice=indice, cuerpo=bloque_o_cabecera(P))
        if v == "return":
            tomar(P)
            valor = None if ver(P)[0] in ("nl", "eof", "dedent") else expresion(P)
            return nodo("return", L, valor=valor)
        if v in ("break", "continue", "stop"):
            tomar(P)
            return nodo(v, L)
        if v == "raise":
            tomar(P)
            return nodo("raise", L, valor=expresion(P))
        if v == "assert":
            tomar(P)
            inicio = P["i"]
            cond = expresion(P)
            texto = texto_de(P, inicio)
            mensaje = expresion(P) if acepta(P, ",") else None
            return nodo("assert", L, cond=cond, texto=texto, mensaje=mensaje)
        if v == "try":
            return sentencia_try(P)
        if v == "use":
            return sentencia_use(P)
    e = expresion(P)
    if es(P, "=") or es(P, "+=") or es(P, "-=") or es(P, "*=") or es(P, "/="):
        op = tomar(P)[1]
        if e["t"] not in ("name", "index", "campo"):
            raise error("solo se puede asignar a una variable, a un elemento ([…]) o a un campo (.campo)", L)
        if e["t"] == "name":
            no_tapar(e["nombre"], L)
        valor = expresion(P)
        if op != "=":
            valor = nodo("bin", L, op=op[0], a=e, b=valor)
        return nodo("asignar", L, destino=e, valor=valor)
    return nodo("expr", L, expr=e)


def texto_de(P, inicio):
    """Reconstruye el código de una expresión, para los mensajes de assert."""
    partes = []
    for tok in P["t"][inicio:P["i"]]:
        if tok[0] == "str":
            partes.append('"' + "".join(x if isinstance(x, str) else "{" + x[1] + "}" for x in tok[1]) + '"')
        else:
            partes.append(str(tok[1]))
    texto = " ".join(partes)
    for a, b in ((" . ", "."), (" ( ", "("), (" )", ")"), ("( ", "("), (" [ ", "["), (" ]", "]"), (" ,", ",")):
        texto = texto.replace(a, b)
    return texto


def sentencia_if(P, como_valor=False):
    L = tomar(P)[2]
    ramas = [(expresion(P), bloque_o_cabecera(P))]
    otro = None
    while True:
        guardado = P["i"]
        saltar_lineas(P)
        tok = ver(P)
        if tok[1] == "elif":
            raise error("en Cupcake, «elif» se escribe «else if»", tok[2])
        if tok[0] == "name" and tok[1] == "other":
            raise error(f"Cupcake ya no usa «other». Se escribe:  {VIEJAS['other']}", tok[2])
        if not acepta(P, "else"):
            P["i"] = guardado
            break
        if acepta(P, "if"):
            ramas.append((expresion(P), bloque_o_cabecera(P)))
            continue
        otro = bloque_o_cabecera(P)
        break
    return nodo("ifvalor" if como_valor else "if", L, ramas=ramas, otro=otro)


def cuerpo_de_caso(P):
    """Lo que hace un caso de when: «:» y, debajo, un bloque con sangría."""
    return bloque(P)


def cuerpo_de_else(P):
    return bloque(P)


def other_en_when(tok):
    return error("en un when, el último caso se escribe «else:»", tok[2])


def abrir_casos(P, L):
    """Después de «when x»: «:» y los casos debajo, con sangría (o en la misma línea). Devuelve si van debajo."""
    if es(P, "{"):
        raise error(LLAVES, ver(P)[2])
    espera(P, ":", "falta «:» al final del when:  when x:")
    if ver(P)[0] not in ("nl", "eof"):
        raise error("los casos del when van en las líneas de abajo, con sangría:  is 1:", ver(P)[2])
    saltar_lineas(P)
    if ver(P)[0] != "indent":
        raise error("los casos del when van debajo, con sangría:  is 1:", L)
    tomar(P)
    return True


def fin_de_casos(P, debajo):
    if debajo:
        return ver(P)[0] in ("dedent", "eof")
    return ver(P)[0] in ("nl", "eof", "dedent") or es(P, ")") or es(P, "]") or es(P, ",")


def patron_de_par(P, clase):
    """Un patrón de un caso de when con varias cosas: un tipo o un valor (con is), o un grupo (con in)."""
    if clase == "is" and ((ver(P)[0] == "name" and ver(P)[1] in TIPOS) or es(P, "none")):
        return ("tipo", tomar(P)[1])
    return ("valor" if clase == "is" else "en", no(P))


def casos_de_par(P, clase, cuantos, nombres, L):
    """«"agua" and "fuego", "fuego" and "planta"»: alternativas separadas por coma, cada una con un patrón por cosa."""
    alternativas = []
    while True:
        alt = [patron_de_par(P, clase)]
        while acepta(P, "and"):
            alt.append(patron_de_par(P, clase))
        if len(alt) != cuantos:
            raise error(f"este when compara {cuantos} cosas ({nombres}): cada caso necesita {cuantos} valores unidos con «and», "
                        f"como  {clase} {' and '.join(['…'] * cuantos)}: …", L)
        alternativas.append(alt)
        if not acepta(P, ","):
            return alternativas


def sentencia_when(P, como_valor=False):
    L = tomar(P)[2]
    # «when ataque and defensor:  is "agua" and "fuego": …» compara varias cosas a la vez
    inicio = P["i"]
    sujetos = [no(P)]
    while acepta(P, "and"):
        sujetos.append(no(P))
    if len(sujetos) > 1 and (es(P, ":") or es(P, "{")):
        return when_de_varias(P, L, sujetos, inicio, como_valor)
    P["i"] = inicio
    valor = expresion(P)
    debajo = abrir_casos(P, L)
    casos, otro = [], None
    while not fin_de_casos(P, debajo):
        tok = ver(P)
        if tok[0] == "name" and tok[1] == "other":
            raise other_en_when(tok)
        if acepta(P, "else"):
            otro = cuerpo_de_else(P)
        elif acepta(P, "is"):
            negado = bool(acepta(P, "not"))
            if (ver(P)[0] == "name" and ver(P)[1] in TIPOS) or es(P, "none"):
                patron = ("tipo", tomar(P)[1])
            else:
                valores = [o(P)]
                while acepta(P, ","):
                    valores.append(o(P))
                patron = ("valores", valores)
            casos.append((patron, negado, cuerpo_de_caso(P), tok[2]))
        elif acepta(P, "in"):
            casos.append((("en", o(P)), False, cuerpo_de_caso(P), tok[2]))
        else:
            raise error("cada caso de when empieza con «is», «in» o «else»:  is \"rojo\": show(\"rojo\")", tok[2])
        if debajo:
            saltar_lineas(P)
    if debajo:
        acepta_dedent(P)
    return nodo("whenvalor" if como_valor else "when", L, valor=valor, casos=casos, otro=otro)


def when_de_varias(P, L, sujetos, inicio, como_valor):
    nombres = " and ".join(nombre_de(s) or "…" for s in sujetos)
    debajo = abrir_casos(P, L)
    casos, otro = [], None
    while not fin_de_casos(P, debajo):
        tok = ver(P)
        if tok[0] == "name" and tok[1] == "other":
            raise other_en_when(tok)
        if acepta(P, "else"):
            otro = cuerpo_de_else(P)
        elif tok[0] == "kw" and tok[1] in ("is", "in"):
            clase = tomar(P)[1]
            negado = clase == "is" and bool(acepta(P, "not"))
            alternativas = casos_de_par(P, clase, len(sujetos), nombres, tok[2])
            casos.append((("pares", alternativas), negado, cuerpo_de_caso(P), tok[2]))
        else:
            raise error(f"cada caso de when empieza con «is», «in» o «else»:  is {' and '.join(['…'] * len(sujetos))}: …", tok[2])
        if debajo:
            saltar_lineas(P)
    if debajo:
        acepta_dedent(P)
    return nodo("whenvalor" if como_valor else "when", L, valor=None, sujetos=sujetos, casos=casos, otro=otro)


def sentencia_try(P):
    L = tomar(P)[2]
    cuerpo = bloque_o_cabecera(P)
    var = manejo = final = None
    guardado = P["i"]
    saltar_lineas(P)
    if acepta(P, "except"):
        if ver(P)[0] == "name":
            var = tomar(P)[1]
        manejo = bloque_o_cabecera(P)
        guardado = P["i"]
        saltar_lineas(P)
    if acepta(P, "finally"):
        final = bloque_o_cabecera(P)
    else:
        P["i"] = guardado
    if manejo is None and final is None:
        raise error("después de try va «except» o «finally»", L)
    return nodo("try", L, cuerpo=cuerpo, var=var, manejo=manejo, final=final)


def sentencia_use(P):
    L = tomar(P)[2]
    nombres = []
    while True:
        n = nombre(P, "el nombre de lo que quieres usar")
        alias = nombre(P, "el nuevo nombre") if acepta(P, "as") else n
        nombres.append((n, alias))
        if not acepta(P, ","):
            break
    if acepta(P, "from"):
        modulo = nombre(P, "el nombre del archivo")
        return nodo("use", L, modulo=modulo, nombres=nombres)
    if len(nombres) > 1 or nombres[0][0] != nombres[0][1]:
        raise error("falta «from»: use curar, describir from pokemon", L)
    return nodo("use", L, modulo=nombres[0][0], nombres=None)


def lista_parametros(P):
    espera(P, "(")
    params = []
    while not es(P, ")"):
        n = nombre(P, "el nombre de un parámetro")
        no_tapar(n, ver(P)[2])
        defecto = expresion(P) if acepta(P, "=") else None
        params.append((n, defecto))
        if not acepta(P, ","):
            break
    espera(P, ")")
    return params


# -- expresiones, de menor a mayor prioridad

def expresion(P):
    e = o(P)
    # «else» como reserva: si lo de la izquierda falla, vale lo de la derecha.
    while es(P, "else") and not es(P, ":", 1) and not es(P, "if", 1):
        L = tomar(P)[2]
        e = nodo("reserva", L, a=e, b=o(P))
    return e


def fx_anonima(P, L):
    """fx(p): … o fx: … (con «it»): una función sin nombre."""
    params = lista_parametros(P) if es(P, "(") else [("it", None)]
    if es(P, "=>"):
        raise error("Cupcake ya no usa «=>». Escribe:  fx(p): p.vida > 0", ver(P)[2])
    if es(P, ":") and ver(P, 1)[0] not in ("nl", "eof"):     # fx: it.vida   → da ese valor
        tomar(P)
        return nodo("anon", L, params=params, cuerpo=expresion(P), lam=True)
    cuerpo = bloque_o_cabecera(P)
    revisar_return(cuerpo)
    return nodo("anon", L, params=params, cuerpo=cuerpo, lam=False)


def o(P):
    a = y(P)
    while es(P, "or"):
        L = tomar(P)[2]
        a = nodo("o", L, a=a, b=y(P))
    return a


def y(P):
    a = no(P)
    while es(P, "and"):
        L = tomar(P)[2]
        a = nodo("y", L, a=a, b=no(P))
    return a


def no(P):
    if es(P, "not"):
        L = tomar(P)[2]
        return nodo("no", L, a=no(P))
    return comparacion(P)


COMPARACIONES = ("==", "!=", "<", ">", "<=", ">=")


def comparacion(P):
    a = rango(P)
    tok = ver(P)
    L = tok[2]
    if tok[0] == "op" and tok[1] in COMPARACIONES:
        t = tomar(P)
        e = nodo("bin", t[2], op=t[1], a=a, b=rango(P))
        if ver(P)[0] == "op" and ver(P)[1] in COMPARACIONES:
            raise error("compara de a una cosa:  x > 0 and x < 10  (o, para un rango:  x in 0..10)", L)
        return e
    if es(P, "in"):
        tomar(P)
        return nodo("en", L, a=a, b=rango(P))
    if es(P, "not") and es(P, "in", 1):
        tomar(P)
        tomar(P)
        return nodo("no", L, a=nodo("en", L, a=a, b=rango(P)))
    if es(P, "has"):
        tomar(P)
        negado = bool(acepta(P, "not"))
        if ver(P)[0] != "name":
            raise error("después de «has» va el nombre de un campo:  pika has vida. "
                        "Para preguntar si algo está en una lista o un texto se usa in:  \"Pikachu\" in equipo", L)
        e = nodo("tiene", L, obj=a, campos=campos_de_has(P))
        return nodo("no", L, a=e) if negado else e
    if es(P, "is"):
        tomar(P)
        negado = bool(acepta(P, "not"))
        if (ver(P)[0] == "name" and ver(P)[1] in TIPOS) or es(P, "none"):
            e = nodo("es_tipo", L, a=a, tipo=tomar(P)[1])
        else:
            raise error("fuera de un when, «is» es para tipos (x is number, x is empty). "
                        "Para comparar valores se usa ==:  color == \"rojo\"", L)
        return nodo("no", L, a=e) if negado else e
    if ver(P)[0] == "name" and ver(P)[1] == "between":
        raise error(f"Cupcake ya no usa «between». Se escribe:  {VIEJAS['between']}", L)
    return a


FIN_DE_CAMPOS = (":", ")", ",", "]", "else")


def campos_de_has(P):
    """Después de has: un campo, o varios unidos con and / or:  pika has piedra and amistad.
    Un «and» sigue la lista solo si lo que viene es otro campo suelto (no  «and rival has vida»)."""
    def termino():
        return ("campo", nombre(P, "el nombre de un campo"))

    def sigue_campo():
        if not (es(P, "and") or es(P, "or")) or ver(P, 1)[0] != "name":
            return False
        despues = ver(P, 2)
        return despues[0] in ("nl", "eof", "dedent") or (despues[0] in ("op", "kw") and despues[1] in FIN_DE_CAMPOS + ("and", "or"))

    arbol = termino()
    while sigue_campo():
        op = tomar(P)[1]
        arbol = ("y" if op == "and" else "o", arbol, termino())
    return arbol


def termina_rango(P):
    return es(P, "]") or es(P, ")") or es(P, ",") or ver(P)[0] in ("nl", "eof") or es(P, ":") or es(P, "by") or es(P, "at")


def cabeza_for(P, o_completo):
    """for p in lista  ·  for i, p at lista  ·  for i at lista.  Devuelve (variable, posición, recorrible)."""
    if ver(P)[0] == "name" and ver(P)[1] == "each":
        raise error(f"Cupcake ya no usa «each». Se escribe:  {VIEJAS['each']}", ver(P)[2])
    nombres = [nombre(P, "el nombre de la variable del ciclo")]
    if acepta(P, ","):
        nombres.append(nombre(P, "el nombre de la variable del ciclo"))
    for n in nombres:
        no_tapar(n, ver(P)[2])
    leer = expresion if o_completo else o
    if acepta(P, "in"):
        if len(nombres) == 2:
            raise error(f"con dos nombres se usa at:  for {nombres[0]}, {nombres[1]} at …", ver(P)[2])
        iterable = leer(P)
        if es(P, "at"):
            raise error(f"la posición va primero:  for posicion, {nombres[0]} at …", ver(P)[2])
        return nombres[0], None, iterable
    if acepta(P, "at"):
        iterable = leer(P)
        if len(nombres) == 1:
            return None, nombres[0], iterable
        return nombres[1], nombres[0], iterable
    raise error("después de la variable va «in» (cada cosa) o «at» (las posiciones):  for p in equipo", ver(P)[2])


def rango(P):
    if es(P, ".."):                                   # ..b: solo dentro de [ ]
        L = tomar(P)[2]
        return nodo("rango", L, a=None, b=suma(P), paso=None)
    a = suma(P)
    if es(P, ".."):
        L = tomar(P)[2]
        b = None if termina_rango(P) else suma(P)
        paso = suma(P) if acepta(P, "by") else None
        return nodo("rango", L, a=a, b=b, paso=paso)
    return a


def suma(P):
    a = producto(P)
    while ver(P)[0] == "op" and ver(P)[1] in ("+", "-"):
        tok = tomar(P)
        a = nodo("bin", tok[2], op=tok[1], a=a, b=producto(P))
    return a


def producto(P):
    a = unario(P)
    while ver(P)[0] == "op" and ver(P)[1] in ("*", "/", "//", "%"):
        tok = tomar(P)
        a = nodo("bin", tok[2], op=tok[1], a=a, b=unario(P))
    return a


def unario(P):
    if ver(P)[0] == "op" and ver(P)[1] in ("-", "+"):
        tok = tomar(P)
        return nodo("neg" if tok[1] == "-" else "pos", tok[2], a=unario(P))
    return potencia(P)


def potencia(P):
    a = postfijo(P)
    if es(P, "**"):
        L = tomar(P)[2]
        return nodo("bin", L, op="**", a=a, b=unario(P))
    return a


SUGERENCIAS_METODOS = {
    "append": "add", "remove": "drop", "sort": "sorted", "reverse": "reversed", "pop": "drop",
    "upper": "upper", "lower": "lower", "strip": "strip", "split": "split", "replace": "replace",
    "keys": "keys", "values": "values", "items": "keys", "get": "dic[clave] other valor", "join": "join", "insert": "add",
    "extend": "+", "count": "count", "index": "in", "format": "\"{…}\"", "startswith": "has", "endswith": "has",
}
CAMBIAN_EL_DATO = {"append", "remove", "sort", "reverse", "pop", "insert", "extend"}


def postfijo(P):
    e = primario(P)
    while True:
        tok = ver(P)
        if es(P, "("):
            tomar(P)
            posicionales, nombrados = [], []
            while not es(P, ")"):
                if ver(P)[0] == "name" and es(P, "=", 1):
                    n = tomar(P)[1]
                    tomar(P)
                    nombrados.append((n, expresion(P)))
                else:
                    if nombrados:
                        raise error("los datos sin nombre van antes de los que tienen nombre", ver(P)[2])
                    posicionales.append(expresion(P))
                if not acepta(P, ","):
                    break
            espera(P, ")", "falta cerrar el paréntesis «)» de esta llamada")
            e = nodo("llamar", tok[2], f=e, args=posicionales, nombrados=nombrados)
        elif es(P, "["):
            tomar(P)
            indice = expresion(P)
            espera(P, "]")
            e = nodo("index", tok[2], obj=e, idx=indice)
        elif es(P, "."):
            tomar(P)
            campo = nombre(P, "el nombre de un campo")
            if es(P, "(") and ver(P)[2] == tok[2]:
                raise error(mensaje_metodo(e, campo, argumentos_como_texto(P)), tok[2])
            e = nodo("campo", tok[2], obj=e, campo=campo)
        else:
            return e


def argumentos_como_texto(P):
    """El código que va entre los paréntesis de una llamada, para sugerirlo en un mensaje."""
    inicio, nivel, j = P["i"], 0, P["i"]
    while j < len(P["t"]):
        v = P["t"][j]
        if v[0] == "op" and v[1] in "([":
            nivel += 1
        elif v[0] == "op" and v[1] in ")]":
            nivel -= 1
            if nivel == 0:
                break
        elif v[0] in ("nl", "eof"):
            break
        j += 1
    guardado = P["i"]
    P["i"] = j
    texto = texto_de(P, inicio + 1)
    P["i"] = guardado
    return texto


def mensaje_metodo(obj, metodo, args):
    quien = obj["nombre"] if obj["t"] == "name" else "dato"
    funcion = SUGERENCIAS_METODOS.get(metodo, metodo)
    dentro = f"{quien}, {args}" if args else quien
    if metodo in CAMBIAN_EL_DATO:
        ejemplo = f"{quien} = {funcion}({dentro})"
    elif metodo == "join":
        ejemplo = f"join(lista, {quien})"
    else:
        ejemplo = f"{funcion}({dentro})" if funcion.isidentifier() else funcion
    return f"Cupcake no tiene métodos: «.{metodo}(…)» no existe. Escribe:  {ejemplo}"


def primario(P):
    tok = tomar(P)
    tipo, v, L = tok
    if tipo == "num":
        return nodo("lit", L, valor=v)
    if tipo == "str":
        return texto_nodo(v, L)
    if tipo == "kw" and v in ("true", "false", "none"):
        return nodo("lit", L, valor={"true": True, "false": False, "none": None}[v])
    if tipo == "kw" and v == "fx":
        return fx_anonima(P, L)
    if tipo == "kw" and v in ("if", "when"):
        raise error(f"«{v}» no da un valor. Guarda el valor dentro de cada caso:\n"
                    f"    mensaje = \"\"\n    {v} …:\n        mensaje = \"…\"", L)
    if tipo == "name":
        if v in PALABRAS_DE_PYTHON and PALABRAS_DE_PYTHON[v] and (v[0].isupper() or v in ("lam", "lambda")):
            raise error(f"«{v}» no es una palabra de Cupcake. Se escribe «{PALABRAS_DE_PYTHON[v]}».", L)
        return nodo("name", L, nombre=v)
    if tipo == "op" and v == "=>":
        raise error("Cupcake ya no usa «=>». Una función sin nombre se escribe:  fx(p): p.vida > 0", L)
    if tipo == "op" and v == "(":
        if es(P, ")"):
            raise error("un registro necesita al menos un campo:  (nombre: \"Pikachu\")", L)
        if ver(P)[0] in ("name", "str") and es(P, ":", 1):      # (campo: valor, …) es un registro
            return registro(P, L)
        e = expresion(P)
        espera(P, ")", "falta cerrar el paréntesis «)»")
        return e
    if tipo == "op" and v == "[":
        return lista_o_diccionario(P, L)
    if tipo == "op" and v == "{":
        raise error("Cupcake no usa llaves. Un registro se escribe con paréntesis:  "
                    "(nombre: \"Pikachu\", vida: 35)", L)
    que = "el final de la línea" if tipo == "nl" else "el final del archivo" if tipo == "eof" else f"«{v}»"
    raise error(f"no esperaba {que} aquí", L)


def texto_nodo(partes, L):
    if all(isinstance(p, str) for p in partes):
        return nodo("lit", L, valor="".join(partes))
    piezas = []
    for p in partes:
        if isinstance(p, str):
            piezas.append(p)
        else:
            sub = {"t": tokenizar(p[1], p[2]), "i": 0}
            e = expresion(sub)
            if ver(sub)[0] not in ("nl", "eof"):
                raise error(f"no entiendo lo que está entre llaves: «{{{p[1]}}}»", p[2])
            piezas.append(e)
    return nodo("texto", L, piezas=piezas)


def lista_o_diccionario(P, L):
    if es(P, ":") and es(P, "]", 1):
        tomar(P)
        tomar(P)
        return nodo("dic", L, pares=[])
    if acepta(P, "]"):
        return nodo("lista", L, items=[])
    primero = expresion(P)
    if acepta(P, ":"):                                # diccionario
        valor = expresion(P)
        if es(P, "for"):
            return comprension(P, L, clave=primero, valor=valor)
        pares = [(primero, valor)]
        while acepta(P, ","):
            if es(P, "]"):
                break
            k = expresion(P)
            espera(P, ":", "en un diccionario cada valor lleva su clave:  [\"a\": 1, \"b\": 2]")
            pares.append((k, expresion(P)))
        espera(P, "]", "falta cerrar el corchete «]»")
        return nodo("dic", L, pares=pares)
    if es(P, "for"):
        return comprension(P, L, clave=None, valor=primero)
    items = [primero]
    while acepta(P, ","):
        if es(P, "]"):
            break
        items.append(expresion(P))
    espera(P, "]", "falta cerrar el corchete «]»")
    return nodo("lista", L, items=items)


def comprension(P, L, clave, valor):
    espera(P, "for")
    var, indice, iterable = cabeza_for(P, o_completo=False)
    cond = o(P) if acepta(P, "if") else None
    espera(P, "]", "falta cerrar el corchete «]»")
    return nodo("comp", L, clave=clave, valor=valor, var=var, indice=indice, iterable=iterable, cond=cond)


def registro(P, L):
    """(campo: valor, campo: valor): el «(» ya se leyó."""
    campos = []
    while not es(P, ")"):
        tok = ver(P)
        if tok[0] == "str":
            raise error("en un registro, los campos van sin comillas:  (nombre: \"Pikachu\"). "
                        "Si quieres claves con comillas, es un diccionario:  [\"nombre\": \"Pikachu\"]", tok[2])
        n = nombre(P, "el nombre de un campo")
        espera(P, ":", f"en un registro, cada campo lleva dos puntos:  ({n}: valor)")
        if any(n == c for c, _ in campos):
            raise error(f"el campo «{n}» está repetido", tok[2])
        campos.append((n, expresion(P)))
        if not acepta(P, ","):
            break
    espera(P, ")", "falta cerrar el registro con «)»")
    return nodo("registro", L, campos=campos)


# ================================================================ 3. ejecución
# Los valores de Cupcake en Python:
#   números, textos, True/False, None  → igual
#   lista                              → list
#   diccionario                        → dict
#   registro                           → ("registro", dict)     ← la forma no cambia
#   función                            → ("funcion", dict)
#   función integrada                  → una función de Python

def es_registro(v):
    return isinstance(v, tuple) and len(v) == 2 and v[0] == "registro"


def es_funcion(v):
    return (isinstance(v, tuple) and len(v) == 2 and v[0] == "funcion") or callable(v)


def copiar(v):
    """Los datos se copian: cada nombre tiene su propio dato."""
    if isinstance(v, list):
        return [copiar(x) for x in v]
    if isinstance(v, dict):
        return {k: copiar(x) for k, x in v.items()}
    if es_registro(v):
        return ("registro", {k: copiar(x) for k, x in v[1].items()})
    return v


def tipo_de(v):
    if v is None:
        return "none"
    if isinstance(v, bool):
        return "un sí/no (true o false)"
    if isinstance(v, (int, float)):
        return "un número"
    if isinstance(v, str):
        return "un texto"
    if isinstance(v, list):
        return "una lista"
    if isinstance(v, dict):
        return "un diccionario"
    if es_registro(v):
        return "un registro"
    return "una función"


def mostrar(v, dentro=False):
    if v is None:
        return "none"
    if v is True:
        return "true"
    if v is False:
        return "false"
    if isinstance(v, str):
        if not dentro:
            return v
        return '"' + v.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n") + '"'
    if isinstance(v, float):
        return repr(v)
    if isinstance(v, list):
        return "[" + ", ".join(mostrar(x, True) for x in v) + "]"
    if isinstance(v, dict):
        if not v:
            return "[:]"
        return "[" + ", ".join(f"{mostrar(k, True)}: {mostrar(x, True)}" for k, x in v.items()) + "]"
    if es_registro(v):
        return "(" + ", ".join(f"{k}: {mostrar(x, True)}" for k, x in v[1].items()) + ")"
    if isinstance(v, tuple) and v[0] == "funcion":
        return f"<función {v[1]['nombre']}>"
    if callable(v):
        return f"<función {v.__name__.rstrip('_')}>"
    return str(v)


# -- entornos: {"vars": {...}, "padre": entorno o None, "carpeta": ruta}

def entorno(padre=None, carpeta=None):
    return {"vars": {}, "padre": padre, "carpeta": carpeta if carpeta is not None else (padre or {}).get("carpeta", ".")}


def buscar(env, n, L):
    e = env
    while e is not None:
        if n in e["vars"]:
            return e["vars"][n]
        e = e["padre"]
    visibles = set()
    e = env
    while e is not None:
        visibles |= set(e["vars"])
        e = e["padre"]
    if n in PALABRAS_DE_PYTHON and PALABRAS_DE_PYTHON[n]:
        raise error(f"«{n}» no es una palabra de Cupcake. Se escribe «{PALABRAS_DE_PYTHON[n]}».", L)
    raise error(f"«{n}» no existe.{parecido(n, visibles)}", L)


def ejecutar_programa(sentencias, env):
    # Las funciones del archivo se registran primero: el orden en que se escriben no importa.
    for s in sentencias:
        if s["t"] == "def":
            env["vars"][s["nombre"]] = ("funcion", {"nombre": s["nombre"], "params": s["params"],
                                                    "cuerpo": s["cuerpo"], "env": env, "lam": False})
    señal = ejecutar_bloque(sentencias, env)
    if señal is not None:
        palabra = {"return": "return", "break": "break", "continue": "continue"}[señal[0]]
        raise error(f"«{palabra}» solo tiene sentido dentro de "
                    f"{'una función' if palabra == 'return' else 'un ciclo'}", señal[2])


def ejecutar_bloque(sentencias, env):
    """Devuelve None, o una señal: ("return", valor, línea), ("break", None, línea), ("continue", None, línea)."""
    for s in sentencias:
        señal = ejecutar(s, env)
        if señal is not None:
            return señal
    return None


def ejecutar(s, env):
    t = s["t"]
    if t == "expr":
        evaluar(s["expr"], env)
        return None
    if t == "asignar":
        asignar(s["destino"], evaluar(s["valor"], env), env, s["l"])
        return None
    if t == "def":
        env["vars"][s["nombre"]] = ("funcion", {"nombre": s["nombre"], "params": s["params"],
                                                "cuerpo": s["cuerpo"], "env": env, "lam": False})
        return None
    if t == "if":
        for cond, cuerpo in s["ramas"]:
            if verdad(evaluar(cond, env)):
                return ejecutar_bloque(cuerpo, env)
        if s["otro"] is not None:
            return ejecutar_bloque(s["otro"], env)
        return None
    if t == "while":
        vueltas = 0
        while verdad(evaluar(s["cond"], env)):
            vueltas += 1
            if vueltas > 10_000_000:
                raise error("el ciclo dio más de diez millones de vueltas; ¿olvidaste cambiar la condición?", s["l"])
            señal = ejecutar_bloque(s["cuerpo"], env)
            if señal is not None:
                if señal[0] == "break":
                    break
                if señal[0] == "return":
                    return señal
        return None
    if t == "repeat":
        veces = evaluar(s["veces"], env)
        if not isinstance(veces, int) or isinstance(veces, bool) or veces < 0:
            raise error(f"repeat necesita un número entero (cuántas veces), y recibió {mostrar(veces, True)}", s["l"])
        for _ in range(veces):
            señal = ejecutar_bloque(s["cuerpo"], env)
            if señal is not None:
                if señal[0] == "break":
                    break
                if señal[0] == "return":
                    return señal
        return None
    if t == "when":
        cuerpo = elegir_caso(s, env)
        return None if cuerpo is None else ejecutar_bloque(cuerpo, env)
    if t == "stop":
        raise Exception("cupcake-stop")
    if t == "for":
        for posicion, elemento in enumerate(recorrible(evaluar(s["iterable"], env), s["l"], s.get("indice"))):
            if s["var"]:
                env["vars"][s["var"]] = copiar(elemento)
            if s.get("indice"):
                env["vars"][s["indice"]] = posicion
            señal = ejecutar_bloque(s["cuerpo"], env)
            if señal is not None:
                if señal[0] == "break":
                    break
                if señal[0] == "return":
                    return señal
        return None
    if t == "return":
        return ("return", None if s["valor"] is None else evaluar(s["valor"], env), s["l"])
    if t in ("break", "continue"):
        return (t, None, s["l"])
    if t == "raise":
        v = evaluar(s["valor"], env)
        raise error(mostrar(v), s["l"])
    if t == "assert":
        if not verdad(evaluar(s["cond"], env)):
            if s["mensaje"] is not None:
                mensaje = mostrar(evaluar(s["mensaje"], env))
            else:
                mensaje = f"assert falló: {s['texto']}"
            detalles = valores_de(s["cond"], env)
            if detalles:
                mensaje += "\n" + "\n".join(f"  {k} vale {v}" for k, v in detalles)
            raise error(mensaje, s["l"])
        return None
    if t == "try":
        try:
            señal = ejecutar_bloque(s["cuerpo"], env)
        except Exception as ex:
            if not es_error_cupcake(ex) or s["manejo"] is None:
                if s["final"] is not None:
                    ejecutar_bloque(s["final"], env)
                raise
            if s["var"]:
                env["vars"][s["var"]] = ex.args[1]
            try:
                señal = ejecutar_bloque(s["manejo"], env)
            finally:
                if s["final"] is not None:
                    ejecutar_bloque(s["final"], env)
            return señal
        if s["final"] is not None:
            otra = ejecutar_bloque(s["final"], env)
            if otra is not None:
                return otra
        return señal
    if t == "use":
        usar(s, env)
        return None
    raise error(f"instrucción desconocida: {t}", s["l"])


def valor_de_bloque(cuerpo, env, L):
    """Un bloque de una sola línea vale lo que esa línea vale (para if, when y fx que dan un valor)."""
    if not cuerpo:
        return None
    if es_de_un_valor(cuerpo):
        return valor_de_linea(cuerpo[0], env)
    raise error("cuando un if o un when da un valor, cada bloque tiene una sola cosa:  if x: 1 other: 2", L)


def es_de_un_valor(cuerpo):
    """¿El bloque tiene una sola línea que da un valor (una expresión, o un if / when completo)?"""
    return len(cuerpo) == 1 and cuerpo[0]["t"] in ("expr", "if", "when")


def bloques_de_un_valor(s):
    """Un if o when cuyos bloques tienen todos una sola línea que da un valor (si no, se ejecuta como siempre)."""
    if s["t"] == "if":
        bloques = [c for _, c in s["ramas"]] + ([s["otro"]] if s["otro"] is not None else [])
    else:
        bloques = [c for _, _, c, _ in s["casos"]] + ([s["otro"]] if s["otro"] is not None else [])
    return all(not b or (es_de_un_valor(b) and (b[0]["t"] == "expr" or bloques_de_un_valor(b[0]))) for b in bloques)


def valor_de_linea(s, env):
    if s["t"] == "expr":
        return evaluar(s["expr"], env)
    if s["t"] == "if":
        for cond, cuerpo in s["ramas"]:
            if verdad(evaluar(cond, env)):
                return valor_de_bloque(cuerpo, env, s["l"])
        return valor_de_bloque(s["otro"], env, s["l"]) if s["otro"] is not None else None
    cuerpo = elegir_caso(s, env)
    return None if cuerpo is None else valor_de_bloque(cuerpo, env, s["l"])


def es_del_tipo(v, tipo):
    if tipo == "number":
        return isinstance(v, (int, float)) and not isinstance(v, bool)
    if tipo == "text":
        return isinstance(v, str)
    if tipo == "list":
        return isinstance(v, list)
    if tipo == "dict":
        return isinstance(v, dict)
    if tipo == "record":
        return es_registro(v)
    if tipo == "function":
        return es_funcion(v)
    if tipo == "bool":
        return isinstance(v, bool)
    if tipo == "none":
        return v is None
    if tipo == "empty":
        return isinstance(v, (list, dict, str)) and len(v) == 0
    return False


def elegir_caso(s, env):
    """El bloque del primer caso de un when que se cumple (o el de other, o ninguno)."""
    if s.get("sujetos"):
        vs = [evaluar(x, env) for x in s["sujetos"]]

        def encaja(v, patron, L):
            clase, dato = patron
            if clase == "tipo":
                return es_del_tipo(v, dato)
            if clase == "valor":
                return v == evaluar(dato, env)
            return esta_en(v, dato, env, L)

        for (_, alternativas), negado, cuerpo, L in s["casos"]:
            cumple = any(all(encaja(v, pt, L) for v, pt in zip(vs, alt)) for alt in alternativas)
            if cumple != negado:
                return cuerpo
        return s["otro"]
    v = evaluar(s["valor"], env)
    for (clase, dato), negado, cuerpo, L in s["casos"]:
        if clase == "tipo":
            cumple = es_del_tipo(v, dato)
        elif clase == "valores":
            cumple = any(v == evaluar(x, env) for x in dato)
        else:
            cumple = esta_en(v, dato, env, L)
        if cumple != negado:
            return cuerpo
    return s["otro"]


def valores_de(e, env):
    """Los nombres y campos que aparecen en una condición, con su valor (para los mensajes de assert)."""
    vistos, salida = set(), []

    def recorrer(x):
        if not isinstance(x, dict):
            return
        if x.get("t") in ("name", "campo", "index"):
            texto = nombre_de(x)
            if texto and texto not in vistos:
                vistos.add(texto)
                try:
                    salida.append((texto, mostrar(evaluar(x, env), True)))
                except Exception:
                    pass
            if x["t"] != "name":
                return
        for v in x.values():
            if isinstance(v, dict):
                recorrer(v)
            elif isinstance(v, list):
                for y in v:
                    recorrer(y)

    recorrer(e)
    return salida


def nombre_de(x):
    if x["t"] == "name":
        return x["nombre"]
    if x["t"] == "campo":
        base = nombre_de(x["obj"])
        return base and f"{base}.{x['campo']}"
    if x["t"] == "index" and x["idx"]["t"] == "lit":
        base = nombre_de(x["obj"])
        return base and f"{base}[{mostrar(x['idx']['valor'], True)}]"
    return None


def verdad(v):
    if es_registro(v):
        return True
    return bool(v)


def recorrible(v, L, con_posicion=None):
    if con_posicion and not isinstance(v, (list, str)):
        raise error(f"«at» da las posiciones de una lista o un texto, y esto es {tipo_de(v)}", L)
    if isinstance(v, (list, str)):
        return list(v)
    if isinstance(v, dict):
        return list(v.keys())
    if es_registro(v):
        raise error("un registro no se recorre con for; para ver sus campos, muéstralo con show(…)", L)
    raise error(f"for necesita una lista, un texto o un diccionario, y recibió {tipo_de(v)}", L)


def asignar(destino, valor, env, L):
    valor = copiar(valor)
    t = destino["t"]
    if t == "name":
        if destino["nombre"] in PALABRAS_DE_PYTHON and PALABRAS_DE_PYTHON[destino["nombre"]] and destino["nombre"][0].isupper():
            raise error(f"«{destino['nombre']}» es de Python.", L)
        env["vars"][destino["nombre"]] = valor
        return
    contenedor = evaluar(destino["obj"], env)          # sin copiar: se cambia el dato de esa variable
    if t == "campo":
        if not es_registro(contenedor):
            raise error(f"solo los registros tienen campos, y esto es {tipo_de(contenedor)}", L)
        campos = contenedor[1]
        if destino["campo"] not in campos:
            raise error(f"el registro no tiene el campo «{destino['campo']}».{parecido(destino['campo'], campos)} "
                        f"Un registro nace con sus campos y no gana campos nuevos.", L)
        campos[destino["campo"]] = valor
        return
    indice = evaluar(destino["idx"], env)
    if isinstance(contenedor, list):
        if not isinstance(indice, int) or isinstance(indice, bool):
            raise error("la posición de una lista es un número entero", L)
        if not -len(contenedor) <= indice < len(contenedor):
            raise error(f"la lista tiene {len(contenedor)} elementos; la posición {indice} no existe", L)
        contenedor[indice] = valor
    elif isinstance(contenedor, dict):
        contenedor[indice] = valor
    elif es_registro(contenedor):
        raise error(f"un registro se cambia con punto:  registro.{indice if isinstance(indice, str) else 'campo'} = …", L)
    else:
        raise error(f"no se puede cambiar un elemento de {tipo_de(contenedor)}", L)


OPERACIONES = {
    "+": lambda a, b: a + b, "-": lambda a, b: a - b, "*": lambda a, b: a * b,
    "/": lambda a, b: a / b, "//": lambda a, b: a // b, "%": lambda a, b: a % b,
    "**": lambda a, b: a ** b,
    "==": lambda a, b: a == b, "!=": lambda a, b: a != b,
    "<": lambda a, b: a < b, ">": lambda a, b: a > b, "<=": lambda a, b: a <= b, ">=": lambda a, b: a >= b,
}
NOMBRES_OPERACION = {"+": "sumar", "-": "restar", "*": "multiplicar", "/": "dividir", "//": "dividir",
                     "%": "sacar el resto de", "**": "elevar", "<": "comparar", ">": "comparar",
                     "<=": "comparar", ">=": "comparar"}


def operar(op, a, b, L):
    if op == "in":
        if isinstance(b, (list, dict)):
            return a in b
        if isinstance(b, str):
            if not isinstance(a, str):
                raise error(f"para buscar dentro de un texto hace falta otro texto, y llegó {tipo_de(a)}", L)
            return a in b
        if es_registro(b):
            if not isinstance(a, str):
                raise error("para preguntar si un registro tiene un campo, se usa su nombre en texto:  \"vida\" in pika", L)
            return a in b[1]
        raise error(f"«in» busca dentro de una lista, un texto o un diccionario, no en {tipo_de(b)}", L)
    if op in ("==", "!="):
        return OPERACIONES[op](a, b)
    numero = lambda x: isinstance(x, (int, float)) and not isinstance(x, bool)
    if op == "+" and isinstance(a, str) != isinstance(b, str):
        raise error(f"no se puede sumar un texto y {tipo_de(b if isinstance(a, str) else a)}. "
                    f"Para juntarlos, ponlos en un texto:  \"…{{valor}}…\"", L)
    if op in ("+", "*") and (isinstance(a, list) or isinstance(b, list)):
        if op == "+" and isinstance(a, list) and isinstance(b, list):
            return copiar(a) + copiar(b)
        if op == "*" and isinstance(a, list) and isinstance(b, int):
            return copiar(a) * b
        raise error(f"no se puede {NOMBRES_OPERACION[op]} una lista y {tipo_de(b)}. "
                    f"Para agregar algo a una lista:  add(lista, x)", L)
    permitido = (numero(a) and numero(b)) or (isinstance(a, str) and isinstance(b, str) and op in ("+", "<", ">", "<=", ">=")) \
        or (isinstance(a, str) and isinstance(b, int) and op == "*")
    if not permitido:
        raise error(f"no se puede {NOMBRES_OPERACION.get(op, 'operar')} {tipo_de(a)} y {tipo_de(b)}", L)
    try:
        return OPERACIONES[op](a, b)
    except ZeroDivisionError:
        raise error("no se puede dividir entre cero", L) from None
    except OverflowError:
        raise error("el número es demasiado grande", L) from None


def evaluar(e, env):
    t = e["t"]
    L = e["l"]
    if t == "lit":
        return e["valor"]
    if t == "name":
        return buscar(env, e["nombre"], L)
    if t == "texto":
        return "".join(p if isinstance(p, str) else mostrar(evaluar(p, env)) for p in e["piezas"])
    if t == "bin":
        return operar(e["op"], evaluar(e["a"], env), evaluar(e["b"], env), L)
    if t == "y":
        a = evaluar(e["a"], env)
        return evaluar(e["b"], env) if verdad(a) else a
    if t == "o":
        a = evaluar(e["a"], env)
        return a if verdad(a) else evaluar(e["b"], env)
    if t == "no":
        return not verdad(evaluar(e["a"], env))
    if t in ("neg", "pos"):
        a = evaluar(e["a"], env)
        if not isinstance(a, (int, float)) or isinstance(a, bool):
            raise error(f"el signo {'-' if t == 'neg' else '+'} va con números, no con {tipo_de(a)}", L)
        return -a if t == "neg" else a
    if t == "lista":
        return [copiar(evaluar(x, env)) for x in e["items"]]
    if t == "dic":
        return {clave_valida(evaluar(k, env), L): copiar(evaluar(v, env)) for k, v in e["pares"]}
    if t == "registro":
        return ("registro", {n: copiar(evaluar(v, env)) for n, v in e["campos"]})
    if t == "rango":
        if e["a"] is None or e["b"] is None:
            raise error("un rango abierto (como 2.. o ..3) solo sirve dentro de [ ], para cortar una lista", L)
        a, b = evaluar(e["a"], env), evaluar(e["b"], env)
        paso = 1 if e.get("paso") is None else evaluar(e["paso"], env)
        if not all(isinstance(x, int) and not isinstance(x, bool) for x in (a, b, paso)):
            raise error("un rango va de un número entero a otro:  1..10  (y el salto también es entero:  by 2)", L)
        if paso == 0:
            raise error("el salto de un rango no puede ser 0", L)
        return list(range(a, b + 1, paso)) if paso > 0 else list(range(a, b - 1, paso))
    if t == "comp":
        local = entorno(env)
        if e["clave"] is None:
            salida = []
        else:
            salida = {}
        for posicion, x in enumerate(recorrible(evaluar(e["iterable"], env), L, e.get("indice"))):
            if e["var"]:
                local["vars"][e["var"]] = copiar(x)
            if e.get("indice"):
                local["vars"][e["indice"]] = posicion
            if e["cond"] is not None and not verdad(evaluar(e["cond"], local)):
                continue
            if e["clave"] is None:
                salida.append(copiar(evaluar(e["valor"], local)))
            else:
                salida[clave_valida(evaluar(e["clave"], local), L)] = copiar(evaluar(e["valor"], local))
        return salida
    if t == "campo":
        obj = evaluar(e["obj"], env)
        if es_registro(obj):
            if e["campo"] not in obj[1]:
                raise error(f"el registro no tiene el campo «{e['campo']}».{parecido(e['campo'], obj[1])}", L)
            return obj[1][e["campo"]]
        if isinstance(obj, dict):
            raise error(f"un diccionario se lee con corchetes:  dic[\"{e['campo']}\"]", L)
        raise error(f"solo los registros tienen campos, y esto es {tipo_de(obj)}", L)
    if t == "index":
        return indexar(evaluar(e["obj"], env), e["idx"], env, L)
    if t == "llamar":
        f = evaluar(e["f"], env)
        args = [evaluar(a, env) for a in e["args"]]
        nombrados = [(n, evaluar(v, env)) for n, v in e["nombrados"]]
        return llamar(f, args, nombrados, L)
    if t == "anon":
        return ("funcion", {"nombre": "fx", "params": e["params"], "cuerpo": e["cuerpo"], "env": env, "lam": e.get("lam", False)})
    if t == "en":
        return esta_en(evaluar(e["a"], env), e["b"], env, L)
    if t == "tiene":
        return tiene(evaluar(e["obj"], env), e["campos"], L)
    if t == "ifvalor":
        for cond, cuerpo in e["ramas"]:
            if verdad(evaluar(cond, env)):
                return valor_de_bloque(cuerpo, env, L)
        return valor_de_bloque(e["otro"], env, L) if e["otro"] is not None else None
    if t == "whenvalor":
        cuerpo = elegir_caso(e, env)
        return None if cuerpo is None else valor_de_bloque(cuerpo, env, L)
    if t == "reserva":
        try:
            return evaluar(e["a"], env)
        except Exception as ex:
            if not es_error_cupcake(ex):
                raise
            return evaluar(e["b"], env)
    if t == "es_tipo":
        return es_del_tipo(evaluar(e["a"], env), e["tipo"])
    if t == "entre":
        v = evaluar(e["a"], env)
        return operar("<=", evaluar(e["bajo"], env), v, L) and operar("<=", v, evaluar(e["alto"], env), L)
    raise error(f"expresión desconocida: {t}", L)


def esta_en(v, nodo_b, env, L):
    """x in grupo. Con un rango sin «by» (0..10) es «entre los dos, contando los dos», también con decimales."""
    if nodo_b["t"] == "rango" and nodo_b.get("paso") is None and nodo_b["a"] is not None and nodo_b["b"] is not None:
        a, b = evaluar(nodo_b["a"], env), evaluar(nodo_b["b"], env)
        if not all(isinstance(x, (int, float)) and not isinstance(x, bool) for x in (a, b)):
            raise error("un rango va de un número a otro:  0..10", L)
        if not isinstance(v, (int, float)) or isinstance(v, bool):
            return False
        return min(a, b) <= v <= max(a, b)
    return operar("in", v, evaluar(nodo_b, env), L)


def tiene_algo(v):
    """Lo que «has» considera tener: un número mayor que 0, un texto o lista con algo, true."""
    if isinstance(v, bool):
        return v
    if isinstance(v, (int, float)):
        return v > 0
    if isinstance(v, (str, list, dict)):
        return len(v) > 0
    return v is not None


def tiene(obj, campos, L):
    """pika has vida · eevee has piedra and amistad · equipo has vida (¿alguno?)."""
    def campos_de(x):
        return x[1] if es_registro(x) else x

    def cumple(x, arbol):
        if arbol[0] == "campo":
            datos = campos_de(x)
            if arbol[1] not in datos:
                return False
            return tiene_algo(datos[arbol[1]])
        a = cumple(x, arbol[1])
        if arbol[0] == "y":
            return a and cumple(x, arbol[2])
        return a or cumple(x, arbol[2])

    def revisar_nombres(conocidos, arbol):
        if arbol[0] == "campo":
            if arbol[1] not in conocidos:
                cerca = difflib.get_close_matches(arbol[1], list(conocidos), 1, 0.7)   # solo errores de escritura
                if cerca:
                    raise error(f"no hay ningún campo «{arbol[1]}». ¿Quisiste decir «{cerca[0]}»?", L)
        else:
            revisar_nombres(conocidos, arbol[1])
            revisar_nombres(conocidos, arbol[2])

    if es_registro(obj) or isinstance(obj, dict):
        revisar_nombres(set(campos_de(obj)), campos)
        return cumple(obj, campos)
    if isinstance(obj, list):
        if any(not (es_registro(x) or isinstance(x, dict)) for x in obj):
            raise error("«has» pregunta por campos, y esta lista tiene cosas sin campos. "
                        "Para saber si algo está en la lista se usa in:  x in lista", L)
        conocidos = set()
        for x in obj:
            conocidos |= set(campos_de(x))
        revisar_nombres(conocidos, campos)
        return any(cumple(x, campos) for x in obj)
    raise error(f"«has» pregunta por los campos de un registro (pika has vida), y esto es {tipo_de(obj)}. "
                f"Para buscar dentro de un texto se usa in:  \"chu\" in nombre", L)


def no_tapar(n, L):
    if n in INTEGRADAS:
        raise error(f"«{n}» ya es una función de Cupcake. Usa otro nombre, para no taparla", L)


def revisar_return(cuerpo):
    """En una función, una línea que solo calcula un valor no hace nada: seguramente le falta return."""
    for s in cuerpo:
        t = s["t"]
        if t == "expr" and s["expr"]["t"] != "llamar" and not (s["expr"]["t"] == "lit" and s["expr"]["valor"] is None):
            raise error("esta línea calcula un valor, pero no hace nada con él. "
                        "Para que la función lo devuelva, escribe return:  return …", s["l"])
        for clave in ("cuerpo", "otro", "manejo", "final"):
            if isinstance(s.get(clave), list) and s["t"] != "def":
                revisar_return(s[clave])
        for _, b in s.get("ramas", []):
            revisar_return(b)
        for caso in s.get("casos", []):
            revisar_return(caso[2])


def clave_valida(k, L):
    if isinstance(k, (list, dict)) or es_registro(k):
        raise error("la clave de un diccionario es un texto o un número", L)
    return k


def indexar(obj, idx_nodo, env, L):
    if idx_nodo["t"] == "rango":                         # cortar: lista[1..3]
        if not isinstance(obj, (list, str)):
            raise error(f"solo se pueden cortar listas y textos, no {tipo_de(obj)}", L)
        a = 0 if idx_nodo["a"] is None else evaluar(idx_nodo["a"], env)
        b = None if idx_nodo["b"] is None else evaluar(idx_nodo["b"], env)
        if not isinstance(a, int) or (b is not None and not isinstance(b, int)):
            raise error("para cortar se usan números enteros:  lista[1..3]", L)
        fin = None if b is None or b == -1 else b + 1     # el último se incluye
        return copiar(obj[a:fin])
    i = evaluar(idx_nodo, env)
    if isinstance(obj, (list, str)):
        if not isinstance(i, int) or isinstance(i, bool):
            raise error(f"la posición es un número entero, y llegó {tipo_de(i)}", L)
        if not -len(obj) <= i < len(obj):
            que = "la lista" if isinstance(obj, list) else "el texto"
            raise error(f"{que} tiene {len(obj)} elementos (de 0 a {len(obj) - 1}); la posición {i} no existe", L)
        return obj[i]
    if isinstance(obj, dict):
        if i not in obj:
            raise error(f"el diccionario no tiene la clave {mostrar(i, True)}."
                        f"{parecido(str(i), [str(k) for k in obj]) if isinstance(i, str) else ''}", L)
        return obj[i]
    if es_registro(obj):
        raise error(f"un registro se lee con punto:  registro.{i if isinstance(i, str) else 'campo'}", L)
    raise error(f"no se puede buscar una posición en {tipo_de(obj)}", L)


def llamar(f, args, nombrados, L):
    if callable(f):
        try:
            return f(*args, **dict(nombrados))
        except TypeError as ex:
            if es_error_cupcake(ex):
                raise
            raise error(f"{f.__name__.rstrip('_')}() recibió datos que no esperaba ({ex})", L) from None
        except Exception as ex:
            if es_error_cupcake(ex):
                if ex.args[2] is None:
                    raise error(ex.args[1], L) from None
                raise
            raise error(f"{f.__name__.rstrip('_')}(): {ex}", L) from None
    if not (isinstance(f, tuple) and f[0] == "funcion"):
        raise error(f"esto no es una función, es {tipo_de(f)}: no se puede llamar con ( )", L)
    datos = f[1]
    params = datos["params"]
    local = entorno(datos["env"])
    if len(args) > len(params):
        raise error(f"{datos['nombre']}() recibe {len(params)} dato(s) y le diste {len(args)}", L)
    for (n, _), v in zip(params, args):
        local["vars"][n] = copiar(v)
    nombres_params = [n for n, _ in params]
    for n, v in nombrados:
        if n not in nombres_params:
            raise error(f"{datos['nombre']}() no tiene un dato llamado «{n}».{parecido(n, nombres_params)}", L)
        if n in local["vars"]:
            raise error(f"{datos['nombre']}(): el dato «{n}» llegó dos veces", L)
        local["vars"][n] = copiar(v)
    for n, defecto in params:
        if n not in local["vars"]:
            if defecto is None:
                raise error(f"{datos['nombre']}() necesita el dato «{n}»", L)
            local["vars"][n] = copiar(evaluar(defecto, datos["env"]))
    if datos["lam"]:
        return evaluar(datos["cuerpo"], local)
    for s in datos["cuerpo"]:
        if s["t"] == "def":
            local["vars"][s["nombre"]] = ("funcion", {"nombre": s["nombre"], "params": s["params"],
                                                      "cuerpo": s["cuerpo"], "env": local, "lam": False})
    señal = ejecutar_bloque(datos["cuerpo"], local)
    if señal is None:
        return None
    if señal[0] == "return":
        return señal[1]
    raise error(f"«{señal[0]}» solo tiene sentido dentro de un ciclo", señal[2])


# -- otros archivos: use

MODULOS = {}            # ruta → variables del archivo ya ejecutado
CARGANDO = set()


def usar(s, env):
    ruta = os.path.join(env["carpeta"], s["modulo"] + ".cup")
    if not os.path.exists(ruta):
        raise error(f"no encuentro el archivo «{s['modulo']}.cup» en la carpeta del programa", s["l"])
    ruta = os.path.abspath(ruta)
    if ruta in CARGANDO:
        raise error(f"«{s['modulo']}.cup» se usa a sí mismo en un círculo", s["l"])
    if ruta not in MODULOS:
        CARGANDO.add(ruta)
        try:
            fuente = open(ruta, encoding="utf-8").read()
            mod_env = entorno(GLOBAL, os.path.dirname(ruta))
            try:
                ejecutar_programa(programa(fuente), mod_env)
            except Exception as ex:
                if es_error_cupcake(ex):
                    raise error(f"en {s['modulo']}.cup, línea {ex.args[2]}: {ex.args[1]}", s["l"]) from None
                raise
            MODULOS[ruta] = mod_env["vars"]
        finally:
            CARGANDO.discard(ruta)
    variables = MODULOS[ruta]
    if s["nombres"] is None:
        for n, v in variables.items():
            env["vars"][n] = v
        return
    for n, alias in s["nombres"]:
        if n not in variables:
            raise error(f"«{s['modulo']}.cup» no tiene «{n}».{parecido(n, variables)}", s["l"])
        env["vars"][alias] = variables[n]


# ================================================================ 4. funciones integradas
# Todas con el dato principal primero. Las que «cambian» algo devuelven una copia nueva.

def pedir_lista(v, quien):
    if not isinstance(v, list):
        raise error(f"{quien}() necesita una lista, y recibió {tipo_de(v)}")
    return v


def pedir_texto(v, quien):
    if not isinstance(v, str):
        raise error(f"{quien}() necesita un texto, y recibió {tipo_de(v)}")
    return v


def pedir_funcion(v, quien):
    if not es_funcion(v):
        raise error(f"{quien}() necesita una función, como  lam x => x > 0")
    return v


def show(*valores):
    print(" ".join(mostrar(v) for v in valores))


def read(aviso=""):
    """Muestra un aviso y devuelve lo que la persona escribe (siempre un texto)."""
    try:
        respuesta = input(mostrar(aviso))
    except EOFError:
        raise error("read() esperaba que alguien escribiera algo, y no llegó nada") from None
    if not sys.stdin.isatty():          # sin una persona escribiendo, se muestra la respuesta
        print(respuesta)
    return respuesta


def len_(v):
    if es_registro(v):
        raise error("len() no cuenta los campos de un registro")
    if not isinstance(v, (list, str, dict)):
        raise error(f"len() cuenta los elementos de una lista, un texto o un diccionario, no de {tipo_de(v)}")
    return len(v)


def add(lista, x):
    return copiar(pedir_lista(lista, "add")) + [copiar(x)]


def drop(coleccion, x):
    if isinstance(coleccion, dict):
        if x not in coleccion:
            raise error(f"drop(): el diccionario no tiene la clave {mostrar(x, True)}")
        return {k: copiar(v) for k, v in coleccion.items() if k != x}
    lista = copiar(pedir_lista(coleccion, "drop"))
    if x not in lista:
        raise error(f"drop(): {mostrar(x, True)} no está en la lista")
    lista.remove(x)
    return lista


def sorted_(lista, clave=None):
    lista = pedir_lista(lista, "sorted")
    try:
        if clave is None:
            return copiar(sorted(lista))
        pedir_funcion(clave, "sorted")
        return copiar(sorted(lista, key=lambda x: llamar(clave, [x], [], None)))
    except TypeError:
        raise error("sorted() no puede ordenar cosas de distinto tipo (por ejemplo, textos y números juntos)") from None


def reversed_(v):
    if isinstance(v, str):
        return v[::-1]
    return copiar(pedir_lista(v, "reversed"))[::-1]


def filter_(lista, f):
    pedir_funcion(f, "filter")
    return [copiar(x) for x in pedir_lista(lista, "filter") if verdad(llamar(f, [x], [], None))]


def map_(lista, f):
    pedir_funcion(f, "map")
    return [copiar(llamar(f, [x], [], None)) for x in pedir_lista(lista, "map")]


def reduce(lista, f, inicio):
    pedir_funcion(f, "reduce")
    acumulado = copiar(inicio)
    for x in pedir_lista(lista, "reduce"):
        acumulado = llamar(f, [acumulado, x], [], None)
    return acumulado


def first(lista):
    if not pedir_lista(lista, "first"):
        raise error("first(): la lista está vacía")
    return copiar(lista[0])


def last(lista):
    if not pedir_lista(lista, "last"):
        raise error("last(): la lista está vacía")
    return copiar(lista[-1])


def numeros(valores, quien):
    if len(valores) == 1 and isinstance(valores[0], list):
        valores = valores[0]
    if not valores:
        raise error(f"{quien}() necesita al menos un número")
    for v in valores:
        if not isinstance(v, (int, float, str)) or isinstance(v, bool):
            raise error(f"{quien}() compara números (o textos), y recibió {tipo_de(v)}")
    return valores


def min_(*valores):
    return min(numeros(valores, "min"))


def max_(*valores):
    return max(numeros(valores, "max"))


def sum_(lista):
    total = 0
    for v in pedir_lista(lista, "sum"):
        if not isinstance(v, (int, float)) or isinstance(v, bool):
            raise error(f"sum() suma números, y la lista tiene {tipo_de(v)}")
        total += v
    return total


def abs_(x):
    if not isinstance(x, (int, float)) or isinstance(x, bool):
        raise error(f"abs() necesita un número, y recibió {tipo_de(x)}")
    return abs(x)


def round_(x, decimales=0):
    if not isinstance(x, (int, float)) or isinstance(x, bool):
        raise error(f"round() necesita un número, y recibió {tipo_de(x)}")
    return round(x) if decimales == 0 else round(x, decimales)


def int_(x):
    if isinstance(x, bool):
        return int(x)
    if isinstance(x, (int, float)):
        return int(x)
    if isinstance(x, str):
        try:
            return int(x.strip())
        except ValueError:
            raise error(f"«{x}» no es un número entero") from None
    raise error(f"int() convierte textos o números, no {tipo_de(x)}")


def float_(x):
    if isinstance(x, (int, float)) and not isinstance(x, bool):
        return float(x)
    if isinstance(x, str):
        try:
            return float(x.strip())
        except ValueError:
            raise error(f"«{x}» no es un número") from None
    raise error(f"float() convierte textos o números, no {tipo_de(x)}")


def str_(x):
    return mostrar(x)


def bool_(x):
    return verdad(x)


def upper(t):
    return pedir_texto(t, "upper").upper()


def lower(t):
    return pedir_texto(t, "lower").lower()


def strip(t):
    return pedir_texto(t, "strip").strip()


def split(t, separador=None):
    return pedir_texto(t, "split").split(separador)


def join(lista, separador=""):
    return pedir_texto(separador, "join").join(mostrar(x) for x in pedir_lista(lista, "join"))


def replace(t, viejo, nuevo):
    return pedir_texto(t, "replace").replace(pedir_texto(viejo, "replace"), pedir_texto(nuevo, "replace"))


def pedir_dic(d, quien):
    if not isinstance(d, dict):
        extra = " (un registro no tiene claves: sus campos se leen con punto)" if es_registro(d) else ""
        raise error(f"{quien}() necesita un diccionario, y recibió {tipo_de(d)}{extra}")
    return d


def keys(d):
    return copiar(list(pedir_dic(d, "keys").keys()))


def values(d):
    return copiar(list(pedir_dic(d, "values").values()))


def count(lista, que):
    lista = pedir_lista(lista, "count")
    if es_funcion(que):
        return sum(1 for x in lista if verdad(llamar(que, [x], [], None)))
    return sum(1 for x in lista if x == que)


def roll(desde, hasta):
    if not all(isinstance(x, int) and not isinstance(x, bool) for x in (desde, hasta)):
        raise error("roll() necesita dos números enteros:  roll(1, 6)")
    if desde > hasta:
        raise error(f"roll({desde}, {hasta}): el primero tiene que ser menor o igual que el segundo")
    return random.randint(desde, hasta)


def pick(lista):
    if not pedir_lista(lista, "pick"):
        raise error("pick(): la lista está vacía")
    return copiar(random.choice(lista))


def read_num(aviso=""):
    """Como read, pero insiste hasta recibir un número."""
    while True:
        respuesta = read(aviso).strip()
        try:
            return int(respuesta)
        except ValueError:
            try:
                return float(respuesta)
            except ValueError:
                print(f"«{respuesta}» no es un número. Prueba otra vez.")


CARPETA_DEL_PROGRAMA = ["."]


def load(ruta):
    """Carga un archivo de texto."""
    try:
        with open(os.path.join(CARPETA_DEL_PROGRAMA[0], pedir_texto(ruta, "load")), encoding="utf-8") as f:
            return f.read()
    except OSError:
        raise error(f"load(): no se pudo cargar «{ruta}»") from None


def save(ruta, texto):
    """Guarda un texto en un archivo."""
    try:
        with open(os.path.join(CARPETA_DEL_PROGRAMA[0], pedir_texto(ruta, "save")), "w", encoding="utf-8") as f:
            f.write(mostrar(texto))
    except OSError:
        raise error(f"save(): no se pudo guardar «{ruta}»") from None


INTEGRADAS = {
    "show": show, "read": read, "len": len_, "add": add, "drop": drop, "sorted": sorted_, "reversed": reversed_,
    "filter": filter_, "map": map_, "reduce": reduce, "first": first, "last": last,
    "min": min_, "max": max_, "sum": sum_, "abs": abs_, "round": round_,
    "int": int_, "float": float_, "str": str_, "bool": bool_,
    "upper": upper, "lower": lower, "strip": strip, "split": split, "join": join, "replace": replace,
    "keys": keys, "values": values, "load": load, "save": save,
    "count": count, "roll": roll, "pick": pick, "read_num": read_num,
}

GLOBAL = entorno(None, ".")
GLOBAL["vars"].update(INTEGRADAS)


# ================================================================ 5. programa

def ejecutar_texto(fuente, carpeta="."):
    """Ejecuta un programa. Devuelve None si salió bien, o (mensaje, línea) si hubo un error."""
    CARPETA_DEL_PROGRAMA[0] = carpeta
    MODULOS.clear()
    env = entorno(GLOBAL, carpeta)
    try:
        ejecutar_programa(programa(fuente), env)
        principal = env["vars"].get("main")
        if es_funcion(principal):                     # main corre al ejecutar el archivo (no al usarlo con use)
            if principal[1]["params"]:
                raise error("main no recibe datos:  fx main():")
            llamar(principal, [], [], None)
    except Exception as ex:
        if ex.args == ("cupcake-stop",):
            return None
        if es_error_cupcake(ex):
            return ex.args[1], ex.args[2]
        if isinstance(ex, RecursionError):
            return "una función se llamó a sí misma demasiadas veces (¿falta una condición para parar?)", None
        raise
    except KeyboardInterrupt:
        return "detenido con Ctrl+C", None
    return None


def informar(nombre_archivo, fuente, resultado):
    mensaje, linea = resultado
    lineas = fuente.split("\n")
    print(f"\nError en {nombre_archivo}" + (f", línea {linea}:" if linea else ":"), file=sys.stderr)
    if linea and 1 <= linea <= len(lineas):
        print(f"    {lineas[linea - 1].strip()}", file=sys.stderr)
    print(f"  {mensaje}", file=sys.stderr)


def consola():
    print("Cupcake: escribe código y pulsa Enter. Para salir: Ctrl+D")
    env = entorno(GLOBAL, ".")
    pendiente = ""
    while True:
        try:
            linea = input("... " if pendiente else ">>> ")
        except EOFError:
            print()
            return
        pendiente += linea + "\n"
        abierto = pendiente.count("[") > pendiente.count("]") or pendiente.count("(") > pendiente.count(")")
        con_bloque = any(l.split("#")[0].rstrip().endswith(":") for l in pendiente.split("\n"))
        if abierto or (con_bloque and linea.strip()):       # un bloque termina con una línea vacía
            continue
        fuente, pendiente = pendiente, ""
        try:
            sentencias = programa(fuente)
            if len(sentencias) == 1 and sentencias[0]["t"] == "expr":
                v = evaluar(sentencias[0]["expr"], env)
                if v is not None:
                    print(mostrar(v, True))
            else:
                ejecutar_programa(sentencias, env)
        except Exception as ex:
            if ex.args == ("cupcake-stop",):
                return
            if not es_error_cupcake(ex):
                raise
            print(f"Error: {ex.args[1]}")


def main(argv):
    if len(argv) < 2:
        consola()
        return 0
    ruta = argv[1]
    if not ruta.endswith(".cup") and not os.path.exists(ruta) and os.path.exists(ruta + ".cup"):
        ruta += ".cup"
    try:
        fuente = open(ruta, encoding="utf-8").read()
    except OSError:
        print(f"No encuentro el archivo «{ruta}».", file=sys.stderr)
        return 1
    resultado = ejecutar_texto(fuente, os.path.dirname(os.path.abspath(ruta)))
    if resultado is not None:
        informar(os.path.basename(ruta), fuente, resultado)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
