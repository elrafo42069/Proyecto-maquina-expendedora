from datetime import datetime
from clase_transaccion import Transaccion

class GestorReportes:
    def __init__(self):
        self.historial_ventas = []
        self.contador_errores = 0

    def registrar_venta(self, codigo_producto, monto, hash_tarjeta):
        venta = Transaccion(codigo_producto, monto, hash_tarjeta)
        self.historial_ventas.append(venta)
        print(f"Venta registrada: {venta}")

    def registrar_intento_fallido(self):
        self.contador_errores += 1
        print(f"Intento fallido registrado (total: {self.contador_errores})")

    def generar_reporte_texto(self, ruta):
        try:
            with open(ruta, 'w', encoding='utf-8') as archivo:
                archivo.write("--- REPORTE DE VENTAS ---\n")
                archivo.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                archivo.write("-------------------------\n\n")

                if not self.historial_ventas:
                    archivo.write("No hay ventas registradas.\n")
                    return

                ventas_por_producto = {}
                total_productos = 0
                total_dinero = 0.0
                gastos_por_usuario = {}

                for venta in self.historial_ventas:
                    codigo = venta.obtener_codigo()
                    monto = venta.obtener_monto()
                    hash_tarjeta = venta.hash_tarjeta

                    if codigo in ventas_por_producto:
                        ventas_por_producto[codigo] += 1
                    else:
                        ventas_por_producto[codigo] = 1

                    total_productos += 1
                    total_dinero += monto

                    if hash_tarjeta in gastos_por_usuario:
                        gastos_por_usuario[hash_tarjeta] += monto
                    else:
                        gastos_por_usuario[hash_tarjeta] = monto

                archivo.write("Ventas por producto:\n")
                for codigo, cantidad in ventas_por_producto.items():
                    archivo.write(f"  - {codigo}: {cantidad} unidades\n")

                archivo.write(f"\nTotal de productos vendidos: {total_productos}\n")
                archivo.write(f"Total de dinero cobrado: ${total_dinero:.2f}\n\n")

                archivo.write("Gastos por usuario (hash de tarjeta):\n")
                for hash_tarjeta, gasto in gastos_por_usuario.items():
                    hash_corto = hash_tarjeta[:10] + "..." if len(hash_tarjeta) > 10 else hash_tarjeta
                    archivo.write(f"  - {hash_corto}: ${gasto:.2f}\n")

                archivo.write(f"\nTotal de usuarios: {len(gastos_por_usuario)}\n")
                archivo.write(f"Intentos fallidos: {self.contador_errores}\n")
                if total_productos > 0:
                    promedio = total_dinero / total_productos
                    archivo.write(f"Promedio por venta: ${promedio:.2f}\n")

                archivo.write("\n--- Fin del reporte ---\n")
            print(f"Reporte generado en: {ruta}")
        except Exception as e:
            print(f"Error al generar reporte: {e}")

    def obtener_resumen(self):
        if not self.historial_ventas:
            return {
                'total_ventas': 0,
                'total_dinero': 0.0,
                'total_usuarios': 0,
                'errores': self.contador_errores
            }
        total_dinero = sum(v.obtener_monto() for v in self.historial_ventas)
        usuarios_unicos = set(v.hash_tarjeta for v in self.historial_ventas)
        return {
            'total_ventas': len(self.historial_ventas),
            'total_dinero': total_dinero,
            'total_usuarios': len(usuarios_unicos),
            'errores': self.contador_errores
        }