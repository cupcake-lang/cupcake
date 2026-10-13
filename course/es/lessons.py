"""
El contenido del curso «Aprende a programar con Cupcake».

Cada lección tiene:
  place:       el lugar del Reino de Cupcake donde pasa la lección
  pose:        lo que muestra el dibujo
  bubble:      lo que dice el protagonista de la lección (el bocadillo)
  story:       una historia corta para empezar: llegar al lugar
  explanation: la idea, con ejemplos de código entre ```
  examples:    código que se puede ejecutar
  exercises:   para practicar, con comprobaciones automáticas
  remember:    lo más importante, en pocas líneas

Formato de los textos: párrafos separados por una línea en blanco, listas con "- ",
`código`, **negritas** y bloques de código entre ```.
build.py ejecuta cada ejemplo y cada solución antes de crear la página.
"""

LESSONS = [

# ───────────────────────────────────────────────────────────── 1
{
"id": "hello", "title": "¡Hola! Empieza el viaje",
"place": "El Castillo de Cupcake",
"pose": "wave", "bubble": "¡Qué bueno que llegaste! ¿Empezamos?",
"story": """
Las puertas del castillo se abren con olor a pastel recién horneado. **Frambuesa**, con su cereza brillante, te da la bienvenida y te presenta a sus amigos: **Vainilla**, que todo lo ordena; **Canela**, que todo lo pregunta; **Menta**, que todo lo revisa dos veces; y **Arándano**, que todo lo inventa. En este reino, **el código es magia**: escribes palabras, y pasan cosas.

La magia se escribe en **Cupcake**, un lenguaje de programación pequeño y fácil. Programar es escribir instrucciones para que la computadora haga cosas, y no hace falta saber nada antes. Aquí empieza un camino de estrellas con 17 lugares. ¡Vamos juntos!
""",
"explanation": """
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
"examples": [
{"text": "Pulsa **Ejecutar** y mira lo que pasa:",
 "code": """show("¡Hola, mundo!")
show("Soy Frambuesa, y llevo una cereza")
"""},
{"text": "Un dato curioso: se llaman *cupcakes* («pasteles de taza») porque antes se horneaban en tazas. Una de las primeras recetas apareció en un libro de cocina de **1796**.",
 "code": """# Datos curiosos sobre los cupcakes
show("Antes se horneaban en tazas")
show("Una de las primeras recetas es de 1796")
"""},
],
"exercises": [
{"task": "Escribe un programa que muestre **tu nombre** en una línea y **tu animal favorito** en otra.",
 "starter": "# Escribe aquí tu primer programa\n",
 "solution": 'show("Me llamo Ana")\nshow("Mi animal favorito es el gato")\n',
 "checks": [
   {"kind": "runs", "text": "El programa funciona"},
   {"kind": "uses", "pattern": r"show\(", "text": "Usa show(…)", "hint": "Escribe show(\"tu texto\")"},
   {"kind": "lines", "min": 2, "text": "Muestra al menos dos líneas", "hint": "Usa dos veces show(…), una en cada línea."},
 ],
 "hints": ["Cada show(…) muestra una línea.", "El texto va entre comillas: show(\"Me llamo Ana\")"]},
],
"remember": [
"`show(\"texto\")` muestra algo en la pantalla.",
"Los textos van entre comillas.",
"Las instrucciones se hacen en orden, de arriba hacia abajo.",
"`#` sirve para escribir notas.",
],
},

# ───────────────────────────────────────────────────────────── 2
{
"id": "variables", "title": "Cajas con nombre: las variables",
"place": "El Almacén de Vainilla",
"pose": "boxes", "bubble": "Cada cosa en su caja, y cada caja con su etiqueta.",
"story": """
El Almacén de Vainilla huele a azúcar y tiene estantes hasta el techo. Aquí nada se pierde: Vainilla guarda cada cosa en una **caja** y le pega una **etiqueta** con un nombre. Cuando necesita algo, busca la etiqueta y listo.
""",
"explanation": """
En programación, esas cajas se llaman **variables**. Se crean así:

```
chispitas = 12
nombre = "Vainilla"
```

Se lee: «guarda 12 en una caja llamada `chispitas`». El signo `=` significa **guardar**, no «es igual».

Después, usas el nombre de la caja para sacar lo que tiene:

```
show(nombre, "tiene", chispitas, "chispitas")
```

`show` puede mostrar varias cosas a la vez, separadas por comas. Las pone en la misma línea, con un espacio entre ellas.

Una caja puede guardar **números** (`12`, `3.5`) o **textos** (`"Vainilla"`). Y se puede **cambiar** lo que tiene:

```
chispitas = 12
chispitas = chispitas + 2      # ahora guarda 14
```

Los nombres de las cajas van **sin espacios** y sin empezar con número: `mis_chispitas`, no `mis chispitas`.
""",
"examples": [
{"text": "Vainilla guarda sus datos:",
 "code": """nombre = "Vainilla"
chispitas = 12
color = "crema"

show(nombre, "tiene", chispitas, "chispitas")
show("Su color favorito es el", color)
"""},
{"text": "Le pusieron dos chispitas nuevas:",
 "code": """chispitas = 12
show("Antes:", chispitas)

chispitas = chispitas + 2
show("Ahora:", chispitas)
"""},
],
"exercises": [
{"task": "Crea una variable `nombre` con tu nombre y una variable `edad` con tu edad. Después muéstralas en una línea con `show`.",
 "starter": "# 1. Crea la variable nombre\n\n# 2. Crea la variable edad\n\n# 3. Muéstralas\n",
 "solution": 'nombre = "Ana"\nedad = 9\nshow(nombre, "tiene", edad, "años")\n',
 "checks": [
   {"kind": "runs", "text": "El programa funciona"},
   {"kind": "uses", "pattern": r"\bnombre\s*=", "text": "Crea la variable nombre", "hint": "nombre = \"Ana\""},
   {"kind": "uses", "pattern": r"\bedad\s*=\s*\d", "text": "Crea la variable edad con un número", "hint": "edad = 9 (sin comillas: es un número)"},
   {"kind": "uses", "pattern": r"show\([^)]*\bnombre\b[^)]*\bedad\b|show\([^)]*\bedad\b[^)]*\bnombre\b", "text": "Muestra las dos con show",
    "hint": "show(nombre, \"tiene\", edad, \"años\")"},
 ],
 "hints": ["Una variable se crea así: nombre = valor", "Para mostrar varias cosas, sepáralas con comas dentro de show(…)"]},
],
"remember": [
"Una variable es una caja con nombre: `chispitas = 12`.",
"`=` significa **guardar**.",
"Puede guardar números o textos, y se puede cambiar.",
],
},

# ───────────────────────────────────────────────────────────── 3
{
"id": "texts", "title": "Textos con valores",
"place": "La Plaza de los Carteles",
"pose": "sign", "bubble": "¡Mi cartel cambia solo!",
"story": """
En la Plaza de los Carteles, cada puerta tiene un letrero de colores. Frambuesa quiere uno que salude a cada visitante por su nombre: «¡Hola, Ana!», «¡Hola, Blip!»… Pero no puede pintar un cartel nuevo para cada persona que llega. ¿Y si el cartel pudiera **cambiar solo**?
""",
"explanation": """
Dentro de un texto puedes poner **llaves** `{ }` con el nombre de una variable. Cupcake pone su valor en ese lugar:

```
nombre = "Blip"
show("¡Hola, {nombre}!")
```

Muestra: `¡Hola, Blip!`. Si cambias lo que guarda `nombre`, el cartel cambia solo.

Puedes poner varias llaves en el mismo texto:

```
nombre = "Frambuesa"
chispitas = 12
show("Aquí vive {nombre}, que tiene {chispitas} chispitas")
```

Muestra: `Aquí vive Frambuesa, que tiene 12 chispitas`.

Entre las llaves también puedes hacer **cuentas**:

```
show("La mitad de sus chispitas son {chispitas / 2}")
```

Y si alguna vez quieres escribir una llave de verdad, pon una barra antes: `\\{`.
""",
"examples": [
{"text": "El cartel de Frambuesa:",
 "code": """nombre = "Frambuesa"
chispitas = 12
show("Aquí vive {nombre}, que tiene {chispitas} chispitas")
"""},
{"text": "Con cuentas dentro de las llaves:",
 "code": """chispitas = 12
show("La mitad de sus chispitas son {chispitas // 2}")
show("Si le ponen 4 chispitas más, tendrá {chispitas + 4}")
"""},
],
"exercises": [
{"task": "Frambuesa reparte `chispitas = 120` entre dos cupcakes. Muestra el texto `Cada cupcake recibe 60 chispitas`, calculando la mitad **dentro de las llaves**.",
 "starter": "chispitas = 120\n\n# Muestra cuántas chispitas recibe cada cupcake\n",
 "solution": 'chispitas = 120\nshow("Cada cupcake recibe {chispitas // 2} chispitas")\n',
 "checks": [
   {"kind": "runs", "text": "El programa funciona"},
   {"kind": "output", "contains": "Cada cupcake recibe 60 chispitas", "text": "Muestra «Cada cupcake recibe 60 chispitas»",
    "hint": "show(\"Cada cupcake recibe {chispitas // 2} chispitas\")"},
   {"kind": "uses", "pattern": r"\{[^}]*chispitas[^}]*\}", "text": "Calcula dentro de las llaves", "hint": "Escribe la cuenta entre llaves: {chispitas // 2}"},
 ],
 "hints": ["Son dos cupcakes: hay que dividir entre 2.", "// divide sin decimales: 120 // 2 da 60."]},
],
"remember": [
"`\"Hola, {nombre}\"`: lo que va entre llaves se reemplaza por su valor.",
"Entre llaves también se pueden hacer cuentas: `{chispitas + 4}`.",
],
},

# ───────────────────────────────────────────────────────────── 4
{
"id": "math", "title": "Cuentas y más cuentas",
"place": "El Molino de las Cuentas",
"pose": "calculator", "bubble": "¿Cien bocas? ¡No me alcanzan los dedos!",
"story": """
Las aspas del Molino de las Cuentas giran y giran, y en cada vuelta sale un número. Justo entonces llega **Argos**, un monstruito con **100 bocas**, ¡y tiene hambre en todas! Quiere un cupcake para cada boca, y los cupcakes cuestan.

Canela empieza a contar con los dedos… y se enreda. Frambuesa se ríe: «Deja que lo haga la computadora. Para eso es buenísima».
""",
"explanation": """
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
"examples": [
{"text": "¿Cuánto cuestan los cupcakes para Argos?",
 "code": """bocas = 100
precio = 3          # cada cupcake cuesta 3 monedas

total = bocas * precio
show("Los cupcakes cuestan {total} monedas")
show("Son {bocas // 2} cajitas de a dos")
"""},
{"text": "Las seis cuentas:",
 "code": """show(7 + 2, 7 - 2, 7 * 2)
show(7 / 2, 7 // 2, 7 % 2)
show(2 ** 10)
"""},
],
"exercises": [
{"task": "Argos tiene un primo con todavía más bocas: **250**. Cada cupcake cuesta **4** monedas. Calcula el total y muéstralo (debe dar **1000**).",
 "starter": "bocas = 250\nprecio = 4\n\n# Calcula el total y muéstralo\n",
 "solution": 'bocas = 250\nprecio = 4\n\ntotal = bocas * precio\nshow("Total: {total} monedas")\n',
 "checks": [
   {"kind": "runs", "text": "El programa funciona"},
   {"kind": "output", "contains": "1000", "text": "Muestra 1000", "hint": "total = bocas * precio"},
   {"kind": "not_uses", "pattern": r"1000", "text": "Lo calcula la computadora (sin escribir 1000 a mano)",
    "hint": "Usa las variables bocas y precio: bocas * precio"},
 ],
 "hints": ["Multiplicar se escribe con *", "total = bocas * precio, y después show(total)"]},
],
"remember": [
"`+ - * /` como en matemáticas; `//` divide sin decimales; `%` da el resto.",
"Los paréntesis cambian el orden de las cuentas.",
],
},

# ───────────────────────────────────────────────────────────── 5
{
"id": "reading", "title": "Leer lo que escribes",
"place": "La Cueva del Eco",
"pose": "question", "bubble": "¿Hola? ¿Me oyes? ¿Cuántas bocas tienes?",
"story": """
La Cueva del Eco es oscura y fresca. Canela grita «¡Hola!», y la cueva le contesta «¡Hola!». Hasta ahora, nuestros programas hablaban solos. Aquí aprendemos a **conversar**: que tú escribas algo y el programa lo escuche y lo use.
""",
"explanation": """
`read` significa «lee». Muestra un aviso, espera a que la persona escriba algo y pulse Enter, y lo guarda:

```
nombre = read("¿Cómo te llamas? ")
show("¡Hola, {nombre}!")
```

Como el eco de la cueva, `read` escucha lo que dices y te lo devuelve para que lo uses.

El aviso puede ser una pregunta, pero no tiene que serlo: `read("Escribe tu nombre: ")` o `read("Pulsa Enter para seguir…")` también sirven.

Lo que escribe la persona **siempre es un texto**. Si quieres un **número**, para hacer cuentas, usa `read_num`:

```
edad = read_num("¿Cuántos años tienes? ")
show("El año que viene tendrás {edad + 1}")
```

Y si la persona escribe letras en vez de un número, `read_num` le vuelve a pedir el número, con paciencia. Cupcake avisa en inglés: `'muchas' is not a number. Try again.` («"muchas" no es un número; prueba otra vez»).

En esta página, las respuestas se escriben **antes de ejecutar**, en la caja **Respuestas**, una por línea.
""",
"examples": [
{"text": "Canela te pregunta. Las respuestas ya están escritas en la caja **Respuestas**: cámbialas y vuelve a ejecutar.",
 "inputs": "Ana\n9",
 "code": """nombre = read("¿Cómo te llamas? ")
edad = read_num("¿Cuántos años tienes? ")

show("¡Hola, {nombre}!")
show("El año que viene tendrás {edad + 1} años")
"""},
{"text": "Si la respuesta no es un número, `read_num` lo vuelve a pedir. Aquí la primera respuesta es `muchas`:",
 "inputs": "muchas\n100",
 "code": """bocas = read_num("¿Cuántas bocas tienes? ")
show("¡{bocas} bocas! Necesitas {bocas // 2} cajitas de cupcakes")
"""},
],
"exercises": [
{"task": "Pregunta **cuántas bocas** tiene un monstruito y muestra **cuántas cajitas** necesita (en cada cajita caben dos cupcakes). Con la respuesta `40`, debe mostrar `20`.",
 "inputs": "40",
 "starter": "# Pregunta cuántas bocas tiene\n\n# Muestra cuántas cajitas necesita\n",
 "solution": 'bocas = read_num("¿Cuántas bocas tienes? ")\nshow("Necesitas {bocas // 2} cajitas de cupcakes")\n',
 "checks": [
   {"kind": "runs", "text": "El programa funciona"},
   {"kind": "uses", "pattern": r"read(_num)?\(", "text": "Lee el número con read_num(…)", "hint": "bocas = read_num(\"¿Cuántas bocas tienes? \")"},
   {"kind": "output", "contains": "20", "text": "Con 40 bocas, muestra 20", "hint": "Las cajitas son bocas // 2"},
 ],
 "hints": ["Para leer un número: read_num(\"aviso\")", "bocas = read_num(\"¿Cuántas bocas tienes? \")"]},
],
"remember": [
"`read(\"aviso\")` muestra el aviso y devuelve lo que la persona escribe, como texto.",
"`read_num(\"aviso\")` insiste hasta recibir un número.",
"Para los archivos: `load(\"archivo.txt\")` carga y `save(\"archivo.txt\", texto)` guarda.",
],
},

# ───────────────────────────────────────────────────────────── 6
{
"id": "decisions", "title": "Decidir: if y else",
"place": "El Bosque de los Caminos",
"pose": "crossroads", "bubble": "Si llueve, por aquí. Si no, por allá.",
"story": """
En el Bosque de los Caminos, el sendero se parte en dos bajo los árboles de algodón de azúcar. Menta lee el letrero dos veces, con atención: **si** llueve, por el camino con techo; **si no**, por el prado. Los programas también toman **decisiones** así.
""",
"explanation": """
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
    is "verde":
        show("¡Como Menta!")
    is "rojo":
        show("Como la cereza de Frambuesa")
    else:
        show("Un color nuevo")
```

Cada caso dice **qué hacer** después de `:`. El último, `else` («si no»), es para todo lo demás. Y si un caso necesita varias líneas, van debajo, con más sangría.

Y `not` da lo contrario: `if not lluvia:` se lee «si no llueve».
""",
"examples": [
{"text": "Cambia la temperatura y vuelve a ejecutar:",
 "code": """temperatura = 22

if temperatura > 30:
    show("¡Qué calor!")
else if temperatura > 15:
    show("Está agradable")
else:
    show("¡A ponerse la bufanda!")
"""},
{"text": "`when` con varios casos. Con `in` se pregunta si está en un rango:",
 "code": """edad = 12

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
"exercises": [
{"task": "Frambuesa tiene `cupcakes = 100` y Argos tiene `bocas = 100`. Si hay un cupcake para cada boca, muestra `¡A comer!`. Si no, muestra `Faltan cupcakes`.",
 "starter": "cupcakes = 100\nbocas = 100\n\n# Decide qué mostrar\n",
 "solution": 'cupcakes = 100\nbocas = 100\n\nif cupcakes >= bocas:\n    show("¡A comer!")\nelse:\n    show("Faltan cupcakes")\n',
 "checks": [
   {"kind": "runs", "text": "El programa funciona"},
   {"kind": "uses", "pattern": r"\bif\b", "text": "Usa if", "hint": "if cupcakes >= bocas: …"},
   {"kind": "uses", "pattern": r"\belse\b", "text": "Usa else para el otro caso", "hint": "else:  (a la misma altura que el if)"},
   {"kind": "output", "contains": "¡A comer!", "text": "Con 100 y 100, muestra «¡A comer!»"},
 ],
 "hints": ["La condición es: cupcakes >= bocas", "if cupcakes >= bocas: … y debajo, else: …"]},
{"task": "Con `when`, haz que según la `nota` se muestre: de 9 a 10 `¡Excelente!`, de 6 a 8 `Aprobado`, y si no, `A estudiar más`. Con `nota = 7` debe mostrar `Aprobado`.",
 "starter": "nota = 7\n\n# Usa when para decidir\n",
 "solution": 'nota = 7\n\nwhen nota:\n    in 9..10:\n        show("¡Excelente!")\n    in 6..8:\n        show("Aprobado")\n    else:\n        show("A estudiar más")\n',
 "checks": [
   {"kind": "runs", "text": "El programa funciona"},
   {"kind": "uses", "pattern": r"\bwhen\b", "text": "Usa when", "hint": "when nota:  y debajo  in 9..10:"},
   {"kind": "output", "contains": "Aprobado", "text": "Con 7, muestra «Aprobado»"},
   {"kind": "no_output", "contains": "Excelente", "text": "No muestra «¡Excelente!»"},
 ],
 "hints": ["Cada caso: in desde..hasta:  y debajo, con sangría, show(…)", "El último caso es: else:  y debajo show(\"A estudiar más\")"]},
],
"remember": [
"`if condición: …` se hace solo si es verdad.",
"`else if` revisa otro caso; `else` es el resto.",
"`when valor:` y debajo los casos `is …: …`, `in …: …` y `else: …`, para muchos casos.",
"Comparar: `== != < > <= >=`, y `x in 1..10` para «entre». Juntar: `and`, `or`, `not`.",
],
},

# ───────────────────────────────────────────────────────────── 7
{
"id": "loops", "title": "Repetir",
"place": "El Carrusel",
"pose": "laps", "bubble": "¡Vuelta uno, vuelta dos, vuelta… ay, me mareé!",
"story": """
En el Carrusel, los caballitos de azúcar suben, bajan y dan vueltas sin parar. Canela se sube y va contando: «Una, dos, tres…». A la vuelta veinte ya está mareado. A la computadora, en cambio, **le encanta repetir**: puede hacer lo mismo mil veces sin cansarse.
""",
"explanation": """
Lo más fácil: `repeat` repite algo **un número de veces**:

```
repeat 3:
    show("¡Hip, hip, hurra!")
```

`for` («para cada») repite **por cada número** de un rango, y en cada vuelta te dice cuál es. El rango `1..5` va del 1 al 5, **los dos incluidos**:

```
for i in 1..5:
    show("Vuelta número {i}")
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

Hay que tener cuidado: si la condición nunca cambia, ¡se repite para siempre, como un carrusel que no para! Dentro de un ciclo, `break` sale de inmediato y `continue` salta a la siguiente vuelta.
""",
"examples": [
{"text": "¡Hurra!",
 "code": """repeat 3:
    show("¡Hip, hip, hurra!")
"""},
{"text": "Canela cuenta sus primeras vueltas, y después cuenta hacia atrás para que el carrusel arranque otra vez:",
 "code": """for i in 1..5:
    show("Vuelta número {i}")

for i in 3..1 by -1:
    show("{i}…")
show("¡Arranca!")
"""},
{"text": "Canela decora cupcakes hasta tener tres:",
 "code": """cupcakes = 0
while cupcakes != 3:
    cupcakes += 1
    show("Decoré el cupcake {cupcakes}")
show("Listo: {cupcakes} cupcakes")
"""},
],
"exercises": [
{"task": "Muestra la **tabla del 7**, del 1 al 10, así: `7 x 1 = 7`, `7 x 2 = 14`… hasta `7 x 10 = 70`.",
 "starter": "# Repite del 1 al 10\n",
 "solution": 'for i in 1..10:\n    show("7 x {i} = {7 * i}")\n',
 "checks": [
   {"kind": "runs", "text": "El programa funciona"},
   {"kind": "uses", "pattern": r"\bfor\b|\bwhile\b", "text": "Usa un ciclo", "hint": "for i in 1..10:"},
   {"kind": "output", "contains": "7 x 1 = 7", "text": "Empieza con 7 x 1 = 7"},
   {"kind": "output", "contains": "7 x 10 = 70", "text": "Termina con 7 x 10 = 70", "hint": "El rango 1..10 incluye el 10."},
 ],
 "hints": ["for i in 1..10:", "Debajo, con sangría: show(\"7 x {i} = {7 * i}\")"]},
],
"remember": [
"`repeat 3: …` repite tres veces.",
"`for i in 1..5: …` repite con i = 1, 2, 3, 4, 5. Con `by 2`, de a dos.",
"`while` repite mientras algo sea verdad.",
"`break` sale; `continue` salta a la siguiente vuelta.",
],
},

# ───────────────────────────────────────────────────────────── 8
{
"id": "lists", "title": "Listas: muchas cosas en fila",
"place": "El Desfile",
"pose": "row", "bubble": "¡En fila! Y el primero es el número 0.",
"story": """
¡Suenan los tambores! Por la avenida pasa **el Desfile**, y los cinco marchan en fila: Frambuesa, Vainilla, Canela, Menta y Arándano. Cada uno lleva un número en la espalda, y Frambuesa, que va primera, lleva el **0**. Muchas cosas en orden, una detrás de otra: eso, en programación, es una **lista**.
""",
"explanation": """
Una lista guarda varias cosas en orden, entre **corchetes** `[ ]`:

```
desfile = ["Frambuesa", "Vainilla", "Canela", "Menta", "Arándano"]
```

Cada cosa tiene una **posición**, y se cuenta **desde 0**:

```
show(desfile[0])      # Frambuesa   (la primera)
show(desfile[2])      # Canela
show(desfile[-1])     # Arándano    (el último)
```

Para **cortar** un pedazo se usa `..`, como en los rangos:

```
show(desfile[0..1])   # ["Frambuesa", "Vainilla"]
```

Funciones para listas:
- `len(lista)` cuenta cuántas cosas tiene;
- `add(lista, x)` agrega algo al final;
- `drop(lista, x)` quita algo;
- `count(lista, x)` cuenta cuántas veces está algo.

Y para preguntar si algo está en la lista, se usa `in`:

```
"Menta" in desfile          # ¿Menta está en la lista?
"Argos" not in desfile      # ¿Argos no está?
desfile is empty            # ¿está vacía?
```

`add` y `drop` **devuelven una lista nueva**. Por eso se guarda el resultado: `desfile = add(desfile, "Argos")`.

Y `for` sirve para recorrer una lista, uno por uno. Con `at`, también sabes la posición:

```
for i, nombre at desfile:
    show("{i}: ¡Hola, {nombre}!")
```
""",
"examples": [
{"text": "El desfile, con el número de cada uno:",
 "code": """desfile = ["Frambuesa", "Vainilla", "Canela", "Menta", "Arándano"]

show(desfile[0], "va primera")
show("Marchan {len(desfile)} amigos")

desfile = add(desfile, "Argos")
show(desfile)

for i, nombre at desfile:
    show("{i}: ¡Hola, {nombre}!")
"""},
{"text": "Buscar y cortar:",
 "code": """cupcakes = ["rojo", "azul", "verde", "amarillo", "morado", "rojo"]

show("azul" in cupcakes, "negro" not in cupcakes)
show(cupcakes[1..3])
show("Hay {count(cupcakes, "rojo")} cupcakes rojos")

for i, c at cupcakes:
    show("{i}: {c}")
"""},
],
"exercises": [
{"task": "Vainilla tiene `frutas = [\"manzana\", \"pera\"]`. Agrega `\"mango\"` a la lista y muestra **cuántas frutas** hay (debe dar 3) y **cuál es la última**.",
 "starter": 'frutas = ["manzana", "pera"]\n\n# Agrega el mango\n\n# Muestra cuántas hay y la última\n',
 "solution": 'frutas = ["manzana", "pera"]\n\nfrutas = add(frutas, "mango")\n\nshow(len(frutas), frutas[-1])\n',
 "checks": [
   {"kind": "runs", "text": "El programa funciona"},
   {"kind": "uses", "pattern": r"frutas\s*=\s*add\(", "text": "Agrega con add y guarda el resultado", "hint": "frutas = add(frutas, \"mango\")"},
   {"kind": "output", "contains": "3", "text": "Muestra 3", "hint": "len(frutas)"},
   {"kind": "output", "contains": "mango", "text": "Muestra el mango, que es el último", "hint": "frutas[-1] es el último"},
 ],
 "hints": ["frutas = add(frutas, \"mango\")", "show(len(frutas), frutas[-1])"]},
],
"remember": [
"Una lista va entre corchetes: `[\"a\", \"b\"]`. Se cuenta desde 0.",
"`len`, `add`, `drop`, `count`. Preguntar: `x in lista`, `x not in lista`, `lista is empty`.",
"Para cortar: `lista[1..3]`. Para saber la posición: `for i, x at lista`.",
"`add` y `drop` devuelven una lista nueva: guárdala.",
],
},

# ───────────────────────────────────────────────────────────── 9
{
"id": "dictionaries", "title": "Diccionarios: buscar por nombre",
"place": "La Biblioteca de Sabores",
"pose": "book", "bubble": "¿Talla chica? Busco «chica» y… ¡2 monedas!",
"story": """
En la Biblioteca de Sabores, los libros huelen a chocolate y a fresa. Frambuesa abre el **libro de precios**: no busca «la tercera línea», busca la palabra «chica» y ahí está su precio. Así funcionan los **diccionarios**: buscas por nombre, no por posición.
""",
"explanation": """
Un diccionario es como una lista, pero cada cosa tiene una **clave** en vez de una posición. Se escribe igual que una lista, agregando `clave:` delante de cada valor:

```
precios = ["chica": 2, "mediana": 3, "grande": 5]
```

Se busca por la clave:

```
show(precios["mediana"])     # 3
```

Se puede **agregar** o **cambiar** un valor:

```
precios["gigante"] = 8
precios["chica"] = 3
```

Funciones útiles:
- `keys(dic)`: las claves;
- `values(dic)`: los valores;
- `clave in dic`: ¿tiene esa clave?

Si buscas una clave que no existe, Cupcake se detiene y te avisa en inglés: `the dictionary has no key "mini".` («el diccionario no tiene la clave "mini"»). Pero si quieres un **valor de reserva**, usa `else`:

```
precio = precios["mini"] else 0     # si no hay talla mini, 0
```

Un diccionario vacío se escribe `[:]`.
""",
"examples": [
{"text": "El libro de precios de Frambuesa:",
 "code": """precios = ["chica": 2, "mediana": 3, "grande": 5]

show("La talla mediana cuesta", precios["mediana"])

precios["gigante"] = 8
show(keys(precios))
show("mini" in precios)
show(precios["mini"] else "no hay talla mini")

for talla in keys(precios):
    show("Talla {talla}: {precios[talla]} monedas")
"""},
],
"exercises": [
{"task": "Crea un diccionario `edades` con dos monstruitos y sus edades (por ejemplo, Blip de 3 y Kora de 5). Después agrega a Zum, de 4, y muestra **la edad de Zum**.",
 "starter": "# Crea el diccionario\n\n# Agrega a Zum\n\n# Muestra la edad de Zum\n",
 "solution": 'edades = ["Blip": 3, "Kora": 5]\nedades["Zum"] = 4\nshow(edades["Zum"])\n',
 "checks": [
   {"kind": "runs", "text": "El programa funciona"},
   {"kind": "uses", "pattern": r"\[\s*\"[^\"]+\"\s*:", "text": "Crea un diccionario con clave: valor", "hint": "edades = [\"Blip\": 3, \"Kora\": 5]"},
   {"kind": "uses", "pattern": r"edades\[\s*\"Zum\"\s*\]\s*=", "text": "Agrega a Zum", "hint": "edades[\"Zum\"] = 4"},
   {"kind": "output", "contains": "4", "text": "Muestra la edad de Zum"},
 ],
 "hints": ["Un diccionario: [\"clave\": valor, …]", "edades[\"Zum\"] = 4 y después show(edades[\"Zum\"])"]},
],
"remember": [
"Diccionario: `[\"clave\": valor]`. Vacío: `[:]`.",
"Se busca con `dic[\"clave\"]` y se agrega con `dic[\"clave\"] = valor`.",
"`keys`, `values`, `clave in dic`. Valor de reserva: `dic[\"x\"] else 0`.",
],
},

# ───────────────────────────────────────────────────────────── 10
{
"id": "records", "title": "Registros: fichas con campos",
"place": "La Torre de las Fichas",
"pose": "card", "bubble": "Nombre, bocas, color… ¡todo en su casilla!",
"story": """
En lo alto de la Torre de las Fichas, Menta guarda una tarjeta por cada cliente de la pastelería. Hoy le toca a Argos: nombre, bocas y color, cada dato en su casilla. Menta la revisa dos veces, claro. En Cupcake, una ficha así se llama **registro**.
""",
"explanation": """
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

Un registro **nace con sus campos** y no se le pueden agregar otros. Si escribes mal un campo, Cupcake te avisa en inglés y te sugiere el correcto: `the record has no field 'bocsa'. Did you mean 'bocas'?` («el registro no tiene el campo "bocsa". ¿Quisiste decir "bocas"?»). ¡Así no se pierden datos por un error de escritura!

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
- Un **diccionario** es una **colección** que puede crecer: los precios de la pastelería.
""",
"examples": [
{"text": "La ficha de Argos:",
 "code": """argos = (nombre: "Argos", bocas: 100, color: "verde")

show("{argos.nombre} es de color {argos.color}")
argos.bocas = 102
show(argos)
"""},
{"text": "Un error de escritura. Ejecútalo y mira cómo te ayuda Cupcake:",
 "expect": "error",
 "code": """argos = (nombre: "Argos", bocas: 100)
argos.bocsa = 102
"""},
{"text": "Las fichas de la torre, en una lista de registros:",
 "code": """clientes = [
    (nombre: "Argos", bocas: 100),
    (nombre: "Blip", bocas: 6),
    (nombre: "Kora", bocas: 8),
]

for cliente in clientes:
    show("{cliente.nombre} come con {cliente.bocas} bocas")
"""},
{"text": "`has` en un juego: ¿quién sigue en pie? Con una lista, `has` pregunta si **alguno** tiene ese campo:",
 "code": """canela = (nombre: "Canela", energia: 3, escudo: false)
rival = (nombre: "Glub", energia: 0, escudo: true)

if canela has energia and rival has not energia:
    show("¡{canela.nombre} ganó la carrera!")

if rival has escudo:
    show("{rival.nombre} tiene escudo")

equipo = [canela, rival]
if equipo has energia:
    show("Alguien del equipo todavía puede jugar")
"""},
],
"exercises": [
{"task": "Crea un registro `mascota` con los campos `nombre`, `animal` y `edad`. Después **cumple años**: súmale 1 a su edad y muestra el registro.",
 "starter": "# Crea el registro mascota\n\n# Súmale 1 a la edad\n\n# Muéstralo\n",
 "solution": 'mascota = (nombre: "Luna", animal: "gata", edad: 3)\nmascota.edad = mascota.edad + 1\nshow(mascota)\n',
 "checks": [
   {"kind": "runs", "text": "El programa funciona"},
   {"kind": "uses", "pattern": r"\(\s*nombre\s*:", "text": "Crea un registro con el campo nombre", "hint": "mascota = (nombre: \"Luna\", animal: \"gata\", edad: 3)"},
   {"kind": "uses", "pattern": r"mascota\.edad\s*=", "text": "Cambia la edad con un punto", "hint": "mascota.edad = mascota.edad + 1"},
   {"kind": "output", "contains": "edad:", "text": "Muestra el registro", "hint": "show(mascota)"},
 ],
 "hints": ["Un registro: (campo: valor, campo: valor)", "mascota.edad = mascota.edad + 1"]},
],
"remember": [
"Registro: `(nombre: \"Argos\", bocas: 100)`.",
"Se lee y se cambia con punto: `argos.bocas`.",
"`argos has bocas` pregunta si ese campo tiene algo; responde `true` o `false`.",
"No gana campos nuevos: así se atrapan los errores de escritura.",
],
},

# ───────────────────────────────────────────────────────────── 11
{
"id": "functions", "title": "Funciones: tus propias instrucciones",
"place": "El Taller de Arándano",
"pose": "tool", "bubble": "¡Bing! Inventé una herramienta nueva.",
"story": """
El Taller de Arándano está lleno de tuercas, resortes y aparatos que hacen «¡bing!». Arándano se cansó de calcular a mano cuántas cajitas necesita cada cliente, así que inventó una herramienta: le dices cuántas bocas tiene alguien, y ella te responde cuántas cajitas hacen falta. Una instrucción inventada por ti: eso es una **función**.
""",
"explanation": """
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

Sin `return`, la función hace lo que dice pero no devuelve nada (devuelve `none`). Si escribes una línea que solo calcula algo, como `bocas // 2`, Cupcake te avisa en inglés que falta el `return`: `this line computes a value but does nothing with it.` («esta línea calcula un valor, pero no hace nada con él»).

Una función puede recibir varios datos, y algunos pueden tener un **valor por defecto**:

```
fx saludar(nombre, saludo = "Hola"):
    show("{saludo}, {nombre}")

saludar("Arándano")                  # Hola, Arándano
saludar("Blip", saludo = "Buenas")   # Buenas, Blip
```

Las funciones también sirven de **molde** para crear registros iguales:

```
fx cliente(nombre, bocas):
    return (nombre: nombre, bocas: bocas)
```
""",
"examples": [
{"text": "La herramienta de Arándano:",
 "code": """fx cajitas(bocas):
    return bocas // 2

show("Argos necesita", cajitas(100), "cajitas")
show("Blip necesita", cajitas(6), "cajitas")
"""},
{"text": "Saludos con valor por defecto:",
 "code": """fx saludar(nombre, saludo = "Hola"):
    show("{saludo}, {nombre}")

saludar("Arándano")
saludar("Blip", saludo = "Buenas")
"""},
],
"exercises": [
{"task": "Crea una función `costo(bocas, precio)` que devuelva cuánto cuestan los cupcakes (bocas × precio). Úsala para mostrar el costo de **100 bocas a 3 monedas** (debe dar 300).",
 "starter": "# Crea la función costo\n\n# Úsala y muestra el resultado\n",
 "solution": 'fx costo(bocas, precio):\n    return bocas * precio\n\nshow(costo(100, 3))\n',
 "checks": [
   {"kind": "runs", "text": "El programa funciona"},
   {"kind": "uses", "pattern": r"fx\s+costo\s*\(", "text": "Crea la función costo", "hint": "fx costo(bocas, precio): …"},
   {"kind": "output", "contains": "300", "text": "Muestra 300", "hint": "show(costo(100, 3))"},
 ],
 "hints": ["fx costo(bocas, precio):  y debajo  return bocas * precio", "Para usarla: show(costo(100, 3))"]},
],
"remember": [
"`fx nombre(datos): …` crea una función.",
"`return` devuelve el resultado. Sin `return`, la función no devuelve nada.",
"Los datos pueden tener valor por defecto: `saludo = \"Hola\"`.",
],
},

# ───────────────────────────────────────────────────────────── 12
{
"id": "copies", "title": "Los datos se copian",
"place": "El Lago Espejo",
"pose": "photocopy", "bubble": "¡Hay dos Canelas! Bueno, uno es una copia.",
"story": """
El agua del Lago Espejo está tan quieta que lo refleja todo. Canela se asoma y ve a otro Canela, igualito pero más clarito. Le tira una piedrita y el reflejo se arruga entero… pero el Canela de verdad sigue igual. En Cupcake, los datos funcionan así: lo que le pasa a la **copia** no le pasa al original.
""",
"explanation": """
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

canela = decorar(canela)       # ← se guarda lo que devolvió
```

Si olvidas guardar el resultado, el cambio se queda en la copia y se pierde.
""",
"examples": [
{"text": "Canela y su reflejo:",
 "code": """canela = (nombre: "Canela", chispitas: 12)
reflejo = canela
reflejo.chispitas = 4

show(canela.chispitas)      # el original no cambió
show(reflejo.chispitas)
"""},
{"text": "Una función que cambia algo y lo devuelve:",
 "code": """fx decorar(c):
    c.chispitas = c.chispitas + 2
    return c

canela = (nombre: "Canela", chispitas: 12)
decorar(canela)
show("Sin guardar:", canela.chispitas)

canela = decorar(canela)
show("Guardando:", canela.chispitas)
"""},
],
"exercises": [
{"task": "Este programa debería mostrar `30`, pero muestra `10`. **Arréglalo**: el resultado de `curar` no se está guardando.",
 "starter": 'fx curar(monstruito, cantidad):\n    monstruito.vida = monstruito.vida + cantidad\n    return monstruito\n\nkora = (nombre: "Kora", vida: 10)\ncurar(kora, 20)\nshow(kora.vida)\n',
 "solution": 'fx curar(monstruito, cantidad):\n    monstruito.vida = monstruito.vida + cantidad\n    return monstruito\n\nkora = (nombre: "Kora", vida: 10)\nkora = curar(kora, 20)\nshow(kora.vida)\n',
 "checks": [
   {"kind": "runs", "text": "El programa funciona"},
   {"kind": "uses", "pattern": r"kora\s*=\s*curar\(", "text": "Guarda lo que devuelve curar", "hint": "kora = curar(kora, 20)"},
   {"kind": "output", "contains": "30", "text": "Muestra 30"},
 ],
 "hints": ["curar devuelve el monstruito curado, pero nadie lo guarda.", "Cambia la línea por: kora = curar(kora, 20)"]},
],
"remember": [
"Asignar o pasar un dato hace una **copia**.",
"Una función que cambia algo lo devuelve: `x = cambiar(x)`.",
],
},

# ───────────────────────────────────────────────────────────── 13
{
"id": "shortcuts", "title": "Atajos: funciones sin nombre y listas rápidas",
"place": "El Mirador",
"pose": "magnifier", "bubble": "Con mi lupa, solo los rojos…",
"story": """
Desde el Mirador se ve todo el reino, y allá abajo hay una montaña de cupcakes de colores. Menta saca su lupa: quiere encontrar **solo los rojos**, y después **ordenarlos por talla**. Podría revisarlos uno por uno con un `for`… o usar unos atajos geniales.
""",
"explanation": """
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
"examples": [
{"text": "Listas rápidas:",
 "code": """show([n * 2 for n in 1..5])
show([n for n in 1..10 if n % 2 == 0])

amigos = ["Blip", "Kora", "Zum"]
show([upper(a) for a in amigos])
"""},
{"text": "Los cupcakes que Menta ve con su lupa:",
 "code": """cupcakes = [
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
"exercises": [
{"task": "De `numeros = [3, 8, 15, 4, 23, 42]`, crea una lista `grandes` solo con los **mayores que 10**, usando una lista rápida, y muéstrala (debe dar `[15, 23, 42]`).",
 "starter": "numeros = [3, 8, 15, 4, 23, 42]\n\n# Crea la lista grandes\n",
 "solution": "numeros = [3, 8, 15, 4, 23, 42]\n\ngrandes = [n for n in numeros if n > 10]\nshow(grandes)\n",
 "checks": [
   {"kind": "runs", "text": "El programa funciona"},
   {"kind": "uses", "pattern": r"\[[^\]]*\bfor\b[^\]]*\bif\b", "text": "Usa una lista rápida con if", "hint": "[n for n in numeros if n > 10]"},
   {"kind": "output", "contains": "[15, 23, 42]", "text": "Muestra [15, 23, 42]"},
 ],
 "hints": ["[n for n in numeros if …]", "La condición es n > 10"]},
],
"remember": [
"Lista rápida: `[x * 2 for x in lista if condición]`.",
"Función sin nombre: `fx(x): …`, o `fx: it…` si recibe un solo dato.",
"`sorted(lista, fx: it.campo)` ordena por un campo.",
],
},

# ───────────────────────────────────────────────────────────── 14
{
"id": "errors", "title": "Errores: tus amigos que avisan",
"place": "El Puente de los Tropiezos",
"pose": "bandage", "bubble": "¡Me tropecé! Pero ya sé dónde no pisar.",
"story": """
El Puente de los Tropiezos tiene tablas sueltas, y Canela pisa justo la que no debía: ¡pum! Se pone una curita, mira bien la tabla y ya sabe dónde no pisar. Con los programas pasa igual: los errores no son malos. Son **amigos que avisan** qué hay que arreglar.
""",
"explanation": """
Cuando algo sale mal, Cupcake se detiene y te dice **en qué línea** y **qué pasó**, y muchas veces **cómo arreglarlo**. ¡Léelo con calma! Es como un amigo que te avisa.

Los mensajes de error están **en inglés**, como en casi todos los lenguajes de programación. Al principio cuesta un poco, pero ayuda a acostumbrarse: son siempre las mismas pocas palabras. Por ejemplo, si sumas un texto y un número, Cupcake dice:

```
can't add a text and a number. To join them, put them in a text:  "…{value}…"
```

Quiere decir: «no se puede sumar un texto y un número. Para juntarlos, ponlos dentro de un texto: `"…{valor}…"`».

**Atrapar un error.** Si sabes que algo puede fallar, como cuando alguien escribe letras en lugar de un número, puedes **intentarlo** con `try` y decir qué hacer si falla con `except`:

```
try:
    edad = int(read("¿Edad? "))
except error:
    show("Eso no es un número")
    edad = 0
```

**Avisar tú.** Con `raise` puedes provocar un error a propósito, cuando algo no tiene sentido. Tus propios mensajes pueden ir en español:

```
if bocas < 0:
    raise "Nadie tiene bocas negativas"
```

**Un valor de reserva.** Para casos simples, `else` dice qué usar si algo falla, en una sola línea:

```
edad = int(read("¿Edad? ")) else 0
```

**Comprobar.** `assert` revisa que algo sea verdad. Si no lo es, se detiene y te muestra los valores (`assert failed` significa «la comprobación falló»):

```
assert cupcakes >= 0
```
""",
"examples": [
{"text": "Un error a propósito. Ejecútalo y lee el mensaje con calma:",
 "expect": "error",
 "code": """bocas = 100
show("Tengo " + bocas + " bocas")
"""},
{"text": "Atrapar el error. La respuesta ya escrita es `muchas`, que no es un número. El mensaje dice `'muchas' is not a whole number` («“muchas” no es un número entero»):",
 "inputs": "muchas",
 "code": """try:
    bocas = int(read("¿Cuántas bocas tienes? "))
    show("Necesitas {bocas // 2} cajitas")
except error:
    show("Ups: {error}")
"""},
],
"exercises": [
{"task": "Pregunta la edad. Si la persona **no escribe un número**, en vez de detenerse, el programa debe mostrar `Eso no es un número`. La respuesta de prueba es `nueve`.",
 "inputs": "nueve",
 "starter": 'edad = int(read("¿Cuántos años tienes? "))\nshow("Tienes {edad} años")\n',
 "solution": 'try:\n    edad = int(read("¿Cuántos años tienes? "))\n    show("Tienes {edad} años")\nexcept error:\n    show("Eso no es un número")\n',
 "checks": [
   {"kind": "runs", "text": "El programa no se detiene con un error", "hint": "Pon el código debajo de try:, con sangría"},
   {"kind": "uses", "pattern": r"\btry\b", "text": "Usa try"},
   {"kind": "output", "contains": "Eso no es un número", "text": "Muestra «Eso no es un número»", "hint": "except error:  y debajo  show(\"Eso no es un número\")"},
 ],
 "hints": ["try:  (debajo lo que puede fallar)   except error:  (debajo qué hacer)", "Mueve las dos líneas debajo de try:, con sangría."]},
],
"remember": [
"Los mensajes de error dicen la línea, qué pasó y, muchas veces, cómo arreglarlo. Están en inglés, como en casi todos los lenguajes.",
"`try: … except error: …` atrapa un error; `algo else reserva` es la versión corta.",
"`raise \"mensaje\"` avisa; `assert condición` comprueba.",
],
},

# ───────────────────────────────────────────────────────────── 15
{
"id": "files", "title": "Usar otros archivos",
"place": "El Puerto de las Mochilas",
"pose": "backpack", "bubble": "Cada herramienta en su bolsillo, ¡y a viajar!",
"story": """
En el Puerto de las Mochilas, los viajeros preparan su equipaje antes de zarpar. Vainilla junta las herramientas que fuimos inventando (`cajitas`, `costo`, `saludar`…) y las guarda, bien etiquetadas, en un archivo aparte: una **mochila**. Así puede usarlas en cualquier programa sin escribirlas otra vez.
""",
"explanation": """
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
"examples": [
{"text": "Vainilla abre su mochila. Fíjate que `herramientas.cup` tiene un `main` con pruebas, pero no se ejecuta, porque aquí solo lo estamos usando:",
 "files": {"herramientas.cup": "fx cajitas(bocas):\n    return bocas // 2\n\nfx costo(bocas, precio):\n    return bocas * precio\n\nfx main():\n    show(\"Prueba:\", cajitas(10))\n"},
 "code": """use cajitas, costo from herramientas

show("Cajitas:", cajitas(100))
show("Costo:", costo(100, 3))
"""},
],
"exercises": [
{"task": "El archivo `saludos.cup` tiene una función `saludar(nombre)`. Úsala para saludar a **Blip**.",
 "files": {"saludos.cup": 'fx saludar(nombre):\n    show("¡Hola, {nombre}! Te damos la bienvenida a la Gran Pastelería.")\n'},
 "starter": "# Trae saludar desde saludos\n\n# Saluda a Blip\n",
 "solution": 'use saludar from saludos\n\nsaludar("Blip")\n',
 "checks": [
   {"kind": "runs", "text": "El programa funciona"},
   {"kind": "uses", "pattern": r"\buse\b", "text": "Usa use", "hint": "use saludar from saludos"},
   {"kind": "output", "contains": "¡Hola, Blip!", "text": "Saluda a Blip", "hint": "saludar(\"Blip\")"},
 ],
 "hints": ["use saludar from saludos", "Después: saludar(\"Blip\")"]},
],
"remember": [
"`use a, b from archivo` trae funciones de `archivo.cup`.",
"`use archivo` trae todo.",
"`fx main():` corre al ejecutar el archivo, pero no cuando otro lo usa.",
],
},

# ───────────────────────────────────────────────────────────── 16
{
"id": "random", "title": "Juegos de azar",
"place": "La Feria del Azar",
"pose": "dice", "bubble": "¡Tira los dados! A ver qué sale…",
"story": """
¡Luces, música y algodón de azúcar! En la Feria del Azar, Arándano armó juegos de dados y una ruleta de premios. Pero ¿cómo se programa algo cuando **no se sabe qué va a salir**? Tranquilo: la computadora también sabe jugar a la suerte.
""",
"explanation": """
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
"examples": [
{"text": "Los dados de Arándano. Ejecútalo varias veces:", "random": True,
 "code": """dado1 = roll(1, 6)
dado2 = roll(1, 6)
show("Salió {dado1} y {dado2}")

if dado1 == dado2:
    show("¡Dobles! Ganaste un cupcake extra")
"""},
{"text": "La ruleta de premios:", "random": True,
 "code": """premios = ["un cupcake", "una gorra", "un globo", "una medalla"]
show("¡Ganaste {pick(premios)}!")
"""},
{"text": "**Adivina el número.** Arándano piensa un número del 1 al 10, y tienes tres intentos. Escribe tus respuestas en **Respuestas** y ejecuta:", "random": True,
 "inputs": "5\n3\n8",
 "code": """secreto = roll(1, 10)
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
"exercises": [
{"task": "Lanza **dos dados** con `roll` y muestra la suma, así: `Suma: 7` (el número cambia cada vez).",
 "starter": "# Lanza dos dados y muestra la suma\n",
 "solution": 'dado1 = roll(1, 6)\ndado2 = roll(1, 6)\nshow("Suma: {dado1 + dado2}")\n',
 "checks": [
   {"kind": "runs", "text": "El programa funciona"},
   {"kind": "uses", "pattern": r"roll\(\s*1\s*,\s*6\s*\)[\s\S]*roll\(\s*1\s*,\s*6\s*\)", "text": "Lanza dos dados con roll(1, 6)", "hint": "dado1 = roll(1, 6) y dado2 = roll(1, 6)"},
   {"kind": "output", "contains": "Suma:", "text": "Muestra «Suma: …»", "hint": "show(\"Suma: {dado1 + dado2}\")"},
 ],
 "hints": ["Guarda cada dado en una variable: dado1 = roll(1, 6)", "show(\"Suma: {dado1 + dado2}\")"]},
],
"remember": [
"`roll(1, 6)` da un número al azar; `pick(lista)` elige un elemento al azar.",
"Con azar, cada ejecución puede ser distinta.",
],
},

# ───────────────────────────────────────────────────────────── 17
{
"id": "project", "title": "Proyecto final: la Gran Pastelería",
"place": "La Gran Pastelería",
"pose": "trophy", "bubble": "¡La Gran Pastelería abre hoy, gracias a ti!",
"story": """
¡Llegaste al final del camino de estrellas! Aquí está **la Gran Pastelería** de Frambuesa, y hoy abre sus puertas a monstruitos golosos con muchas bocas. Vainilla ordena, Canela pregunta, Menta revisa y Arándano inventa. Y tú vas a programarla, con todo lo que aprendiste en el viaje.
""",
"explanation": """
La pastelería necesita:
- una lista de **clientes**, cada uno un **registro** con su nombre y sus bocas;
- un **diccionario** con los precios de cada talla;
- una **función** que calcule cuánto paga cada cliente;
- un **ciclo** para atender a todos, y un **if** para dar descuento a los que tienen muchas bocas.

¡Todo lo que aprendiste, junto!
""",
"examples": [
{"text": "Un día en la Gran Pastelería:",
 "code": """precios = ["chica": 2, "mediana": 3, "grande": 5]

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
show("Hoy la Gran Pastelería ganó {ganancia} monedas")
"""},
],
"exercises": [
{"task": "Agrega un cliente nuevo a la lista: **Zib**, el primo de Argos, con **100 bocas** y talla **mediana**. Con el descuento, Zib debe pagar **270** monedas.",
 "starter": """precios = ["chica": 2, "mediana": 3, "grande": 5]

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
 "solution": """precios = ["chica": 2, "mediana": 3, "grande": 5]

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
   {"kind": "runs", "text": "El programa funciona"},
   {"kind": "output", "contains": "Zib paga 270 monedas", "text": "Zib paga 270 monedas",
    "hint": "clientes = add(clientes, (nombre: \"Zib\", bocas: 100, talla: \"mediana\"))"},
 ],
 "hints": ["Para agregar a una lista: lista = add(lista, nuevo)", "El nuevo cliente es un registro: (nombre: \"Zib\", bocas: 100, talla: \"mediana\")"]},
],
"remember": [
"¡Ya sabes programar! Variables, decisiones, ciclos, listas, diccionarios, registros, funciones y errores.",
"Ahora inventa tu propio programa: un juego, una lista de tareas, una calculadora… lo que imagines.",
],
},
]
