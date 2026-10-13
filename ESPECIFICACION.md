# Cupcake

**Versión 1.0 «Frambuesa»**

Un lenguaje de scripting con la comodidad de Python, pero **sin clases, sin objetos y sin métodos**. Solo hay **datos** y **funciones**.

Los archivos llevan la extensión `.cup`.

> Un cupcake es pequeño, dulce y se entiende de un vistazo: una porción completa, sin capas escondidas. Así quiere ser Cupcake: datos simples y funciones pequeñas, sin jerarquías ni nada escondido.

---

## 1. Las ideas

1. **Los datos son solo datos.** Un registro guarda campos y nada más: no tiene funciones dentro ni «sabe hacer» nada.
2. **Todo lo que hace algo es una función.** No existe `lista.append(x)`: se escribe `add(lista, x)`.
3. **Los datos se copian.** Si un dato cambió, se ve en la línea donde se le asignó. Nada cambia a escondidas.
4. **Se lee como una frase.** `"Pikachu" in equipo`, `if lista is empty`, `edad in 10..18`.
5. **Simple.** Cuando hay que elegir entre una forma corta y una clara, gana la clara.

---

## 2. Un programa completo

```
# Un pequeño equipo Pokémon en Cupcake

use describir from pokemon

equipo = [
    (nombre: "Pikachu",    tipo: "eléctrico", vida: 12),
    (nombre: "Charmander", tipo: "fuego",     vida: 39),
    (nombre: "Squirtle",   tipo: "agua",      vida: 0),
]

fx curar(p, cantidad):
    p.vida = min(p.vida + cantidad, 40)
    return p

vivos = [curar(p, 20) for p in equipo if p.vida > 0]

for p in sorted(vivos, fx: it.nombre):
    show(describir(p))

for p in equipo:
    when p.vida:
        is 0:
            estado = "necesita ir al Centro Pokémon"
        in 1..19:
            estado = "está débil"
        else:
            estado = "está bien"
    show("{p.nombre} {estado}")
```

---

## 3. Lo básico

```
# Un comentario

nombre = "Ash"
edad = 10
altura = 1.45
listo = true
ganador = none
```

| Qué | Cómo se escribe |
|---|---|
| Comentario | `# hasta el final de la línea` |
| Números | `10`, `1.45` |
| Texto | `"Hola"` o `'Hola'` |
| Texto de varias líneas | `"""…"""` |
| Sí, no, nada | `true`, `false`, `none` |

Una variable por línea: no existe `a, b = 1, 2`. Sí existen `+=`, `-=`, `*=` y `/=`.

### Texto con valores

**Cualquier texto** puede llevar valores entre llaves. No hace falta ninguna `f` delante.

```
show("{nombre} tiene {edad} años")             # Ash tiene 10 años
show("El año que viene tendrá {edad + 1}")     # El año que viene tendrá 11
show("Su primer Pokémon es {equipo[0].nombre}")
```

Entre llaves va cualquier cosa que dé un valor. Para escribir una llave de verdad: `\{`. Las llaves solo se usan **dentro de los textos**: los bloques de código van con sangría.

---

## 4. Operadores

| Qué | Operadores |
|---|---|
| Aritmética | `+  -  *  /  //  %  **` |
| Comparar | `==  !=  <  >  <=  >=` (de a una: `x > 0 and x < 10`) |
| Lógica | `and  or  not` |
| ¿Está ahí? | `x in lista`, `x not in lista` (también diccionarios, textos y campos: `"vida" in pika`) |
| ¿Tiene algo? | `pika has vida`, `pika has not vida`, `eevee has piedra and amistad` |
| ¿Qué es? | `x is number`, `x is not empty` |
| ¿Está entre? | `x in 1..10` (incluye los dos, también con decimales) |
| Desde… hasta | `1..10`, `0..10 by 2` |
| Valor de reserva | `algo else valor` |

### `in`: ¿está ahí?

```
"Pikachu" in equipo          # ¿está en la lista?
"pokeball" in precios        # ¿el diccionario tiene esa clave?
"chu" in "Pikachu"           # ¿el texto tiene esas letras?
"vida" in pika               # ¿el registro tiene ese campo?
edad in 0..12                # ¿está entre 0 y 12, contando los dos?
```

