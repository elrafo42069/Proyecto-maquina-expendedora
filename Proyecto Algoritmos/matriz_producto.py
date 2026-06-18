import json
import os
from typing import Optional, Dict

class Producto:
    """Clase base para todos los productos."""
    
    def __init__(self, codigo: str, nombre_completo: str, precio: float, 
                 stock: int, mensaje_despedida: str = ""):
        self.codigo = codigo                # 5 letras
        self.nombre_completo = nombre_completo
        self.precio = precio
        self._stock = stock                 # privado para control
        self.mensaje_despedida = mensaje_despedida
    
    @property
    def stock(self) -> int:
        return self._stock
    
    def actualizar_precio(self, nuevo_precio: float) -> None:
        """Cambia el precio del producto."""
        self.precio = nuevo_precio
    
    def disminuir_stock(self, cantidad: int = 1) -> bool:
        """Reduce el stock en 'cantidad'. Devuelve True si fue posible."""
        if self._stock >= cantidad:
            self._stock -= cantidad
            return True
        return False
    
    def aumentar_stock(self, cantidad: int) -> None:
        """Aumenta el stock (para restock)."""
        self._stock += cantidad


class Bebida(Producto):
    """Subclase de Producto para bebidas (añade mililitros)."""
    
    def __init__(self, codigo: str, nombre_completo: str, precio: float, 
                 stock: int, mensaje_despedida: str, mililitros: int):
        super().__init__(codigo, nombre_completo, precio, stock, mensaje_despedida)
        self.mililitros = mililitros


class Chucheria(Producto):
    """Subclase de Producto para chucherías (añade gramos)."""
    
    def __init__(self, codigo: str, nombre_completo: str, precio: float, 
                 stock: int, mensaje_despedida: str, gramos: int):
        super().__init__(codigo, nombre_completo, precio, stock, mensaje_despedida)
        self.gramos = gramos


