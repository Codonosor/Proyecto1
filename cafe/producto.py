"""Módulo de productos.

Contiene clases simples que representan productos de la cafetería. Está
intencionadamente ligero y con métodos claros para que sean fáciles de
entender y extender.
"""


class Producto:
    """Producto base para la cafetería.

    Atributos protegidos (_codigo, _nombre, _precio). Proporciona propiedades
    de solo lectura y un método obtener_precio que puede ser sobrescrito por
    subclases si el cálculo del precio cambia.
    """

    def __init__(self, codigo, nombre, precio):
        # Inicializa los datos básicos del producto
        self._codigo = codigo
        self._nombre = nombre
        self._precio = float(precio)

    @property
    def codigo(self):
        # Código identificador del producto (ej. "D001")
        return self._codigo

    @property
    def nombre(self):
        # Nombre legible del producto
        return self._nombre

    @property
    def precio(self):
        # Precio base almacenado
        return self._precio

    def obtener_precio(self):
        """Devuelve el precio del producto.

        Este método es el punto de extensión para polimorfismo: subclases pueden
        sobrescribirlo para aplicar reglas de precio específicas.
        """
        return self._precio


class Alimento(Producto):
    """Producto del tipo alimento.

    Añade atributo de calorías y mantiene el comportamiento por defecto de
    precio.
    """

    def __init__(self, codigo, nombre, precio, calorias=0):
        super().__init__(codigo, nombre, precio)
        self._calorias = int(calorias)

    @property
    def calorias(self):
        # Calorías aproximadas del alimento
        return self._calorias

    def obtener_precio(self):
        # Por ahora, no hay recálculo; devolvemos el precio base
        return self._precio


class Bebida(Producto):
    """Producto del tipo bebida.

    Añade atributo de tamaño en ml y mantiene el comportamiento por defecto de
    precio.
    """

    def __init__(self, codigo, nombre, precio, tam_ml=0):
        super().__init__(codigo, nombre, precio)
        self._tam_ml = int(tam_ml)

    @property
    def tam_ml(self):
        # Volumen de la bebida en mililitros
        return self._tam_ml

    def obtener_precio(self):
        # Por ahora, no hay recálculo; devolvemos el precio base
        return self._precio
