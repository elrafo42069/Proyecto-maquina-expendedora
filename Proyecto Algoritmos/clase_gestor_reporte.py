from datetime import datetime
from collections import defaultdict
from typing import List
from clase_transaccion import Transaccion

class GestorReportes:
    """Genera reportes a partir del historial de transacciones."""
    
    def __init__(self):
        self._historial_ventas: List[Transaccion] = []
        self._contador_errores = 0   # intentos fallidos de venta
    
    def registrar_venta(self, codigo_producto: str, monto: float, hash_tarjeta: str) -> None:
        """Añade una transacción exitosa al historial."""
        trans = Transaccion(codigo_producto, monto, hash_tarjeta)
        self._historial_ventas.append(trans)
    
    def registrar_intento_fallido(self) -> None:
        """Incrementa el contador de errores (tarjeta inválida, saldo insuficiente, etc.)."""
        self._contador_errores += 1
    
    def generar_reporte_texto(self, ruta: str) -> None:
        """Genera un archivo de texto con estadísticas de ventas."""
        if not self._historial_ventas:
            # Si no hay ventas, igual generamos un reporte vacío
            with open(ruta, 'w', encoding='utf-8') as f:
                f.write("=== REPORTE DE VENTAS ===\n")
                f.write(f"Fecha: {datetime.now()}\n")
                f.write("No hay ventas registradas.\n")
            return
        
        # Calcular estadísticas
        total_productos = len(self._historial_ventas)
        total_dinero = sum(t.monto for t in self._historial_ventas)
        gasto_por_tarjeta = defaultdict(float)
        for t in self._historial_ventas:
            gasto_por_tarjeta[t.hash_tarjeta] += t.monto
        total_usuarios = len(gasto_por_tarjeta)
        
        # Productos más vendidos (contar por código)
        ventas_por_producto = defaultdict(int)
        for t in self._historial_ventas:
            ventas_por_producto[t.codigo_producto] += 1
        
        with open(ruta, 'w', encoding='utf-8') as f:
            f.write("=== REPORTE DE VENTAS ===\n")
            f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("--- Productos vendidos ---\n")
            for cod, cant in ventas_por_producto.items():
                f.write(f"{cod}: {cant} unidades\n")
            
            f.write(f"\n--- Totales ---\n")
            f.write(f"Total productos vendidos: {total_productos}\n")
            f.write(f"Total dinero cobrado: ${total_dinero:.2f}\n")
            
            f.write(f"\n--- Gasto por usuario (hash tarjeta) ---\n")
            for hash_t, gasto in gasto_por_tarjeta.items():
                f.write(f"{hash_t[:10]}...: ${gasto:.2f}\n")
            
            f.write(f"\nTotal usuarios: {total_usuarios}\n")
            f.write(f"Intentos fallidos de venta: {self._contador_errores}\n")
    
    def generar_graficas_estadisticas(self) -> None:
        """(Opcional) Genera gráficas si se desea. No implementado."""
        print("Función de gráficas no implementada aún.")