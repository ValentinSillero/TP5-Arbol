"""Ejercicio 23 de Arbol - criaturas de la mitologia griega."""

import sys

from tda_arbol import (
    buscar,
    busqueda_proximidad,
    eliminar_nodo,
    insertar_nodo,
)
from tda_cola import Cola, arribo, atencion, cola_vacia


# Cada registro contiene:
# [criatura, derrotado_por, descripcion, capturada_por]
DATOS_CRIATURAS = [
    ["Ceto", None],
    ["Tifón", "Zeus"],
    ["Equidna", "Argos Panoptes"],
    ["Dino", None],
    ["Pefredo", None],
    ["Enio", None],
    ["Escila", None],
    ["Caribdis", None],
    ["Euríale", None],
    ["Esteno", None],
    ["Medusa", "Perseo"],
    ["Ladón", "Heracles"],
    ["Águila del Cáucaso", None],
    ["Quimera", "Belerofonte"],
    ["Hidra de Lerna", "Heracles"],
    ["León de Nemea", "Heracles"],
    ["Esfinge", "Edipo"],
    ["Dragón de la Cólquida", None],
    ["Cerbero", None],
    ["Cerda de Cromión", "Teseo"],
    ["Ortro", "Heracles"],
    ["Toro de Creta", "Teseo"],
    ["Jabalí de Calidón", "Atalanta"],
    ["Carcinos", None],
    ["Gerión", "Heracles"],
    ["Cloto", None],
    ["Láquesis", None],
    ["Átropos", None],
    ["Minotauro de Creta", "Teseo"],
    ["Harpías", None],
    ["Argos Panoptes", "Hermes"],
    ["Aves del Estínfalo", None],
    ["Talos", "Medea"],
    ["Sirenas", None],
    ["Pitón", "Apolo"],
    ["Cierva de Cerinea", None],
    ["Basilisco", None],
    ["Jabalí de Erimanto", None],
]


def cargar_arbol(datos=DATOS_CRIATURAS):
    raiz = None
    for nombre, derrotado_por in datos:
        registro = [nombre, derrotado_por, "Sin descripción cargada", None]
        raiz = insertar_nodo(raiz, registro, 0)
    return raiz


def listado_criaturas_y_vencedores(raiz):
    """Punto a: listado alfabetico mediante recorrido inorden."""
    if raiz is not None:
        listado_criaturas_y_vencedores(raiz.izq)
        vencedor = raiz.info[1] if raiz.info[1] is not None else "No derrotada"
        print(f"{raiz.info[0]} - Derrotada por: {vencedor}")
        listado_criaturas_y_vencedores(raiz.der)


def cargar_descripcion(raiz, criatura, descripcion):
    """Punto b: permite cargar o reemplazar una descripcion breve."""
    nodo = buscar(raiz, criatura, 0)
    if nodo is None:
        return False
    nodo.info[2] = descripcion
    return True


def mostrar_criatura(nodo):
    """Muestra todos los campos de una criatura."""
    if nodo is None:
        print("Criatura no encontrada")
        return
    print("Nombre:", nodo.info[0])
    print("Derrotada por:", nodo.info[1] or "Nadie")
    print("Descripcion:", nodo.info[2])
    print("Capturada por:", nodo.info[3] or "Nadie")


def _contar_vencedores(raiz, cantidades):
    if raiz is not None:
        _contar_vencedores(raiz.izq, cantidades)
        vencedor = raiz.info[1]
        if vencedor is not None:
            pos = 0
            while pos < len(cantidades) and cantidades[pos][0] != vencedor:
                pos += 1
            if pos == len(cantidades):
                cantidades.append([vencedor, 1])
            else:
                cantidades[pos][1] += 1
        _contar_vencedores(raiz.der, cantidades)


def tres_mayores_vencedores(raiz):
    """Punto d: devuelve los tres vencedores con mas criaturas."""
    cantidades = []
    _contar_vencedores(raiz, cantidades)
    cantidades.sort(key=lambda dato: (-dato[1], dato[0].casefold()))
    return cantidades[:3]


def listar_derrotadas_por(raiz, vencedor):
    if raiz is not None:
        listar_derrotadas_por(raiz.izq, vencedor)
        if raiz.info[1] == vencedor:
            print(raiz.info[0])
        listar_derrotadas_por(raiz.der, vencedor)


