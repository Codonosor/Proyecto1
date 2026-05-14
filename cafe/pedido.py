"""
Módulo de pedidos.
Define las clases necesarias para representar pedidos locales y delivery, con sus respectivas reglas de cálculo de total y descuentos.
Incluye las clases Pedido, PedidoLocal, PedidoDelivery e ItemPedido.
"""


class ItemPedido:
    """Representa una línea de pedido: producto + cantidad."""

    def __init__(self, producto, cantidad=1):
        self.producto = producto
        self.cantidad = int(cantidad)

    def total_linea(self):
        # Total simple de la línea: precio del producto por cantidad
        return self.producto.obtener_precio() * self.cantidad


class Pedido:
    """Pedido que mantiene una lista de ItemPedido y un descuento."""

    def __init__(self, id_pedido, cliente, mesa=0):
        self.id_pedido = id_pedido
        self.cliente = cliente
        self.mesa = int(mesa)
        # _items es privado para evitar modificaciones externas directas
        self.__items = []
        # descuento fijo o en fracción (legacy)
        self._descuento = 0.0
        # descuento en porcentaje (ej. 25 para 25%) - preferido en la interfaz
        self._descuento_percent = 0.0

    def agregar_item(self, producto, cantidad=1):
        # Añade una línea al pedido
        self.__items.append(ItemPedido(producto, cantidad))

    def items(self):
        # Devuelve una copia de las líneas del pedido
        return list(self.__items)

    def aplicar_descuento_operador(self, monto):
        """Aplica el descuento ingresado por el operador al monto dado."""
        if 0 < getattr(self, "_descuento_percent", 0):
            pct = float(self._descuento_percent)
            return monto * (1 - pct / 100.0)

        d = getattr(self, "_descuento", 0.0)
        if 0 < d < 1:
            return monto * (1 - d)
        return max(0.0, monto - d)

    def total(self):
        """
        Cálculo del total de un pedido.
        Calcula la suma de las líneas y aplica el descuento del operador.
        """
        # calcular suma de líneas directamente (evita método subtotal)
        suma = 0.0
        for it in self.__items:
            suma += it.total_linea()
        return self.aplicar_descuento_operador(suma)

class PedidoLocal(Pedido):
    """
    Pedido para consumo en local.
    Aplica un descuento fijo del 10% (oferta de pedido en tienda) y además respeta el
    descuento ingresado por el operador. Usa polimorfismo, redefiniendo total().
    """
    def total(self):
        # calcular suma de líneas, aplicar 10% de tienda y luego descuento del operador
        suma = 0.0
        for it in self.__items:
            suma += it.total_linea()
        sub_after_local = suma * (1 - 10.0 / 100.0)
        return self.aplicar_descuento_operador(sub_after_local)


class PedidoDelivery(Pedido):
    """
    Pedido para delivery que añade un cargo por envío.
    Aplica un descuento fijo del 5% (descuento para envío gratis), además
    del descuento ingresado por el operador. Añade el cargo por envío normal al final.
    """

    def __init__(self, id_pedido, cliente, descuento=0.0, cargo_envio=5.0):
        super().__init__(id_pedido, cliente, mesa=0)
        # valor legacy
        self._descuento = descuento
        self._descuento_percent = 0.0
        self._cargo_envio = float(cargo_envio)

    def total(self):
        # calcular suma de líneas, aplicar 5% de tienda, luego descuento del operador y cargo
        suma = 0.0
        for it in self.__items:
            suma += it.total_linea()
        sub_after_delivery = suma * (1 - 5.0 / 100.0)
        return self.aplicar_descuento_operador(sub_after_delivery) + self._cargo_envio
