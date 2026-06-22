# Clase MaquinaExpendedora

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from clase_matrizproducto import MatrizProductos
from clase_gestortarjetas import GestorTarjetas
from clase_gestorreportes import GestorReportes

class MaquinaExpendedora:
    def __init__(self, url_repositorio):
        self.url_repositorio = url_repositorio
        self.inventario = MatrizProductos()
        self.gestor_tarjetas = GestorTarjetas()
        self.gestor_reportes = GestorReportes()
        self.iniciar_sistema()

    def iniciar_sistema(self):
        print("---CARGANDO SISTEMA---")
        self.inventario.cargar_desde_archivo('datos/inventario.txt')
        self.inventario.sincronizar_precios_github(self.url_repositorio)
        self.gestor_tarjetas.sincronizar_tarjetas_remoto(self.url_repositorio)
        print("Sistema iniciado correctamente")
        print("--------------------------\n")

    def ejecutar_menu_principal(self):
        while True:
            self.inventario.mostrar_catalogo_matriz()
            entrada = input("\nIngresa una opcion: ").strip().upper()
            if entrada == 'SALIR':
                print("Gracias por usar la maquina expendedora")
                self.inventario.guardar_en_archivo('datos/inventario.txt')
                break
            elif entrada == 'RS':
                self.procesar_restock()
            elif entrada == 'RP':
                self.procesar_reporte()
            else:
                self.procesar_venta(entrada)

    def procesar_venta(self, coordenada):
        if len(coordenada) < 2:
            print("Formato de coordenada invalido. Usa ej: A1")
            return
        producto = self.inventario.obtener_producto(coordenada)
        if producto is None:
            print(f"No hay producto disponible en {coordenada}")
            self.gestor_reportes.registrar_intento_fallido()
            return
        print(f"\nProducto: {producto.nombre_completo}")
        print(f"Precio: ${producto.precio:.2f}")
        numero_tarjeta = input("Ingresa el numero de tu tarjeta (o presiona Enter para cancelar): ").strip()
        if numero_tarjeta == "":
            print("Venta cancelada")
            return
        hash_tarjeta = self.gestor_tarjetas.calcular_hash_sha256(numero_tarjeta)
        if not self.gestor_tarjetas.verificar_tarjeta(hash_tarjeta):
            print("Tarjeta no valida. Venta cancelada.")
            self.gestor_reportes.registrar_intento_fallido()
            return
        saldo = self.gestor_tarjetas.obtener_saldo(hash_tarjeta)
        if saldo < producto.precio:
            print(f"Saldo insuficiente. Saldo actual: ${saldo:.2f}")
            return
        confirmar = input(f"Confirmar compra de {producto.nombre_completo} por ${producto.precio:.2f}? (S/N): ").strip().upper()
        if confirmar != 'S':
            print("Venta cancelada")
            return
        if not self.gestor_tarjetas.deducir_saldo(hash_tarjeta, producto.precio):
            print("Error al procesar el pago")
            return
        if not producto.disminuir_stock(1):
            print("Error al actualizar el stock")
            return
        self.inventario.actualizar_stock_celda(coordenada, producto.stock)
        self.gestor_reportes.registrar_venta(producto.codigo, producto.precio, hash_tarjeta)
        print(f"\nDispensando {producto.nombre_completo}...")
        print(f"{producto.mensaje_despedida}")
        self.inventario.guardar_en_archivo('datos/inventario.txt')

    def procesar_restock(self):
        print("\n--- OPERACION DE RESTOCK ---")
        print("1. Actualizar existencia de inventario")
        print("2. Cambiar producto")
        print("3. Volver al menu principal")
        opcion = input("\nSelecciona una opcion: ").strip()
        if opcion == '1':
            coordenada = input("Ingresa la coordenada del producto (ej: A1): ").strip().upper()
            if coordenada not in self.inventario.celdas:
                print(f"La coordenada {coordenada} no tiene producto asignado")
                return
            try:
                nueva_cantidad = int(input("Ingresa la nueva cantidad de stock: "))
                if nueva_cantidad < 0:
                    print("La cantidad no puede ser negativa")
                    return
                self.inventario.actualizar_stock_celda(coordenada, nueva_cantidad)
                self.inventario.guardar_en_archivo('datos/inventario.txt')
            except ValueError:
                print("Error: Debes ingresar un numero valido")
        elif opcion == '2':
            coordenada = input("Ingresa la coordenada donde quieres poner el producto (ej: A1): ").strip().upper()
            try:
                codigo = input("Ingresa el codigo de 5 letras del nuevo producto: ").strip().upper()
                if len(codigo) != 5:
                    print("El codigo debe tener exactamente 5 letras")
                    return
                cantidad = int(input("Ingresa la cantidad inicial: "))
                if cantidad < 0:
                    print("La cantidad no puede ser negativa")
                    return
                self.inventario.asignar_nuevo_producto(coordenada, codigo, cantidad)
                self.inventario.guardar_en_archivo('datos/inventario.txt')
            except ValueError:
                print("Error: Debes ingresar un numero valido para la cantidad")
        elif opcion == '3':
            print("Volviendo al menu principal...")
        else:
            print("Opcion no valida")

    def procesar_reporte(self):
        print("\n--- GENERACION DE REPORTE ---")
        self.gestor_reportes.generar_reporte_texto('reporte_ventas.txt')
        print("\nReporte generado exitosamente")
        input("Presiona Enter para continuar...")