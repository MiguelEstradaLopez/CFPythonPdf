# src/ui/main_window.py
# Define la ventana principal de la aplicación y su lógica de interacción.
# Utiliza PyQt6 para construir la interfaz gráfica de usuario.

import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QFormLayout,
    QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QHBoxLayout, QMessageBox
)
from PyQt6.QtCore import Qt

from src.db.models import Cliente, Producto
from src.logic.invoice_manager import InvoiceManager
from src.db.database import guardar_factura
from src.pdf.pdf_generator import generar_pdf


class MainWindow(QMainWindow):
    """
    Ventana principal de la aplicación de facturación.
    Contiene los campos para los datos del cliente, una tabla para los productos
    y los botones para realizar las acciones principales.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Facturación")
        self.setGeometry(200, 200, 700, 500)

        # Inicializa el gestor de lógica de negocio para manejar las facturas.
        self.manager = InvoiceManager()
        # Obtiene el número para la primera factura al iniciar.
        self.numero_factura = self.manager.obtener_siguiente_numero()

        # --- Configuración de la Interfaz ---
        # Widget contenedor principal y layout vertical.
        contenedor = QWidget()
        layout = QVBoxLayout()

        # --- Formulario para los Datos del Cliente ---
        form_layout = QFormLayout()
        self.nombre_input = QLineEdit()
        self.identificacion_input = QLineEdit()
        self.direccion_input = QLineEdit()
        self.telefono_input = QLineEdit()

        form_layout.addRow("Nombre:", self.nombre_input)
        form_layout.addRow("Identificación:", self.identificacion_input)
        form_layout.addRow("Dirección:", self.direccion_input)
        form_layout.addRow("Teléfono:", self.telefono_input)
        layout.addLayout(form_layout)

        # --- Tabla para los Productos/Servicios ---
        self.tabla = QTableWidget(0, 3)
        self.tabla.setHorizontalHeaderLabels(["Descripción", "Cantidad", "Precio Unitario"])
        layout.addWidget(QLabel("Productos/Servicios:"))
        layout.addWidget(self.tabla)

        # --- Botones de Acción para la Tabla ---
        botones_layout = QHBoxLayout()
        self.agregar_btn = QPushButton("Agregar Producto")
        self.calcular_btn = QPushButton("Calcular Total")
        botones_layout.addWidget(self.agregar_btn)
        botones_layout.addWidget(self.calcular_btn)
        layout.addLayout(botones_layout)

        # --- Botón para Exportar a PDF ---
        self.exportar_btn = QPushButton("Exportar a PDF")
        layout.addWidget(self.exportar_btn)

        contenedor.setLayout(layout)
        self.setCentralWidget(contenedor)

        # --- Conexión de Señales y Slots (Eventos) ---
        self.agregar_btn.clicked.connect(self.agregar_producto)
        self.calcular_btn.clicked.connect(self.calcular_total)
        self.exportar_btn.clicked.connect(self.exportar_pdf)

    def agregar_producto(self):
        """Slot para el botón 'Agregar Producto'. Añade una fila en blanco a la tabla."""
        fila = self.tabla.rowCount()
        self.tabla.insertRow(fila)
        # Rellena la nueva fila con celdas vacías.
        for col in range(3):
            self.tabla.setItem(fila, col, QTableWidgetItem(""))

    def calcular_total(self):
        """Slot para 'Calcular Total'. Lee la tabla, calcula el total y lo muestra."""
        try:
            # Obtiene la lista de productos desde la tabla de la UI.
            productos = self.obtener_productos()
            # Calcula el total sumando los subtotales de los productos.
            total = sum(p.subtotal for p in productos)
            QMessageBox.information(self, "Total", f"Total calculado: ${total:.2f}")
        except Exception as e:
            # Muestra un diálogo de advertencia si ocurre un error.
            QMessageBox.warning(self, "Error", str(e))

    def exportar_pdf(self):
        """
        Slot para 'Exportar a PDF'. Orquesta todo el proceso:
        1. Recoge datos de la UI.
        2. Crea la factura usando el InvoiceManager.
        3. Guarda la factura en la base de datos (CSV).
        4. Genera el archivo PDF.
        5. Incrementa el número de factura para la siguiente.
        """
        try:
            # 1. Recoge los datos del cliente desde los campos de texto.
            cliente = Cliente(
                nombre=self.nombre_input.text(),
                identificacion=self.identificacion_input.text(),
                direccion=self.direccion_input.text(),
                telefono=self.telefono_input.text(),
            )
            # Recoge los productos desde la tabla.
            productos = self.obtener_productos()

            # 2. Usa el manager para validar y crear el objeto Factura.
            factura = self.manager.crear_factura(
                cliente=cliente,
                productos=productos,
                numero=self.numero_factura
            )

            # 3. Guarda la factura en el archivo CSV.
            guardar_factura(factura)
            # 4. Genera el archivo PDF.
            archivo = generar_pdf(factura)

            QMessageBox.information(self, "Éxito", f"Factura generada: {archivo}")

            # 5. Prepara el número para la siguiente factura.
            self.numero_factura += 1

        except Exception as e:
            QMessageBox.warning(self, "Error", f"No se pudo generar la factura:\n{e}")

    def obtener_productos(self) -> list[Producto]:
        """
        Lee los datos de la tabla de productos de la UI y los convierte
        en una lista de objetos Producto.
        
        Returns:
            list[Producto]: La lista de productos leídos de la tabla.
            
        Raises:
            ValueError: Si la cantidad o el precio no son números válidos.
        """
        productos = []
        for fila in range(self.tabla.rowCount()):
            item_desc = self.tabla.item(fila, 0)
            item_cant = self.tabla.item(fila, 1)
            item_precio = self.tabla.item(fila, 2)

            # Obtiene el texto de cada celda, con un valor por defecto si está vacía.
            descripcion = item_desc.text().strip() if item_desc else ""
            cantidad_str = item_cant.text().strip() if item_cant else "0"
            precio_str = item_precio.text().strip() if item_precio else "0"

            try:
                # Convierte cantidad y precio a tipos numéricos.
                cantidad = int(cantidad_str)
                precio = float(precio_str)
            except ValueError:
                raise ValueError(f"En la fila {fila + 1}, la cantidad y el precio deben ser números válidos.")

            productos.append(Producto(descripcion, cantidad, precio))
        return productos


# Este bloque permite ejecutar la ventana como un script independiente para pruebas.
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = MainWindow()
    ventana.show()
    sys.exit(app.exec())