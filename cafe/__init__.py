"""Sistema de gestión de cafetería (módulo principal).
Exponemos los componentes principales en español para facilitar su uso:
`from cafe import GestorCafe, Inventario, Producto, Alimento, Bebida, Pedido`.
"""
from .gestor import GestorCafe
from .inventario import Inventario
from .producto import Producto, Alimento, Bebida
from .pedido import Pedido, PedidoLocal, PedidoDelivery

__all__ = [
    "GestorCafe",
    "Inventario",
    "Producto",
    "Alimento",
    "Bebida",
    "Pedido",
    "PedidoLocal",
    "PedidoDelivery",
]