def listar_no_derrotadas(raiz):
    if raiz is not None:
        listar_no_derrotadas(raiz.izq)
        if raiz.info[1] is None:
            print(raiz.info[0])
        listar_no_derrotadas(raiz.der)


def marcar_captura(raiz, criatura, captor):
    """Carga el campo capturada sin alterar la clave del arbol."""
    nodo = buscar(raiz, criatura, 0)
    if nodo is None:
        return False
    nodo.info[3] = captor
    return True


def capturar_criaturas_de_heracles(raiz):
    """Punto h, contemplando el nombre de la tabla: Cierva de Cerinea."""
    nombres = ["Cerbero", "Toro de Creta", "Cierva de Cerinea", "Jabalí de Erimanto"]
    for nombre in nombres:
        marcar_captura(raiz, nombre, "Heracles")


def actualizar_aves_del_estinfalo(raiz):
    nodo = buscar(raiz, "Aves del Estínfalo", 0)
    if nodo is not None:
        nodo.info[1] = "Heracles"
        nodo.info[2] = "Heracles derrotó a varias de estas aves mitológicas."
        return True
    return False


def renombrar_ladon(raiz):
    """Cambia una clave respetando eliminar-modificar-reinsertar."""
    raiz, registro = eliminar_nodo(raiz, "Ladón", 0)
    if registro is not None:
        registro[0] = "Dragón Ladón"
        raiz = insertar_nodo(raiz, registro, 0)
    return raiz


def listado_por_nivel(raiz):
    """Punto m: recorrido por nivel mediante el TDA Cola."""
    if raiz is None:
        return
    pendientes = Cola()
    arribo(pendientes, raiz)
    while not cola_vacia(pendientes):
        nodo = atencion(pendientes)
        print(nodo.info[0])
        if nodo.izq is not None:
            arribo(pendientes, nodo.izq)
        if nodo.der is not None:
            arribo(pendientes, nodo.der)


def listar_capturadas_por(raiz, captor):
    if raiz is not None:
        listar_capturadas_por(raiz.izq, captor)
        if raiz.info[3] == captor:
            print(raiz.info[0])
        listar_capturadas_por(raiz.der, captor)


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    raiz = cargar_arbol()

    print("EJERCICIO 23 - ARBOL DE CRIATURAS MITOLOGICAS")
    print("\na) Criaturas y quien las derroto (inorden):")
    listado_criaturas_y_vencedores(raiz)

    print("\nb) Carga de una descripcion breve para Talos:")
    cargar_descripcion(
        raiz,
        "Talos",
        "Gigante de bronce que protegía la isla de Creta.",
    )
    print("Descripcion cargada.")

    print("\nc) Informacion completa de Talos:")
    mostrar_criatura(buscar(raiz, "Talos", 0))

    print("\nd) Tres heroes o dioses con mas victorias:")
    for posicion, dato in enumerate(tres_mayores_vencedores(raiz), start=1):
        print(f"{posicion}. {dato[0]}: {dato[1]} criatura(s)")

    print("\ne) Criaturas derrotadas por Heracles:")
    listar_derrotadas_por(raiz, "Heracles")

    print("\nf) Criaturas no derrotadas:")
    listar_no_derrotadas(raiz)

    print("\ng-h) Campo capturada y capturas realizadas por Heracles:")
    capturar_criaturas_de_heracles(raiz)
    print("Capturas actualizadas.")

    print("\ni) Busqueda por coincidencia 'Dragón':")
    for nodo in busqueda_proximidad(raiz, "Dragón", 0):
        print(nodo.info[0])

    print("\nj) Eliminacion de Basilisco y Sirenas:")
    raiz, basilisco = eliminar_nodo(raiz, "Basilisco", 0)
    raiz, sirenas = eliminar_nodo(raiz, "Sirenas", 0)
    print("Eliminados:", basilisco[0], "y", sirenas[0])

    print("\nk) Actualizacion de Aves del Estinfalo:")
    actualizar_aves_del_estinfalo(raiz)
    mostrar_criatura(buscar(raiz, "Aves del Estínfalo", 0))

    print("\nl) Cambio de Ladon por Dragon Ladon:")
    raiz = renombrar_ladon(raiz)
    print("Nuevo nombre:", buscar(raiz, "Dragón Ladón", 0).info[0])

    print("\nm) Listado por nivel:")
    listado_por_nivel(raiz)

    print("\nn) Criaturas capturadas por Heracles:")
    listar_capturadas_por(raiz, "Heracles")


if __name__ == "__main__":
    main()
