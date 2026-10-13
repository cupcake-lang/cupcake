"""
Pruebas de Cupcake: cada caso es un programa y lo que debe mostrar (o el error que debe dar).

    python3 pruebas.py
"""
import contextlib
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cupcake  # noqa: E402

# (nombre, código, entrada para read, salida esperada)   — o  ("error", fragmento del mensaje)
CASOS = [
("hola", 'show("Hola, mundo")', "", "Hola, mundo\n"),
("variables y textos con valores", '''
nombre = "Ash"
edad = 10
show("{nombre} tiene {edad} años")
show("El año que viene tendrá {edad + 1}")
''', "", "Ash tiene 10 años\nEl año que viene tendrá 11\n"),
("llave escapada", r'show("usa \{ para abrir")', "", "usa { para abrir\n"),
("texto de varias líneas", '''
nombre = "Misty"
show("""Hola, {nombre}.
Bienvenida.""")
''', "", "Hola, Misty.\nBienvenida.\n"),
("true false none", '''
show(true, false, none)
ganador = none
show(ganador == none)
''', "", "true false none\ntrue\n"),
("if else if else", """
fx nivel(edad):
    if edad >= 10:
        return "entrenador"
    else if edad > 5:
        return "casi"
    else:
        return "todavía no"
show(nivel(12), nivel(7), nivel(3))
""", "", "entrenador casi todavía no\n"),
("else en la línea siguiente", """
listo = false
if listo:
    show("Vamos")
else:
    show("Espera")
""", "", "Espera\n"),
("bloque con líneas vacías y notas", """
if true:

    # una nota dentro del bloque
    show("ok")
""", "", "ok\n"),
("llaves dan un aviso", 'if true {\n    show(1)\n}', "", ("error", "Cupcake no usa llaves para los bloques")),
("falta dos puntos", 'if true\n    show(1)', "", ("error", "falta «:»")),
("sangría de más", 'show(1)\n    show(2)', "", ("error", "sangría de más")),
("bloque vacío con none", 'if true:\n    none\nfx nada():\n    return none\nshow(nada())', "", "none\n"),
("while, break y continue", """
i = 0
while true:
    i = i + 1
    if i == 2:
        continue
    if i > 4:
        break
    show(i)
""", "", "1\n3\n4\n"),
("rangos incluyen el último", """
for i in 1..4:
    show(i)
show(1..3)
""", "", "1\n2\n3\n4\n[1, 2, 3]\n"),
("cortar listas", '''
equipo = ["Pikachu", "Charmander", "Squirtle", "Bulbasaur", "Eevee"]
show(equipo[0], equipo[-1])
show(equipo[1..3])
show(equipo[2..])
show(equipo[..1])
show(equipo[-2..])
''', "", 'Pikachu Eevee\n["Charmander", "Squirtle", "Bulbasaur"]\n["Squirtle", "Bulbasaur", "Eevee"]\n'
         '["Pikachu", "Charmander"]\n["Bulbasaur", "Eevee"]\n'),
("diccionarios", """
precios = ["pokeball": 200, "pocion": 300]
precios["superball"] = 600
show(precios["pocion"], len(precios))
show(keys(precios))
vacio = [:]
show(vacio, "pokeball" in precios)
medallas = [1: "Roca", 2: "Cascada"]
show(medallas[2])
""", "", '300 3\n["pokeball", "pocion", "superball"]\n[:] true\nCascada\n'),
("listas de comprensión", """
show([i * 2 for i in 1..5])
equipo = [(nombre: "Pikachu", vida: 12), (nombre: "Squirtle", vida: 0)]
show([p.nombre for p in equipo if p.vida > 0])
show([p.nombre: p.vida for p in equipo])
""", "", '[2, 4, 6, 8, 10]\n["Pikachu"]\n["Pikachu": 12, "Squirtle": 0]\n'),
("registros", '''
pika = (nombre: "Pikachu", tipo: "eléctrico", vida: 35)
show(pika.nombre)
pika.vida = 30
show(pika)
''', "", 'Pikachu\n(nombre: "Pikachu", tipo: "eléctrico", vida: 30)\n'),
("registro en varias líneas", '''
pika = (
    nombre: "Pikachu",
    vida: 35
)
show(pika.vida)
''', "", "35\n"),
("registro no gana campos", '''
pika = (nombre: "Pikachu", vida: 35)
pika.vdia = 10
''', "", ("error", "no tiene el campo «vdia». ¿Quisiste decir «vida»?")),
("registro: leer campo inexistente", '''
pika = (nombre: "Pikachu", vida: 35)
show(pika.nombr)
''', "", ("error", "¿Quisiste decir «nombre»?")),
("función como molde", """
fx pokemon(nombre, tipo, vida = 35):
    return (nombre: nombre, tipo: tipo, vida: vida)
pika = pokemon("Pikachu", "eléctrico")
charm = pokemon("Charmander", "fuego", vida = 39)
show(pika.vida, charm.vida)
""", "", "35 39\n"),
("los datos se copian", '''
a = [1, 2]
b = a
b = add(b, 3)
b[0] = 99
show(a, b)
pika = (nombre: "Pikachu", vida: 35)
copia = pika
copia.vida = 10
show(pika.vida, copia.vida)
''', "", "[1, 2] [99, 2, 3]\n35 10\n"),
("una función no cambia lo de afuera", """
fx curar(p, cantidad):
    p.vida = p.vida + cantidad
    return p
pika = (nombre: "Pikachu", vida: 10)
curar(pika, 5)
show(pika.vida)
pika = curar(pika, 5)
show(pika.vida)
""", "", "10\n15\n"),
("funciones anónimas: fx(…) { }, λ e it", """
equipo = [(nombre: "Squirtle", vida: 0), (nombre: "Pikachu", vida: 12), (nombre: "Charmander", vida: 39)]
vivos = filter(equipo, fx(p): p.vida > 0)
show([p.nombre for p in sorted(vivos, λ(p): p.nombre)])
sumar = fx(a, b): a + b
show(sumar(2, 3))
show(map([1, 2, 3], fx: it * 10))
show(reduce([1, 2, 3, 4], fx(a, b): a + b, 0))
""", "", '["Charmander", "Pikachu"]\n5\n[10, 20, 30]\n10\n'),
("devolver un registro", """
fx dividir_con_resto(a, b):
    return (cociente: a // b, resto: a % b)
r = dividir_con_resto(17, 5)
show(r.cociente, r.resto)
""", "", "3 2\n"),
("funciones integradas de listas", '''
equipo = ["Pikachu", "Charmander"]
equipo = add(equipo, "Eevee")
equipo = drop(equipo, "Charmander")
show(equipo, len(equipo), first(equipo), last(equipo))
show(sorted([3, 1, 2]), reversed([1, 2, 3]))
show(sum([1, 2, 3]), min(4, 2, 8), max([4, 2, 8]))
''', "", '["Pikachu", "Eevee"] 2 Pikachu Eevee\n[1, 2, 3] [3, 2, 1]\n6 2 8\n'),
("funciones integradas de textos", '''
show(upper("hola"), lower("HOLA"), strip("  x  "))
show(split("a,b,c", ","), join(["a", "b"], "-"), replace("gato", "g", "p"))
show(int("42") + 1, float("1.5"), str(10) + "!")
''', "", 'HOLA hola x\n["a", "b", "c"] a-b gato\n43 1.5 10!\n'.replace("gato", "pato")),
("try, except, finally", """
try:
    edad = int("abc")
except error:
    show("Falló: {error}")
finally:
    show("Listo")
""", "", "Falló: «abc» no es un número entero\nListo\n"),
("raise atrapado", """
fx validar(edad):
    if edad < 0:
        raise "La edad no puede ser negativa"
    return edad
try:
    validar(-1)
except e:
    show(e)
""", "", "La edad no puede ser negativa\n"),
("assert con valores", """
fx curar(p, cantidad):
    assert cantidad > 0
    return p
curar((vida: 1), -5)
""", "", ("error", "assert falló: cantidad > 0\n  cantidad vale -5")),
("assert con mensaje", '''
vida = -3
assert vida >= 0, "la vida no puede ser negativa"
''', "", ("error", "la vida no puede ser negativa")),
("read", '''
nombre = read("¿Nombre? ")
edad = int(read("¿Edad? "))
show("Hola, {nombre}. El año que viene tendrás {edad + 1}.")
''', "Ash\n10\n", "¿Nombre? Ash\n¿Edad? 10\nHola, Ash. El año que viene tendrás 11.\n"),
("in y not in", '''
equipo = ["Pikachu", "Eevee"]
show("Pikachu" in equipo, "Mew" not in equipo, "chu" in "Pikachu")
''', "", "true true true\n"),
("funciones en cualquier orden", """
show(doble(21))
fx doble(x):
    return x * 2
""", "", "42\n"),
("recursión", """
fx factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
show(factorial(10))
""", "", "3628800\n"),
("+=", '''
x = 5
x += 3
show(x)
''', "", "8\n"),
# -- errores amables
("método: append", 'equipo = ["a"]\nequipo.append("b")', "",
 ("error", "Cupcake no tiene métodos: «.append(…)» no existe. Escribe:  equipo = add(equipo, \"b\")")),
("método: upper", 'nombre = "ash"\nshow(nombre.upper())', "", ("error", "Escribe:  upper(nombre)")),
("palabra de Python: def", "def saludar(x): none", "", ("error", "«def» no es una palabra de Cupcake. Se escribe «fx».")),
("palabra de Python: print", 'print("hola")', "", ("error", "«print» no es una palabra de Cupcake. Se escribe «show».")),
("palabra de Python: True", "x = True", "", ("error", "«True» no es una palabra de Cupcake. Se escribe «true».")),
("nombre mal escrito", 'equipo = []\nshow(equipoo)', "", ("error", "«equipoo» no existe. ¿Quisiste decir «equipo»?")),
("sumar texto y número", 'show("Edad: " + 10)', "", ("error", "no se puede sumar un texto y un número")),
("dividir entre cero", "show(1 / 0)", "", ("error", "no se puede dividir entre cero")),
("posición que no existe", 'l = [1, 2]\nshow(l[5])', "", ("error", "la lista tiene 2 elementos (de 0 a 1); la posición 5 no existe")),
("diccionario con punto", 'd = ["a": 1]\nshow(d.a)', "", ("error", 'un diccionario se lee con corchetes:  dic["a"]')),
("registro con comillas", 'r = ("nombre": "x")', "", ("error", "en un registro, los campos van sin comillas")),
("registro con llaves (forma vieja)", 'r = {nombre: "x"}', "", ("error", "Un registro se escribe con paréntesis")),
("paréntesis que agrupan siguen funcionando", 'show((2 + 3) * 4)', "", "20\n"),
("falta cerrar texto", 'show("hola)', "", ("error", "falta cerrar las comillas")),
("sangría que no coincide", 'if true:\n    show(1)\n  show(2)\n', "", ("error", "no coincide con la de ninguna línea")),
("parámetro con nombre equivocado", 'fx f(nombre):\n    return none\nf(nombr = "x")', "", ("error", "¿Quisiste decir «nombre»?")),
("int de un texto que no es número", 'int("hola")', "", ("error", "«hola» no es un número entero")),
("return fuera de función", "return 5", "", ("error", "«return» solo tiene sentido dentro de una función")),
# -- lo nuevo
("fx con una línea devuelve su valor", """
fx doble(x):
    return x * 2
show(doble(21))
""", "", "42\n"),
("fx { it }", """
equipo = [(nombre: "Pikachu", vida: 12), (nombre: "Squirtle", vida: 0)]
show(count(equipo, fx: it.vida > 0))
show(count([1, 2, 2, 3], 2))
""", "", "1\n2\n"),
("has y has not", """
equipo = ["Pikachu", "Eevee"]
show("Pikachu" in equipo, "Mew" not in equipo, "chu" in "Pikachu")
precios = ["pokeball": 200]
show("pokeball" in precios, "pocion" not in precios)
""", "", "true true true\ntrue true\n"),
("repeat", """
repeat 3:
    show("¡Hurra!")
""", "", "¡Hurra!\n¡Hurra!\n¡Hurra!\n"),
("until", """
zapatos = 0
while zapatos != 3:
    zapatos += 1
show(zapatos)
""", "", "3\n"),
("unless con other", """
lluvia = true
if not lluvia:
    show("Al parque")
else:
    show("A casa")
""", "", "A casa\n"),
("is: tipos y vacío", """
show(5 is number, "a" is text, [] is empty, [1] is not empty, none is none, (a: 1) is record)
equipo = []
if equipo is empty:
    show("No tienes Pokémon")
""", "", "true true true true true true\nNo tienes Pokémon\n"),
("if que da un valor", """
vida = 0
if vida > 0:
    estado = "vivo"
else:
    estado = "debilitado"
show(estado)
if 5 > 3:
    show("sí")
else if 5 > 1:
    show("casi")
else:
    show("no")
""", "", "debilitado\nsí\n"),
("if no da un valor", 'x = if true:\n    1', "", ("error", "«if» no da un valor")),
("when no da un valor", 'x = when 1:\n    is 1:\n        2', "", ("error", "«when» no da un valor")),
("when con is, in y other", """
fx etapa(edad):
    when edad:
        in 0..9:
            return "niño"
        in 10..17:
            return "adolescente"
        else:
            return "adulto"
show(etapa(5), etapa(12), etapa(40))
color = "rojo"
when color:
    is "rojo":
        show("¡Como la cereza de Cupi!")
    in ["naranja", "amarillo"]:
        show("Cálido")
    else:
        show("Otro")
when 3.5:
    is text:
        show("texto")
    is number:
        show("número")
""", "", "niño adolescente adulto\n¡Como la cereza de Cupi!\nnúmero\n"),
("when con varias cosas unidas con and", """
fx multiplicador(ataque, defensor):
    when ataque and defensor:
        is "agua" and "fuego", "fuego" and "planta":
            return 2
        is "fuego" and "agua":
            return 0.5
        else:
            return 1
show(multiplicador("agua", "fuego"), multiplicador("fuego", "planta"), multiplicador("fuego", "agua"), multiplicador("agua", "agua"))
x = 3
when x and "hola":
    is text and text:
        show("mal")
    is number and text:
        show("número y texto")
when x and x * 2:
    in 0..2 and 0..9:
        show("mal")
    in 0..5 and 6..10:
        show("chico y mediano")
when x > 1 and x:
    is true and 3:
        show("bien")
    else:
        show("mal")
""", "", "2 2 0.5 1\nnúmero y texto\nchico y mediano\nbien\n"),
("when con and: falta un valor", """
when 1 and 2:
    is 1:
        show(1)
""", "", ("error", "cada caso necesita 2 valores unidos con «and»")),
("in con un rango: entre los dos, también con decimales", """
edad = 12
show(edad in 10..18, edad in 13..18)
show(5.5 in 0..10, 10 in 0..10, 11 in 0..10, "a" in 0..10)
show(3 in 0..10 by 2, 4 in 0..10 by 2)
when 2.5:
    in 0..3:
        show("chico")
""", "", "true false\ntrue true false false\nfalse true\nchico\n"),
("between y comparaciones encadenadas ya no existen", 'show(5 between 1 and 9)', "", ("error", "Cupcake ya no usa «between»")),
("comparación encadenada", 'show(0 < 5 < 9)', "", ("error", "compara de a una cosa")),
("other como reserva", """
precios = ["pokeball": 200]
show(precios["mini"] else 0)
show(int("hola") else -1)
show(precios["pokeball"] else 0)
""", "", "0\n-1\n200\n"),
("rangos con by", """
show(0..10 by 2)
show(5..1 by -1)
""", "", "[0, 2, 4, 6, 8, 10]\n[5, 4, 3, 2, 1]\n"),
("for at", """
for i, p at ["a", "b"]:
    show(i, p)
for i at "xy":
    show(i)
show(["{i}{x}" for i, x at ["a", "b"]], [x for x in [1, 2, 3] if x > 1])
""", "", "0 a\n1 b\n0\n1\n[\"0a\", \"1b\"] [2, 3]\n"),
("for: la posición va primero", 'for x in [1] at i:\n    none', "", ("error", "la posición va primero")),
("for: dos nombres con in", 'for i, x in [1]:\n    none', "", ("error", "con dos nombres se usa at")),
("stop", """
show("antes")
stop
show("después")
""", "", "antes\n"),
("roll y pick", """
d = roll(1, 6)
show(d in 1..6, pick(["x"]))
""", "", "true x\n"),
("read_number vuelve a preguntar", """
edad = read_num("¿Edad? ")
show(edad + 1)
""", "nueve\n9\n", "¿Edad? nueve\n«nueve» no es un número. Prueba otra vez.\n¿Edad? 9\n10\n"),
("return dentro de if y when", """
fx mult(a, d):
    when a:
        is "agua":
            if d == "fuego":
                return 2
            return 1
        else:
            return 1
fx signo(x):
    if x > 0:
        return "positivo"
    else if x < 0:
        return "negativo"
    return "cero"
show(mult("agua", "fuego"), mult("agua", "planta"), signo(-3), signo(0))
""", "", "2 1 negativo cero\n"),
("una función sin return devuelve none", 'fx f():\n    show("hola")\nshow(f())', "", "hola\nnone\n"),
("falta return", 'fx doble(x):\n    x * 2', "", ("error", "Para que la función lo devuelva, escribe return")),
("bloque en la misma línea", 'if true: show(1)', "", ("error", "va en la línea de abajo")),
("caso de when en la misma línea", 'when 1:\n    is 1: show(1)', "", ("error", "va en la línea de abajo")),
("fx sin nombre en una línea da su valor", 'show(map([1, 2], fx: it * 10), map([1, 2], fx(n): n + 1))', "", "[10, 20] [2, 3]\n"),
("fx sin nombre con bloque usa return", 'f = fx(n):\n    return n * 3\nshow(f(2))', "", "6\n"),
("palabras viejas", 'if true:\n    none\nother:\n    none', "", ("error", "Cupcake ya no usa «other»")),
("other como reserva vieja", 'x = int("a") other 0', "", ("error", "Cupcake ya no usa «other»")),
("unless", 'unless true:\n    none', "", ("error", "Cupcake ya no usa «unless»")),
("until", 'until true:\n    none', "", ("error", "Cupcake ya no usa «until»")),
("each", 'for each p in [1]:\n    none', "", ("error", "Cupcake ya no usa «each»")),
("then", 'if true then\n    none', "", ("error", "Cupcake ya no usa «then»")),
("else suelto", "else:\n    show(1)", "", ("error", "este «else» no tiene un «if» antes")),
("other en when", "when 1:\n    is 1:\n        none\n    other:\n        none", "", ("error", "el último caso se escribe «else:»")),
("is con un valor fuera del when", 'c = "rojo"\nshow(c is "rojo")', "", ("error", "Para comparar valores se usa ==")),
("has: campos de un registro", """
pika = (nombre: "Pikachu", vida: 35, dormido: false, nivel: 0)
show(pika has vida, pika has dormido, pika has nivel, pika has edad, pika has not dormido)
eevee = (piedra: true, amistad: 220, nivel: 0)
show(eevee has piedra and amistad, eevee has piedra and nivel, eevee has nivel or amistad)
rival = (vida: 0)
show(pika has vida and rival has vida, pika has vida or rival has vida)
if pika has vida and nivel:
    show("mal")
else:
    show("bien")
""", "", "true false false false true\ntrue false true\nfalse true\nbien\n"),
("has: ¿alguno de la lista?", """
equipo = [(nombre: "A", vida: 0), (nombre: "B", vida: 12)]
show(equipo has vida, equipo has not vida, [(vida: 0)] has vida)
""", "", "true false false\n"),
("has: errores", 'show([1, 2] has vida)', "", ("error", "esta lista tiene cosas sin campos")),
("has: después va un campo", 'show(["a"] has "a")', "", ("error", "después de «has» va el nombre de un campo")),
("has: campo mal escrito", 'p = (vida: 3)\nshow(p has vdia)', "", ("error", "¿Quisiste decir «vida»?")),
("in con registros: ¿tiene el campo?", 'p = (vida: 3)\nshow("vida" in p, "edad" in p, "edad" not in p)', "", "true false true\n"),
("registro vacío", 'x = ()', "", ("error", "un registro necesita al menos un campo")),
("no tapar funciones integradas", 'count = 3', "", ("error", "«count» ya es una función de Cupcake")),
("main corre al final", 'fx main():\n    show("en main", doble(2))\nfx doble(x):\n    return x * 2\nshow("arriba")', "", "arriba\nen main 4\n"),
("main no recibe datos", 'fx main(x):\n    none', "", ("error", "main no recibe datos")),
("palabra vieja: fn", "fn f(x): none", "", ("error", "Se escribe «fx»")),
("flecha vieja", "f = fx(x) => x", "", ("error", "Cupcake ya no usa «=>»")),
]


def correr(codigo, entrada):
    salida = io.StringIO()
    stdin_original = sys.stdin
    sys.stdin = io.StringIO(entrada)
    try:
        with contextlib.redirect_stdout(salida):
            resultado = cupcake.ejecutar_texto(codigo.strip("\n") + "\n")
    finally:
        sys.stdin = stdin_original
    return salida.getvalue(), resultado


def main():
    fallas = 0
    for nombre, codigo, entrada, esperado in CASOS:
        salida, resultado = correr(codigo, entrada)
        if isinstance(esperado, tuple):
            ok = resultado is not None and esperado[1] in resultado[0]
            obtenido = resultado[0] if resultado else f"(sin error) {salida!r}"
        else:
            ok = resultado is None and salida == esperado
            obtenido = salida if resultado is None else f"ERROR: {resultado[0]} (línea {resultado[1]})"
        if not ok:
            fallas += 1
            print(f"FALLA  {nombre}\n  esperado: {esperado!r}\n  obtenido: {obtenido!r}\n")
    print(f"{len(CASOS) - fallas} de {len(CASOS)} pruebas pasan")
    return 1 if fallas else 0


if __name__ == "__main__":
    sys.exit(main())