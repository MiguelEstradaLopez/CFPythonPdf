# 🧾 Sistema de Facturación en Python (PyQt6 + ReportLab)

Este proyecto es una aplicación de escritorio en **Python** para gestionar facturas.
Incluye interfaz gráfica con **PyQt6**, exportación a **PDF** con ReportLab y almacenamiento en **CSV**.

---

## ✨ Características

- Interfaz gráfica moderna con **PyQt6**.
- Formulario de cliente con validaciones:
  - Nombre
  - Identificación (NIT o cédula)
  - Dirección
  - Teléfono
- Gestión de productos/servicios:
  - Descripción
  - Cantidad
  - Precio unitario
  - Subtotal calculado automáticamente
- Exportación de facturas a **PDF profesional** con logo y formato tabular.
- Almacenamiento de facturas en un archivo **CSV**.
- Numeración automática de facturas.
- Validaciones de datos en cliente y productos.

---

## 🗂️ Estructura del proyecto

mi_proyecto_facturas/
├── main.pyw # Punto de entrada de la aplicación
├── output/ # Facturas generadas en PDF
├── src/
│ ├── assets/ # Recursos (logo de la empresa, etc.)
│ │ └── logo.jpg
│ ├── db/
│ │ └── database.py # Manejo de CSV (facturas)
│ ├── logic/
│ │ └── invoice_manager.py # Lógica de negocio (validaciones, numeración)
│ ├── models.py # Definición de clases: Cliente, Producto, Factura
│ ├── pdf/
│ │ └── pdf_generator.py # Generación de facturas en PDF
│ └── ui/
│ └── main_window.py # Interfaz gráfica (PyQt6)

---

## 🛠️ Requisitos

- Python 3.10 o superior
- Entorno virtual recomendado (`venv`)

Librerías necesarias:

- **PyQt6**
- **reportlab**

---

## ⚙️ Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/tuusuario/mi_proyecto_facturas.git
   cd mi_proyecto_facturas

    Crea un entorno virtual:

   ```

python3 -m venv venv
source venv/bin/activate   # Linux / MacOS
venv\Scripts\activate      # Windows

Instala dependencias:

pip install pyqt6 reportlab

Ejecuta la aplicación:

    python main.pyw

📤 Exportación a PDF

    Los PDFs se guardan en la carpeta output/.

    El logo se carga desde src/assets/logo.jpg (puedes reemplazarlo por el de tu empresa).

    Ejemplo de nombre de archivo:

    factura_1.pdf

🗃️ Base de datos (CSV)

    Las facturas quedan registradas en facturas.csv en la raíz del proyecto.

    Ejemplo de registro:

numero,fecha_emision,cliente_nombre,cliente_identificacion,cliente_direccion,cliente_telefono,productos,total
1,2025-09-19 15:30:12,Juan Pérez,12345678,Calle 10 #5-20,3001234567,"Laptop x1 @ 2500.0; Mouse x2 @ 50.0",2600.00

🚀 Mejoras futuras

    Integrar una base de datos real (SQLite o PostgreSQL).

    Añadir reportes de ventas.

    Implementar búsqueda y consulta de facturas anteriores desde la interfaz.

    Generar gráficos estadísticos de facturación.

👨‍💻 Autor: Miguel Angel Estrada Lopez (Miki)

Proyecto desarrollado en Python con ❤️ para prácticas de facturación y generación de PDFs.
