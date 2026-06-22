class Transaccion:
    def __init__(self, codigo_producto, monto, hash_tarjeta):
        self.codigo_producto = codigo_producto
        self.monto = monto
        self.hash_tarjeta = hash_tarjeta

    def obtener_codigo(self):
        return self.codigo_producto

    def obtener_monto(self):
        return self.monto

    def __str__(self):
        return f"Producto: {self.codigo_producto} - Monto: ${self.monto:.2f}"