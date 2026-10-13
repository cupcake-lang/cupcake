"""
El contenido del curso «Aprende a programar con Cupcake».

Cada lección tiene:
  cupi:        qué está haciendo Cupi en el dibujo
  bocadillo:   lo que dice Cupi
  historia:    para empezar, una situación
  explicacion: la idea, con ejemplos de código entre ```
  ejemplos:    código que se puede ejecutar
  ejercicios:  para practicar, con comprobaciones automáticas
  recuerda:    lo más importante, en pocas líneas

Formato de los textos: párrafos separados por una línea en blanco, listas con "- ",
`código`, **negritas** y bloques de código entre ```.
construir.py ejecuta cada ejemplo y cada solución antes de crear la página.
"""

LECCIONES = [

# ───────────────────────────────────────────────────────────── 1
{
"id": "hola", "titulo": "¡Hola! Soy Cupi",
"cupi": "saludo", "bocadillo": "¡Hola! Vamos a aprender juntos.",
"historia": """
Te presento a **Cupi**. Es un cupcake de fresa que vive en la vitrina de una pastelería. Tiene doce chispitas de colores, mucha curiosidad, y un problema que ya vas a descubrir.

Cupi te va a enseñar un lenguaje de programación que se llama como él: **Cupcake**. Pequeño, dulce y fácil de entender. Programar es escribir instrucciones para que la computadora haga cosas. Y no hace falta saber nada antes: empezamos desde cero.
""",
"explicacion": """
La primera instrucción es `show`, que significa «muestra». Lo que pongas entre los paréntesis aparece en la pantalla:

```
show("¡Hola, mundo!")
```

Las palabras van **entre comillas**. Así la computadora sabe que es un texto para mostrar tal cual.

Puedes escribir varias instrucciones, una por línea. La computadora las hace **en orden**, de arriba hacia abajo.

Y si una línea empieza con `#`, es una **nota para personas**. La computadora la ignora:

```
# Esto es una nota: la computadora no la lee
show("Esto sí se muestra")
```
""",
"ejemplos": [
{"texto": "Pulsa **Ejecutar** y mira lo que pasa:",
 "codigo": """show("¡Hola, mundo!")
show("Soy Cupi, y tengo doce chispitas")
"""},
{"texto": "Un dato curioso: se llaman *cupcakes* («pasteles de taza») porque antes se horneaban en tazas. Una de las primeras recetas apareció en un libro de cocina de **1796**.",
 "codigo": """# Datos curiosos sobre los cupcakes
show("Antes se horneaban en tazas")
show("Una de las primeras recetas es de 1796")
"""},
],
"ejercicios": [
{"enunciado": "Escribe un programa que muestre **tu nombre** en una línea y **tu animal favorito** en otra.",
 "inicial": "# Escribe aquí tu primer programa\n",
 "solucion": 'show("Me llamo Ana")\nshow("Mi animal favorito es el gato")\n',
 "checks": [
   {"tipo": "ejecuta", "texto": "El programa funciona"},
   {"tipo": "usa", "patron": r"show\(", "texto": "Usa show(…)", "pista": "Escribe show(\"tu texto\")"},
   {"tipo": "lineas", "minimo": 2, "texto": "Muestra al menos dos líneas", "pista": "Usa dos veces show(…), una en cada línea."},
 ],
 "pistas": ["Cada show(…) muestra una línea.", "El texto va entre comillas: show(\"Me llamo Ana\")"]},
],
"recuerda": [
"`show(\"texto\")` muestra algo en la pantalla.",
"Los textos van entre comillas.",
"Las instrucciones se hacen en orden, de arriba hacia abajo.",
"`#` sirve para escribir notas.",
],
},

# ───────────────────────────────────────────────────────────── 2
{
"id": "cajas", "titulo": "Cajas con nombre: las variables",
"cupi": "cajas", "bocadillo": "¡Guardo todo en cajitas con etiqueta!",
"historia": """
Cupi es muy ordenado. Todo lo que quiere recordar lo guarda en **cajas**, y a cada caja le pega una **etiqueta** con un nombre. Así, cuando necesita algo, busca la etiqueta y listo.
""",
"explicacion": """
En programación, esas cajas se llaman **variables**. Se crean así:

```
chispitas = 12
nombre = "Cupi"
```

Se lee: «guarda 12 en una caja llamada `chispitas`». El signo `=` significa **guardar**, no «es igual».

Después, usas el nombre de la caja para sacar lo que tiene:

```
show(nombre, "tiene", chispitas, "chispitas")
```

`show` puede mostrar varias cosas a la vez, separadas por comas. Las pone en la misma línea, con un espacio entre ellas.

Una caja puede guardar **números** (`12`, `3.5`) o **textos** (`"Cupi"`). Y se puede **cambiar** lo que tiene:

```
chispitas = 12
chispitas = chispitas + 2      # ahora guarda 14
```

Los nombres de las cajas van **sin espacios** y sin empezar con número: `mis_chispitas`, no `mis chispitas`.
""",
"ejemplos": [
{"texto": "Cupi guarda sus datos:",
 "codigo": """nombre = "Cupi"
chispitas = 12
color = "naranja"

show(nombre, "tiene", chispitas, "chispitas")
show("Su color favorito es el", color)
"""},
{"texto": "Le pusieron dos chispitas nuevas:",
 "codigo": """chispitas = 12
show("Antes:", chispitas)

chispitas = chispitas + 2
show("Ahora:", chispitas)
"""},
],
"ejercicios": [
{"enunciado": "Crea una variable `nombre` con tu nombre y una variable `edad` con tu edad. Después muéstralas en una línea con `show`.",
 "inicial": "# 1. Crea la variable nombre\n\n# 2. Crea la variable edad\n\n# 3. Muéstralas\n",
 "solucion": 'nombre = "Ana"\nedad = 9\nshow(nombre, "tiene", edad, "años")\n',
 "checks": [
   {"tipo": "ejecuta", "texto": "El programa funciona"},
   {"tipo": "usa", "patron": r"\bnombre\s*=", "texto": "Crea la variable nombre", "pista": "nombre = \"Ana\""},
   {"tipo": "usa", "patron": r"\bedad\s*=\s*\d", "texto": "Crea la variable edad con un número", "pista": "edad = 9 (sin comillas: es un número)"},
   {"tipo": "usa", "patron": r"show\([^)]*\bnombre\b[^)]*\bedad\b|show\([^)]*\bedad\b[^)]*\bnombre\b", "texto": "Muestra las dos con show",
    "pista": "show(nombre, \"tiene\", edad, \"años\")"},
 ],
 "pistas": ["Una variable se crea así: nombre = valor", "Para mostrar varias cosas, sepáralas con comas dentro de show(…)"]},
],
"recuerda": [
"Una variable es una caja con nombre: `chispitas = 12`.",
"`=` significa **guardar**.",
"Puede guardar números o textos, y se puede cambiar.",
],
},

# ───────────────────────────────────────────────────────────── 3
{
"id": "textos", "titulo": "Textos con valores",
"cupi": "cartel", "bocadillo": "¡Mi cartel cambia solo!",
"historia": """
Cupi hizo un cartel para la puerta de su casa: «Aquí vive Cupi, que tiene 12 chispitas». Pero cada vez que le ponen una chispita nueva, tiene que hacer el cartel otra vez. ¿Y si el cartel pudiera **cambiar solo**?
""",
"explicacion": """
Dentro de un texto puedes poner **llaves** `{ }` con el nombre de una variable. Cupcake pone su valor en ese lugar:

```
nombre = "Cupi"
chispitas = 12
show("Aquí vive {nombre}, que tiene {chispitas} chispitas")
```

Muestra: `Aquí vive Cupi, que tiene 12 chispitas`.

Entre las llaves también puedes hacer **cuentas**:

```
show("La mitad de sus chispitas son {chispitas / 2}")
```

Y si alguna vez quieres escribir una llave de verdad, pon una barra antes: `\\{`.
""",
"ejemplos": [
{"texto": "El cartel de Cupi:",
 "codigo": """nombre = "Cupi"
chispitas = 12
show("Aquí vive {nombre}, que tiene {chispitas} chispitas")
"""},
{"texto": "Con cuentas dentro de las llaves:",
 "codigo": """chispitas = 12
show("La mitad de sus chispitas son {chispitas // 2}")
show("Si le ponen 4 chispitas más, tendrá {chispitas + 4}")
"""},
],
"ejercicios": [
{"enunciado": "Cupi reparte `chispitas = 120` entre dos cupcakes. Muestra el texto `Cada cupcake recibe 60 chispitas`, calculando la mitad **dentro de las llaves**.",
 "inicial": "chispitas = 120\n\n# Muestra cuántas chispitas recibe cada cupcake\n",
 "solucion": 'chispitas = 120\nshow("Cada cupcake recibe {chispitas // 2} chispitas")\n',
 "checks": [
   {"tipo": "ejecuta", "texto": "El programa funciona"},
   {"tipo": "salida", "contiene": "Cada cupcake recibe 60 chispitas", "texto": "Muestra «Cada cupcake recibe 60 chispitas»",
    "pista": "show(\"Cada cupcake recibe {chispitas // 2} chispitas\")"},
   {"tipo": "usa", "patron": r"\{[^}]*chispitas[^}]*\}", "texto": "Calcula dentro de las llaves", "pista": "Escribe la cuenta entre llaves: {chispitas // 2}"},
 ],
 "pistas": ["Son dos cupcakes: hay que dividir entre 2.", "// divide sin decimales: 120 // 2 da 60."]},
],
"recuerda": [
"`\"Hola, {nombre}\"`: lo que va entre llaves se reemplaza por su valor.",
"Entre llaves también se pueden hacer cuentas: `{chispitas + 4}`.",
],
},

# ───────────────────────────────────────────────────────────── 4
{
"id": "cuentas", "titulo": "Cuentas y más cuentas",
"cupi": "calculadora", "bocadillo": "¿Cuántos cupcakes dijiste?",
"historia": """
Aquí está el problema de Cupi: **sus amigos son muy golosos**. Su mejor amigo, **Argos**, es un monstruito con **100 bocas**, ¡y tiene hambre en todas! Cupi quiere regalarle cupcakes: uno para cada boca. Y los cupcakes cuestan. Cupi no es muy bueno con las cuentas, pero la computadora sí.
""",
"explicacion": """
Cupcake sabe hacer cuentas:

- `+` suma y `-` resta
- `*` multiplica (es el «por»)
- `/` divide
- `//` divide **sin decimales**: `7 // 2` da `3`
- `%` es el **resto** de una división: `7 % 2` da `1`
- `**` es «elevado a»: `2 ** 3` da `8`

Como en matemáticas, primero se multiplica y se divide, y después se suma y se resta. Los **paréntesis** cambian el orden:

```
show(2 + 3 * 4)        # 14
show((2 + 3) * 4)      # 20
```
""",
"ejemplos": [
{"texto": "¿Cuánto cuestan los cupcakes para Argos?",
 "codigo": """bocas = 100
precio = 3          # cada cupcake cuesta 3 monedas

total = bocas * precio
show("Los cupcakes cuestan {total} monedas")
show("Son {bocas // 2} cajitas de a dos")
"""},
{"texto": "Las seis cuentas:",
 "codigo": """show(7 + 2, 7 - 2, 7 * 2)
show(7 / 2, 7 // 2, 7 % 2)
show(2 ** 10)
"""},
],
"ejercicios": [
{"enunciado": "Argos tiene un primo con todavía más bocas: **250**. Cada cupcake cuesta **4** monedas. Calcula el total y muéstralo (debe dar **1000**).",
 "inicial": "bocas = 250\nprecio = 4\n\n# Calcula el total y muéstralo\n",
 "solucion": 'bocas = 250\nprecio = 4\n\ntotal = bocas * precio\nshow("Total: {total} monedas")\n',
 "checks": [
   {"tipo": "ejecuta", "texto": "El programa funciona"},
   {"tipo": "salida", "contiene": "1000", "texto": "Muestra 1000", "pista": "total = bocas * precio"},
   {"tipo": "no_usa", "patron": r"1000", "texto": "Lo calcula la computadora (sin escribir 1000 a mano)",
    "pista": "Usa las variables bocas y precio: bocas * precio"},
 ],
 "pistas": ["Multiplicar se escribe con *", "total = bocas * precio, y después show(total)"]},
],
"recuerda": [
"`+ - * /` como en matemáticas; `//` divide sin decimales; `%` da el resto.",
"Los paréntesis cambian el orden de las cuentas.",
],
},

# ───────────────────────────────────────────────────────────── 5
{
"id": "preguntar", "titulo": "Leer lo que escribes",
"cupi": "pregunta", "bocadillo": "¿Y tú cuántas bocas tienes?",
"historia": """
Hasta ahora, Cupi hablaba solo. Ahora quiere **conversar**: que tú le escribas cosas, y usar lo que escribiste.
""",
"explicacion": """
`read` significa «lee». Muestra un aviso, espera a que la persona escriba algo y pulse Enter, y lo guarda:

```
nombre = read("¿Cómo te llamas? ")
show("¡Hola, {nombre}!")
```

El aviso puede ser una pregunta, pero no tiene que serlo: `read("Escribe tu nombre: ")` o `read("Pulsa Enter para seguir…")` también sirven.

Lo que escribe la persona **siempre es un texto**. Si quieres un **número**, para hacer cuentas, usa `read_num`:

```
edad = read_num("¿Cuántos años tienes? ")
show("El año que viene tendrás {edad + 1}")
```

Y si la persona escribe letras en vez de un número, `read_num` le vuelve a pedir el número, con paciencia.

En esta página, las respuestas se escriben **antes de ejecutar**, en la caja **Respuestas**, una por línea.
""",
"ejemplos": [
{"texto": "Cupi te pregunta. Las respuestas ya están escritas en la caja **Respuestas**: cámbialas y vuelve a ejecutar.",
 "entradas": "Ana\n9",
 "codigo": """nombre = read("¿Cómo te llamas? ")
edad = read_num("¿Cuántos años tienes? ")

show("¡Hola, {nombre}!")
show("El año que viene tendrás {edad + 1} años")
"""},
{"texto": "Si la respuesta no es un número, `read_num` lo vuelve a pedir. Aquí la primera respuesta es `muchas`:",
 "entradas": "muchas\n100",
 "codigo": """bocas = read_num("¿Cuántas bocas tienes? ")
show("¡{bocas} bocas! Necesitas {bocas // 2} cajitas de cupcakes")
"""},
],
"ejercicios": [
{"enunciado": "Pregunta **cuántas bocas** tiene un monstruito y muestra **cuántas cajitas** necesita (en cada cajita caben dos cupcakes). Con la respuesta `40`, debe mostrar `20`.",
 "entradas": "40",
 "inicial": "# Pregunta cuántas bocas tiene\n\n# Muestra cuántas cajitas necesita\n",
 "solucion": 'bocas = read_num("¿Cuántas bocas tienes? ")\nshow("Necesitas {bocas // 2} cajitas de cupcakes")\n',
 "checks": [
   {"tipo": "ejecuta", "texto": "El programa funciona"},
   {"tipo": "usa", "patron": r"read(_num)?\(", "texto": "Lee el número con read_num(…)", "pista": "bocas = read_num(\"¿Cuántas bocas tienes? \")"},
   {"tipo": "salida", "contiene": "20", "texto": "Con 40 bocas, muestra 20", "pista": "Las cajitas son bocas // 2"},
 ],
 "pistas": ["Para leer un número: read_num(\"aviso\")", "bocas = read_num(\"¿Cuántas bocas tienes? \")"]},
],
"recuerda": [
"`read(\"aviso\")` muestra el aviso y devuelve lo que la persona escribe, como texto.",
"`read_num(\"aviso\")` insiste hasta recibir un número.",
"Para los archivos: `load(\"archivo.txt\")` carga y `save(\"archivo.txt\", texto)` guarda.",
],
},

# ───────────────────────────────────────────────────────────── 6
{
"id": "decidir", "titulo": "Decidir: if y else",
"cupi": "caminos", "bocadillo": "¿Por dónde voy?",
"historia": """
Cupi sale a pasear y llega a un cruce: si llueve, va por el camino con techo; si no, por el parque. Los programas también toman **decisiones**.
""",
"explicacion": """
Para decidir se usa `if` («si»). La línea del `if` termina con `:` («dos puntos»), y lo que va **debajo, con sangría**, se hace **solo si** la condición es verdad:

```
if lluvia:
    show("Voy por el camino con techo")
```

La **sangría** son los espacios al principio de la línea: 4 espacios, o la tecla **Tab**. Así se ve qué está **adentro** del `if`. Cuando una línea vuelve a empezar más a la izquierda, el bloque terminó. Lo de adentro siempre va **en la línea de abajo**, con sangría, aunque sea una sola instrucción.

Con `else` («si no») decides qué hacer en el otro caso, y con `else if` puedes revisar más casos:

```
if temperatura > 30:
    show("¡Qué calor!")
else if temperatura > 15:
    show("Está agradable")
else:
    show("¡A ponerse la bufanda!")
```

Las **comparaciones** responden `true` (verdad) o `false` (mentira):

- `==` es igual, `!=` es distinto
- `<` menor, `>` mayor, `<=` menor o igual, `>=` mayor o igual
- `x in 10..20`: ¿está entre 10 y 20, contando los dos?

`==` lleva **dos** signos, porque uno solo es para guardar. Y para juntar condiciones: `and` (las dos), `or` (al menos una), `not` (lo contrario).

**Cuando hay muchos casos**, `when` los ordena como una lista. Gana el primero que se cumpla:

```
when color:
    is "rosado":
        show("¡Como Cupi!")
    is "rojo":
        show("Como su cereza")
    else:
        show("Un color nuevo")
```

Cada caso dice **qué hacer** después de `:`. El último, `else` («si no»), es para todo lo demás. Y si un caso necesita varias líneas, van debajo, con más sangría.

Y `not` da lo contrario: `if not lluvia:` se lee «si no llueve».
""",
"ejemplos": [
{"texto": "Cambia la temperatura y vuelve a ejecutar:",
 "codigo": """temperatura = 22

if temperatura > 30:
    show("¡Qué calor!")
else if temperatura > 15:
    show("Está agradable")
else:
    show("¡A ponerse la bufanda!")
"""},
{"texto": "`when` con varios casos. Con `in` se pregunta si está en un rango:",
 "codigo": """edad = 12

when edad:
    in 0..5:
        show("Pequeñito")
    in 6..12:
        show("Niño o niña")
    in 13..17:
        show("Adolescente")
    else:
        show("Adulto")

show(edad in 10..15)
"""},
],
"ejercicios": [
{"enunciado": "Cupi tiene `cupcakes = 100` y Argos tiene `bocas = 100`. Si hay un cupcake para cada boca, muestra `¡A comer!`. Si no, muestra `Faltan cupcakes`.",
 "inicial": "cupcakes = 100\nbocas = 100\n\n# Decide qué mostrar\n",
 "solucion": 'cupcakes = 100\nbocas = 100\n\nif cupcakes >= bocas:\n    show("¡A comer!")\nelse:\n    show("Faltan cupcakes")\n',
 "checks": [
   {"tipo": "ejecuta", "texto": "El programa funciona"},
   {"tipo": "usa", "patron": r"\bif\b", "texto": "Usa if", "pista": "if cupcakes >= bocas: …"},
   {"tipo": "usa", "patron": r"\belse\b", "texto": "Usa else para el otro caso", "pista": "else:  (a la misma altura que el if)"},
   {"tipo": "salida", "contiene": "¡A comer!", "texto": "Con 100 y 100, muestra «¡A comer!»"},
 ],
 "pistas": ["La condición es: cupcakes >= bocas", "if cupcakes >= bocas: … y debajo, else: …"]},
{"enunciado": "Con `when`, haz que según la `nota` se muestre: de 9 a 10 `¡Excelente!`, de 6 a 8 `Aprobado`, y si no, `A estudiar más`. Con `nota = 7` debe mostrar `Aprobado`.",
 "inicial": "nota = 7\n\n# Usa when para decidir\n",
 "solucion": 'nota = 7\n\nwhen nota:\n    in 9..10:\n        show("¡Excelente!")\n    in 6..8:\n        show("Aprobado")\n    else:\n        show("A estudiar más")\n',
 "checks": [
   {"tipo": "ejecuta", "texto": "El programa funciona"},
   {"tipo": "usa", "patron": r"\bwhen\b", "texto": "Usa when", "pista": "when nota:  y debajo  in 9..10:"},
   {"tipo": "salida", "contiene": "Aprobado", "texto": "Con 7, muestra «Aprobado»"},
   {"tipo": "no_salida", "contiene": "Excelente", "texto": "No muestra «¡Excelente!»"},
 ],
 "pistas": ["Cada caso: in desde..hasta:  y debajo, con sangría, show(…)", "El último caso es: else:  y debajo show(\"A estudiar más\")"]},
],
"recuerda": [
"`if condición: …` se hace solo si es verdad.",
"`else if` revisa otro caso; `else` es el resto.",
"`when valor:` y debajo los casos `is …: …`, `in …: …` y `else: …`, para muchos casos.",
"Comparar: `== != < > <= >=`, y `x in 1..10` para «entre». Juntar: `and`, `or`, `not`.",
],
},

# ───────────────────────────────────────────────────────────── 7
{
"id": "repetir", "titulo": "Repetir",
"cupi": "vueltas", "bocadillo": "¡Una chispita, otra chispita, otra…!",
"historia": """
Cupi quiere contar sus chispitas, pero son tantas que se cansa. Por suerte, a la computadora **le encanta repetir**: puede hacer lo mismo mil veces sin aburrirse.
""",
"explicacion": """
Lo más fácil: `repeat` repite algo **un número de veces**:

```
repeat 3:
    show("¡Hip, hip, hurra!")
```

`for` («para cada») repite **por cada número** de un rango, y en cada vuelta te dice cuál es. El rango `1..5` va del 1 al 5, **los dos incluidos**:

```
for i in 1..5:
    show("Chispita número {i}")
```

Con `by` puedes ir de a saltos, o hacia atrás:

```
for i in 0..10 by 2:
    show(i)        # 0, 2, 4, 6, 8, 10
for i in 3..1 by -1:
    show(i)        # 3, 2, 1
```

`while` («mientras») repite **mientras** algo sea verdad:

```
cupcakes = 0
while cupcakes != 3:
    cupcakes += 1
    show("Decoré el cupcake {cupcakes}")
```

`cupcakes += 1` es lo mismo que `cupcakes = cupcakes + 1`: «súmale uno».

Hay que tener cuidado: si la condición nunca cambia, ¡se repite para siempre! Dentro de un ciclo, `break` sale de inmediato y `continue` salta a la siguiente vuelta.
""",
"ejemplos": [
{"texto": "¡Hurra!",
 "codigo": """repeat 3:
    show("¡Hip, hip, hurra!")
"""},
{"texto": "Cupi cuenta sus primeras chispitas, y después cuenta hacia atrás para entrar al horno:",
 "codigo": """for i in 1..5:
    show("Chispita número {i}")

for i in 3..1 by -1:
    show("{i}…")
show("¡Al horno!")
"""},
{"texto": "Cupi decora cupcakes hasta tener tres:",
 "codigo": """cupcakes = 0
while cupcakes != 3:
    cupcakes += 1
    show("Decoré el cupcake {cupcakes}")
show("Listo: {cupcakes} cupcakes")
"""},
],
"ejercicios": [
{"enunciado": "Muestra la **tabla del 7**, del 1 al 10, así: `7 x 1 = 7`, `7 x 2 = 14`… hasta `7 x 10 = 70`.",
 "inicial": "# Repite del 1 al 10\n",
 "solucion": 'for i in 1..10:\n    show("7 x {i} = {7 * i}")\n',
 "checks": [
   {"tipo": "ejecuta", "texto": "El programa funciona"},
   {"tipo": "usa", "patron": r"\bfor\b|\bwhile\b", "texto": "Usa un ciclo", "pista": "for i in 1..10:"},
   {"tipo": "salida", "contiene": "7 x 1 = 7", "texto": "Empieza con 7 x 1 = 7"},
   {"tipo": "salida", "contiene": "7 x 10 = 70", "texto": "Termina con 7 x 10 = 70", "pista": "El rango 1..10 incluye el 10."},
 ],
 "pistas": ["for i in 1..10:", "Debajo, con sangría: show(\"7 x {i} = {7 * i}\")"]},
],
"recuerda": [
"`repeat 3: …` repite tres veces.",
"`for i in 1..5: …` repite con i = 1, 2, 3, 4, 5. Con `by 2`, de a dos.",
"`while` repite mientras algo sea verdad.",
"`break` sale; `continue` salta a la siguiente vuelta.",
],
},

# ───────────────────────────────────────────────────────────── 8
{
"id": "listas", "titulo": "Listas: muchas cosas en fila",
"cupi": "tren", "bocadillo": "¡Mis cupcakes van en fila!",
"historia": """
¿Te diste cuenta de que en la vitrina de la pastelería los cupcakes están **en fila**? El primero, el segundo, el tercero… uno detrás de otro. Eso, en programación, es una **lista**.
""",
"explicacion": """
Una lista guarda varias cosas en orden, entre **corchetes** `[ ]`:

```
amigos = ["Blip", "Kora", "Zum"]
```

Cada cosa tiene una **posición**, y se cuenta **desde 0**:

```
show(amigos[0])      # Blip    (el primero)
show(amigos[2])      # Zum
show(amigos[-1])     # Zum   (el último)
```

Para **cortar** un pedazo se usa `..`, como en los rangos:

```
show(amigos[0..1])   # ["Blip", "Kora"]
```

Funciones para listas:
- `len(lista)` cuenta cuántas cosas tiene;
- `add(lista, x)` agrega algo al final;
- `drop(lista, x)` quita algo;
- `count(lista, x)` cuenta cuántas veces está algo.

Y para preguntar si algo está en la lista, se usa `in`:

```
"Kora" in amigos          # ¿Kora está en la lista?
"Nova" not in amigos      # ¿Nova no está?
amigos is empty           # ¿está vacía?
```

`add` y `drop` **devuelven una lista nueva**. Por eso se guarda el resultado: `amigos = add(amigos, "Nova")`.

Y `for` sirve para recorrer una lista, uno por uno. Con `at`, también sabes la posición:

```
for i, amigo at amigos:
    show("{i}: ¡Hola, {amigo}!")
```
""",
"ejemplos": [
{"texto": "Los amigos de Cupi:",
 "codigo": """amigos = ["Blip", "Kora", "Zum"]

show(amigos[0], "va primero")
show("Tiene {len(amigos)} amigos")

amigos = add(amigos, "Nova")
show(amigos)

for amigo in amigos:
    show("¡Hola, {amigo}!")
"""},
{"texto": "Buscar y cortar:",
 "codigo": """cupcakes = ["rojo", "azul", "verde", "amarillo", "morado", "rojo"]

show("azul" in cupcakes, "negro" not in cupcakes)
show(cupcakes[1..3])
show("Hay {count(cupcakes, "rojo")} cupcakes rojos")

for i, c at cupcakes:
    show("{i}: {c}")
"""},
],
"ejercicios": [
{"enunciado": "Cupi tiene `frutas = [\"manzana\", \"pera\"]`. Agrega `\"mango\"` a la lista y muestra **cuántas frutas** hay (debe dar 3) y **cuál es la última**.",
 "inicial": 'frutas = ["manzana", "pera"]\n\n# Agrega el mango\n\n# Muestra cuántas hay y la última\n',
 "solucion": 'frutas = ["manzana", "pera"]\n\nfrutas = add(frutas, "mango")\n\nshow(len(frutas), frutas[-1])\n',
 "checks": [
   {"tipo": "ejecuta", "texto": "El programa funciona"},
   {"tipo": "usa", "patron": r"frutas\s*=\s*add\(", "texto": "Agrega con add y guarda el resultado", "pista": "frutas = add(frutas, \"mango\")"},
   {"tipo": "salida", "contiene": "3", "texto": "Muestra 3", "pista": "len(frutas)"},
   {"tipo": "salida", "contiene": "mango", "texto": "Muestra el mango, que es el último", "pista": "frutas[-1] es el último"},
 ],
 "pistas": ["frutas = add(frutas, \"mango\")", "show(len(frutas), frutas[-1])"]},
],
"recuerda": [
"Una lista va entre corchetes: `[\"a\", \"b\"]`. Se cuenta desde 0.",
"`len`, `add`, `drop`, `count`. Preguntar: `x in lista`, `x in lista`, `lista is empty`.",
"Para cortar: `lista[1..3]`. Para saber la posición: `for x in lista at i`.",
"`add` y `drop` devuelven una lista nueva: guárdala.",
],
},

# ───────────────────────────────────────────────────────────── 9
{
"id": "diccionarios", "titulo": "Diccionarios: buscar por nombre",
"cupi": "libro", "bocadillo": "Busco la palabra, y encuentro su valor.",
"historia": """
En la pastelería, cada talla de cupcake tiene un precio. Cupi no quiere recordar «la tercera de la lista»: quiere preguntar «¿cuánto cuesta la talla chica?». Para eso están los **diccionarios**.
""",
"explicacion": """
Un diccionario es como una lista, pero cada cosa tiene una **clave** en vez de una posición. Se escribe igual que una lista, agregando `clave:` delante de cada valor:

```
precios = ["chica": 3, "mediana": 5, "grande": 8]
```

Se busca por la clave:

```
show(precios["mediana"])     # 5
```

Se puede **agregar** o **cambiar** un valor:

```
precios["gigante"] = 12
precios["chica"] = 4
```

Funciones útiles:
- `keys(dic)`: las claves;
- `values(dic)`: los valores;
- `clave in dic`: ¿tiene esa clave?

Si buscas una clave que no existe, Cupcake te avisa con un error. Pero si quieres un **valor de reserva**, usa `else`:

```
precio = precios["mini"] else 0     # si no hay talla mini, 0
```

Un diccionario vacío se escribe `[:]`.
""",
"ejemplos": [
{"texto": "Los precios de la pastelería:",
 "codigo": """precios = ["chica": 3, "mediana": 5, "grande": 8]

show("La talla mediana cuesta", precios["mediana"])

precios["gigante"] = 12
show(keys(precios))
show("mini" in precios)
show(precios["mini"] else "no hay talla mini")

for talla in keys(precios):
    show("Talla {talla}: {precios[talla]} monedas")
"""},
],
"ejercicios": [
{"enunciado": "Crea un diccionario `edades` con dos amigos y sus edades (por ejemplo, Blip de 3 y Kora de 5). Después agrega a Zum, de 4, y muestra **la edad de Zum**.",
 "inicial": "# Crea el diccionario\n\n# Agrega a Zum\n\n# Muestra la edad de Zum\n",
 "solucion": 'edades = ["Blip": 3, "Kora": 5]\nedades["Zum"] = 4\nshow(edades["Zum"])\n',
 "checks": [
   {"tipo": "ejecuta", "texto": "El programa funciona"},
   {"tipo": "usa", "patron": r"\[\s*\"[^\"]+\"\s*:", "texto": "Crea un diccionario con clave: valor", "pista": "edades = [\"Blip\": 3, \"Kora\": 5]"},
   {"tipo": "usa", "patron": r"edades\[\s*\"Zum\"\s*\]\s*=", "texto": "Agrega a Zum", "pista": "edades[\"Zum\"] = 4"},
   {"tipo": "salida", "contiene": "4", "texto": "Muestra la edad de Zum"},
 ],
 "pistas": ["Un diccionario: [\"clave\": valor, …]", "edades[\"Zum\"] = 4 y después show(edades[\"Zum\"])"]},
],
"recuerda": [
"Diccionario: `[\"clave\": valor]`. Vacío: `[:]`.",
"Se busca con `dic[\"clave\"]` y se agrega con `dic[\"clave\"] = valor`.",
"`keys`, `values`, `clave in dic`. Valor de reserva: `dic[\"x\"] else 0`.",
],
},

# ───────────────────────────────────────────────────────────── 10
{
"id": "registros", "titulo": "Registros: fichas con campos",
"cupi": "ficha", "bocadillo": "¡Esta es mi ficha!",
"historia": """
Argos se inscribió en el club de pasteleros, y le dieron una **ficha**: nombre, bocas, color. Cada dato en su casilla. En Cupcake, una ficha así se llama **registro**.
""",
"explicacion": """
Un registro junta varios datos sobre **una misma cosa**, cada uno con su nombre (su **campo**). Va entre paréntesis:

```
argos = (nombre: "Argos", bocas: 100, color: "verde")
```

Cada campo se lee con un **punto**:

```
show(argos.nombre)       # Argos
show(argos.bocas)         # 100
```

Y se puede cambiar:

```
argos.bocas = 102
```

Un registro **nace con sus campos** y no se le pueden agregar otros. Si escribes mal un campo, Cupcake te avisa y te sugiere el correcto. ¡Así no se pierden datos por un error de escritura!

**¿Tiene algo en ese campo?** Con `has` («tiene») preguntas si un campo tiene algo: un número mayor que 0, un texto o una lista con algo, o `true`. Siempre responde `true` o `false`:

```
argos = (nombre: "Argos", bocas: 100, dormido: false)

if argos has bocas:
    show("¡Argos tiene hambre!")

if argos has not dormido:
    show("Y está despierto")
```

Se pueden preguntar varios campos a la vez con `and` y `or`: `argos has bocas and nombre`. Y si el campo no existe, `has` responde `false`.

**¿Diccionario o registro?**
- Un **registro** describe **una cosa**, con campos fijos: la ficha de Argos.
- Un **diccionario** es una **colección** que puede crecer: los precios de la tienda.
""",
"ejemplos": [
{"texto": "La ficha de Argos:",
 "codigo": """argos = (nombre: "Argos", bocas: 100, color: "verde")

show("{argos.nombre} es de color {argos.color}")
argos.bocas = 102
show(argos)
"""},
{"texto": "Un error de escritura. Ejecútalo y mira cómo te ayuda Cupcake:",
 "espera": "error",
 "codigo": """argos = (nombre: "Argos", bocas: 100)
argos.bocsa = 102
"""},
{"texto": "Una lista de registros:",
 "codigo": """club = [
    (nombre: "Argos", bocas: 100),
    (nombre: "Blip", bocas: 6),
    (nombre: "Kora", bocas: 8),
]

for socio in club:
    show("{socio.nombre} come con {socio.bocas} bocas")
"""},
{"texto": "`has` en un juego: ¿quién sigue en pie? Con una lista, `has` pregunta si **alguno** tiene ese campo:",
 "codigo": """cupi = (nombre: "Cupi", energia: 3, escudo: false)
rival = (nombre: "Glub", energia: 0, escudo: true)

if cupi has energia and rival has not energia:
    show("¡{cupi.nombre} ganó la carrera!")

if rival has escudo:
    show("{rival.nombre} tiene escudo")

equipo = [cupi, rival]
if equipo has energia:
    show("Alguien del equipo todavía puede jugar")
"""},
],
"ejercicios": [
{"enunciado": "Crea un registro `mascota` con los campos `nombre`, `animal` y `edad`. Después **cumple años**: súmale 1 a su edad y muestra el registro.",
 "inicial": "# Crea el registro mascota\n\n# Súmale 1 a la edad\n\n# Muéstralo\n",
 "solucion": 'mascota = (nombre: "Luna", animal: "gata", edad: 3)\nmascota.edad = mascota.edad + 1\nshow(mascota)\n',
 "checks": [
   {"tipo": "ejecuta", "texto": "El programa funciona"},
   {"tipo": "usa", "patron": r"\(\s*nombre\s*:", "texto": "Crea un registro con el campo nombre", "pista": "mascota = (nombre: \"Luna\", animal: \"gata\", edad: 3)"},
   {"tipo": "usa", "patron": r"mascota\.edad\s*=", "texto": "Cambia la edad con un punto", "pista": "mascota.edad = mascota.edad + 1"},
   {"tipo": "salida", "contiene": "edad:", "texto": "Muestra el registro", "pista": "show(mascota)"},
 ],
 "pistas": ["Un registro: (campo: valor, campo: valor)", "mascota.edad = mascota.edad + 1"]},
],
"recuerda": [
"Registro: `(nombre: \"Argos\", bocas: 100)`.",
"Se lee y se cambia con punto: `argos.bocas`.",
"`argos has bocas` pregunta si ese campo tiene algo; responde `true` o `false`.",
"No gana campos nuevos: así se atrapan los errores de escritura.",
],
},

# ───────────────────────────────────────────────────────────── 11
{
"id": "funciones", "titulo": "Funciones: tus propias instrucciones",
"cupi": "herramienta", "bocadillo": "¡Fabriqué mi propia herramienta!",
"historia": """
Cupi se cansó de calcular cada vez cuántas cajitas necesita un amigo. Así que inventó su propia instrucción: le dice cuántas bocas tiene alguien, y ella responde cuántas cajitas necesita. Eso es una **función**.
""",
"explicacion": """
Una función es una instrucción **que inventas tú**. Se crea con `fx`, como la f(x) de matemáticas:

```
fx cajitas(bocas):
    return bocas // 2
```

- `cajitas` es su nombre;
- `bocas`, entre paréntesis, es el dato que **recibe**;
- `return` dice qué **devuelve**.

Y se usa como cualquier otra instrucción:

```
show(cajitas(100))     # 50
show(cajitas(6))       # 3
```

Sin `return`, la función hace lo que dice pero no devuelve nada (devuelve `none`). Si escribes una línea que solo calcula algo, como `bocas // 2`, Cupcake te avisa que falta el `return`.

Una función puede recibir varios datos, y algunos pueden tener un **valor por defecto**:

```
fx saludar(nombre, saludo = "Hola"):
    show("{saludo}, {nombre}")

saludar("Cupi")                      # Hola, Cupi
saludar("Blip", saludo = "Buenas")   # Buenas, Blip
```

Las funciones también sirven de **molde** para crear registros iguales:

```
fx amigo(nombre, bocas):
    return (nombre: nombre, bocas: bocas)
```
""",
"ejemplos": [
{"texto": "La herramienta de Cupi:",
 "codigo": """fx cajitas(bocas):
    return bocas // 2

show("Argos necesita", cajitas(100), "cajitas")
show("Blip necesita", cajitas(6), "cajitas")
"""},
{"texto": "Saludos con valor por defecto:",
 "codigo": """fx saludar(nombre, saludo = "Hola"):
    show("{saludo}, {nombre}")

saludar("Cupi")
saludar("Blip", saludo = "Buenas")
"""},
],
"ejercicios": [
{"enunciado": "Crea una función `costo(bocas, precio)` que devuelva cuánto cuestan los cupcakes (bocas × precio). Úsala para mostrar el costo de **100 bocas a 3 monedas** (debe dar 300).",
 "inicial": "# Crea la función costo\n\n# Úsala y muestra el resultado\n",
 "solucion": 'fx costo(bocas, precio):\n    return bocas * precio\n\nshow(costo(100, 3))\n',
 "checks": [
   {"tipo": "ejecuta", "texto": "El programa funciona"},
   {"tipo": "usa", "patron": r"fx\s+costo\s*\(", "texto": "Crea la función costo", "pista": "fx costo(bocas, precio): …"},
   {"tipo": "salida", "contiene": "300", "texto": "Muestra 300", "pista": "show(costo(100, 3))"},
 ],
 "pistas": ["fx costo(bocas, precio):  y debajo  return bocas * precio", "Para usarla: show(costo(100, 3))"]},
],
"recuerda": [
"`fx nombre(datos): …` crea una función.",
"`return` devuelve el resultado. Sin `return`, la función no devuelve nada.",
"Los datos pueden tener valor por defecto: `saludo = \"Hola\"`.",
],
},

# ───────────────────────────────────────────────────────────── 12
{
"id": "copias", "titulo": "Los datos se copian",
"cupi": "fotocopia", "bocadillo": "¡Hay dos Cupis! Bueno, uno es una copia.",
"historia": """
Cupi le prestó su ficha a Blip para que viera cómo llenarla. Blip tachó cosas, dibujó, escribió encima… ¡pero la ficha de Cupi quedó perfecta! ¿Por qué? Porque Cupi le dio una **fotocopia**.
""",
"explicacion": """
En Cupcake, cuando guardas algo en otra variable, o se lo pasas a una función, se hace una **copia**. Cada nombre tiene **su propio dato**:

```
a = [1, 2]
b = a
b = add(b, 3)
show(a)      # [1, 2]       ← a no cambió
show(b)      # [1, 2, 3]
```

Esto evita sorpresas: nada cambia «a escondidas». (En otros lenguajes, como Python, `a` también habría cambiado, y eso confunde mucho.)

Por eso, si una función **cambia** algo, tiene que **devolverlo**, y tú decides guardarlo:

```
fx decorar(c):
    c.chispitas = c.chispitas + 2
    return c

cupi = decorar(cupi)       # ← se guarda lo que devolvió
```

Si olvidas guardar el resultado, el cambio se queda en la copia y se pierde.
""",
"ejemplos": [
{"texto": "Las fotocopias:",
 "codigo": """cupi = (nombre: "Cupi", chispitas: 12)
copia = cupi
copia.chispitas = 4

show(cupi.chispitas)      # el original no cambió
show(copia.chispitas)
"""},
{"texto": "Una función que cambia algo y lo devuelve:",
 "codigo": """fx decorar(c):
    c.chispitas = c.chispitas + 2
    return c

cupi = (nombre: "Cupi", chispitas: 12)
decorar(cupi)
show("Sin guardar:", cupi.chispitas)

cupi = decorar(cupi)
show("Guardando:", cupi.chispitas)
"""},
],
"ejercicios": [
{"enunciado": "Este programa debería mostrar `30`, pero muestra `10`. **Arréglalo**: el resultado de `curar` no se está guardando.",
 "inicial": 'fx curar(monstruito, cantidad):\n    monstruito.vida = monstruito.vida + cantidad\n    return monstruito\n\nkora = (nombre: "Kora", vida: 10)\ncurar(kora, 20)\nshow(kora.vida)\n',
 "solucion": 'fx curar(monstruito, cantidad):\n    monstruito.vida = monstruito.vida + cantidad\n    return monstruito\n\nkora = (nombre: "Kora", vida: 10)\nkora = curar(kora, 20)\nshow(kora.vida)\n',
 "checks": [
   {"tipo": "ejecuta", "texto": "El programa funciona"},
   {"tipo": "usa", "patron": r"kora\s*=\s*curar\(", "texto": "Guarda lo que devuelve curar", "pista": "kora = curar(kora, 20)"},
   {"tipo": "salida", "contiene": "30", "texto": "Muestra 30"},
 ],
 "pistas": ["curar devuelve el monstruito curado, pero nadie lo guarda.", "Cambia la línea por: kora = curar(kora, 20)"]},
],
"recuerda": [
"Asignar o pasar un dato hace una **copia**.",
"Una función que cambia algo lo devuelve: `x = cambiar(x)`.",
],
},

# ───────────────────────────────────────────────────────────── 13
{
"id": "atajos", "titulo": "Atajos: funciones sin nombre y listas rápidas",
"cupi": "lupa", "bocadillo": "Solo quiero los cupcakes rojos…",
"historia": """
Cupi tiene una montaña de cupcakes de colores y quiere **solo los rojos**, u **ordenarlos por tamaño**. Podría revisarlos uno por uno con un `for`… o usar algunos atajos geniales.
""",
"explicacion": """
**Listas rápidas.** Puedes crear una lista nueva a partir de otra en una sola línea:

```
dobles = [n * 2 for n in 1..5]               # [2, 4, 6, 8, 10]
pares = [n for n in 1..10 if n % 2 == 0]     # [2, 4, 6, 8, 10]
```

Se lee: «`n * 2`, por cada `n` del 1 al 5». Y con `if` al final, solo los que cumplen la condición.

**Funciones sin nombre.** A veces necesitas una función pequeña, para usarla una sola vez. Se escribe con `fx`, pero **sin nombre**:

```
fx(c): c.talla
```

Se lee: «dado un `c`, devuelve `c.talla`». Sirve, por ejemplo, para decirle a `sorted` **por qué** ordenar:

```
ordenados = sorted(cupcakes, fx(c): c.talla)
```

Y si recibe un solo dato, ni siquiera hace falta ponerle nombre: se llama `it` («eso»):

```
ordenados = sorted(cupcakes, fx: it.talla)
```

`λ` (la letra griega lambda) es lo mismo que `fx`, por si te gusta más: `λ(c): c.talla`.

Otras funciones que aceptan una función sin nombre:
- `filter(lista, fx: condición)`: se queda con los que cumplen;
- `map(lista, fx: cambio)`: cambia cada uno;
- `count(lista, fx: condición)`: cuenta cuántos cumplen.
""",
"ejemplos": [
{"texto": "Listas rápidas:",
 "codigo": """show([n * 2 for n in 1..5])
show([n for n in 1..10 if n % 2 == 0])

amigos = ["Blip", "Kora", "Zum"]
show([upper(a) for a in amigos])
"""},
{"texto": "Los cupcakes de Cupi:",
 "codigo": """cupcakes = [
    (color: "rojo", talla: 3),
    (color: "azul", talla: 1),
    (color: "rojo", talla: 2),
]

rojos = [c for c in cupcakes if c.color == "rojo"]
show("Rojos:", len(rojos))
show("Grandes:", count(cupcakes, fx: it.talla >= 2))

for c in sorted(cupcakes, fx: it.talla):
    show("Talla {c.talla}: {c.color}")
"""},
],
"ejercicios": [
{"enunciado": "De `numeros = [3, 8, 15, 4, 23, 42]`, crea una lista `grandes` solo con los **mayores que 10**, usando una lista rápida, y muéstrala (debe dar `[15, 23, 42]`).",
 "inicial": "numeros = [3, 8, 15, 4, 23, 42]\n\n# Crea la lista grandes\n",
 "solucion": "numeros = [3, 8, 15, 4, 23, 42]\n\ngrandes = [n for n in numeros if n > 10]\nshow(grandes)\n",
 "checks": [
   {"tipo": "ejecuta", "texto": "El programa funciona"},
   {"tipo": "usa", "patron": r"\[[^\]]*\bfor\b[^\]]*\bif\b", "texto": "Usa una lista rápida con if", "pista": "[n for n in numeros if n > 10]"},
   {"tipo": "salida", "contiene": "[15, 23, 42]", "texto": "Muestra [15, 23, 42]"},
 ],
 "pistas": ["[n for n in numeros if …]", "La condición es n > 10"]},
],
"recuerda": [
"Lista rápida: `[x * 2 for x in lista if condición]`.",
"Función sin nombre: `fx(x): …`, o `fx: it…` si recibe un solo dato.",
"`sorted(lista, fx: it.campo)` ordena por un campo.",
],
},

# ───────────────────────────────────────────────────────────── 14
{
"id": "errores", "titulo": "Errores: tus amigos que avisan",
"cupi": "curita", "bocadillo": "¡Me tropecé! Pero aprendí algo.",
"historia": """
A Cupi a veces se le cae una chispita: con tantas, ¡es normal! Lo importante es **levantarse y entender qué pasó**. Con los programas es igual: los errores no son malos. Son **avisos** que te dicen qué arreglar.
""",
"explicacion": """
Cuando algo sale mal, Cupcake se detiene y te dice **en qué línea** y **qué pasó**, y muchas veces **cómo arreglarlo**. ¡Léelo con calma! Es como un amigo que te avisa.

**Atrapar un error.** Si sabes que algo puede fallar, como cuando alguien escribe letras en lugar de un número, puedes **intentarlo** con `try` y decir qué hacer si falla con `except`:

```
try:
    edad = int(read("¿Edad? "))
except error:
    show("Eso no es un número")
    edad = 0
```

**Avisar tú.** Con `raise` puedes provocar un error a propósito, cuando algo no tiene sentido:

```
if bocas < 0:
    raise "Nadie tiene bocas negativas"
```

**Un valor de reserva.** Para casos simples, `else` dice qué usar si algo falla, en una sola línea:

```
edad = int(read("¿Edad? ")) else 0
```

**Comprobar.** `assert` revisa que algo sea verdad. Si no lo es, se detiene y te muestra los valores:

```
assert cupcakes >= 0
```
""",
"ejemplos": [
{"texto": "Un error a propósito. Ejecútalo y lee el mensaje con calma:",
 "espera": "error",
 "codigo": """bocas = 100
show("Tengo " + bocas + " bocas")
"""},
{"texto": "Atrapar el error. La respuesta ya escrita es `muchas`, que no es un número:",
 "entradas": "muchas",
 "codigo": """try:
    bocas = int(read("¿Cuántas bocas tienes? "))
    show("Necesitas {bocas // 2} cajitas")
except error:
    show("Ups: {error}")
"""},
],
"ejercicios": [
{"enunciado": "Pregunta la edad. Si la persona **no escribe un número**, en vez de detenerse, el programa debe mostrar `Eso no es un número`. La respuesta de prueba es `nueve`.",
 "entradas": "nueve",
 "inicial": 'edad = int(read("¿Cuántos años tienes? "))\nshow("Tienes {edad} años")\n',
 "solucion": 'try:\n    edad = int(read("¿Cuántos años tienes? "))\n    show("Tienes {edad} años")\nexcept error:\n    show("Eso no es un número")\n',
 "checks": [
   {"tipo": "ejecuta", "texto": "El programa no se detiene con un error", "pista": "Pon el código debajo de try:, con sangría"},
   {"tipo": "usa", "patron": r"\btry\b", "texto": "Usa try"},
   {"tipo": "salida", "contiene": "Eso no es un número", "texto": "Muestra «Eso no es un número»", "pista": "except error:  y debajo  show(\"Eso no es un número\")"},
 ],
 "pistas": ["try:  (debajo lo que puede fallar)   except error:  (debajo qué hacer)", "Mueve las dos líneas debajo de try:, con sangría."]},
],
"recuerda": [
"Los mensajes de error dicen la línea, qué pasó y, muchas veces, cómo arreglarlo.",
"`try: … except error: …` atrapa un error; `algo else reserva` es la versión corta.",
"`raise \"mensaje\"` avisa; `assert condición` comprueba.",
],
},

# ───────────────────────────────────────────────────────────── 15
{
"id": "archivos", "titulo": "Usar otros archivos",
"cupi": "mochila", "bocadillo": "En mi mochila llevo mis herramientas.",
"historia": """
Cupi ya tiene muchas herramientas: `cajitas`, `costo`, `saludar`… y quiere usarlas en todos sus programas sin escribirlas otra vez. Las guarda en un archivo aparte, como en una **mochila**, y las saca cuando las necesita.
""",
"explicacion": """
Un programa de Cupcake se guarda en un archivo que termina en `.cup`. Puedes poner tus funciones en un archivo, por ejemplo `herramientas.cup`, y usarlas desde otro con `use`:

```
use cajitas, costo from herramientas
```

Se lee: «usa `cajitas` y `costo` de `herramientas`». Después se usan normalmente: `cajitas(100)`.

Otras formas:

```
use herramientas                 # trae todo
use cajitas as mitad from herramientas    # con otro nombre
```

En esta página, el archivo `herramientas.cup` ya existe: puedes ver lo que tiene debajo de cada ejemplo.

**`main`: lo que corre al ejecutar.** Si un archivo tiene una función llamada `main`, Cupcake la ejecuta al final, **solo cuando ejecutas ese archivo**. Si otro archivo lo usa con `use`, su `main` **no** corre. Así puedes guardar pruebas en tus herramientas sin que molesten:

```
fx cajitas(bocas):
    return bocas // 2

fx main():
    show(cajitas(100))       # solo corre si ejecutas este archivo
```

`main` es opcional: un programa corto no lo necesita.
""",
"ejemplos": [
{"texto": "Cupi usa su mochila. Fíjate que `herramientas.cup` tiene un `main` con pruebas, pero no se ejecuta, porque aquí solo lo estamos usando:",
 "archivos": {"herramientas.cup": "fx cajitas(bocas):\n    return bocas // 2\n\nfx costo(bocas, precio):\n    return bocas * precio\n\nfx main():\n    show(\"Prueba:\", cajitas(10))\n"},
 "codigo": """use cajitas, costo from herramientas

show("Cajitas:", cajitas(100))
show("Costo:", costo(100, 3))
"""},
],
"ejercicios": [
{"enunciado": "El archivo `saludos.cup` tiene una función `saludar(nombre)`. Úsala para saludar a **Blip**.",
 "archivos": {"saludos.cup": 'fx saludar(nombre):\n    show("¡Hola, {nombre}! Te damos la bienvenida al club.")\n'},
 "inicial": "# Trae saludar desde saludos\n\n# Saluda a Blip\n",
 "solucion": 'use saludar from saludos\n\nsaludar("Blip")\n',
 "checks": [
   {"tipo": "ejecuta", "texto": "El programa funciona"},
   {"tipo": "usa", "patron": r"\buse\b", "texto": "Usa use", "pista": "use saludar from saludos"},
   {"tipo": "salida", "contiene": "¡Hola, Blip!", "texto": "Saluda a Blip", "pista": "saludar(\"Blip\")"},
 ],
 "pistas": ["use saludar from saludos", "Después: saludar(\"Blip\")"]},
],
"recuerda": [
"`use a, b from archivo` trae funciones de `archivo.cup`.",
"`use archivo` trae todo.",
"`fx main():` corre al ejecutar el archivo, pero no cuando otro lo usa.",
],
},

# ───────────────────────────────────────────────────────────── 16
{
"id": "azar", "titulo": "Juegos de azar",
"cupi": "dado", "bocadillo": "¡A ver qué sale!",
"historia": """
Cupi organizó una feria en la pastelería, con juegos de dados y una ruleta de premios. Pero hay un problema: ¡no sabe programar algo que **no se sabe qué va a salir**! Por suerte, la computadora también sabe jugar a la suerte.
""",
"explicacion": """
Dos funciones para jugar con el azar:

- `roll(1, 6)` da un número **al azar** entre 1 y 6, como un dado;
- `pick(lista)` elige **un elemento al azar** de una lista.

```
dado = roll(1, 6)
premio = pick(["un cupcake", "una gorra", "un globo"])
```

Cada vez que ejecutes el programa, puede salir algo distinto. ¡Pruébalo varias veces!

Con `roll`, `read_num` y `while` ya puedes hacer tu primer juego de verdad: adivinar un número.
""",
"ejemplos": [
{"texto": "Los dados de Cupi. Ejecútalo varias veces:", "azar": True,
 "codigo": """dado1 = roll(1, 6)
dado2 = roll(1, 6)
show("Salió {dado1} y {dado2}")

if dado1 == dado2:
    show("¡Dobles! Ganaste un cupcake extra")
"""},
{"texto": "La ruleta de premios:", "azar": True,
 "codigo": """premios = ["un cupcake", "una gorra", "un globo", "una medalla"]
show("¡Ganaste {pick(premios)}!")
"""},
{"texto": "**Adivina el número.** Cupi piensa un número del 1 al 10, y tienes tres intentos. Escribe tus respuestas en **Respuestas** y ejecuta:", "azar": True,
 "entradas": "5\n3\n8",
 "codigo": """secreto = roll(1, 10)
intentos = 0
adivinaste = false

while not (adivinaste or intentos == 3):
    n = read_num("¿Qué número pensé? ")
    intentos += 1
    if n == secreto:
        adivinaste = true
    else if n < secreto:
        show("Más alto…")
    else:
        show("Más bajo…")

if adivinaste:
    show("¡Adivinaste en {intentos} intentos!")
else:
    show("Era el {secreto}. ¡La próxima será!")
"""},
],
"ejercicios": [
{"enunciado": "Lanza **dos dados** con `roll` y muestra la suma, así: `Suma: 7` (el número cambia cada vez).",
 "inicial": "# Lanza dos dados y muestra la suma\n",
 "solucion": 'dado1 = roll(1, 6)\ndado2 = roll(1, 6)\nshow("Suma: {dado1 + dado2}")\n',
 "checks": [
   {"tipo": "ejecuta", "texto": "El programa funciona"},
   {"tipo": "usa", "patron": r"roll\(\s*1\s*,\s*6\s*\)[\s\S]*roll\(\s*1\s*,\s*6\s*\)", "texto": "Lanza dos dados con roll(1, 6)", "pista": "dado1 = roll(1, 6) y dado2 = roll(1, 6)"},
   {"tipo": "salida", "contiene": "Suma:", "texto": "Muestra «Suma: …»", "pista": "show(\"Suma: {dado1 + dado2}\")"},
 ],
 "pistas": ["Guarda cada dado en una variable: dado1 = roll(1, 6)", "show(\"Suma: {dado1 + dado2}\")"]},
],
"recuerda": [
"`roll(1, 6)` da un número al azar; `pick(lista)` elige un elemento al azar.",
"Con azar, cada ejecución puede ser distinta.",
],
},

# ───────────────────────────────────────────────────────────── 17
{
"id": "proyecto", "titulo": "Proyecto final: la pastelería de Cupi",
"cupi": "trofeo", "bocadillo": "¡Abrí mi propia pastelería!",
"historia": """
Después de tanto repartir cupcakes, Cupi tuvo una idea: **abrir su propia pastelería**, para monstruitos golosos con muchas bocas. Vamos a programarla juntos, usando todo lo que aprendiste.
""",
"explicacion": """
La pastelería necesita:
- una lista de **clientes**, cada uno un **registro** con su nombre y sus bocas;
- un **diccionario** con los precios de cada talla;
- una **función** que calcule cuánto paga cada cliente;
- un **ciclo** para atender a todos, y un **if** para dar descuento a los que tienen muchas bocas.

¡Todo lo que aprendiste, junto!
""",
"ejemplos": [
{"texto": "La pastelería de Cupi:",
 "codigo": """precios = ["chica": 2, "mediana": 3, "grande": 5]

clientes = [
    (nombre: "Blip", bocas: 6, talla: "chica"),
    (nombre: "Kora", bocas: 8, talla: "mediana"),
    (nombre: "Argos", bocas: 100, talla: "grande"),
]

fx cuenta(cliente):
    total = cliente.bocas * precios[cliente.talla]
    if cliente.bocas >= 50:
        total = total - total // 10       # 10% de descuento
    return total

ganancia = 0
for c in clientes:
    pago = cuenta(c)
    show("{c.nombre} paga {pago} monedas por {c.bocas} cupcakes")
    ganancia = ganancia + pago
show("Hoy Cupi ganó {ganancia} monedas")
"""},
],
"ejercicios": [
{"enunciado": "Agrega un cliente nuevo a la lista: **Zib**, el primo de Argos, con **100 bocas** y talla **mediana**. Con el descuento, Zib debe pagar **270** monedas.",
 "inicial": """precios = ["chica": 2, "mediana": 3, "grande": 5]

clientes = [
    (nombre: "Blip", bocas: 6, talla: "chica"),
    (nombre: "Kora", bocas: 8, talla: "mediana"),
]

# Agrega a Zib a la lista de clientes

fx cuenta(cliente):
    total = cliente.bocas * precios[cliente.talla]
    if cliente.bocas >= 50:
        total = total - total // 10
    return total

for c in clientes:
    show("{c.nombre} paga {cuenta(c)} monedas")
""",
 "solucion": """precios = ["chica": 2, "mediana": 3, "grande": 5]

clientes = [
    (nombre: "Blip", bocas: 6, talla: "chica"),
    (nombre: "Kora", bocas: 8, talla: "mediana"),
]

clientes = add(clientes, (nombre: "Zib", bocas: 100, talla: "mediana"))

fx cuenta(cliente):
    total = cliente.bocas * precios[cliente.talla]
    if cliente.bocas >= 50:
        total = total - total // 10
    return total

for c in clientes:
    show("{c.nombre} paga {cuenta(c)} monedas")
""",
 "checks": [
   {"tipo": "ejecuta", "texto": "El programa funciona"},
   {"tipo": "salida", "contiene": "Zib paga 270 monedas", "texto": "Zib paga 270 monedas",
    "pista": "clientes = add(clientes, (nombre: \"Zib\", bocas: 100, talla: \"mediana\"))"},
 ],
 "pistas": ["Para agregar a una lista: lista = add(lista, nuevo)", "El nuevo cliente es un registro: (nombre: \"Zib\", bocas: 100, talla: \"mediana\")"]},
],
"recuerda": [
"¡Ya sabes programar! Variables, decisiones, ciclos, listas, diccionarios, registros, funciones y errores.",
"Ahora inventa tu propio programa: un juego, una lista de tareas, una calculadora… lo que imagines.",
],
},
]