class MatrizProducto:
    """Catálogo en forma de matriz con coordenadas (ej: 'A1')."""
    
    def __init__(self):
        self._celdas: Dict[str, Producto] = {}   # clave: coordenada, valor: Producto
        self.filas = 5
        self.columnas = 4
    
    def cargar_desde_archivo(self, ruta: str) -> bool:
        """
        Carga el inventario desde un archivo JSON.
        Retorna True si se cargó correctamente, False si no.
        """
        if not os.path.exists(ruta):
            print(f"Archivo no encontrado: {ruta}")
            return False
        
        try:
            with open(ruta, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            if not data:
                print("El archivo está vacío.")
                return False
            
            for item in data:
                # Verificar campos obligatorios
                if 'coordenada' not in item or 'codigo' not in item:
                    print("Error: faltan campos obligatorios en el JSON")
                    continue
                
                tipo = item.get('tipo', 'Producto')
                
                # Crear el producto según su tipo
                if tipo == 'Bebida':
                    prod = Bebida(
                        codigo=item['codigo'],
                        nombre_completo=item.get('nombre', item['codigo']),
                        precio=item.get('precio', 0.0),
                        stock=item.get('stock', 0),
                        mensaje_despedida=item.get('mensaje_despedida', ''),
                        mililitros=item.get('mililitros', 0)
                    )
                elif tipo == 'Chucheria':
                    prod = Chucheria(
                        codigo=item['codigo'],
                        nombre_completo=item.get('nombre', item['codigo']),
                        precio=item.get('precio', 0.0),
                        stock=item.get('stock', 0),
                        mensaje_despedida=item.get('mensaje_despedida', ''),
                        gramos=item.get('gramos', 0)
                    )
                else:
                    prod = Producto(
                        codigo=item['codigo'],
                        nombre_completo=item.get('nombre', item['codigo']),
                        precio=item.get('precio', 0.0),
                        stock=item.get('stock', 0),
                        mensaje_despedida=item.get('mensaje_despedida', '')
                    )
                
                self._celdas[item['coordenada']] = prod
            
            print(f"Inventario cargado correctamente ({len(self._celdas)} productos).")
            return True
            
        except json.JSONDecodeError as e:
            print(f"Error al leer el archivo JSON: {e}")
            return False
        except Exception as e:
            print(f"Error al cargar inventario: {e}")
            return False
    
    def guardar_en_archivo(self, ruta: str) -> None:
        """Guarda el inventario actual en un archivo JSON."""
        try:
            data = []
            for coord, prod in self._celdas.items():
                item = {
                    'coordenada': coord,
                    'codigo': prod.codigo,
                    'nombre': prod.nombre_completo,
                    'precio': prod.precio,
                    'stock': prod.stock,
                    'mensaje_despedida': prod.mensaje_despedida,
                    'tipo': prod.__class__.__name__
                }
                
                # Agregar atributos específicos según el tipo
                if isinstance(prod, Bebida):
                    item['mililitros'] = prod.mililitros
                elif isinstance(prod, Chucheria):
                    item['gramos'] = prod.gramos
                
                data.append(item)
            
            # Crear directorio si no existe
            directorio = os.path.dirname(ruta)
            if directorio and not os.path.exists(directorio):
                os.makedirs(directorio)
            
            with open(ruta, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"Inventario guardado en {ruta}")
            
        except Exception as e:
            print(f"Error al guardar inventario: {e}")
    
    def mostrar_catalogo_matriz(self) -> None:
        """Imprime la matriz con formato del enunciado."""
        if not self._celdas:
            print("Inventario vacío.")
            return
        
        # Determinar dimensiones máximas
        letras = set()
        filas = set()
        for coord in self._celdas.keys():
            if len(coord) >= 2:
                letras.add(coord[0])
                try:
                    filas.add(int(coord[1:]))
                except ValueError:
                    continue
        
        if not letras or not filas:
            print("No se pudo determinar la estructura de la matriz.")
            return
        
        columnas = sorted(letras)
        filas_max = max(filas)
        
        # Imprimir encabezado
        print("   " + " ".join(columnas))
        
        # Imprimir filas
        for f in range(1, filas_max + 1):
            linea = f"{f:2} "
            for col in columnas:
                coord = f"{col}{f}"
                prod = self._celdas.get(coord)
                if prod and prod.stock > 0:
                    # Mostrar código de 5 letras (ajustar a 6 caracteres)
                    linea += f"{prod.codigo:6} "
                else:
                    linea += "       "  # 7 espacios (coincide con el formato)
            print(linea)
    
    def obtener_producto(self, coordenada: str) -> Optional[Producto]:
        """Devuelve el producto en la coordenada si existe y tiene stock."""
        prod = self._celdas.get(coordenada)
        if prod and prod.stock > 0:
            return prod
        return None
    
    def actualizar_stock_celda(self, coordenada: str, nueva_cantidad: int) -> bool:
        """
        Actualiza el stock de un producto existente en la coordenada.
        Retorna True si se actualizó correctamente.
        """
        prod = self._celdas.get(coordenada)
        if prod:
            # Acceso directo al stock (se puede hacer con un método setter)
            prod._stock = nueva_cantidad
            print(f"Stock actualizado a {nueva_cantidad} en coordenada {coordenada}")
            return True
        else:
            print(f"No hay producto en la coordenada {coordenada}")
            return False
    
    def asignar_nuevo_producto(self, coordenada: str, codigo: str, cantidad: int) -> None:
        """
        Asigna un nuevo producto a una coordenada.
        Crea un producto básico (se puede mejorar pidiendo más datos).
        """
        # Verificar que el código tenga 5 caracteres
        if len(codigo) != 5:
            print(f"Advertencia: el código {codigo} no tiene 5 letras.")
        
        # Crear producto genérico
        prod = Producto(
            codigo=codigo,
            nombre_completo=f"Producto {codigo}",
            precio=0.0,
            stock=cantidad,
            mensaje_despedida=""
        )
        self._celdas[coordenada] = prod
        print(f"Nuevo producto {codigo} asignado en coordenada {coordenada} con {cantidad} unidades")
    
    def obtener_todos_productos(self) -> list:
        """Devuelve lista de todos los productos (incluidos sin stock)."""
        return list(self._celdas.values())
    
    def obtener_producto_por_codigo(self, codigo: str) -> Optional[Producto]:
        """Busca un producto por su código (útil para reportes)."""
        for prod in self._celdas.values():
            if prod.codigo == codigo:
                return prod
        return None
    
    def __repr__(self):
        return f"MatrizProducto({len(self._celdas)} productos)"