<p align="center"><a href="README.md">English</a> · <b>Español</b></p>

<p align="center">
  <img src="logo/cupcake.svg" width="120" alt="Logo de Cupcake">
</p>

<h1 align="center">Cupcake</h1>

<p align="center">
  Un lenguaje de programación pequeño y amable, <b>sin clases, sin objetos y sin métodos</b>.<br>
  Solo <b>datos</b> y <b>funciones</b>, con errores amables que te dicen cómo arreglarlos.<br>
  <i>Versión 1.0 "Frambuesa"</i>
</p>

---

```
# La pastelería de Frambuesa
prices = ["small": 2, "medium": 3, "large": 5]

fx bill(mouths, size):
    total = mouths * (prices[size] else 0)
    if mouths >= 50:
        total -= total // 10          # 10% de descuento
    return total

fx main():
    name = read("¿Cómo te llamas? ")
    argos = (name: "Argos", mouths: 100, happy: true)

    if argos has mouths and happy:
        show("¡Hola, {name}! Argos paga {bill(argos.mouths, "small")} monedas")

    for i, flavor at ["fresa", "chocolate", "vainilla"]:
        show("{i}. {flavor}")
```

## Por qué Cupcake

- **Se lee como piensas.** `:` y sangría. `if`, `else if`, `else`, `when`, `for`, `while`.
- **Sin clases ni métodos.** Los datos son listas `[1, 2]`, diccionarios `["a": 1]` y registros `(name: "Menta", hp: 3)`. Todo lo demás es una función: `add(list, x)`, nunca `list.append(x)`.
- **Los datos se copian.** `b = a` hace una copia: nada cambia a tus espaldas.
- **Una sola forma de hacer cada cosa.** No hay atajos que memorizar.
- **Errores amables.** Te dicen la línea, qué pasó y cómo arreglarlo. Si escribes algo de otro lenguaje (`def`, `print`, `elif`, `list.append(x)`), Cupcake te dice cómo se escribe.

Las palabras del lenguaje y los mensajes de error están en inglés, como en casi todos los lenguajes de programación. El [curso en español](course/es) te explica cada uno.

## De un vistazo

| Qué | Cupcake |
|---|---|
| Mostrar y leer | `show("Hola")`, `name = read("Nombre: ")`, `age = read_num("Edad: ")` |
| Texto con valores | `"Hola, {name}"` |
| Decidir | `if … :` / `else if … :` / `else:` |
| Varios casos | `when color:` y debajo `is "red":`, `in 0..9:`, `is number:`, `else:` |
| Repetir | `for p in team:`, `for i, p at team:`, `while …:`, `repeat 3:` |
| Rangos | `1..10` (incluye el 10), `0..10 by 2`, `x in 0..10` |
| Funciones | `fx double(x):` y debajo `return x * 2` |
| Funciones sin nombre | `sorted(team, fx: it.hp)` |
| ¿Está ahí? | `"Pikachu" in team` |
| ¿Tiene algo? | `pika has hp`, `eevee has stone and friendship`, `team has hp` |
| ¿Qué es? | `x is number`, `list is empty` |
| Valor de repuesto | `int(text) else 0` |
| Errores | `try:` / `except error:` / `finally:`, `raise "mensaje"`, `assert x > 0` |
| Otros archivos | `use heal from pokemon` |
| Al ejecutar | `fx main():` solo corre cuando ejecutas ese archivo |

La referencia completa está en [SPEC.es.md](SPEC.es.md).

## Pruébalo

Solo necesitas **Python 3.8 o más nuevo**.

```
git clone https://github.com/cupcake-lang/cupcake.git
cd cupcake
python3 cupcake.py examples/hello.cup
```

Sin archivo, abre una consola donde escribes y ves el resultado al momento:

```
python3 cupcake.py
```

Para usarlo como comando (`cupcake archivo.cup`) en Linux o macOS:

```
chmod +x cupcake.py
ln -s "$PWD/cupcake.py" ~/.local/bin/cupcake
```

[`examples/`](examples) tiene programas completos: una Pokédex, un combate por turnos, una tienda y más.

## VS Code

La carpeta [`vscode-cupcake/`](vscode-cupcake) tiene una extensión con colores, sangría automática y fragmentos. Para instalarla:

```
python3 vscode-cupcake/pack.py
code --install-extension vscode-cupcake/cupcake-1.0.0.vsix
```

## El curso

[`course/`](course) tiene un curso para aprender a programar desde cero con Cupcake, para adultos y también para niños: un viaje por el Reino de Cupcake, con 17 lugares, muchos ejemplos con Pokémon y una galería de programas completos. Cada ejemplo se ejecuta y cada desafío se revisa solo, en el mismo navegador. Está en inglés y en español.

**Haz el curso en línea:** [en español](https://cupcake-lang.github.io/cupcake/es/) · [in English](https://cupcake-lang.github.io/cupcake/)

Para construirlo tú mismo:

```
python3 course/build.py
```

Luego abre `course/es/course.html` (español) o `course/en/course.html` (inglés) en tu navegador.

## Pruebas

```
python3 tests.py
```

## Cómo está hecho

El intérprete es un solo archivo y **tampoco usa clases**: solo funciones, diccionarios, listas y tuplas, igual que el lenguaje que implementa.

## Licencia

[MIT](LICENSE) © 2026 Jesús Denizard
