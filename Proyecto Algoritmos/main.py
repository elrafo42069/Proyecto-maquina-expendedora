from clase_maquina import MaquinaExpendedora
from menu import Menu

def main():
    url_repo = "https://raw.githubusercontent.com/FernandoSapient/BPTSP05_2526-3/main/"
    
    # Crear máquina
    maquina = MaquinaExpendedora(url_repo)
    maquina.iniciar_sistema()
    
    # Crear menú y ejecutar
    menu = Menu(maquina)
    menu.loop_principal()

if __name__ == "__main__":
    main()