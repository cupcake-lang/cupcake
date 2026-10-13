[English](SPEC.md) · **Español**

# Cupcake

**Versión 1.0 "Frambuesa"**

Un lenguaje de scripting pequeño y cómodo **sin clases, sin objetos y sin métodos**. Solo hay **datos** y **funciones**.

Los archivos usan la extensión `.cup`.

> Un cupcake es pequeño, dulce y se entiende de un vistazo: una porción entera, sin capas ocultas. Eso es lo que Cupcake quiere ser: datos simples y funciones pequeñas, sin jerarquías y sin nada escondido.

---

## 1. Las ideas

1. **Los datos son solo datos.** Un registro guarda campos y nada más: no tiene funciones adentro y no "sabe hacer" nada.
2. **Todo lo que hace algo es una función.** No existe `list.append(x)`: se escribe `add(list, x)`.
3. **Los datos se copian.** Si un dato cambió, lo ves en la línea donde se asignó. Nada cambia a tus espaldas.
4. **Se lee como una frase.** `"Pikachu" in team`, `if list is empty`, `age in 10..18`.
5. **Simple.** Cuando hay que elegir entre una forma corta y una forma clara, gana la clara.

---

## 2. Un programa completo

```
# Un pequeño equipo Pokémon en Cupcake

use describe from pokemon

team = [
    (name: "Pikachu",    type: "eléctrico", hp: 12),
    (name: "Charmander", type: "fuego",     hp: 39),
    (name: "Squirtle",   type: "agua",      hp: 0),
]

fx heal(p, amount):
    p.hp = min(p.hp + amount, 40)
    return p

alive = [heal(p, 20) for p in team if p.hp > 0]

for p in sorted(alive, fx: it.name):
    show(describe(p))

for p in team:
    when p.hp:
        is 0:
            status = "tiene que ir al Centro Pokémon"
        in 1..19:
            status = "está débil"
        else:
            status = "está bien"
    show("{p.name} {status}")
```

---

## 3. Lo básico

```
# Un comentario

name = "Ash"
age = 10
height = 1.45
ready = true
winner = none
```

| Qué | Cómo se escribe |
|---|---|
| Comentario | `# hasta el final de la línea` |
| Números | `10`, `1.45` |
| Texto | `"Hola"` o `'Hola'` |
| Texto de varias líneas | `"""…"""` |
| Sí, no, nada | `true`, `false`, `none` |

Una variable por línea: no existe `a, b = 1, 2`. Pero `+=`, `-=`, `*=` y `/=` sí existen.

### Texto con valores

**Cualquier texto** puede llevar valores entre llaves. No hace falta ninguna `f` adelante.

```
show("{name} tiene {age} años")                # Ash tiene 10 años
show("El año que viene tendrá {age + 1}")      # El año que viene tendrá 11
show("Su primer Pokémon es {team[0].name}")
```

Entre las llaves puede ir cualquier cosa que dé un valor. Para escribir una llave de verdad: `\{`. Las llaves solo se usan **dentro del texto**: los bloques de código usan la sangría.

---

## 4. Operadores

| Qué | Operadores |
|---|---|
| Aritmética | `+  -  *  /  //  %  **` |
| Comparar | `==  !=  <  >  <=  >=` (de a uno: `x > 0 and x < 10`) |
| Lógica | `and  or  not` |
| ¿Está ahí? | `x in list`, `x not in list` (también diccionarios, texto y campos: `"hp" in pika`) |
| ¿Tiene algo? | `pika has hp`, `pika has not hp`, `eevee has stone and friendship` |
| ¿Qué es? | `x is number`, `x is not empty` |
| ¿Está entre? | `x in 1..10` (incluye ambos extremos, también decimales) |
| Desde… hasta | `1..10`, `0..10 by 2` |
| Valor de respaldo | `algo else valor` |

### `in`: ¿está ahí?

