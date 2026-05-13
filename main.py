"""Interfaz de terminal para crear y procesar pedidos en la cafetería.

Esta interfaz guía al operador (trabajador del café) en tres tareas
principales: crear pedidos, finalizar pedidos pendientes y modificar el
inventario. El diseño prioriza claridad: cada paso queda documentado con
comentarios para facilitar su comprensión.
"""
from cafe import GestorCafe, Inventario, Bebida, Alimento, PedidoLocal, PedidoDelivery
import time


def imprimir_productos(inventario: Inventario):
    # Muestra en pantalla los productos actualmente en el inventario
    print("Productos disponibles:")
    for codigo, nombre, precio, stock in inventario.listar_productos():
        print(f"  {codigo}: {nombre} - ${precio:.2f} (stock: {stock})")


def interfaz_terminal():
    # Crear inventario y poblar con algunos productos iniciales
    inv = Inventario()
    cafe = Bebida("B001", "Café Americano", 2.5, tam_ml=250)
    latte = Bebida("B002", "Café Latte", 3.5, tam_ml=300)
    sandwich = Alimento("A001", "Sandwich", 4.0, calorias=450)
    pastel = Alimento("A002", "Porción de pastel", 2.8, calorias=350)

    inv.agregar_producto(cafe, cantidad=10)
    inv.agregar_producto(latte, cantidad=5)
    inv.agregar_producto(sandwich, cantidad=3)
    inv.agregar_producto(pastel, cantidad=4)

    # Crear gestor (simple) y contenedor de pedidos pendientes
    gestor = GestorCafe(inventario=inv, trabajadores=3)
    pedidos_pendientes = ()  # tupla inmutable que contiene pedidos en espera

    try:
        # Bucle principal del menú: se repite hasta que el operador elige salir
        while True:
            print("\n=== Menú principal ===")
            print("1. Nuevo pedido")
            print("2. Finalizar pedido pendiente")
            print("3. Modificar inventario")
            print("4. Salir")
            opcion = input("Escriba el número de su opción: ").strip()
            if opcion == "4":
                break

            if opcion == "1":
                # Opción 1: Nuevo pedido
                # Solicitamos los datos básicos y creamos la instancia adecuada
                print("\n--- Nuevo pedido ---")
                nombre_cliente = input("Nombre del cliente: ").strip()
                try:
                    mesa = int(input("Número de mesa (0 para delivery): ").strip())
                except ValueError:
                    # Si la entrada no es un entero, asumimos delivery
                    print("Mesa inválida, se usará 0 (delivery)")
                    mesa = 0

                # Asignar ID correlativo según el tipo de pedido
                if mesa == 0:
                    idp = gestor.siguiente_id_delivery()
                    pedido = PedidoDelivery(id_pedido=idp, cliente=nombre_cliente)
                else:
                    idp = gestor.siguiente_id_local()
                    pedido = PedidoLocal(id_pedido=idp, cliente=nombre_cliente, mesa=mesa)

                # Bucle para añadir items al pedido hasta que el operador deje vacío el código
                while True:
                    imprimir_productos(inv)
                    codigo = input("Código de producto a añadir (enter para terminar): ").strip()
                    if codigo == "":
                        # Fin de la adición de productos
                        break
                    producto = inv.obtener_producto(codigo)
                    if not producto:
                        print("Código no encontrado")
                        continue
                    try:
                        cantidad = int(input("Cantidad: ").strip())
                    except ValueError:
                        # Por simplicidad, usar una unidad si el operador no introduce un número
                        print("Cantidad inválida, usando 1")
                        cantidad = 1

                    # Si la cantidad solicitada excede el stock, solicitar confirmación
                    stock_actual = inv.stock_de(producto.codigo)
                    if cantidad > stock_actual:
                        print(f"Solicitaste {cantidad} pero el stock es {stock_actual}.")
                        if stock_actual <= 0:
                            print("Producto sin stock, no se añadirá.")
                            continue
                        confirmar = input(f"¿Deseas añadir la cantidad disponible ({stock_actual}) en su lugar? (s/n): ").strip().lower()
                        if confirmar != "s":
                            print("No se añadió el producto.")
                            continue
                        cantidad = stock_actual

                    # Reservar inmediatamente la cantidad en inventario para evitar overbooking
                    reservado = inv.reservar(producto.codigo, cantidad)
                    if not reservado:
                        print("No fue posible reservar en inventario. No se añadió el producto.")
                        continue
                    pedido.agregar_item(producto, cantidad)

                # Si no se añadieron items, volvemos al menú (liberando reservas si hubiera)
                if len(pedido.items()) == 0:
                    print("No se puede crear un pedido vacío. Volviendo al menú principal.")
                    # Aunque no debería haber reservas en un pedido vacío, nos aseguramos
                    for it in pedido.items():
                        inv.liberar(it.producto.codigo, it.cantidad)
                    continue

                # Preguntar si se finaliza ahora o se guarda como pendiente (pendiente ya tiene stock reservado)
                estado = input("Estado del pedido: (1) Finalizar inmediatamente, (2) Pendiente de pago [1/2]: ").strip()
                if estado != "2":
                    # Antes de procesar, ofrecer aplicar descuento en porcentaje (ej. 25 para 25%)
                    aplicar = input("¿Aplicar descuento en porcentaje ahora? (ej. 25 para 25%) (enter para no): ").strip()
                    if aplicar != "":
                        try:
                            pct = float(aplicar)
                            if pct > 0:
                                pedido._descuento_percent = pct
                        except ValueError:
                            print("Descuento inválido, no se aplicará")

                    # Procesar inmediatamente: en la versión simplificada, procesar_pedido imprime el resultado
                    gestor.procesar_pedido(pedido)
                    print(f"Pedido procesado inmediatamente. Total: ${pedido.total():.2f}")
                else:
                    # Guardar en la colección de pendientes (tupla)
                    pedidos_pendientes = pedidos_pendientes + (pedido,)
                    print(f"Pedido guardado en pendientes. Total pendientes: {len(pedidos_pendientes)}")

            elif opcion == "2":
                # Finalizar pedido pendiente
                # Opción 2: Finalizar o cancelar un pedido pendiente
                if len(pedidos_pendientes) == 0:
                    print("No hay pedidos pendientes.")
                    continue
                # Mostrar listadode pendientes con un índice
                print("Pedidos pendientes:")
                for idx, ped in enumerate(pedidos_pendientes, start=1):
                    destino = f"MESA {ped.mesa}" if ped.mesa > 0 else "DELIVERY"
                    print(f"{idx}. {ped.cliente} - {destino} - items: {len(ped.items())}")
                try:
                    sel = int(input("Selecciona número de pedido para procesar: ").strip())
                except ValueError:
                    print("Selección inválida")
                    continue
                if not (1 <= sel <= len(pedidos_pendientes)):
                    print("Selección fuera de rango")
                    continue
                ped = pedidos_pendientes[sel - 1]
                accion = input("(1) Finalizar y cobrar / (2) Cancelar y liberar stock [1/2]: ").strip()
                if accion != "2":
                    # Antes de finalizar, preguntar si aplicar descuento en porcentaje
                    aplicar = input("¿Aplicar descuento en porcentaje? (ej. 25 para 25%) (enter para no): ").strip()
                    if aplicar != "":
                        try:
                            pct = float(aplicar)
                            if pct > 0:
                                ped._descuento_percent = pct
                        except ValueError:
                            print("Descuento inválido, no se aplicará")

                    # Finalizar: calcular deuda y eliminar de pendientes
                    deuda = ped.total()
                    print(f"Finalizando pedido de {ped.cliente}. Monto a cobrar: ${deuda:.2f}")
                    pedidos_pendientes = pedidos_pendientes[: sel - 1] + pedidos_pendientes[sel:]
                else:
                    # Cancelar: liberar el stock reservado por las líneas del pedido
                    for it in ped.items():
                        inv.liberar(it.producto.codigo, it.cantidad)
                    print(f"Pedido de {ped.cliente} cancelado y stock liberado.")
                    pedidos_pendientes = pedidos_pendientes[: sel - 1] + pedidos_pendientes[sel:]

            elif opcion == "3":
                # Modificar inventario
                print("\n--- Modificar inventario ---")
                imprimir_productos(inv)
                print("a) Añadir/actualizar producto")
                print("b) Eliminar producto")
                print("c) Volver al menú principal")
                sub = input("Elige opción [a/b/c]: ").strip().lower()
                if sub == "a":
                    # Añadir o actualizar producto en el inventario
                    codigo = input("Código: ").strip()
                    nombre = input("Nombre: ").strip()
                    try:
                        precio = float(input("Precio: ").strip())
                    except ValueError:
                        print("Precio inválido")
                        continue
                    try:
                        cantidad = int(input("Cantidad en stock: ").strip())
                    except ValueError:
                        print("Cantidad inválida")
                        continue
                    # Elegir tipo para instanciar la clase apropiada
                    tipo = input("Tipo (b)ebida/(a)limento [b/a]: ").strip().lower()
                    if tipo == "a":
                        producto = Alimento(codigo, nombre, precio)
                    else:
                        producto = Bebida(codigo, nombre, precio)
                    inv.agregar_producto(producto, cantidad=cantidad)
                    print("Producto agregado/actualizado.")
                elif sub == "b":
                    codigo = input("Código a eliminar: ").strip()
                    ok = inv.eliminar_producto(codigo)
                    if ok:
                        print("Producto eliminado.")
                    else:
                        print("Código no encontrado.")
                elif sub == "c":
                    print("Volviendo al menú principal.")
                    continue
                else:
                    print("Opción inválida")

            else:
                print("Opción inválida")

    except KeyboardInterrupt:
        print("\nInterrupción por teclado. Saliendo...")


if __name__ == "__main__":
    interfaz_terminal()