Con un rango sin `by`, `in` pregunta «¿está entre los dos?», también con decimales: `5.5 in 0..10` es `true`. Con `by` pregunta si es uno de esa lista: `4 in 0..10 by 2` es `true`, `3 in 0..10 by 2` es `false`.

### `has`: ¿tiene algo en ese campo?

`has` mira el valor de un campo y responde `true` o `false`:

```
pika = (nombre: "Pikachu", vida: 35, dormido: false)

pika has vida          # true:  35 es mayor que 0
pika has dormido       # false: vale false
pika has edad          # false: no tiene ese campo
pika has not dormido   # true
```

| El campo vale… | `has` da… |
|---|---|
| `true` / `false` | lo mismo |
| un número | `true` si es mayor que 0 |
| un texto, lista o diccionario | `true` si no está vacío |
| `none`, o el campo no existe | `false` |

Se pueden unir varios campos con `and` y `or`: `eevee has piedra and amistad`. Con una **lista** de registros, pregunta si **alguno** lo tiene: `equipo has vida` («¿me queda alguien que pueda pelear?»).

Para comparar, se usa el punto: `pika.nivel >= 36`. Si el nombre del campo está mal escrito, Cupcake avisa: «¿Quisiste decir «vida»?».

### `is`: qué es un dato

Después de `is` va un **tipo**: `number`, `text`, `bool`, `list`, `dict`, `record`, `function`, `none` o `empty` (una lista, diccionario o texto vacío).

```
if respuesta is number:
    …
if equipo is empty:
    show("No tienes Pokémon")
```

Para comparar **valores** se usa `==`: `color == "rojo"`. (Dentro de un `when`, los casos sí se escriben `is "rojo":`.)

### `else` como valor de reserva

Si lo de la izquierda **falla**, vale lo de la derecha:

```
edad = int(read("¿Edad? ")) else 0
precio = precios["mini"] else 0
```

---

## 5. Decidir

Los bloques van con **sangría**, como en Python: la línea que abre el bloque termina con `:`, y las de adentro van debajo, con 4 espacios más. El bloque termina cuando la sangría vuelve atrás. No hay punto y coma: cada instrucción termina con el salto de línea.

```
if edad >= 10:
    show("Ya puedes ser entrenador")
else if edad > 5:
    show("Casi")
else:
    show("Todavía no")
```

`else:` va a la misma altura que su `if`. Lo de adentro **siempre va en la línea de abajo**, con sangría, aunque sea una sola instrucción. La condición no necesita paréntesis, aunque se aceptan. Para un bloque que no hace nada, escribe `none`. Para lo contrario de una condición: `if not lluvia:`.

Las líneas dentro de `( )` o `[ ]` pueden seguir en la línea de abajo sin importar la sangría. Si la sangría no coincide, o falta el `:`, Cupcake avisa en qué línea.

### `if` y `when` no dan un valor

El valor se guarda dentro de cada caso. Así se ve claro qué variable cambia y dónde:

```
if vida > 0:
    estado = "vivo"
else:
    estado = "debilitado"
```

`estado = if …` da un aviso que explica cómo escribirlo.

### `when`: elegir según un valor

```
when color:
    is "rojo":
        show("¡Como la cereza de Cupi!")
    in ["naranja", "amarillo"]:
        show("Colores cálidos")
    else:
        show("Un color nuevo")
```

- `is valor`: igual a ese valor (o a varios: `is "a", "b"`);
- `is tipo`: de ese tipo (`is number`, `is empty`…);
- `in grupo`: dentro de una lista o un rango (`in 0..9`);
- `else`: si ninguno se cumple.

Lo que hace cada caso va debajo, con más sangría. Gana el **primer** caso que se cumpla. Para guardar un valor, se guarda dentro de cada caso:

```
when edad:
    in 0..9:
        etapa = "niño"
    in 10..17:
        etapa = "adolescente"
    else:
        etapa = "adulto"
```

**Varias cosas a la vez.** Se unen con `and`, y cada caso lleva un valor para cada una, también unidos con `and`. La coma sigue siendo «o»:

```
fx multiplicador(ataque, defensor):
    when ataque and defensor:
        is "agua" and "fuego", "fuego" and "planta", "planta" and "agua":
            return 2
        is "fuego" and "agua", "planta" and "fuego", "agua" and "planta":
            return 0.5
        else:
            return 1
```

