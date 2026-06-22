import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from clase_maquinaexpendedora import MaquinaExpendedora

if __name__ == "__main__":
    print("\n---BIENVENIDO A LA MAQUINA EXPENDEDORA---")
    print("Usa coordenadas tipo ajedrez (ej: A1, B3)")
    print("--------------------------------------------\n")

    url_repo = "https://github.com/FernandoSapient/BPTSP05_2526-3"
    maquina = MaquinaExpendedora(url_repo)
    maquina.ejecutar_menu_principal()

    print("\n--- HASTA LUEGO ---")