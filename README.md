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

Concurrencia (threading)

Para cumplir el requisito de concurrencia sin cambiar la estructura principal,
se agregó procesamiento concurrente solo en la etapa de procesamiento de
pedidos:

- `GestorCafe.procesar_pedidos_concurrentes(pedidos)` crea un hilo por pedido.
- Se usa `threading.Semaphore` para limitar la cantidad de hilos activos según
  `trabajadores`.
- Cada hilo ejecuta la lógica existente (`procesar_pedido`) y guarda su total.
- Se usa `join()` para esperar que todos terminen antes de continuar.
- Se protege la salida por consola con `Lock` para evitar mensajes mezclados.

En el menú, opción "Finalizar pedido pendiente", existe la selección:

- `0. Procesar TODOS concurrentemente`

Esto mantiene el modelo original y agrega una simulación simple de atención en
paralelo.

Justificación de decisiones de diseño

1) Encapsulamiento

- Los datos sensibles del dominio se protegen con atributos internos, por
  ejemplo el precio en `Producto` y las líneas en `Pedido`.
- Las clases exponen métodos de acceso y operación (`mostrar_precio`,
  `obtener_precio`, `items`, `agregar_item`) para evitar modificaciones
  externas directas.
- Esta decisión reduce acoplamiento y evita estados inconsistentes.

2) Herencia

- `Alimento` y `Bebida` heredan de `Producto` para reutilizar comportamiento
  común.
- `PedidoLocal` y `PedidoDelivery` heredan de `Pedido`, compartiendo estructura
  de cliente, items y descuentos del operador.
- Esto evita duplicación y facilita extender nuevos tipos de producto o pedido.

3) Polimorfismo

- El método `total()` se redefine en `PedidoLocal` y `PedidoDelivery` para
  aplicar reglas distintas sin cambiar el uso desde el exterior.
- El sistema trata pedidos de forma uniforme (`pedido.total()`), pero cada
  subtipo calcula su total según su propia lógica.

4) Composición

- Un `Pedido` está compuesto por múltiples `ItemPedido`.
- Cada `ItemPedido` referencia un `Producto` y su cantidad.
- Esta composición modela correctamente la relación real del dominio: el pedido
  existe como agregado de líneas.

5) Inventario

- `Inventario` centraliza altas, bajas, consulta de stock, reserva y liberación.
- Al agregar un producto al pedido se reserva stock de forma inmediata, evitando
  sobreventa.
- Si un pedido pendiente se cancela, el stock reservado se libera.
- Esta estrategia mantiene consistencia entre pedidos en curso y disponibilidad.

6) Concurrencia

- Se eligió `threading` por simplicidad y bajo impacto sobre el diseño existente.
- La concurrencia se acota al procesamiento de múltiples pedidos, sin alterar el
  modelo de clases principal.
- Se usan primitivas básicas y entendibles (`Thread`, `Semaphore`, `Lock`), lo
  que facilita justificar la solución en un informe académico.
- El resultado es una simulación realista de trabajo paralelo (caja/cocina), con
  cambios mínimos y controlados.