También con tipos y grupos: `is number and text`, `in 0..5 and 6..10`. `is not` niega el caso entero.

---

## 6. Repetir

```
repeat 3:
    show("¡Hurra!")

while contador < 3:
    contador += 1

while cupcakes != bocas:
    cupcakes += 1

for p in equipo:
    show(p.nombre)

for i, p at equipo:          # i es la posición: 0, 1, 2…
    show("{i}: {p.nombre}")

for i at equipo:             # solo las posiciones
    show(i)

for i in 1..4:               # 1, 2, 3, 4
    show(i)
```

- `for x in grupo:` recorre **lo que hay**. `for i, x at lista:` recorre **las posiciones**, y da también lo que hay en cada una (la posición va primero).

- `break` sale del ciclo; `continue` salta a la siguiente vuelta.
- `stop` termina el programa.

### Desde… hasta: `..`

`a..b` va de `a` a `b`, **incluyendo los dos**. Con `by`, de a saltos:

```
1..4            # 1, 2, 3, 4
0..10 by 2      # 0, 2, 4, 6, 8, 10
5..1 by -1      # 5, 4, 3, 2, 1
```

---

## 7. Listas y diccionarios: corchetes

Los corchetes son para **colecciones**: cosas que crecen y se buscan con `[ ]`.

### Listas

```
equipo = ["Pikachu", "Charmander", "Squirtle", "Bulbasaur", "Eevee"]

equipo[0]         # "Pikachu"  (se cuenta desde 0)
equipo[-1]        # "Eevee"    (el último)
equipo[1..3]      # ["Charmander", "Squirtle", "Bulbasaur"]
equipo[2..]       # desde la 2 hasta el final
equipo[..1]       # desde el principio hasta la 1
```

### Diccionarios

**Agregando `clave:` delante de cada valor, la lista se vuelve diccionario.**

```
precios = ["pokeball": 200, "pocion": 300]
medallas = [1: "Roca", 2: "Cascada"]
vacio = [:]

precios["pokeball"]            # 200
precios["superball"] = 600     # un diccionario puede crecer
```

### Listas de comprensión

Como en Python. Con `clave:` delante, hacen un diccionario.

```
nombres = [p.nombre for p in equipo if p.vida > 0]
dobles = [i * 2 for i in 1..5]                 # [2, 4, 6, 8, 10]
vidas = [p.nombre: p.vida for p in equipo]     # diccionario
```

---

## 8. Registros: paréntesis

Los paréntesis con campos son **registros**: datos con forma fija, que se leen con punto.

```
pika = (nombre: "Pikachu", tipo: "eléctrico", vida: 35)

show(pika.nombre)          # Pikachu
pika.vida = 30             # se puede cambiar un campo
```

**Un registro nace con sus campos y no gana campos nuevos**:

```
pika.vdia = 10
```
```
Error, línea 1: el registro no tiene el campo «vdia». ¿Quisiste decir «vida»?
```

Para crear muchos registros con la misma forma, una función hace de molde:

```
fx pokemon(nombre, tipo, vida = 35):
    return (nombre: nombre, tipo: tipo, vida: vida)

pika = pokemon("Pikachu", "eléctrico")
charm = pokemon("Charmander", "fuego", vida = 39)
```

Cada signo tiene un solo trabajo:

| | `:` y sangría | Corchetes `[ ]` | Paréntesis `( )` |
|---|---|---|---|
| Qué son | **código**: bloques de `if`, `for`, `fx`… | **colecciones**: listas y diccionarios | **datos con nombre**: registros (y los datos de una función) |
| Ejemplo | `if x:` (y debajo, con sangría) | `[1, 2]`, `["a": 1]` | `(nombre: "Pikachu")` |
| Cómo se leen | — | `lista[0]`, `dic["clave"]` | `registro.campo` |
| ¿Crecen? | — | sí | no: nacen con sus campos |

---

## 9. Funciones: `fx`

```
fx saludar(nombre, saludo = "Hola"):
    show("{saludo}, {nombre}")

saludar("Ash")
saludar("Misty", saludo = "Buenas")
```

