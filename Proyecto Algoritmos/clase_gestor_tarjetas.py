import hashlib
import requests
from typing import Dict

class GestorTarjetas:
    """Gestiona tarjetas prepagadas: hash, saldo, validación."""
    
    def __init__(self):
        self._tarjetas_validas: Dict[str, float] = {}   # hash -> saldo
    
    def sincronizar_tarjetas_remoto(self, url_repo: str) -> bool:
        """Descarga tarjetas desde GitHub (formato JSON)."""
        try:
            # Asumimos que hay un archivo tarjetas.json en el repo
            resp = requests.get(url_repo + "tarjetas.json", timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                for item in data:
                    # Cada item: {"numero": "123...", "saldo": 100}
                    hash_num = self.calcular_hash_sha256(item['numero'])
                    self._tarjetas_validas[hash_num] = item['saldo']
                return True
        except:
            pass
        return False
    
    @staticmethod
    def calcular_hash_sha256(texto: str) -> str:
        """Calcula el hash SHA-256 de un texto."""
        return hashlib.sha256(texto.encode()).hexdigest()
    
    def verificar_tarjeta(self, hash_tarjeta: str) -> bool:
        """Comprueba si el hash corresponde a una tarjeta válida."""
        return hash_tarjeta in self._tarjetas_validas
    
    def obtener_saldo(self, hash_tarjeta: str) -> float:
        """Devuelve el saldo de una tarjeta, o 0.0 si no existe."""
        return self._tarjetas_validas.get(hash_tarjeta, 0.0)
    
    def deducir_saldo(self, hash_tarjeta: str, monto: float) -> bool:
        """Descuenta monto del saldo si es suficiente. Devuelve True si éxito."""
        if hash_tarjeta not in self._tarjetas_validas:
            return False
        saldo_actual = self._tarjetas_validas[hash_tarjeta]
        if saldo_actual >= monto:
            self._tarjetas_validas[hash_tarjeta] = saldo_actual - monto
            return True
        return False

