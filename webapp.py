from flask import Flask, render_template, request, redirect, url_for, flash
from cafe import Inventario, Bebida, Alimento, PedidoLocal, PedidoDelivery, GestorCafe

app = Flask(__name__)
app.secret_key = 'cafeweb2026'

# Instancias globales (simples, no persistentes)
inventario = Inventario()
gestor = GestorCafe(inventario=inventario, trabajadores=3)
pedidos_pendientes = []
pedidos_finalizados = []

# Productos de ejemplo
if not inventario.listar_productos():
    inventario.agregar_producto(Bebida("B001", "Café Americano", 2.5, tam_ml=250), cantidad=10)
    inventario.agregar_producto(Bebida("B002", "Café Latte", 3.5, tam_ml=300), cantidad=5)
    inventario.agregar_producto(Alimento("A001", "Sandwich", 4.0, calorias=450), cantidad=3)
    inventario.agregar_producto(Alimento("A002", "Porción de pastel", 2.8, calorias=350), cantidad=4)

@app.route('/')
def index():
    return render_template('index.html', productos=inventario.listar_productos(), pedidos=pedidos_pendientes)

@app.route('/nuevo_pedido', methods=['GET', 'POST'])
def nuevo_pedido():
    if request.method == 'POST':
        nombre = request.form['cliente']
        mesa = int(request.form['mesa'])
        tipo = request.form['tipo']
        if tipo == 'delivery':
            idp = gestor.siguiente_id_delivery()
            pedido = PedidoDelivery(id_pedido=idp, cliente=nombre)
        else:
            idp = gestor.siguiente_id_local()
            pedido = PedidoLocal(id_pedido=idp, cliente=nombre, mesa=mesa)
        # Agregar productos
        for codigo in request.form.getlist('producto'):
            cantidad = int(request.form.get(f'cantidad_{codigo}', 1))
            prod = inventario.obtener_producto(codigo)
            if prod and inventario.reservar(codigo, cantidad):
                pedido.agregar_item(prod, cantidad)
        if pedido.items():
            pedidos_pendientes.append(pedido)
            flash('Pedido creado correctamente.', 'success')
            return redirect(url_for('index'))
        else:
            flash('No se pudo crear el pedido (sin productos válidos o stock).', 'danger')
    return render_template('nuevo_pedido.html', productos=inventario.listar_productos())

@app.route('/procesar_pedido/<int:idx>')
def procesar_pedido(idx):
    if 0 <= idx < len(pedidos_pendientes):
        pedido = pedidos_pendientes.pop(idx)
        gestor.procesar_pedido(pedido)
        pedidos_finalizados.append(pedido)
        flash(f'Pedido {pedido.id_pedido} procesado.', 'success')
    return redirect(url_for('index'))

@app.route('/cancelar_pedido/<int:idx>')
def cancelar_pedido(idx):
    if 0 <= idx < len(pedidos_pendientes):
        pedido = pedidos_pendientes.pop(idx)
        for it in pedido.items():
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
