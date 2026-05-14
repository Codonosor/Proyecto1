# Sistema de gestión para cafetería

Proyecto Python orientado a objetos para gestionar productos, pedidos e
inventario en una cafetería. Está pensado para uso desde la terminal y con
una API interna sencilla.

Características principales.
- IDs de pedidos correlativos: Local -> L01, L02..., Delivery -> D001, D002...
- Reserva de stock inmediata al añadir productos a un pedido.
- Descuentos: el operador puede aplicar descuentos en porcentaje al cobrar;
  además, hay descuentos automáticos por tipo de pedido (10% local, 5% delivery).
- Atributos sensibles protegidos: campos críticos (por ejemplo, precio en Producto
  y líneas de pedido en Pedido) son privados y se modifican mediante métodos públicos.

Estructura del proyecto
- cafe/producto.py: Producto, Alimento, Bebida
- cafe/inventario.py: Inventario (agregar, eliminar, obtener, reservar, liberar, listar)
- cafe/pedido.py: Pedido, PedidoLocal, PedidoDelivery, ItemPedido (cálculo de totales y descuentos)
- cafe/gestor.py: GestorCafe (genera IDs correlativos y procesa pedidos)
- main.py: Interfaz de terminal con menú interactivo

Uso rápido

1. Ejecuta: `python main.py` en la raíz del proyecto.
2. El menú interactivo permite crear pedidos, finalizar o cancelar pedidos
   pendientes, y modificar el inventario.
