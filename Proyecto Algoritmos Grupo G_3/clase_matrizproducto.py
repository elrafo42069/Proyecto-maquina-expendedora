import requests
from clase_producto import Producto, Bebida, Chucheria

class MatrizProductos:
    def __init__(self):
        self.celdas = {}
        self.columnas = ['A', 'B', 'C', 'D', 'E']
        self.filas = ['1', '2', '3', '4', '5']

    def sincronizar_precios_github(self, url_repo):
        print("Verificando precios en GitHub...")
        try:
            if 'github.com' in url_repo:
                url_raw = url_repo.replace('github.com', 'raw.githubusercontent.com')
                if not url_raw.endswith('/'):
                    url_raw += '/'
                url_raw += 'main/inventario.txt'
                respuesta = requests.get(url_raw, timeout=5)
                if respuesta.status_code == 200:
                    precios_actualizados = 0
                    lineas = respuesta.text.split('\n')
                    for linea in lineas:
                        linea = linea.strip()
                        if linea and not linea.startswith('#'):
                            partes = linea.split(',')
                            if len(partes) >= 8:
                                coordenada = partes[0].strip()
                                codigo = partes[1].strip()
                                precio_github = float(partes[3].strip())
                                if coordenada in self.celdas:
                                    producto = self.celdas[coordenada][0]
                                    if producto.codigo == codigo and producto.precio != precio_github:
                                        producto.actualizar_precio(precio_github)
                                        precios_actualizados += 1
                    if precios_actualizados > 0:
                        print(f"Precios actualizados: {precios_actualizados} productos")
                    else:
                        print("Todos los precios estan actualizados")
                    return True
        except:
            print("No se pudo conectar a GitHub. Usando precios locales.")
        print("Usando precios locales (sin cambios)")
        return False

    def cargar_desde_archivo(self, ruta):
        try:
            with open(ruta, 'r', encoding='utf-8') as archivo:
                for linea in archivo:
                    linea = linea.strip()
                    if not linea or linea.startswith('#'):
                        continue
                    partes = linea.split(',')
                    if len(partes) >= 8:
                        coordenada = partes[0].strip()
                        codigo = partes[1].strip()
                        nombre = partes[2].strip()
                        precio = float(partes[3].strip())
                        stock = int(partes[4].strip())
                        mensaje = partes[5].strip()
                        tipo = partes[6].strip()
                        extra = int(partes[7].strip())

                        if tipo == 'Bebida':
                            producto = Bebida(codigo, nombre, precio, stock, mensaje, extra)
                        elif tipo == 'Chucheria':
                            producto = Chucheria(codigo, nombre, precio, stock, mensaje, extra)
                        else:
                            producto = Producto(codigo, nombre, precio, stock, mensaje)

                        self.celdas[coordenada] = [producto, stock]
            print(f"Inventario cargado desde {ruta}")
            return True
        except FileNotFoundError:
            print(f"Archivo {ruta} no encontrado. Creando inventario de ejemplo...")
            self.crear_inventario_ejemplo()
            return False
        except Exception as e:
            print(f"Error al cargar inventario: {e}")
            return False

    def crear_inventario_ejemplo(self):
        productos_ejemplo = [
            ('A1', 'CocaC', 'Coca-Cola', 1.50, 10, 'Disfruta tu Coca-Cola!', 'Bebida', 330),
            ('B1', 'Pepsi', 'Pepsi', 1.40, 8, 'Refrescate con Pepsi!', 'Bebida', 330),
            ('C1', 'Fanta', 'Fanta', 1.30, 6, 'Sabor a naranja!', 'Bebida', 330),
            ('D1', 'Malta', 'Malta', 1.60, 5, 'Energia y sabor!', 'Bebida', 330),
            ('A2', 'Chint', 'Chintos', 0.80, 12, 'Crujientes!', 'Chucheria', 50),
            ('B2', 'SvvUp', 'Suvup', 0.90, 10, 'Sabor intenso!', 'Chucheria', 40),
            ('C2', 'Goldn', 'Golden', 1.00, 8, 'Los clasicos!', 'Chucheria', 45),
            ('D2', 'Aquak', 'Aqua-K', 0.70, 15, 'Hidratacion!', 'Bebida', 500),
            ('A3', 'Ruffl', 'Ruffles', 1.10, 7, 'Onduladas!', 'Chucheria', 60),
            ('B3', 'Dorit', 'Doritos', 1.20, 6, 'Sabor a queso!', 'Chucheria', 55),
            ('C3', 'Cheet', 'Cheetos', 1.00, 9, 'Bolitas de queso!', 'Chucheria', 50),
            ('D3', 'Yuqts', 'Yogurt', 1.30, 4, 'Saludable!', 'Bebida', 200),
        ]
        for datos in productos_ejemplo:
            if datos[7] == 'Bebida':
                producto = Bebida(datos[1], datos[2], datos[3], datos[4], datos[5], datos[7])
            else:
                producto = Chucheria(datos[1], datos[2], datos[3], datos[4], datos[5], datos[7])
            self.celdas[datos[0]] = [producto, datos[4]]
        print("Inventario de ejemplo creado")

    def guardar_en_archivo(self, ruta):
        try:
            with open(ruta, 'w', encoding='utf-8') as archivo:
                archivo.write("#Inventario de la Maquina Expendedora\n")
                archivo.write("#coordenada,codigo,nombre,precio,stock,mensaje,tipo,extra\n\n")
                for coordenada, datos in self.celdas.items():
                    producto = datos[0]
                    stock = datos[1]
                    tipo = 'Producto'
                    extra = 0
                    if isinstance(producto, Bebida):
                        tipo = 'Bebida'
                        extra = producto.mililitros
                    elif isinstance(producto, Chucheria):
                        tipo = 'Chucheria'
                        extra = producto.gramos
                    linea = f"{coordenada},{producto.codigo},{producto.nombre_completo},{producto.precio},{stock},{producto.mensaje_despedida},{tipo},{extra}\n"
                    archivo.write(linea)
            print(f"Inventario guardado en {ruta}")
        except Exception as e:
            print(f"Error al guardar inventario: {e}")

    def mostrar_catalogo_matriz(self):
        print("\n---CATALOGO DE PRODUCTOS---")
        encabezado = "   "
        for col in self.columnas:
            encabezado += f"{col:>8}"
        print(encabezado)
        print("-----------------------------")
        for fila in self.filas:
            linea = f"{fila:>2} "
            for col in self.columnas:
                coordenada = col + fila
                if coordenada in self.celdas and self.celdas[coordenada][1] > 0:
                    producto = self.celdas[coordenada][0]
                    nombre_corto = producto.nombre_completo[:7]
                    linea += f"{nombre_corto:>8}"
                else:
                    linea += "   ---  "
            print(linea)
        print("-----------------------------")
        print("Instrucciones:")
        print("-Escribe una coordenada (ej: A1) para comprar")
        print("-Escribe 'RS' para hacer restock")
        print("-Escribe 'RP' para generar reporte")
        print("-Escribe 'SALIR' para terminar")
        print("-----------------------------")

    def obtener_producto(self, coordenada):
        if coordenada in self.celdas and self.celdas[coordenada][1] > 0:
            return self.celdas[coordenada][0]
        return None

    def actualizar_stock_celda(self, coordenada, nueva_cantidad):
        if coordenada in self.celdas:
            if nueva_cantidad >= 0:
                self.celdas[coordenada][1] = nueva_cantidad
                self.celdas[coordenada][0].stock = nueva_cantidad
                print(f"Stock actualizado en {coordenada}: {nueva_cantidad}")
            else:
                print("La cantidad no puede ser negativa")
        else:
            print(f"La coordenada {coordenada} no existe")

    def asignar_nuevo_producto(self, coordenada, codigo, cantidad):
        nombre = input(f"Nombre del producto para {codigo}: ")
        while True:
            try:
                precio = float(input("Precio del producto: "))
                if precio >= 0:
                    break
                else:
                    print("El precio no puede ser negativo")
            except ValueError:
                print("Debes ingresar un numero valido")
        mensaje = input("Mensaje de despedida: ")
        while True:
            tipo = input("Tipo (Bebida/Chucheria): ").strip().lower()
            if tipo in ['bebida', 'chucheria']:
                break
            else:
                print("Tipo debe ser 'Bebida' o 'Chucheria'")
        if tipo == 'bebida':
            while True:
                try:
                    mililitros = int(input("Mililitros: "))
                    if mililitros > 0:
                        break
                    else:
                        print("Los mililitros deben ser positivos")
                except ValueError:
                    print("Debes ingresar un numero entero")
            producto = Bebida(codigo, nombre, precio, cantidad, mensaje, mililitros)
        else:
            while True:
                try:
                    gramos = int(input("Gramos: "))
                    if gramos > 0:
                        break
                    else:
                        print("Los gramos deben ser positivos")
                except ValueError:
                    print("Debes ingresar un numero entero")
            producto = Chucheria(codigo, nombre, precio, cantidad, mensaje, gramos)
        self.celdas[coordenada] = [producto, cantidad]
        print(f"Producto {codigo} asignado a {coordenada} con {cantidad} unidades")