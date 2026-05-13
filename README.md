
# Sistema de gestión para cafetería (versión simplificada)

Esta versión del proyecto está diseñada para ser compacta, legible y libre
de dependencias externas. A continuación se describen las decisiones y
el uso actual.

Decisiones principales
- Nombres en español para módulos y clases.
- Sin dependencias: no se usan typing, abc, __future__, uuid ni threading.
- IDs de pedidos correlativos y legibles: Local -> L01, L02..., Delivery -> D001, D002...
- Inventario con reserva inmediata: al añadir un item al pedido se reduce el stock.

Estructura del proyecto (módulos dentro de la carpeta cafe)
- producto.py: Producto, Alimento, Bebida
- inventario.py: Inventario (agregar, eliminar, reservar, liberar, listar)
- pedido.py: Pedido, PedidoLocal, PedidoDelivery, ItemPedido
- gestor.py: GestorCafe (genera IDs correlativos y procesa pedidos)
- main.py: Interfaz de terminal con menú (Nuevo pedido / Finalizar pedido / Modificar inventario)
- run_tests.py: Script de pruebas para validar reservas y liberaciones

Uso rápido

1. Ejecuta: `python main.py` en una terminal.
2. El menú permite:
   - Nuevo pedido: crear pedido (mesa 0 = delivery), añadir productos (reserva inmediata),
     y elegir si finalizar ahora o guardar como pendiente.
   - Finalizar pedido pendiente: listar pendientes, y elegir Finalizar (cobrar) o Cancelar (liberar stock).
   - Modificar inventario: añadir/actualizar productos o eliminar por código.
   - Salir: cerrar la aplicación.

3. Los pedidos pendientes conservan la reserva de stock hasta que se finalicen o cancelen.

Probar que todo funciona

Ejecuta `python run_tests.py` para ejecutar las pruebas incluidas que verifican
reservas, liberaciones y límites de stock.

Notas

- Esta versión fue simplificada para mayor claridad. Si quieres volver a una
  versión con procesamiento en paralelo (workers) o agregar persistencia en
  JSON/BD, puedo implementarlo.
