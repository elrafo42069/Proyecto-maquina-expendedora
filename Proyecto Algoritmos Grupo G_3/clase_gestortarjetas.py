import hashlib
import requests

class GestorTarjetas:
    def __init__(self):
        self.tarjetas_validas = {}

    def calcular_hash_sha256(self, texto):
        texto_bytes = texto.encode('utf-8')
        hash_obj = hashlib.sha256(texto_bytes)
        return hash_obj.hexdigest()

    def sincronizar_tarjetas_remoto(self, url_repo):
        print(f"Conectando al repositorio: {url_repo}")
        try:
            if 'github.com' in url_repo:
                url_raw = url_repo.replace('github.com', 'raw.githubusercontent.com')
                if not url_raw.endswith('/'):
                    url_raw += '/'
                url_raw += 'main/tarjetas.txt'
                respuesta = requests.get(url_raw, timeout=5)
                if respuesta.status_code == 200:
                    lineas = respuesta.text.split('\n')
                    for linea in lineas:
                        linea = linea.strip()
                        if linea and not linea.startswith('#'):
                            partes = linea.split(',')
                            if len(partes) >= 2:
                                hash_tarjeta = partes[0].strip()
                                saldo = float(partes[1].strip())
                                self.tarjetas_validas[hash_tarjeta] = saldo
                    print(f"Tarjetas cargadas desde GitHub: {len(self.tarjetas_validas)} tarjetas")
                    return True
                else:
                    print(f"No se pudo descargar desde GitHub (codigo: {respuesta.status_code})")
        except:
            print("Error de conexion a GitHub. Usando archivo local.")

        print("Cargando tarjetas desde archivo local...")
        try:
            with open('datos/tarjetas.txt', 'r', encoding='utf-8') as archivo:
                for linea in archivo:
                    linea = linea.strip()
                    if linea and not linea.startswith('#'):
                        partes = linea.split(',')
                        if len(partes) >= 2:
                            hash_tarjeta = partes[0].strip()
                            saldo = float(partes[1].strip())
                            self.tarjetas_validas[hash_tarjeta] = saldo
            print(f"Tarjetas cargadas desde archivo local: {len(self.tarjetas_validas)} tarjetas")
            return True
        except FileNotFoundError:
            print("No se encontró archivo local. Usando tarjetas de prueba.")
            tarjetas_prueba = {
                '1234567890': 100.0,
                '9876543210': 150.0,
                '1223334444': 200.0,
                '4444333221': 50.0,
                '1010101010': 300.0
            }
            for numero, saldo in tarjetas_prueba.items():
                hash_calculado = self.calcular_hash_sha256(numero)
                self.tarjetas_validas[hash_calculado] = saldo
            return True
        except Exception as e:
            print(f"Error al cargar tarjetas: {e}")
            return False

    def verificar_tarjeta(self, hash_tarjeta):
        return hash_tarjeta in self.tarjetas_validas

    def obtener_saldo(self, hash_tarjeta):
        if self.verificar_tarjeta(hash_tarjeta):
            return self.tarjetas_validas[hash_tarjeta]
        return -1

    def deducir_saldo(self, hash_tarjeta, monto):
        if not self.verificar_tarjeta(hash_tarjeta):
            print("Tarjeta no valida")
            return False
        saldo_actual = self.tarjetas_validas[hash_tarjeta]
        if saldo_actual >= monto:
            self.tarjetas_validas[hash_tarjeta] = saldo_actual - monto
            print(f"Saldo deducido: ${monto:.2f} - Nuevo saldo: ${saldo_actual - monto:.2f}")
            return True
        else:
            print(f"Saldo insuficiente. Saldo actual: ${saldo_actual:.2f}")
            return False