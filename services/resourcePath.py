import sys
import os

def resource_path(relative_path):
    """Obter o caminho absoluto do recurso, lidando com o executável."""
    if hasattr(sys, '_MEIPASS'):
        # Caso o executável esteja em execução
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)
