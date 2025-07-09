import os

class Image:
    BASE_DIR = os.path.dirname(__file__)  # Diretório onde _my_images.py está

    LOGO = os.path.join(BASE_DIR, "logo.png")
    POWERED = os.path.join(BASE_DIR, "powered.png")

    # Converte para caminhos absolutos finais
    LOGO = os.path.abspath(LOGO)
    POWERED = os.path.abspath(POWERED)
