# main.pyw
# Punto de entrada principal para la aplicación de facturación.
# Este script inicializa y ejecuta la interfaz gráfica de usuario (GUI).

import sys
from PyQt6.QtWidgets import QApplication
from src.ui.main_window import MainWindow

def main():
    """
    Configura e inicia la aplicación PyQt.
    Crea la instancia de la aplicación, muestra la ventana principal
    y comienza el bucle de eventos.
    """
    # Crea una instancia de QApplication, necesaria para cualquier aplicación con GUI de PyQt.
    app = QApplication(sys.argv)
    
    # Crea una instancia de la ventana principal de la aplicación.
    window = MainWindow()
    
    # Muestra la ventana principal.
    window.show()
    
    # Inicia el bucle de eventos de la aplicación y asegura una salida limpia.
    sys.exit(app.exec())


if __name__ == "__main__":
    # Llama a la función principal solo cuando el script se ejecuta directamente.
    # Esto previene que el código se ejecute si el script es importado en otro módulo.
    main()