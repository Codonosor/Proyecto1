# Sistema de gestión para cafetería

Aplicación Python orientada a objetos para gestionar productos, inventario y pedidos en una cafetería. La aplicación expone una interfaz web sencilla para operar desde el punto de venta y permite trabajar concurrentemente desde varios dispositivos dentro de un mismo proceso.

Características principales
- Interfaz web (Flask) como punto de entrada: `main.py`.
- Gestión de productos: bebidas y alimentos con precio y atributos específicos.
- Inventario con operaciones atómicas (agregar, eliminar, consultar, reservar, liberar).
- Pedidos compuestos por líneas (item + cantidad). Soporta pedidos locales y delivery.
- Descuentos:
  - Descuentos automáticos por tipo de pedido: 10% para consumo en local, 5% para delivery.
  - El operador puede aplicar un descuento en porcentaje al momento de cobrar.
- Reservas de stock inmediatas al añadir un producto a un pedido.
- Procesado de pedidos uno por uno desde la UI; la aplicación informa al operador el total a cobrar.

Estructura del proyecto
- cafe/
  - producto.py: definiciones de Producto, Alimento y Bebida.
  - inventario.py: clase Inventario con operaciones sobre stock.
  - pedido.py: ItemPedido, Pedido, PedidoLocal y PedidoDelivery (cálculo de totales y manejo de descuentos).
  - gestor.py: GestorCafe (genera IDs correlativos y contiene utilidades para procesar pedidos).
- templates/: plantillas Jinja2 usadas por la interfaz web (index, nuevo_pedido, procesar_pedido, inventario, agregar_producto).
- main.py: servidor web (Flask) — punto de entrada recomendado.
- run_tests.py: script de pruebas que valida comportamiento de reservas y stock.

Rutas principales (web)
- / : panel principal con pedidos pendientes y acceso a crear pedidos o ver inventario.
- /nuevo_pedido : formulario para crear un pedido (selección de productos, estado: finalizar o guardar como pendiente, campo de descuento operador).
- /procesar_pedido/<idx> : vista para procesar o cancelar un pedido pendiente; muestra subtotal, permite aplicar descuento del operador y confirma el cobro.
- /inventario : lista de productos y stock.
- /agregar_producto : formulario para agregar o actualizar productos.
- /eliminar_producto/<codigo> : elimina un producto por código.

Concurrencia y uso multiusuario
- La aplicación está diseñada para funcionar concurrentemente dentro de un único proceso: usa bloqueos (locks) para proteger operaciones críticas sobre el inventario y las listas de pedidos en memoria. Esto permite atender varias conexiones/solicitudes simultáneamente sin corromper el estado compartido.
- Recomendación de despliegue para entorno con concurrencia dentro de un proceso:
  - Ejecutar con Gunicorn configurado a 1 worker y varios threads, por ejemplo:
    - `gunicorn -w 1 --threads 8 main:app`
  - O ejecutar localmente con threading habilitado y sin reloader: `python main.py` (asegúrate de ejecutar con debug=False si pruebas multi-hilo)
- Nota: el estado (inventario, pedidos) se mantiene en memoria del proceso; para escalado a múltiples procesos o servidores es necesario introducir persistencia externa (base de datos o Redis) y una cola de trabajo.

Arranque rápido
1. Instalar dependencias: `pip install flask`.
2. Ejecutar la aplicación web: `python main.py`.
3. Abrir navegador: `http://127.0.0.1:5000/`.

Pruebas
- Ejecutar: `python run_tests.py` — realiza comprobaciones básicas de reservas, liberación y límites de stock.

Contacto y notas
- El diseño prioriza claridad y mínima complejidad: las reglas de negocio están en el paquete `cafe/` y la capa de presentación en `main.py` con plantillas en `templates/`.