`return` devuelve un valor, y **siempre se escribe**. Una función sin `return` devuelve `none`. Si una línea de la función solo calcula algo y no lo usa (`x * 2`), Cupcake avisa que falta el `return`:

```
fx doble(x):
    return x * 2
```

Para devolver varios valores, se devuelve un registro:

```
fx dividir_con_resto(a, b):
    return (cociente: a // b, resto: a % b)

r = dividir_con_resto(17, 5)
show(r.cociente, r.resto)      # 3 2
```

El orden no importa: una función se puede usar antes de escribirla.

### Funciones sin nombre: `fx(…): …`

`fx` sin nombre es una función anónima. `λ` es lo mismo que `fx`. Si va en la misma línea, **da el valor de lo que tiene**, sin `return` (como `lambda` en Python). Es la única excepción a «el bloque va debajo», porque suele ir dentro de unos paréntesis.

```
vivos = filter(equipo, fx(p): p.vida > 0)
ordenados = sorted(equipo, λ(p): p.nombre)
sumar = fx(a, b): a + b
```

Si recibe **un solo dato**, se puede omitir el nombre: se llama `it` («eso»):

```
vivos = filter(equipo, fx: it.vida > 0)
```

### Una función no cambia nada de afuera

No existen `global` ni `nonlocal`. Una función recibe datos y devuelve datos.

---

## 10. Los datos se copian

Asignar o pasar un dato hace una **copia**. Cada nombre tiene su propio dato.

```
a = [1, 2]
b = a
b = add(b, 3)
show(a)      # [1, 2]
show(b)      # [1, 2, 3]
```

Por eso una función que cambia algo **lo devuelve**, y quien la llama decide guardarlo:

```
pika = curar(pika, 20)
```

---

## 11. Sin métodos

El punto solo sirve para los campos de un registro. Todo lo que hace algo es una función, con **el dato principal primero**.

```
equipo.append("Eevee")
```
```
Error, línea 1: Cupcake no tiene métodos: «.append(…)» no existe. Escribe:  equipo = add(equipo, "Eevee")
```

---

## 12. Mostrar, leer y archivos

```
nombre = read("¿Cómo te llamas? ")
show("Hola,", nombre)

edad = read_num("¿Cuántos años tienes? ")
```

- `show(…)` muestra lo que le pases; si son varias cosas, las separa con un espacio.
- `read("aviso")` muestra el aviso, espera a que la persona escriba algo, y lo devuelve como **texto**. El aviso no tiene que ser una pregunta: `read("Pulsa Enter para seguir…")`.
- `read_num("aviso")` insiste **hasta recibir un número**, y lo devuelve como número.
- `load("archivo.txt")` carga un archivo y devuelve su texto; `save("archivo.txt", texto)` lo guarda.

---

## 13. Errores: `try`, `except`, `finally`, `raise`, `assert`

```
try:
    edad = int(read("¿Edad? "))
except error:
    show("Eso no es un número: {error}")
    edad = 0
finally:
    show("Listo")
```

- `error` es un texto que explica qué falló. El nombre lo eliges tú, y se puede omitir: `except: …`.
- `finally` se ejecuta siempre, haya error o no. Es opcional.
- Para casos simples, basta el valor de reserva: `int(read("¿Edad? ")) else 0`.

Para provocar un error a propósito:

```
if edad < 0:
    raise "La edad no puede ser negativa"
```

Para comprobar algo que siempre debería ser verdad:

```
assert cantidad > 0
assert p.vida >= 0, "la vida no puede ser negativa"
```

Si no se cumple, el programa se detiene y dice qué falló y cuánto valía cada cosa.

---

## 14. Otros archivos: `use`

```
use curar, describir from pokemon      # trae solo esas dos
use curar as sanar from pokemon        # con otro nombre
use pokemon                            # trae todo
```

`pokemon` es el archivo `pokemon.cup` de la misma carpeta. Las funciones se usan directamente por su nombre: `curar(pika)`, nunca `pokemon.curar(pika)`.

### `main`: lo que corre al ejecutar el archivo

`main` es opcional. Si un archivo tiene `fx main():`, Cupcake la ejecuta al final, **solo cuando ejecutas ese archivo**. Si otro archivo lo usa con `use`, su `main` no corre:

