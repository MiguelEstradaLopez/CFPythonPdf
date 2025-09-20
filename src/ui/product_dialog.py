# src/ui/product_dialog.py
from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from src.db.models import Producto


class ProductDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Agregar Producto")
        self.setFixedSize(300, 200)

        self.descripcion = QLineEdit()
        self.cantidad = QLineEdit()
        self.precio_unitario = QLineEdit()

        form = QFormLayout()
        form.addRow("Descripción:", self.descripcion)
        form.addRow("Cantidad:", self.cantidad)
        form.addRow("Precio unitario:", self.precio_unitario)

        btn_guardar = QPushButton("Agregar")
        btn_guardar.clicked.connect(self.acceptar)

        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addWidget(btn_guardar)

        self.setLayout(layout)

    def acceptar(self):
        try:
            cantidad = int(self.cantidad.text())
            precio = float(self.precio_unitario.text())
            if not self.descripcion.text():
                raise ValueError("Descripción vacía")

            self.producto = Producto(self.descripcion.text(), cantidad, precio)
            self.accept()
        except ValueError:
            QMessageBox.warning(self, "Error", "Debe ingresar valores válidos.")

    def get_producto(self):
        return getattr(self, "producto", None)
