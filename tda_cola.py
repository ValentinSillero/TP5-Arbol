"""TDA Cola dinamica utilizado por el recorrido por nivel del arbol."""


class nodoCola(object):
    """Nodo de la cola dinamica."""

    def __init__(self, info):
        self.info = info
        self.sig = None


class Cola(object):
    """Cola dinamica con punteros al frente y al final."""

    def __init__(self):
        self.frente = None
        self.final = None
        self.tamanio = 0


def arribo(cola, dato):
    """Agrega un dato al final de la cola."""
    nodo = nodoCola(dato)
    if cola.frente is None:
        cola.frente = nodo
    else:
        cola.final.sig = nodo
    cola.final = nodo
    cola.tamanio += 1


def atencion(cola):
    """Quita y devuelve el dato ubicado en el frente de la cola."""
    if cola.frente is None:
        return None

    dato = cola.frente.info
    cola.frente = cola.frente.sig
    cola.tamanio -= 1
    if cola.frente is None:
        cola.final = None
    return dato


def cola_vacia(cola):
    """Devuelve True si la cola no contiene elementos."""
    return cola.frente is None


def tamanio(cola):
    """Devuelve la cantidad de elementos almacenados."""
    return cola.tamanio
