"""Capa de servicios de products.

Aqui vive la logica de negocio de la app (calculos y decisiones),
separada de las vistas (views.py) y de los modelos (models.py).

Patron de comportamiento: Strategy.
Cada categoria de producto tiene su propia estrategia de descuento;
obtener_estrategia() decide, en tiempo de ejecucion, cual aplicar.
"""


class EstrategiaDescuento:
    """Interfaz comun para todas las estrategias de descuento."""

    def calcular(self, precio):
        raise NotImplementedError


class DescuentoElectronica(EstrategiaDescuento):
    """10% de descuento para productos de la categoria Electronica."""

    def calcular(self, precio):
        return precio * 0.90


class DescuentoRopa(EstrategiaDescuento):
    """20% de descuento para productos de la categoria Ropa."""

    def calcular(self, precio):
        return precio * 0.80


class SinDescuento(EstrategiaDescuento):
    """Estrategia por default: no aplica ningun descuento."""

    def calcular(self, precio):
        return precio


def obtener_estrategia(categoria_nombre):
    """Devuelve la estrategia de descuento que corresponde al nombre
    de categoria recibido. Si la categoria no tiene una estrategia
    registrada, regresa SinDescuento."""
    estrategias = {
        'Electronica': DescuentoElectronica(),
        'Ropa': DescuentoRopa(),
    }
    return estrategias.get(categoria_nombre, SinDescuento())
