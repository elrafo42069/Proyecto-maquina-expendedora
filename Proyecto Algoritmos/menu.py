from clase_maquina import MaquinaExpendedora

class Menu:
    """Interfaz de usuario en consola."""
    
    def __init__(self, maquina: MaquinaExpendedora):
        self.maquina = maquina
    
    def mostrar_catalogo(self):
        self.maquina.inventario.mostrar_catalogo_matriz()
    
    def leer_opcion(self) -> str:
        return input("Ingrese código de producto (ej: A1), 'RS' o 'RP': ").strip()
    
    def loop_principal(self):
        while True:
            self.mostrar_catalogo()
            opcion = self.leer_opcion()
            
            if opcion.upper() == "RS":
                self.maquina.procesar_restock()
            elif opcion.upper() == "RP":
                self.maquina.procesar_reporte()
            else:
                #Asumimos coordenada
                self.maquina.procesar_venta(opcion.upper())