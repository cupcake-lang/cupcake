"""
Más ejemplos para cada lección, en el mundo Pokémon.

POKEMON[id_de_la_lección] = lista de ejemplos, con el mismo formato que los de lecciones.py.
Aparecen en la página en una sección «Con Pokémon», después de los ejemplos de Cupi.
Los marcados con "azar": True dan un resultado distinto cada vez.
"""

POKEMON = {

"hola": [
{"texto": "El grito de todo entrenador:",
 "codigo": """show("¡Pikachu, te elijo a ti!")
show("Pika pika")
"""},
{"texto": "Una presentación, con una nota para personas:",
 "codigo": """# Ash se presenta
show("Hola, me llamo Ash")
show("Soy de Pueblo Paleta")
show("Y voy a ser el mejor Maestro Pokémon")
"""},
],

"cajas": [
{"texto": "Los datos de un Pokémon, cada uno en su caja:",
 "codigo": """pokemon = "Pikachu"
tipo = "eléctrico"
nivel = 5

show(pokemon, "es de tipo", tipo)
show("Está en el nivel", nivel)
"""},
{"texto": "¡Pikachu sube de nivel!",
 "codigo": """nivel = 5
show("Nivel antes de entrenar:", nivel)

nivel = nivel + 1
show("Nivel después de entrenar:", nivel)
"""},
{"texto": "Las variables también guardan textos largos:",
 "codigo": """entrenador = "Misty"
favorito = "Starmie"
ciudad = "Ciudad Celeste"

show(entrenador, "vive en", ciudad)
show("Su Pokémon favorito es", favorito)
"""},
],

"textos": [
{"texto": "Una ficha de Pokédex hecha con un texto:",
 "codigo": """nombre = "Charmander"
tipo = "fuego"
numero = 4
show("Pokédex #{numero}: {nombre}, de tipo {tipo}")
"""},
{"texto": "Cuentas dentro del texto:",
 "codigo": """nombre = "Squirtle"
vida = 44
dano = 12
show("{nombre} recibió {dano} de daño")
show("Le quedan {vida - dano} puntos de vida")
"""},
],

"cuentas": [
{"texto": "De compras en la Tienda Pokémon:",
 "codigo": """precio_pokeball = 200
cantidad = 5
total = precio_pokeball * cantidad

show("{cantidad} Poké Balls cuestan {total} monedas")
show("Con 1500 monedas te sobran {1500 - total}")
"""},
{"texto": "Experiencia y niveles: cada nivel necesita 100 puntos.",
 "codigo": """experiencia = 1250
por_nivel = 100

show("Subió {experiencia // por_nivel} niveles")
show("Y le sobran {experiencia % por_nivel} puntos")
"""},
{"texto": "Un ataque súper eficaz hace el doble de daño:",
 "codigo": """poder = 40
multiplicador = 2
show("Impactrueno hace {poder * multiplicador} de daño")
"""},
],

"preguntar": [
{"texto": "Elige tu Pokémon inicial. Las respuestas ya están en **Respuestas**:",
 "entradas": "Ash\nPikachu",
 "codigo": """entrenador = read("¿Cómo te llamas? ")
inicial = read("¿Cuál es tu Pokémon inicial? ")
show("¡{entrenador} eligió a {inicial}!")
"""},
{"texto": "Comprar Poké Balls:",
 "entradas": "3",
 "codigo": """cantidad = read_num("¿Cuántas Poké Balls quieres? ")
show("Son {cantidad * 200} monedas, por favor")
"""},
],

"decidir": [
{"texto": "¿Es súper eficaz? Cambia los tipos y prueba:",
 "codigo": """ataque = "agua"
defensor = "fuego"

if ataque == "agua" and defensor == "fuego":
    show("¡Es súper eficaz!")
else if ataque == defensor:
    show("No es muy eficaz…")
else:
    show("Es un ataque normal")
"""},
{"texto": "Con `when`, lo que dice el Profesor Oak de cada tipo:",
 "codigo": """tipo = "planta"

when tipo:
    is "fuego":
        show("Fuerte contra planta, débil contra agua")
    is "agua":
        show("Fuerte contra fuego, débil contra planta")
    is "planta":
        show("Fuerte contra agua, débil contra fuego")
    else:
        show("Ese tipo no lo conozco")
"""},
{"texto": "¿Cómo está de vida?",
 "codigo": """vida = 8
vida_maxima = 35

if vida == 0:
    show("Está debilitado: ¡al Centro Pokémon!")
else if vida in 1..10:
    show("¡Cuidado! Le queda poca vida")
else:
    show("Está listo para pelear")
"""},
],

"repetir": [
{"texto": "Pikachu está contento:",
 "codigo": """repeat 3:
    show("¡Pika!")
show("¡Pikachuuuu!")
"""},
{"texto": "Entrenando del nivel 14 al 18. En el 16, ¡Charmander evoluciona!",
 "codigo": """for nivel in 14..18:
    show("Charmander llegó al nivel {nivel}")
    if nivel == 16:
        show("   ¡Charmander evolucionó a Charmeleon!")
"""},
{"texto": "Un combate: ataca hasta que el rival se debilite.",
 "codigo": """vida_rival = 30
turno = 0

while vida_rival > 0:
    turno += 1
    vida_rival -= 12
    show("Turno {turno}: al rival le quedan {max(vida_rival, 0)}")
show("¡El rival se debilitó!")
"""},
],

"listas": [
{"texto": "El equipo de Ash:",
 "codigo": """equipo = ["Pikachu", "Bulbasaur", "Charmander"]
equipo = add(equipo, "Squirtle")

show("Ash tiene {len(equipo)} Pokémon")
for i, p at equipo:
    show("{i + 1}. {p}")
"""},
{"texto": "¿Ya lo atrapaste?",
 "codigo": """atrapados = ["Pidgey", "Rattata", "Pikachu", "Caterpie"]

show("Pikachu" in atrapados)
show("Mew" not in atrapados)
show("Los dos primeros:", atrapados[0..1])
"""},
{"texto": "Un Pokémon se va a vivir con el Profesor Oak:",
 "codigo": """equipo = ["Pikachu", "Bulbasaur", "Charmander", "Squirtle"]
equipo = drop(equipo, "Bulbasaur")
show(equipo)
show("¿Está vacío el equipo?", equipo is empty)
"""},
],

"diccionarios": [
{"texto": "Una Pokédex: el tipo de cada Pokémon.",
 "codigo": """pokedex = ["Pikachu": "eléctrico", "Squirtle": "agua", "Bulbasaur": "planta"]

show("Squirtle es de tipo", pokedex["Squirtle"])

pokedex["Eevee"] = "normal"
for nombre in keys(pokedex):
    show("{nombre}: {pokedex[nombre]}")
"""},
{"texto": "Buscar uno que no está, con un valor de reserva:",
 "codigo": """pokedex = ["Pikachu": "eléctrico", "Squirtle": "agua"]

show(pokedex["Pikachu"] else "desconocido")
show(pokedex["Mewtwo"] else "desconocido")
show("Mewtwo" in pokedex)
"""},
{"texto": "La tienda: precio de cada cosa.",
 "codigo": """tienda = ["pokeball": 200, "pocion": 300, "superball": 600]

total = tienda["pokeball"] * 3 + tienda["pocion"]
show("Tres Poké Balls y una Poción: {total} monedas")
"""},
],

"registros": [
{"texto": "Un Pokémon con todos sus datos:",
 "codigo": """pika = (nombre: "Pikachu", tipo: "eléctrico", nivel: 5, vida: 35)

show("{pika.nombre}, nivel {pika.nivel}, tipo {pika.tipo}")
pika.nivel += 1
show(pika)
"""},
{"texto": "Un equipo: una lista de registros.",
 "codigo": """equipo = [
    (nombre: "Pikachu", tipo: "eléctrico", nivel: 12),
    (nombre: "Bulbasaur", tipo: "planta", nivel: 10),
    (nombre: "Charmander", tipo: "fuego", nivel: 11),
]

for p in equipo:
    show("{p.nombre} ({p.tipo}) está en el nivel {p.nivel}")
"""},
{"texto": "Un registro dentro de otro: el entrenador y su Pokémon favorito.",
 "codigo": """ash = (
    nombre: "Ash",
    medallas: 8,
    favorito: (nombre: "Pikachu", nivel: 25)
)

show("{ash.nombre} tiene {ash.medallas} medallas")
show("Su favorito es {ash.favorito.nombre}, nivel {ash.favorito.nivel}")
"""},
],

"funciones": [
{"texto": "Una función que hace de molde para crear Pokémon:",
 "codigo": """fx pokemon(nombre, tipo, nivel = 5):
    return (nombre: nombre, tipo: tipo, nivel: nivel, vida: nivel * 7)

pika = pokemon("Pikachu", "eléctrico")
charizard = pokemon("Charizard", "fuego", nivel = 36)
show(pika)
show(charizard)
"""},
{"texto": "¿Cuánto daño hace un ataque?",
 "codigo": """fx dano(poder, nivel):
    return poder * nivel // 10

show("Impactrueno, nivel 10:", dano(40, 10))
show("Lanzallamas, nivel 36:", dano(90, 36))
"""},
{"texto": "Una función que decide, con `when`. Compara **dos cosas a la vez**, el ataque y el defensor, unidas con `and`:",
 "codigo": """fx multiplicador(ataque, defensor):
    when ataque and defensor:
        is "agua" and "fuego", "fuego" and "planta", "planta" and "agua":
            return 2
        is "fuego" and "agua", "planta" and "fuego", "agua" and "planta":
            return 0.5
        else:
            return 1

show(multiplicador("agua", "fuego"))
show(multiplicador("fuego", "agua"))
show(multiplicador("eléctrico", "planta"))
"""},
],

"copias": [
{"texto": "Un clon no cambia al original:",
 "codigo": """pika = (nombre: "Pikachu", vida: 35)
clon = pika
clon.nombre = "Pikachu clon"
clon.vida = 10

show(pika)
show(clon)
"""},
{"texto": "El Centro Pokémon cura y devuelve al Pokémon:",
 "codigo": """fx centro_pokemon(p):
    p.vida = p.vida_maxima
    return p

pika = (nombre: "Pikachu", vida: 3, vida_maxima: 35)
pika = centro_pokemon(pika)
show("{pika.nombre} tiene {pika.vida} de vida. ¡Como nuevo!")
"""},
],

"atajos": [
{"texto": "Los que están listos para pelear, en una línea:",
 "codigo": """equipo = [
    (nombre: "Pikachu", nivel: 12, vida: 30),
    (nombre: "Bulbasaur", nivel: 8, vida: 0),
    (nombre: "Charmander", nivel: 15, vida: 39),
]

listos = [p.nombre for p in equipo if p.vida > 0]
show("Listos:", listos)
show("Debilitados:", count(equipo, fx: it.vida == 0))
"""},
{"texto": "Ordenar el equipo por nivel, de mayor a menor:",
 "codigo": """equipo = [
    (nombre: "Pikachu", nivel: 12),
    (nombre: "Bulbasaur", nivel: 8),
    (nombre: "Charmander", nivel: 15),
]

for p in reversed(sorted(equipo, fx: it.nivel)):
    show("{p.nombre}: nivel {p.nivel}")
"""},
{"texto": "Subirle un nivel a todos, con `map`:",
 "codigo": """niveles = [5, 12, 30]
show(map(niveles, fx(n): n + 1))
show([n * 2 for n in niveles])
"""},
],

"errores": [
{"texto": "Buscar en la Pokédex algo que no está:",
 "codigo": """pokedex = ["Pikachu": "eléctrico"]

try:
    show(pokedex["Mew"])
except error:
    show("No está en la Pokédex: {error}")
"""},
{"texto": "Comprobar que no haya vida negativa:",
 "espera": "error",
 "codigo": """vida = 10
dano = 25
vida = vida - dano
assert vida >= 0, "la vida no puede ser negativa"
"""},
],

"archivos": [
{"texto": "Una Pokédex guardada en otro archivo:",
 "archivos": {"pokedex.cup": 'fx tipo_de(nombre):\n    tipos = ["Pikachu": "eléctrico", "Squirtle": "agua", "Charmander": "fuego"]\n    return tipos[nombre] else "desconocido"\n'},
 "codigo": """use tipo_de from pokedex

show("Pikachu:", tipo_de("Pikachu"))
show("Mewtwo:", tipo_de("Mewtwo"))
"""},
],

"azar": [
{"texto": "¡Un Pokémon salvaje aparece!", "azar": True,
 "codigo": """salvaje = pick(["Pidgey", "Rattata", "Caterpie", "Pikachu", "Abra"])
nivel = roll(2, 10)
show("¡Un {salvaje} salvaje de nivel {nivel} apareció!")
"""},
{"texto": "Lanzar una Poké Ball: atrapa con 40 % de probabilidad.", "azar": True,
 "codigo": """suerte = roll(1, 100)

if suerte <= 40:
    show("¡Bien! Atrapaste al Pokémon")
else:
    show("¡Oh, no! Se escapó de la Poké Ball")
"""},
{"texto": "Un mini combate con daño al azar.", "azar": True,
 "codigo": """vida_pikachu = 35
vida_rival = 35

while not (vida_pikachu <= 0 or vida_rival <= 0):
    vida_rival -= roll(5, 12)
    vida_pikachu -= roll(5, 12)

if vida_rival <= 0 and vida_pikachu > 0:
    show("¡Pikachu ganó!")
else if vida_pikachu <= 0 and vida_rival > 0:
    show("Pikachu perdió esta vez")
else:
    show("¡Empate! Los dos se debilitaron")
"""},
],

"proyecto": [
{"texto": "Cupi también vende para entrenadores Pokémon:",
 "codigo": """precios = ["pokeball": 200, "pocion": 300]

compras = [
    (entrenador: "Ash", cosa: "pokeball", cantidad: 5),
    (entrenador: "Misty", cosa: "pocion", cantidad: 2),
    (entrenador: "Brock", cosa: "superball", cantidad: 1),
]

for c in compras:
    precio = precios[c.cosa] else 0
    if precio == 0:
        show("{c.entrenador}: no vendemos {c.cosa}")
    else:
        show("{c.entrenador} paga {precio * c.cantidad} por {c.cantidad} {c.cosa}")
"""},
],
}
