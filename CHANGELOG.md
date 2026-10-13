# Cambios

## 1.0 «Frambuesa» — 2026

La primera versión pública de Cupcake.

- Bloques con `:` y sangría, como en Python. Lo de adentro siempre va en la línea de abajo.
- Decidir con `if`, `else if`, `else`; varios casos con `when` (`is`, `in`, `else`), también con varias cosas a la vez (`when ataque and defensor:`).
- Repetir con `for x in lista:`, `for i, x at lista:` (la posición primero), `while` y `repeat`.
- `in` pregunta si algo está ahí, también en rangos con decimales (`x in 0..10`).
- `has` pregunta si un campo tiene algo: `pika has vida`, `eevee has piedra and amistad`, y con listas, si alguno lo tiene.
- Las funciones devuelven con `return`; las funciones sin nombre en una línea (`fx: it.vida`) dan su valor.
- `fx main():` corre solo cuando ejecutas ese archivo, no cuando otro lo usa con `use`.
- `read` y `read_num` para leer lo que escribe la persona; `load` y `save` para archivos.
- Valor de reserva: `int(texto) else 0`.
- Errores en español, con la forma correcta cuando se escribe algo de Python o de versiones anteriores.
- Extensión para VS Code y un curso para aprender desde cero.