```
"Pikachu" in team            # ¿está en la lista?
"pokeball" in prices         # ¿el diccionario tiene esa clave?
"chu" in "Pikachu"           # ¿el texto contiene esas letras?
"hp" in pika                 # ¿el registro tiene ese campo?
age in 0..12                 # ¿está entre 0 y 12, ambos incluidos?
```

Con un rango sin `by`, `in` pregunta "¿está entre los dos?", también con decimales: `5.5 in 0..10` es `true`. Con `by` pregunta si es uno de los valores de esa lista: `4 in 0..10 by 2` es `true`, `3 in 0..10 by 2` es `false`.

### `has`: ¿hay algo en ese campo?

`has` mira el valor de un campo y responde `true` o `false`:

```
pika = (name: "Pikachu", hp: 35, asleep: false)

pika has hp            # true:  35 es mayor que 0
pika has asleep        # false: es false
pika has age           # false: no existe ese campo
pika has not asleep    # true
```

| Si el campo es… | `has` da… |
|---|---|
| `true` / `false` | lo mismo |
| un número | `true` si es mayor que 0 |
| un texto, una lista o un diccionario | `true` si no está vacío |
| `none`, o el campo no existe | `false` |

Se pueden combinar varios campos con `and` y `or`: `eevee has stone and friendship`. Con una **lista** de registros, pregunta si **alguno** lo tiene: `team has hp` ("¿todavía me queda alguien que pueda pelear?").

Para comparar, se usa el punto: `pika.level >= 36`. Si el nombre del campo está mal escrito, Cupcake te avisa: "Did you mean 'hp'?" ("¿Quisiste decir 'hp'?").

### `is`: qué tipo de dato es

Después de `is` va un **tipo**: `number`, `text`, `bool`, `list`, `dict`, `record`, `function`, `none` o `empty` (una lista, un diccionario o un texto vacíos).

```
if answer is number:
    …
if team is empty:
    show("No tienes ningún Pokémon")
```

Para comparar **valores**, se usa `==`: `color == "rojo"`. (Dentro de un `when`, los casos se escriben `is "rojo":`.)

### `else` como valor de respaldo

Si el lado izquierdo **falla**, obtienes el lado derecho:

```
age = int(read("¿Edad? ")) else 0
price = prices["mini"] else 0
```

---

## 5. Tomar decisiones

Los bloques usan **sangría**: la línea que abre un bloque termina en `:`, y las líneas de adentro van debajo, 4 espacios más adentro. El bloque termina cuando la sangría retrocede. No hay punto y coma: cada instrucción termina con el salto de línea.

```
if age >= 10:
    show("Puedes ser entrenador")
else if age > 5:
    show("Casi")
else:
    show("Todavía no")
```

`else:` se alinea con su `if`. El cuerpo **siempre va en la línea de abajo**, con sangría, aunque sea una sola instrucción. La condición no necesita paréntesis, aunque se permiten. Para un bloque que no hace nada, se escribe `none`. Para lo contrario de una condición: `if not raining:`.

Las líneas dentro de `( )` o `[ ]` pueden seguir en la línea siguiente, con cualquier sangría. Si la sangría no coincide, o falta el `:`, Cupcake te dice en qué línea.

### `if` y `when` no dan un valor

El valor se guarda dentro de cada caso. Así queda claro qué variable cambia y dónde:

```
if hp > 0:
    status = "vivo"
else:
    status = "debilitado"
```

`status = if …` da un error que explica cómo escribirlo.

### `when`: elegir según un valor

```
when color:
    is "rojo":
        show("¡Como la cereza de Frambuesa!")
    in ["naranja", "amarillo"]:
        show("Colores cálidos")
    else:
        show("Un color nuevo")
```

- `is valor`: igual a ese valor (o a uno de varios: `is "a", "b"`);
- `is tipo`: de ese tipo (`is number`, `is empty`…);
- `in grupo`: dentro de una lista o un rango (`in 0..9`);
- `else`: si ninguno coincide.

Lo que hace cada caso va debajo, con más sangría. Gana el **primer** caso que coincide. Para guardar un valor, se guarda dentro de cada caso:

```
when age:
    in 0..9:
        stage = "niño"
    in 10..17:
        stage = "adolescente"
    else:
        stage = "adulto"
```

**Varias cosas a la vez.** Se unen con `and`, y cada caso tiene un valor para cada una, también unidos con `and`. La coma sigue significando "o":

```
fx multiplier(attack, defender):
    when attack and defender:
        is "agua" and "fuego", "fuego" and "planta", "planta" and "agua":
            return 2
        is "fuego" and "agua", "planta" and "fuego", "agua" and "planta":
            return 0.5
        else:
            return 1
```

También funcionan los tipos y los grupos: `is number and text`, `in 0..5 and 6..10`. `is not` niega el caso entero.

---

## 6. Repetir

```
repeat 3:
    show("¡Hurra!")

while counter < 3:
    counter += 1

while cupcakes != mouths:
    cupcakes += 1

for p in team:
    show(p.name)

for i, p at team:            # i es la posición: 0, 1, 2…
    show("{i}: {p.name}")

for i at team:               # solo las posiciones
    show(i)

for i in 1..4:               # 1, 2, 3, 4
    show(i)
```

- `for x in grupo:` recorre **lo que hay**. `for i, x at lista:` recorre **las posiciones**, y además te da lo que hay en cada una (la posición va primero).

- `break` sale del bucle; `continue` salta a la siguiente vuelta.
- `stop` termina el programa.

### Desde… hasta: `..`

`a..b` va de `a` a `b`, **incluyendo ambos**. Con `by`, de a saltos:

```
1..4            # 1, 2, 3, 4
0..10 by 2      # 0, 2, 4, 6, 8, 10
5..1 by -1      # 5, 4, 3, 2, 1
```

---

## 7. Listas y diccionarios: corchetes

Los corchetes son para **colecciones**: cosas que crecen y se consultan con `[ ]`.

### Listas

```
team = ["Pikachu", "Charmander", "Squirtle", "Bulbasaur", "Eevee"]

team[0]           # "Pikachu"  (se cuenta desde 0)
team[-1]          # "Eevee"    (el último)
team[1..3]        # ["Charmander", "Squirtle", "Bulbasaur"]
team[2..]         # desde la posición 2 hasta el final
team[..1]         # desde el principio hasta la posición 1
```

### Diccionarios

**Pon `clave:` delante de cada valor y la lista se convierte en un diccionario.**

```
prices = ["pokeball": 200, "potion": 300]
badges = [1: "Roca", 2: "Cascada"]
empty = [:]

prices["pokeball"]             # 200
prices["greatball"] = 600      # un diccionario puede crecer
```

### Listas por comprensión

Con `clave:` delante, forman un diccionario.

```
names = [p.name for p in team if p.hp > 0]
doubles = [i * 2 for i in 1..5]                # [2, 4, 6, 8, 10]
hps = [p.name: p.hp for p in team]             # diccionario
```

---

## 8. Registros: paréntesis

Los paréntesis con campos son **registros**: datos con una forma fija, que se leen con un punto.

```
pika = (name: "Pikachu", type: "eléctrico", hp: 35)

show(pika.name)            # Pikachu
pika.hp = 30               # se puede cambiar un campo
```

**Un registro nace con sus campos y no recibe campos nuevos**:

```
pika.hpp = 10
```
```
Error in archivo.cup, line 2:
    pika.hpp = 10
  the record has no field 'hpp'. Did you mean 'hp'? A record is born with its fields and doesn't get new ones.
```

(El intérprete habla en inglés: "el registro no tiene el campo 'hpp'. ¿Quisiste decir 'hp'? Un registro nace con sus campos y no recibe campos nuevos.")

Para hacer muchos registros con la misma forma, una función sirve de molde:

```
fx pokemon(name, type, hp = 35):
    return (name: name, type: type, hp: hp)

pika = pokemon("Pikachu", "eléctrico")
charm = pokemon("Charmander", "fuego", hp = 39)
```

Cada símbolo tiene un solo trabajo:

| | `:` y sangría | Corchetes `[ ]` | Paréntesis `( )` |
|---|---|---|---|
| Qué son | **código**: bloques de `if`, `for`, `fx`… | **colecciones**: listas y diccionarios | **datos con nombre**: registros (y las entradas de una función) |
| Ejemplo | `if x:` (y debajo, con sangría) | `[1, 2]`, `["a": 1]` | `(name: "Pikachu")` |
| Cómo se leen | — | `list[0]`, `dict["clave"]` | `registro.campo` |
| ¿Crecen? | — | sí | no: nacen con sus campos |

---

## 9. Funciones: `fx`

```
fx greet(name, greeting = "Hola"):
    show("{greeting}, {name}")

greet("Ash")
greet("Misty", greeting = "Buenas tardes")
```

`return` devuelve un valor, y **siempre se escribe**. Una función sin `return` devuelve `none`. Si una línea de la función solo calcula algo y no lo usa (`x * 2`), Cupcake te avisa que falta el `return`:

```
fx double(x):
    return x * 2
```

Para devolver varios valores, devuelve un registro:

```
fx divide_with_remainder(a, b):
    return (quotient: a // b, remainder: a % b)

r = divide_with_remainder(17, 5)
show(r.quotient, r.remainder)      # 3 2
```

El orden no importa: puedes usar una función antes de escribirla.

### Funciones sin nombre: `fx(…): …`

`fx` sin nombre es una función anónima. `λ` es lo mismo que `fx`. Si está en la misma línea, **da el valor de lo que contiene**, sin `return`. Es la única excepción a "el bloque va debajo", porque suele ir dentro de paréntesis.

```
alive = filter(team, fx(p): p.hp > 0)
by_name = sorted(team, λ(p): p.name)
plus = fx(a, b): a + b
```

Si recibe **una sola entrada**, puedes omitir el nombre: se llama `it`:

```
alive = filter(team, fx: it.hp > 0)
```

### Una función no cambia nada fuera de ella

No existen `global` ni `nonlocal`. Una función recibe datos y devuelve datos.

---

## 10. Los datos se copian

Asignar o pasar un dato hace una **copia**. Cada nombre tiene sus propios datos.

```
a = [1, 2]
b = a
b = add(b, 3)
show(a)      # [1, 2]
show(b)      # [1, 2, 3]
```

Por eso una función que cambia algo **lo devuelve**, y quien la llama decide si lo guarda:

```
pika = heal(pika, 20)
```

---

## 11. Sin métodos

El punto es solo para los campos de un registro. Todo lo que hace algo es una función, con **el dato principal primero**.

```
team.append("Eevee")
```
```
Error in archivo.cup, line 2:
    team.append("Eevee")
  Cupcake has no methods: '.append(…)' doesn't exist. Write:  team = add(team, "Eevee")
```

(En español: "Cupcake no tiene métodos: '.append(…)' no existe. Escribe: `team = add(team, "Eevee")`".)

---

## 12. Mostrar, leer y archivos

```
name = read("¿Cómo te llamas? ")
show("Hola,", name)

age = read_num("¿Cuántos años tienes? ")
```

- `show(…)` muestra lo que le des; si son varias cosas, las separa con un espacio.
- `read("mensaje")` muestra el mensaje, espera a que la persona escriba algo y lo devuelve como **texto**. El mensaje no tiene que ser una pregunta: `read("Presiona Enter para continuar…")`.
- `read_num("mensaje")` sigue preguntando **hasta que recibe un número**, y lo devuelve como número.
- `load("archivo.txt")` carga un archivo y devuelve su texto; `save("archivo.txt", text)` lo guarda.

---

## 13. Errores: `try`, `except`, `finally`, `raise`, `assert`

```
try:
    age = int(read("¿Edad? "))
except error:
    show("Eso no es un número: {error}")
    age = 0
finally:
    show("Listo")
```

- `error` es un texto que explica qué salió mal. El nombre lo eliges tú, y lo puedes omitir: `except: …`.
- `finally` siempre se ejecuta, haya habido un error o no. Es opcional.
- Para casos simples, alcanza con el valor de respaldo: `int(read("¿Edad? ")) else 0`.

