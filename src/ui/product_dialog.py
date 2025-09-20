# src/ui/product_dialog.py
# Define un cuadro de diálogo modal para agregar un nuevo producto a la factura.

from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from src.db.models import Producto


class ProductDialog(QDialog):
    """
    Un cuadro de diálogo que permite al usuario ingresar los detalles de un
    producto (descripción, cantidad, precio) y lo devuelve como un objeto Producto.
    """
    def __init__(self, parent=None):
        """
        Inicializa el diálogo, creando los campos de entrada y los botones.
        
        Args:
            parent (QWidget, optional): El widget padre de este diálogo. Defaults to None.
        """
        super().__init__(parent)
        self.setWindowTitle("Agregar Producto")
        self.setFixedSize(300, 200)

        # --- Campos de Entrada ---
        self.descripcion = QLineEdit()
        self.cantidad = QLineEdit()
        self.precio_unitario = QLineEdit()

        # --- Layout del Formulario ---
        form = QFormLayout()
        form.addRow("Descripción:", self.descripcion)
        form.addRow("Cantidad:", self.cantidad)
        form.addRow("Precio unitario:", self.precio_unitario)

        # --- Botón de Guardar ---
        btn_guardar = QPushButton("Agregar")
        # Conecta el clic del botón al método que valida y acepta los datos.
        btn_guardar.clicked.connect(self.acceptar)

        # --- Layout Principal ---
        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addWidget(btn_guardar)
        self.setLayout(layout)
        
        # Atributo para almacenar el producto creado.
        self.producto = None

    def acceptar(self):
        """
        Se ejecuta al hacer clic en 'Agregar'.
        Valida los datos de entrada, crea un objeto Producto y cierra el diálogo.
        """
        try:
            # Intenta convertir los campos de texto a los tipos de datos correctos.
            cantidad = int(self.cantidad.text())
            precio = float(self.precio_unitario.text())
            
            # Valida que la descripción no esté vacía.
            if not self.descripcion.text().strip():
                raise ValueError("La descripción no puede estar vacía.")

            # Si los datos son válidos, crea el objeto Producto.
            self.producto = Producto(self.descripcion.text(), cantidad, precio)
            
            # Llama al método accept() de QDialog, que cierra el diálogo
            # y establece su código de resultado en "Aceptado".
            self.accept()
            
        except ValueError as e:
            # Si ocurre un error de conversión o validación, muestra un mensaje de advertencia.
            QMessageBox.warning(self, "Error de Validación", f"Por favor, ingrese valores válidos.\n\n{e}")

    def get_producto(self) -> Producto | None:
        """
        Método de conveniencia para obtener el producto creado después de que el diálogo se cierra.
        
        Returns:
            Producto | None: El objeto Producto si fue creado exitosamente, o None si no.
        """
        return self.producto