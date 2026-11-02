"""TDA arbol binario de busqueda AVL basado en el capitulo X del libro.

La raiz se representa con una variable que apunta a ``nodoArbol`` o vale
``None``. La informacion puede ser un valor simple o una lista. Cuando se
utiliza una lista, ``campo`` indica la posicion que funciona como clave.
"""

from tda_cola import Cola, arribo, atencion, cola_vacia


class nodoArbol(object):
    """Nodo del arbol con informacion, hijos y altura AVL."""

    def __init__(self, info):
        self.izq = None
        self.der = None
        self.info = info
        self.altura = 0


def _clave(info, campo):
    """Obtiene la clave de ordenamiento de la informacion del nodo."""
    if campo is None:
        return info
    return info[campo]


def altura(raiz):
    """Devuelve la altura de un nodo."""
    if raiz is None:
        return -1
    return raiz.altura


def actualizaraltura(raiz):
    """Actualiza la altura de un nodo."""
    if raiz is not None:
        alt_izq = altura(raiz.izq)
        alt_der = altura(raiz.der)
        raiz.altura = (alt_izq if alt_izq > alt_der else alt_der) + 1


def rotar_simple(raiz, control):
    """Realiza una rotacion simple a la derecha o a la izquierda."""
    if control:
        aux = raiz.izq
        raiz.izq = aux.der
        aux.der = raiz
    else:
        aux = raiz.der
        raiz.der = aux.izq
        aux.izq = raiz

    actualizaraltura(raiz)
    actualizaraltura(aux)
    raiz = aux
    return raiz


def rotar_doble(raiz, control):
    """Realiza una rotacion doble a la derecha o a la izquierda."""
    if control:
        raiz.izq = rotar_simple(raiz.izq, False)
        raiz = rotar_simple(raiz, True)
    else:
        raiz.der = rotar_simple(raiz.der, True)
        raiz = rotar_simple(raiz, False)
    return raiz


def balancear(raiz):
    """Determina que rotacion debe aplicarse para balancear el arbol."""
    if raiz is not None:
        if altura(raiz.izq) - altura(raiz.der) == 2:
            if altura(raiz.izq.izq) >= altura(raiz.izq.der):
                raiz = rotar_simple(raiz, True)
            else:
                raiz = rotar_doble(raiz, True)
        elif altura(raiz.der) - altura(raiz.izq) == 2:
            if altura(raiz.der.der) >= altura(raiz.der.izq):
                raiz = rotar_simple(raiz, False)
            else:
                raiz = rotar_doble(raiz, False)
    return raiz


def insertar_nodo(raiz, dato, campo=None):
    """Inserta un dato y devuelve la nueva raiz del arbol AVL."""
    if raiz is None:
        raiz = nodoArbol(dato)
    elif _clave(dato, campo) < _clave(raiz.info, campo):
        raiz.izq = insertar_nodo(raiz.izq, dato, campo)
    else:
        raiz.der = insertar_nodo(raiz.der, dato, campo)

    raiz = balancear(raiz)
    actualizaraltura(raiz)
    return raiz


def reemplazar(raiz):
    """Determina el nodo que reemplazara al que se elimina."""
    if raiz.der is None:
        aux = raiz
        raiz = raiz.izq
    else:
        raiz.der, aux = reemplazar(raiz.der)
        raiz = balancear(raiz)
        actualizaraltura(raiz)
    return raiz, aux


def eliminar_nodo(raiz, clave, campo=None):
    """Elimina por clave y devuelve la raiz y la informacion eliminada."""
    eliminado = None
    if raiz is not None:
        clave_raiz = _clave(raiz.info, campo)
        if clave < clave_raiz:
            raiz.izq, eliminado = eliminar_nodo(raiz.izq, clave, campo)
        elif clave > clave_raiz:
            raiz.der, eliminado = eliminar_nodo(raiz.der, clave, campo)
        else:
            eliminado = raiz.info
            if raiz.izq is None:
                raiz = raiz.der
            elif raiz.der is None:
                raiz = raiz.izq
            else:
                raiz.izq, aux = reemplazar(raiz.izq)
                raiz.info = aux.info

    raiz = balancear(raiz)
    actualizaraltura(raiz)
    return raiz, eliminado


def arbol_vacio(raiz):
    """Devuelve True si el arbol no contiene elementos."""
    return raiz is None


def buscar(raiz, clave, campo=None):
    """Devuelve el nodo cuya clave coincide con la indicada."""
    if raiz is None:
        return None

    clave_raiz = _clave(raiz.info, campo)
    if clave == clave_raiz:
        return raiz
    if clave < clave_raiz:
        return buscar(raiz.izq, clave, campo)
    return buscar(raiz.der, clave, campo)


def busqueda_proximidad(raiz, buscado, campo=None, coincidencias=None):
    """Busca recursivamente nodos cuya clave contiene el texto indicado."""
    if coincidencias is None:
        coincidencias = []
    if raiz is not None:
        busqueda_proximidad(raiz.izq, buscado, campo, coincidencias)
        if buscado.casefold() in str(_clave(raiz.info, campo)).casefold():
            coincidencias.append(raiz)
        busqueda_proximidad(raiz.der, buscado, campo, coincidencias)
    return coincidencias


def inorden(raiz):
    """Realiza el barrido inorden del arbol."""
    if raiz is not None:
        inorden(raiz.izq)
        print(raiz.info)
        inorden(raiz.der)


def preorden(raiz):
    """Realiza el barrido preorden del arbol."""
    if raiz is not None:
        print(raiz.info)
        preorden(raiz.izq)
        preorden(raiz.der)


def postorden(raiz):
    """Realiza el barrido postorden descendente usado en el libro."""
    if raiz is not None:
        postorden(raiz.der)
        print(raiz.info)
        postorden(raiz.izq)


def por_nivel(raiz):
    """Realiza el barrido por nivel utilizando el TDA Cola."""
    if raiz is None:
        return

    pendientes = Cola()
    arribo(pendientes, raiz)
    while not cola_vacia(pendientes):
        nodo = atencion(pendientes)
        print(nodo.info)
        if nodo.izq is not None:
            arribo(pendientes, nodo.izq)
        if nodo.der is not None:
            arribo(pendientes, nodo.der)


def contar_nodos(raiz):
    """Cuenta recursivamente los nodos del arbol."""
    if raiz is None:
        return 0
    return 1 + contar_nodos(raiz.izq) + contar_nodos(raiz.der)
