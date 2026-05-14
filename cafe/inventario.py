"""Módulo de inventario.

Contiene una implementación pequeña y clara de inventario que mantiene un
mapa interno de productos y sus cantidades. Proporciona operaciónes para
agregar, eliminar, reservar y liberar stock.
"""


class Inventario:
    """Gestor simple de inventario.

    La estructura interna es un diccionario privado que mapea el código del
    producto a una tupla (producto, stock). Se exponen métodos para operar
    sobre esa estructura sin revelar su implementación.
    """

    def __init__(self):
        # mapa codigo -> (producto, stock)
        self._productos = {}

    def agregar_producto(self, producto, cantidad=0):
        """Agrega o actualiza un producto con la cantidad dada.

        Lanza ValueError si la cantidad es negativa.
        """
        if cantidad < 0:
            raise ValueError("cantidad debe ser mayor o igual a 0")
        # Use el nuevo método mostrar_codigo para obtener el código
        self._productos[producto.mostrar_codigo()] = (producto, int(cantidad))

    def eliminar_producto(self, codigo):
        """Elimina un producto por su código. Devuelve True si se eliminó."""
        if codigo in self._productos:
            del self._productos[codigo]
            return True
        return False

    def obtener_producto(self, codigo):
        """Devuelve la instancia de producto si existe, o None."""
        # Devuelve la instancia de producto si existe
        item = self._productos.get(codigo)
        return item[0] if item else None

    def stock_de(self, codigo):
        """Devuelve la cantidad disponible del producto (0 si no existe)."""
        item = self._productos.get(codigo)
        return item[1] if item else 0

    def reservar(self, codigo, cantidad=1):
        """Intenta reservar 'cantidad' unidades. Devuelve True si la reserva fue exitosa."""
        if codigo not in self._productos:
            return False
        producto, stock = self._productos[codigo]
        if stock < cantidad:
            return False
        # decrementar stock
        self._productos[codigo] = (producto, stock - cantidad)
        return True

    def liberar(self, codigo, cantidad=1):
        """Libera unidades devueltas al stock. Devuelve True si OK."""
        if codigo not in self._productos:
            return False
        producto, stock = self._productos[codigo]
        self._productos[codigo] = (producto, stock + int(cantidad))
        return True

    def listar_productos(self):
        """Devuelve una lista de tuplas (codigo, nombre, precio, stock)."""
        salida = []
        for p, q in self._productos.values():
            # Usar los métodos descriptivos para exponer los atributos
            salida.append((p.mostrar_codigo(), p.mostrar_nombre(), p.mostrar_precio(), q))
        return salida