```
# herramientas.cup
fx doble(x):
    return x * 2

fx main():
    show(doble(4))       # una prueba: solo corre con  cupcake herramientas.cup
```

`main` no recibe datos. (Es lo que Python hace con `if __name__ == "__main__":`.)

---

## 15. Funciones integradas

Todas en inglés, con el dato principal primero.

Si sabes el nombre en Python, es el mismo en Cupcake: solo se escribe `nombre(dato, …)` en vez de `dato.nombre(…)`. Las excepciones son `add` (en vez de `append`) y `drop` (en vez de `remove`), más cortas.

| Grupo | Funciones |
|---|---|
| Mostrar y leer | `show`, `read`, `read_num` |
| Números | `abs`, `round`, `min`, `max`, `sum` |
| Conversión | `int`, `float`, `str`, `bool` |
| Listas | `len`, `add`, `drop`, `sorted`, `reversed`, `filter`, `map`, `reduce`, `count`, `first`, `last` |
| Textos | `len`, `upper`, `lower`, `strip`, `split`, `join`, `replace` |
| Diccionarios | `keys`, `values`, `drop` |
| Azar | `roll(1, 6)`: un número entero al azar; `pick(lista)`: un elemento al azar |
| Archivos | `load`, `save` |

- `sorted(lista, clave)` acepta una función que dice por qué ordenar: `sorted(equipo, fx: it.vida)`.
- `count(lista, x)` cuenta cuántas veces está `x`; `count(lista, fx: …)` cuenta cuántos cumplen algo.

---

## 16. Las palabras reservadas

```
true  false  none  and  or  not  in  has  is
if  else  when  while  repeat  for  at  by
break  continue  return  stop
fx  λ
try  except  finally  raise  assert
use  from  as
```

---

## 17. Lo que Cupcake no tiene, a propósito

| No tiene | Porque |
|---|---|
| `class`, herencia, `self`, métodos | solo hay datos y funciones |
| `global`, `nonlocal` | una función no cambia nada de afuera |
| tuplas | bastan listas y registros |
| `a, b = 1, 2` | una variable por línea |
| `pass` | `none` |
| la tubería `\|>` | se prefiere paso a paso, con nombres |
| `del` | para quitar algo: `drop(…)` |
| `with` | depende de objetos; los archivos se leen con `load(…)` |
| `yield`, `async`, `await`, `type` | avanzados: quizás en otra versión |

---

## 18. Diferencias con Python, de un vistazo

| Python | Cupcake |
|---|---|
| `:` y sangría | `:` y sangría (igual) |
| `else`, `elif` | `else`, `else if` |
| `match` … `case _:` | `when` … `else` |
| `True`, `False`, `None` | `true`, `false`, `none` |
| `def` | `fx` |
| `lambda p: …` | `fx(p): …`, `fx: it…` o `λ(p): …` |
| `print`, `input` | `show`, `read` |
| `f"{x}"` | `"{x}"` |
| `{"a": 1}` | `["a": 1]` |
| `range(1, 4)` | `1..4` (incluye el 4) |
| `range(0, 11, 2)` | `0..10 by 2` |
| `lista[1:3]` | `lista[1..3]` (incluye la 3) |
| `for x in l` | `for x in l` |
| `for i, x in enumerate(l)` | `for i, x at l` |
| `match` | `when` |
| `class` | registros `(campo: valor)` |
| `p["nombre"]` | `p.nombre` |
| `lista.append(x)` | `add(lista, x)` |
| `x in lista` | `x in lista` |
| `0 < x < 10` | `x > 0 and x < 10`, o `x in 0..10` |
| `if __name__ == "__main__":` | `fx main():` |
| `isinstance(x, int)` | `x is number` |
| `len(l) == 0` | `l is empty` |
| `import x` / `from x import y` | `use x` / `use y from x` |
| `b = a` comparte | `b = a` copia |

---

## 19. Cómo está construido

- Un intérprete escrito en Python: `cupcake archivo.cup`. Sin archivo, abre una consola.
- **El intérprete tampoco usa clases:** solo funciones y datos, fiel al lenguaje que implementa.
- Errores en español, que dicen qué pasó y cómo arreglarlo. Si escribes una palabra de Python (`def`, `else`, `print`…), te dice cuál es la de Cupcake.
- Una extensión para VS Code con colores para `.cup`.