Para provocar un error a propósito:

```
if age < 0:
    raise "La edad no puede ser negativa"
```

Para comprobar algo que siempre debería ser cierto:

```
assert amount > 0
assert p.hp >= 0, "hp no puede ser negativo"
```

Si no es cierto, el programa se detiene y te dice qué falló y cuánto valía cada cosa:

```
Error in archivo.cup, line 2:
    assert amount > 0
  assert failed: amount > 0
  amount is 0
```

(Es decir: falló el `assert` `amount > 0`, y `amount` valía 0.)

---

## 14. Otros archivos: `use`

```
use heal, describe from pokemon        # trae solo esas dos
use heal as cure from pokemon          # con otro nombre
use pokemon                            # trae todo
```

`pokemon` es el archivo `pokemon.cup` en la misma carpeta. Las funciones se usan directamente por su nombre: `heal(pika)`, nunca `pokemon.heal(pika)`.

### `main`: lo que se ejecuta cuando ejecutas el archivo

`main` es opcional. Si un archivo tiene `fx main():`, Cupcake lo ejecuta al final, **solo cuando ejecutas ese archivo**. Si otro archivo lo trae con `use`, su `main` no se ejecuta:

```
# tools.cup
fx double(x):
    return x * 2

fx main():
    show(double(4))       # una prueba: solo se ejecuta con  cupcake tools.cup
```

`main` no recibe entradas.

---

## 15. Funciones incorporadas

Todas en inglés, con el dato principal primero.

No hay métodos: siempre se escribe `nombre(dato, …)`, nunca `dato.nombre(…)`.

| Grupo | Funciones |
|---|---|
| Mostrar y leer | `show`, `read`, `read_num` |
| Números | `abs`, `round`, `min`, `max`, `sum` |
| Conversión | `int`, `float`, `str`, `bool` |
| Listas | `len`, `add`, `drop`, `sorted`, `reversed`, `filter`, `map`, `reduce`, `count`, `first`, `last` |
| Texto | `len`, `upper`, `lower`, `strip`, `split`, `join`, `replace` |
| Diccionarios | `keys`, `values`, `drop` |
| Azar | `roll(1, 6)`: un número entero al azar; `pick(list)`: un elemento al azar |
| Archivos | `load`, `save` |

- `sorted(list, key)` recibe una función que dice por qué ordenar: `sorted(team, fx: it.hp)`.
- `count(list, x)` cuenta cuántas veces aparece `x`; `count(list, fx: …)` cuenta cuántos cumplen algo.

---

## 16. Palabras reservadas

```
true  false  none  and  or  not  in  has  is
if  else  when  while  repeat  for  at  by
break  continue  return  stop
fx  λ
try  except  finally  raise  assert
use  from  as
```

---

## 17. Lo que Cupcake deja fuera, a propósito

| No tiene | Porque |
|---|---|
| `class`, herencia, `self`, métodos | solo hay datos y funciones |
| `global`, `nonlocal` | una función no cambia nada fuera de ella |
| tuplas | alcanza con listas y registros |
| `a, b = 1, 2` | una variable por línea |
| `pass` | `none` |
| el pipe `\|>` | se prefiere paso a paso, con nombres |
| `del` | para quitar algo: `drop(…)` |
| `with` | depende de objetos; los archivos se leen con `load(…)` |
| `yield`, `async`, `await`, `type` | avanzados: quizás en una versión futura |

---

## 18. Cómo está hecho

- Un intérprete: `cupcake archivo.cup`. Sin archivo, abre una consola.
- **El intérprete tampoco usa clases:** solo funciones y datos, fiel al lenguaje que implementa.
- Mensajes de error que dicen qué pasó y cómo arreglarlo. Si escribes una palabra de otro lenguaje (`def`, `elif`, `print`…), te dice la de Cupcake.
- Una extensión para VS Code con colores de sintaxis para `.cup`.
