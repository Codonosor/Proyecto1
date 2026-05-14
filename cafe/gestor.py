"""Módulo gestor.

Genera IDs correlativos para pedidos locales y delivery, 
y tiene un método procesar_pedido que simula el procesamiento de un pedido mostrando su total.
"""
class GestorCafe:
    def __init__(self, inventario=None, trabajadores=1):
        # referencia al inventario y número de trabajadores (informativo)
        self.inventario = inventario
        self.trabajadores = trabajadores
        # contadores simples para IDs correlativos
        self._contador_local = 0
        self._contador_delivery = 0

    def siguiente_id_local(self):
        # Devuelve IDs tipo L01, L02, ...
        self._contador_local += 1
        return f"L{self._contador_local:02d}"

    def siguiente_id_delivery(self):
        # Devuelve IDs tipo D001, D002, ...
        self._contador_delivery += 1
        return f"D{self._contador_delivery:03d}"

    def procesar_pedido(self, pedido):
        # Procesa el pedido (simulación): calcula total y lo muestra.
        destino = f"MESA {pedido.mesa}" if pedido.mesa > 0 else "DELIVERY"
        total = pedido.total()
        print(f"Procesado pedido {pedido.id_pedido} para {pedido.cliente} ({destino}): total={total:.2f}")
