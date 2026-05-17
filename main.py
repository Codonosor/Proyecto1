from flask import Flask, render_template, request, redirect, url_for, flash
import threading
from cafe import Inventario, Bebida, Alimento, PedidoLocal, PedidoDelivery, GestorCafe

app = Flask(__name__)
app.secret_key = 'cafeweb2026'

# Instancias globales (simples, no persistentes)
inventario = Inventario()
gestor = GestorCafe(inventario=inventario, trabajadores=3)
pedidos_pendientes = []
pedidos_finalizados = []

# Locks simples para proteger el estado en memoria cuando hay múltiples hilos
inventory_lock = threading.Lock()
pedidos_lock = threading.Lock()

# Productos de ejemplo
if not inventario.listar_productos():
    inventario.agregar_producto(Bebida("B001", "Café Americano", 2.5, tam_ml=250), cantidad=30)
    inventario.agregar_producto(Bebida("B002", "Café Latte", 3.5, tam_ml=300), cantidad=15)
    inventario.agregar_producto(Alimento("A001", "Sandwich", 4.0, calorias=450), cantidad=20)
    inventario.agregar_producto(Alimento("A002", "Porción de pastel", 2.8, calorias=350), cantidad=24)


@app.route('/')
def index():
    return render_template('index.html', productos=inventario.listar_productos(), pedidos=pedidos_pendientes)


@app.route('/nuevo_pedido', methods=['GET', 'POST'])
def nuevo_pedido():
    if request.method == 'POST':
        nombre = request.form['cliente']
        mesa = int(request.form.get('mesa', 0) or 0)
        tipo = request.form['tipo']
        estado = request.form.get('estado', 'finalizar')
        descuento_raw = request.form.get('descuento', '').strip()

        if tipo == 'delivery':
            idp = gestor.siguiente_id_delivery()
            pedido = PedidoDelivery(id_pedido=idp, cliente=nombre)
        else:
            idp = gestor.siguiente_id_local()
            pedido = PedidoLocal(id_pedido=idp, cliente=nombre, mesa=mesa)

        # Agregar productos (reservar stock de forma protegida)
        for codigo in request.form.getlist('producto'):
            try:
                cantidad = int(request.form.get(f'cantidad_{codigo}', 1) or 1)
            except ValueError:
                cantidad = 1
            prod = None
            reservado = False
            # proteger acceso al inventario
            with inventory_lock:
                prod = inventario.obtener_producto(codigo)
                if prod:
                    reservado = inventario.reservar(codigo, cantidad)
            if prod and reservado:
                pedido.agregar_item(prod, cantidad)

        # Aplicar descuento ingresado por operador (si hubiera)
        if descuento_raw != '':
            try:
                pct = float(descuento_raw)
                if pct > 0:
                    pedido._descuento_percent = pct
            except ValueError:
                # ignorar descuento inválido
                pass

        if not pedido.items():
            flash('No se pudo crear el pedido (sin productos válidos o stock).', 'danger')
            return redirect(url_for('nuevo_pedido'))

        if estado == 'finalizar':
            # Procesar inmediatamente (síncrono): se informa al operador del total
            gestor.procesar_pedido(pedido)
            with pedidos_lock:
                pedidos_finalizados.append(pedido)
            flash(f'Pedido {pedido.id_pedido} procesado. Total a cobrar: ${pedido.total():.2f}', 'success')
            return redirect(url_for('index'))
        else:
            # Guardar como pendiente (stock ya reservado)
            with pedidos_lock:
                pedidos_pendientes.append(pedido)
            flash('Pedido creado y guardado en pendientes.', 'success')
            return redirect(url_for('index'))

    return render_template('nuevo_pedido.html', productos=inventario.listar_productos())


@app.route('/procesar_pedido/<int:idx>', methods=['GET', 'POST'])
def procesar_pedido(idx):
    # Mostrar formulario para aplicar descuento y confirmar procesamiento o cancelar
    if not (0 <= idx < len(pedidos_pendientes)):
        flash('Pedido no encontrado.', 'danger')
        return redirect(url_for('index'))

    if request.method == 'GET':
        with pedidos_lock:
            pedido = pedidos_pendientes[idx]
        # subtotal para mostrar antes de descuentos
        subtotal = sum(it.total_linea() for it in pedido.items())
        return render_template('procesar_pedido.html', pedido=pedido, idx=idx, subtotal=subtotal)

    # POST: confirmar acción
    accion = request.form.get('accion', 'finalizar')
    # Popear el pedido del listado de pendientes de forma protegida
    pedido = None
    with pedidos_lock:
        if 0 <= idx < len(pedidos_pendientes):
            pedido = pedidos_pendientes.pop(idx)

    if not pedido:
        flash('Pedido no encontrado.', 'danger')
        return redirect(url_for('index'))

    if accion == 'cancelar':
        # liberar stock de forma protegida
        for it in pedido.items():
            with inventory_lock:
                inventario.liberar(it.producto.mostrar_codigo(), it.cantidad)
        flash(f'Pedido {pedido.id_pedido} cancelado y stock liberado.', 'info')
        return redirect(url_for('index'))

    # aplicar descuento si se envió
    descuento_raw = request.form.get('descuento', '').strip()
    if descuento_raw != '':
        try:
            pct = float(descuento_raw)
            if pct > 0:
                pedido._descuento_percent = pct
        except ValueError:
            pass

    gestor.procesar_pedido(pedido)
    with pedidos_lock:
        pedidos_finalizados.append(pedido)
    flash(f'Pedido {pedido.id_pedido} procesado. Total a cobrar: ${pedido.total():.2f}', 'success')
    return redirect(url_for('index'))


@app.route('/cancelar_pedido/<int:idx>')
def cancelar_pedido(idx):
    pedido = None
    with pedidos_lock:
        if 0 <= idx < len(pedidos_pendientes):
            pedido = pedidos_pendientes.pop(idx)
    if pedido:
        # liberar stock de forma protegida
        for it in pedido.items():
            with inventory_lock:
                inventario.liberar(it.producto.mostrar_codigo(), it.cantidad)
        flash(f'Pedido {pedido.id_pedido} cancelado y stock liberado.', 'info')
    return redirect(url_for('index'))


@app.route('/inventario')
def ver_inventario():
    return render_template('inventario.html', productos=inventario.listar_productos())


@app.route('/agregar_producto', methods=['GET', 'POST'])
def agregar_producto():
    if request.method == 'POST':
        codigo = request.form['codigo']
        nombre = request.form['nombre']
        precio = float(request.form['precio'])
        cantidad = int(request.form['cantidad'])
        tipo = request.form['tipo']
        if tipo == 'alimento':
            prod = Alimento(codigo, nombre, precio)
        else:
            prod = Bebida(codigo, nombre, precio)
        inventario.agregar_producto(prod, cantidad)
        flash('Producto agregado/actualizado.', 'success')
        return redirect(url_for('ver_inventario'))
    return render_template('agregar_producto.html')


@app.route('/eliminar_producto/<codigo>')
def eliminar_producto(codigo):
    inventario.eliminar_producto(codigo)
    flash('Producto eliminado.', 'info')
    return redirect(url_for('ver_inventario'))


if __name__ == '__main__':
    app.run(debug=True)
