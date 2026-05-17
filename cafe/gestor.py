"""
Módulo gestor.
Genera IDs correlativos para pedidos locales y delivery, 
y tiene un método procesar_pedido que simula el procesamiento de un pedido mostrando su total.
"""
import threading


class GestorCafe:
    def __init__(self, inventario=None, trabajadores=1):
        # referencia al inventario y número de trabajadores (informativo)
        self.inventario = inventario
        self.trabajadores = trabajadores
        # contadores simples para IDs correlativos
        self._contador_local = 0
        self._contador_delivery = 0
        # locks para proteger secciones críticas con hilos
        self._lock_ids = threading.Lock()
        self._lock_print = threading.Lock()

    def siguiente_id_local(self):
        # Devuelve IDs tipo L01, L02, ...
        with self._lock_ids:
            self._contador_local += 1
            return f"L{self._contador_local:02d}"

    def siguiente_id_delivery(self):
        # Devuelve IDs tipo D001, D002, ...
        with self._lock_ids:
            self._contador_delivery += 1
            return f"D{self._contador_delivery:03d}"

    def procesar_pedido(self, pedido):
        # Procesa el pedido (simulación): calcula total y lo muestra.
        destino = f"MESA {pedido.mesa}" if pedido.mesa > 0 else "DELIVERY"
        total = pedido.total()
        with self._lock_print:
            print(f"Procesado pedido {pedido.id_pedido} para {pedido.cliente} ({destino}): total={total:.2f}")

    def procesar_pedidos_concurrentes(self, pedidos):
        """Procesa varios pedidos al mismo tiempo usando threading.

        No modifica el contrato de procesar_pedido; solo coordina hilos para
        simular atención concurrente en cocina/caja.
        """
        if not pedidos:
            return []

        max_hilos = max(1, int(self.trabajadores))
        semaforo = threading.Semaphore(max_hilos)
        hilos = []
        resultados = [0.0] * len(pedidos)

        def worker(idx, pedido):
            with semaforo:
                self.procesar_pedido(pedido)
                resultados[idx] = pedido.total()

        for idx, pedido in enumerate(pedidos):
            hilo = threading.Thread(target=worker, args=(idx, pedido), daemon=False)
            hilos.append(hilo)
            hilo.start()

        for hilo in hilos:
            hilo.join()

        return resultados
