<p align="center">
  <img src="logo/cupcake.svg" width="120" alt="Logo de Cupcake">
</p>

<h1 align="center">Cupcake</h1>

<p align="center">
  Un lenguaje como Python, pero <b>sin clases, sin objetos y sin métodos</b>.<br>
  Solo <b>datos</b> y <b>funciones</b>, con errores en español que te dicen cómo arreglarlos.<br>
  <i>Versión 1.0 «Frambuesa»</i>
</p>

---

```
# La pastelería de Cupi
precios = ["chica": 2, "mediana": 3, "grande": 5]

fx cuenta(bocas, talla):
    total = bocas * (precios[talla] else 0)
    if bocas >= 50:
        total -= total // 10          # 10% de descuento
    return total

fx main():
    nombre = read("¿Cómo te llamas? ")
    argos = (nombre: "Argos", bocas: 100, feliz: true)

    if argos has bocas and feliz:
        show("¡Hola, {nombre}! Argos paga {cuenta(argos.bocas, "chica")} monedas")

    for i, sabor at ["fresa", "chocolate", "vainilla"]:
        show("{i}. {sabor}")
```

## Por qué Cupcake

- **Se lee como se piensa.** `:` y sangría, como en Python. `if`, `else if`, `else`, `when`, `for`, `while`.
- **Sin clases ni métodos.** Los datos son listas `[1, 2]`, diccionarios `["a": 1]` y registros `(nombre: "Cupi", vida: 3)`. Todo lo demás son funciones: `add(lista, x)`, nunca `lista.append(x)`.
- **Los datos se copian.** `b = a` hace una copia: nada cambia «a escondidas».
- **Una sola forma de hacer cada cosa.** Sin atajos que haya que memorizar.
- **Errores amables.** Dicen la línea, qué pasó y cómo arreglarlo. Si escribes algo de Python (`def`, `print`, `elif`, `lista.append(x)`), te dice cómo se escribe en Cupcake.

## Un vistazo

| Qué | Cupcake |
|---|---|
| Mostrar y leer | `show("Hola")`, `nombre = read("Nombre: ")`, `edad = read_num("Edad: ")` |
| Texto con valores | `"Hola, {nombre}"` |
| Decidir | `if … :` / `else if … :` / `else:` |
| Varios casos | `when color:` y debajo `is "rojo":`, `in 0..9:`, `is number:`, `else:` |
| Repetir | `for p in equipo:`, `for i, p at equipo:`, `while …:`, `repeat 3:` |
| Rangos | `1..10` (incluye el 10), `0..10 by 2`, `x in 0..10` |
| Funciones | `fx doble(x):` y debajo `return x * 2` |
| Funciones sin nombre | `sorted(equipo, fx: it.vida)` |
| ¿Está ahí? | `"Pikachu" in equipo` |
| ¿Tiene algo? | `pika has vida`, `eevee has piedra and amistad`, `equipo has vida` |
| ¿Qué es? | `x is number`, `lista is empty` |
| Valor de reserva | `int(texto) else 0` |
| Errores | `try:` / `except error:` / `finally:`, `raise "mensaje"`, `assert x > 0` |
| Otros archivos | `use curar from pokemon` |
| Al ejecutar | `fx main():` corre solo cuando ejecutas ese archivo |

La referencia completa está en [ESPECIFICACION.md](ESPECIFICACION.md).

## Cómo probarlo

Solo necesitas **Python 3.8 o más nuevo**.

```
git clone https://github.com/cupcake-lang/cupcake.git
cd cupcake
python3 cupcake.py ejemplos/hola.cup
```

Sin archivo, abre una consola donde escribes y ves el resultado al instante:

```
python3 cupcake.py
```

Para usarlo como comando (`cupcake archivo.cup`), en Linux o macOS:

```
chmod +x cupcake.py
ln -s "$PWD/cupcake.py" ~/.local/bin/cupcake
```

En [`ejemplos/`](ejemplos) hay programas completos: una Pokédex, un combate por turnos, una tienda y más.

## VS Code

La carpeta [`vscode-cupcake/`](vscode-cupcake) tiene una extensión con colores, sangría automática y atajos. Para instalarla:

```
python3 vscode-cupcake/empaquetar.py
code --install-extension vscode-cupcake/cupcake-1.0.0.vsix
```

## El curso

[`curso/`](curso) tiene un curso para aprender a programar desde cero con Cupcake, para niños y adultos, con Cupi, el cupcake, y muchos ejemplos de Pokémon. Cada ejemplo se puede ejecutar y cada desafío se comprueba solo, en el navegador. Para construirlo:

```
python3 curso/construir.py
```

Después abre `curso/curso.html` en el navegador.

## Pruebas

```
python3 pruebas.py
```

## Cómo está hecho

El intérprete está escrito en Python, en un solo archivo, y **tampoco usa clases**: solo funciones, diccionarios, listas y tuplas, igual que el lenguaje que implementa.

## Licencia

[MIT](LICENSE) © 2026 Jesús Denizard
