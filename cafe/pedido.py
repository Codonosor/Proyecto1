"""Módulo de pedidos.

Define estructuras sencillas para representar items de pedido y pedidos
(local y delivery). Incluye cálculo de subtotal y total con soporte para
descuentos.
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
    """Pedido genérico que mantiene una lista de ItemPedido y un descuento."""

    def __init__(self, id_pedido, cliente, mesa=0):
        self.id_pedido = id_pedido
        self.cliente = cliente
        self.mesa = int(mesa)
        self._items = []
        # descuento fijo o en fracción (legacy)
        self._descuento = 0.0
        # descuento en porcentaje (ej. 25 para 25%) - preferido en la interfaz
        self._descuento_percent = 0.0

    def agregar_item(self, producto, cantidad=1):
        # Añade una línea al pedido
        self._items.append(ItemPedido(producto, cantidad))

    def items(self):
        # Devuelve una copia de las líneas del pedido
        return list(self._items)

    def subtotal(self):
        # Calcula la suma de las líneas
        total = 0.0
        for it in self._items:
            total += it.total_linea()
        return total

    def total(self):
        # Calcula total aplicando descuento.
        # Prioriza _descuento_percent si está establecido (>0).
        sub = self.subtotal()
        # Si se indicó descuento en porcentaje (ej. 25 -> 25%), aplicarlo primero
        if 0 < getattr(self, "_descuento_percent", 0):
            pct = float(self._descuento_percent)
            return sub * (1 - pct / 100.0)
        # Compatibilidad hacia atrás: si _descuento está en (0,1) se interpreta como fracción
        d = self._descuento
        if 0 < d < 1:
            return sub * (1 - d)
        # si _descuento >= 1 se interpreta como monto fijo
        return max(0.0, sub - d)


class PedidoLocal(Pedido):
    """Pedido para consumo en local. Actualmente no añade comportamiento extra."""


class PedidoDelivery(Pedido):
    """Pedido para delivery que añade un cargo por envío."""

    def __init__(self, id_pedido, cliente, descuento=0.0, cargo_envio=5.0):
        super().__init__(id_pedido, cliente, mesa=0)
        self._descuento = descuento
        self._descuento_percent = 0.0
        self._cargo_envio = float(cargo_envio)

    def total(self):
        # Aplica descuento (se prioriza _descuento_percent) y suma el cargo por envío
        sub = self.subtotal()
        if 0 < getattr(self, "_descuento_percent", 0):
            pct = float(self._descuento_percent)
            sub = sub * (1 - pct / 100.0)
        else:
            d = self._descuento
            if 0 < d < 1:
                sub = sub * (1 - d)
            else:
                sub = max(0.0, sub - d)
        return sub + self._cargo_envio
