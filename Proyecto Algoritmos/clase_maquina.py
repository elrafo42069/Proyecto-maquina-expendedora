from matriz_producto import MatrizProducto
from clase_gestor_tarjetas import GestorTarjetas
from clase_gestor_reporte import GestorReportes
from clase_producto import Producto

class MaquinaExpendedora:
    """Clase principal que orquesta el sistema."""
    
    def __init__(self, url_repo: str):
        self.url_repositorio = url_repo
        self.inventario = MatrizProducto()
        self.gestor_tarjetas = GestorTarjetas()
        self.gestor_reportes = GestorReportes()
    
    def iniciar_sistema(self) -> None:
        """Carga inicial: inventario local y sincronización con GitHub."""
        # Cargar inventario local
        if not self.inventario.cargar_desde_archivo("datos/inventario.json"):
            print("Archivo de inventario no encontrado. Se inicia con inventario vacío.")
        
        # Sincronizar tarjetas desde GitHub
        if self.gestor_tarjetas.sincronizar_tarjetas_remoto(self.url_repositorio):
            print("Tarjetas sincronizadas desde GitHub.")
        else:
            print("No se pudo conectar a GitHub. Se usan tarjetas locales si existen.")
    
    def ejecutar_menu_principal(self) -> None:
        """Bucle principal de la interfaz (delegado a Menu más adelante)."""
        # Este método se implementará en el menú. Lo dejamos como placeholder.
        pass
    
    def procesar_venta(self, coordenada: str) -> None:
        """Procesa la venta de un producto en la coordenada dada."""
        # 1. Obtener producto
        producto = self.inventario.obtener_producto(coordenada)
        if not producto:
            print("Producto no disponible o sin stock.")
            return
        
        # 2. Mostrar precio
        print(f"Precio: ${producto.precio:.2f}")
        
        # 3. Pedir número de tarjeta
        num_tarjeta = input("Ingrese número de tarjeta: ").strip()
        if not num_tarjeta:
            print("Venta cancelada.")
            return
        
        # 4. Validar tarjeta (hash)
        hash_tarjeta = GestorTarjetas.calcular_hash_sha256(num_tarjeta)
        if not self.gestor_tarjetas.verificar_tarjeta(hash_tarjeta):
            print("Tarjeta no válida.")
            self.gestor_reportes.registrar_intento_fallido()
            return
        
        # 5. Verificar saldo
        saldo = self.gestor_tarjetas.obtener_saldo(hash_tarjeta)
        if saldo < producto.precio:
            print("Saldo insuficiente.")
            self.gestor_reportes.registrar_intento_fallido()
            return
        
        # 6. Confirmación
        confirm = input(f"¿Confirma compra de {producto.nombre_completo}? (s/N): ").strip().lower()
        if confirm != 's':
            print("Venta cancelada.")
            return
        
        # 7. Ejecutar venta
        if producto.disminuir_stock(1):
            if self.gestor_tarjetas.deducir_saldo(hash_tarjeta, producto.precio):
                # Registrar transacción
                self.gestor_reportes.registrar_venta(producto.codigo, producto.precio, hash_tarjeta)
                # Guardar inventario
                self.inventario.guardar_en_archivo("datos/inventario.json")
                print(f"Dispensando {producto.nombre_completo}...")
                if producto.mensaje_despedida:
                    print(producto.mensaje_despedida)
                else:
                    print("¡Disfrute su producto!")
            else:
                # Si falla el descuento, revertir stock (no debería ocurrir)
                producto.aumentar_stock(1)
                print("Error al procesar el pago.")
        else:
            print("Error: no se pudo descontar stock.")
    
    def procesar_restock(self) -> None:
        """Menú de restock con dos opciones."""
        print("\n--- RESTOCK ---")
        print("1. Actualizar existencia de inventario")
        print("2. Cambiar producto")
        opcion = input("Seleccione opción: ").strip()
        
        coordenada = input("Ingrese coordenada (ej: A1): ").strip().upper()
        
        if opcion == "1":
            nueva_cant = int(input("Ingrese nueva cantidad: "))
            self.inventario.actualizar_stock_celda(coordenada, nueva_cant)
            self.inventario.guardar_en_archivo("datos/inventario.json")
            print("Stock actualizado.")
        elif opcion == "2":
            nuevo_codigo = input("Ingrese nuevo código de 5 letras: ").strip()
            cantidad = int(input("Ingrese cantidad: "))
            self.inventario.asignar_nuevo_producto(coordenada, nuevo_codigo, cantidad)
            self.inventario.guardar_en_archivo("datos/inventario.json")
            print("Producto asignado.")
        else:
            print("Opción inválida.")
    
    def procesar_reporte(self) -> None:
        """Genera un reporte de ventas con fecha."""
        from datetime import datetime
        fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
        ruta = f"datos/reportes/reporte_{fecha}.txt"
        self.gestor_reportes.generar_reporte_texto(ruta)
        print(f"Reporte generado en {ruta}")