class Transaccion:
    """Registro de una venta (producto, monto, tarjeta)."""
    
    def __init__(self, codigo_producto: str, monto: float, hash_tarjeta: str):
        self.codigo_producto = codigo_producto
        self.monto = monto
        self.hash_tarjeta = hash_tarjeta
    
    def obtener_codigo(self) -> str:
        return self.codigo_producto
    
    def obtener_monto(self) -> float:
        return self.monto
    
    def __repr__(self):
        return f"Transaccion({self.codigo_producto}, ${self.monto}, {self.hash_tarjeta[:6]}...)"