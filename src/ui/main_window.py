# src/ui/main_window.py
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
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Facturación")
        self.setGeometry(200, 200, 700, 500)

        # Manager (valida, crea facturas, numeración)
        self.manager = InvoiceManager()
        self.numero_factura = self.manager.obtener_siguiente_numero()

        # Layout principal
        contenedor = QWidget()
        layout = QVBoxLayout()

        # --- Datos cliente ---
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

        # --- Tabla productos ---
        self.tabla = QTableWidget(0, 3)
        self.tabla.setHorizontalHeaderLabels(["Descripción", "Cantidad", "Precio Unitario"])
        layout.addWidget(QLabel("Productos/Servicios:"))
        layout.addWidget(self.tabla)

        # Botones tabla
        botones_layout = QHBoxLayout()
        self.agregar_btn = QPushButton("Agregar Producto")
        self.calcular_btn = QPushButton("Calcular Total")
        botones_layout.addWidget(self.agregar_btn)
        botones_layout.addWidget(self.calcular_btn)
        layout.addLayout(botones_layout)

        # Botón exportar
        self.exportar_btn = QPushButton("Exportar a PDF")
        layout.addWidget(self.exportar_btn)

        contenedor.setLayout(layout)
        self.setCentralWidget(contenedor)

        # Eventos
        self.agregar_btn.clicked.connect(self.agregar_producto)
        self.calcular_btn.clicked.connect(self.calcular_total)
        self.exportar_btn.clicked.connect(self.exportar_pdf)

    def agregar_producto(self):
        """Agrega una fila vacía para un nuevo producto"""
        fila = self.tabla.rowCount()
        self.tabla.insertRow(fila)
        for col in range(3):
            self.tabla.setItem(fila, col, QTableWidgetItem(""))

    def calcular_total(self):
        """Valida y calcula el total de productos en la tabla"""
        try:
            productos = self.obtener_productos()
            total = sum(p.subtotal for p in productos)
            QMessageBox.information(self, "Total", f"Total calculado: ${total:.2f}")
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def exportar_pdf(self):
        """Crea factura, guarda en CSV y genera PDF"""
        try:
            cliente = Cliente(
                nombre=self.nombre_input.text(),
                identificacion=self.identificacion_input.text(),
                direccion=self.direccion_input.text(),
                telefono=self.telefono_input.text(),
            )
            productos = self.obtener_productos()

            factura = self.manager.crear_factura(
                cliente=cliente,
                productos=productos,
                numero=self.numero_factura
            )

            guardar_factura(factura)
            archivo = generar_pdf(factura)

            QMessageBox.information(self, "Éxito", f"Factura generada: {archivo}")

            # Incrementa número de factura para la siguiente
            self.numero_factura += 1

        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def obtener_productos(self):
        """Lee productos de la tabla y devuelve lista de Producto"""
        productos = []
        for fila in range(self.tabla.rowCount()):
            item_desc = self.tabla.item(fila, 0)
            item_cant = self.tabla.item(fila, 1)
            item_precio = self.tabla.item(fila, 2)

            descripcion = item_desc.text().strip() if item_desc else ""
            cantidad_str = item_cant.text().strip() if item_cant else "0"
            precio_str = item_precio.text().strip() if item_precio else "0"

            try:
                cantidad = int(cantidad_str)
                precio = float(precio_str)
            except ValueError:
                raise ValueError("Cantidad y precio deben ser números válidos.")

            productos.append(Producto(descripcion, cantidad, precio))
        return productos


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = MainWindow()
    ventana.show()
    sys.exit(app.exec())
