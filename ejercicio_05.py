"""Ejercicio 5 de Arbol - superheroes y villanos del MCU."""

import sys

from tda_arbol import (
    buscar,
    busqueda_proximidad,
    contar_nodos,
    eliminar_nodo,
    insertar_nodo,
)


# Cada registro contiene [nombre, es_heroe].
# True indica heroe y False indica villano, como pide el enunciado.
PERSONAJES = [
    ["Iron Man", True],
    ["Thanos", False],
    ["Capitana Marvel", True],
    ["Loki", False],
    ["Capitán América", True],
    ["Ultron", False],
    ["Thor", True],
    ["Hela", False],
    ["Hulk", True],
    ["Red Skull", False],
    ["Black Widow", True],
    ["Killmonger", False],
    ["Doctor Strange", True],  # Nombre cargado incorrectamente.
    ["Ronan", False],
    ["Spider-Man", True],
    ["Black Panther", True],
]


def cargar_arbol(personajes=PERSONAJES):
    raiz = None
    for personaje in personajes:
        raiz = insertar_nodo(raiz, personaje.copy(), 0)
    return raiz


def listar_villanos(raiz):
    """Lista villanos alfabeticamente mediante un recorrido inorden."""
    if raiz is not None:
        listar_villanos(raiz.izq)
        if raiz.info[1] is False:
            print(raiz.info[0])
        listar_villanos(raiz.der)


def listar_heroes_con_c(raiz):
    """Muestra los heroes cuyos nombres comienzan con C."""
    if raiz is not None:
        listar_heroes_con_c(raiz.izq)
        if raiz.info[1] is True and raiz.info[0].casefold().startswith("c"):
            print(raiz.info[0])
        listar_heroes_con_c(raiz.der)


def contar_heroes(raiz):
    """Cuenta recursivamente los heroes almacenados."""
    if raiz is None:
        return 0
    cantidad = 1 if raiz.info[1] is True else 0
    return cantidad + contar_heroes(raiz.izq) + contar_heroes(raiz.der)


def corregir_doctor_strange(raiz):
    """Encuentra por proximidad, elimina, corrige y reinserta la clave."""
    coincidencias = busqueda_proximidad(raiz, "Doctor", 0)
    if not coincidencias:
        return raiz, None

    nombre_incorrecto = coincidencias[0].info[0]
    raiz, personaje = eliminar_nodo(raiz, nombre_incorrecto, 0)
    personaje[0] = "Dr. Strange"
    raiz = insertar_nodo(raiz, personaje, 0)
    return raiz, personaje[0]


def listar_heroes_descendente(raiz):
    """Lista heroes de Z a A mediante inorden inverso."""
    if raiz is not None:
        listar_heroes_descendente(raiz.der)
        if raiz.info[1] is True:
            print(raiz.info[0])
        listar_heroes_descendente(raiz.izq)


def generar_bosque(raiz, heroes=None, villanos=None):
    """Genera un arbol de heroes y otro de villanos."""
    if raiz is not None:
        heroes, villanos = generar_bosque(raiz.izq, heroes, villanos)
        if raiz.info[1] is True:
            heroes = insertar_nodo(heroes, raiz.info.copy(), 0)
        else:
            villanos = insertar_nodo(villanos, raiz.info.copy(), 0)
        heroes, villanos = generar_bosque(raiz.der, heroes, villanos)
    return heroes, villanos


def listar_nombres_inorden(raiz):
    """Lista solo los nombres en orden alfabetico."""
    if raiz is not None:
        listar_nombres_inorden(raiz.izq)
        print(raiz.info[0])
        listar_nombres_inorden(raiz.der)


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    raiz = cargar_arbol()

    print("EJERCICIO 5 - ARBOL DE PERSONAJES MCU")
    print("\nb) Villanos ordenados alfabeticamente:")
    listar_villanos(raiz)

    print("\nc) Superheroes que comienzan con C:")
    listar_heroes_con_c(raiz)

    print("\nd) Cantidad de superheroes:", contar_heroes(raiz))

    print("\ne) Busqueda por proximidad y correccion de Doctor Strange:")
    encontrados = busqueda_proximidad(raiz, "Doctor", 0)
    print("Encontrado:", encontrados[0].info[0] if encontrados else "ninguno")
    raiz, nombre_corregido = corregir_doctor_strange(raiz)
    print("Nombre corregido:", nombre_corregido)
    print("Comprobacion:", buscar(raiz, "Dr. Strange", 0).info[0])

    print("\nf) Superheroes en orden descendente:")
    listar_heroes_descendente(raiz)

    print("\ng) Bosque de superheroes y villanos:")
    heroes, villanos = generar_bosque(raiz)
    print("Cantidad de nodos del arbol de heroes:", contar_nodos(heroes))
    print("Cantidad de nodos del arbol de villanos:", contar_nodos(villanos))
    print("\nHeroes ordenados alfabeticamente:")
    listar_nombres_inorden(heroes)
    print("\nVillanos ordenados alfabeticamente:")
    listar_nombres_inorden(villanos)


if __name__ == "__main__":
    main()
