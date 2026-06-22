# Clases Producto, Bebida y Chucheria

class Producto:
    def __init__(self, codigo, nombre_completo, precio, stock, mensaje_despedida):
        self.codigo = codigo
        self.nombre_completo = nombre_completo
        self.precio = precio
        self.stock = stock
        self.mensaje_despedida = mensaje_despedida

    def actualizar_precio(self, nuevo_precio):
        if nuevo_precio >= 0:
            self.precio = nuevo_precio
            print(f"Precio actualizado a {nuevo_precio} para {self.nombre_completo}")
        else:
            print("Error: El precio no puede ser negativo")

    def disminuir_stock(self, cantidad):
        if self.stock >= cantidad:
            self.stock -= cantidad
            return True
        else:
            print(f"No hay suficiente stock de {self.nombre_completo}")
            return False

    def __str__(self):
        return f"{self.codigo} - {self.nombre_completo} - ${self.precio} - Stock: {self.stock}"


class Bebida(Producto):
    def __init__(self, codigo, nombre_completo, precio, stock, mensaje_despedida, mililitros):
        super().__init__(codigo, nombre_completo, precio, stock, mensaje_despedida)
        self.mililitros = mililitros

    def __str__(self):
        return f"{super().__str__()} - {self.mililitros}ml"


class Chucheria(Producto):
    def __init__(self, codigo, nombre_completo, precio, stock, mensaje_despedida, gramos):
        super().__init__(codigo, nombre_completo, precio, stock, mensaje_despedida)
        self.gramos = gramos

    def __str__(self):
        return f"{super().__str__()} - {self.gramos}g"
