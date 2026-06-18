#archivo para trabajar la clase producto y sus subclases
class Producto:
    def __init__(self, codigo:str, nombre_completo:str, precio:float, stock:int, mensaje_despedida:str):
        self.codigo = codigo
        self.nombre_completo = nombre_completo
        self.precio = precio 
        self._stock = stock 
        self.mensaje_despedida = mensaje_despedida
    
    @property
    def stock(self) -> int:
        return self._stock
    
    #Para actualizar precio se usa el atributo de precio
    def actualizar_precio(self, nuevo_precio:float):
        self.precio = nuevo_precio
        
    
    #Reduce el stock en cantidad y si es posible devuelve el true.
    def disminuir_stock(self, cantidad: int = 1) -> bool:
        if self._stock >= cantidad:
            self._stock -= cantidad
            return True
        return False
    
    #Aumenta el stock (para restock).
    def aumentar_stock(self, cantidad: int) -> None:
        self._stock += cantidad

    def __repr__(self):
        return f"{self.codigo} ({self.nombre_completo}) ${self.precio} stock:{self._stock}"


#Subclase de Producto para bebidas (trabja en mL)
class Bebida(Producto):
    
    def __init__(self, codigo: str, nombre_completo: str, precio: float, stock: int, mensaje_despedida: str, mililitros: int):
        super().__init__(codigo, nombre_completo, precio, stock, mensaje_despedida)
        self.mililitros = mililitros
    
    def __repr__(self):
        return f"{super().__repr__()} ({self.mililitros}ml)"


class Chucheria(Producto):
    """Subclase de Producto para chucherías (añade gramos)."""
    
    def __init__(self, codigo: str, nombre_completo: str, precio: float, stock: int, mensaje_despedida: str, gramos: int):
        super().__init__(codigo, nombre_completo, precio, stock, mensaje_despedida)
        self.gramos = gramos
    
    def __repr__(self):
        return f"{super().__repr__()} ({self.gramos}g)"