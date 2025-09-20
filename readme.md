# Sistema de Generación de Facturas en PDF

Este es un sistema de escritorio simple, desarrollado en Python, para crear y gestionar facturas, guardarlas en un archivo CSV y exportarlas a formato PDF.

## Características

- **Interfaz Gráfica de Usuario (GUI)**: Interfaz de usuario intuitiva construida con PyQt6 para una fácil entrada de datos.
- **Gestión de Clientes y Productos**: Permite ingresar datos del cliente y añadir múltiples productos o servicios a cada factura.
- **Numeración Automática**: Asigna automáticamente un número de factura secuencial.
- **Cálculo de Totales**: Calcula automáticamente los subtotales por producto y el total de la factura.
- **Persistencia de Datos**: Guarda un registro de todas las facturas emitidas en un archivo `facturas.csv`.
- **Exportación a PDF**: Genera un archivo PDF con un formato profesional para cada factura, incluyendo un logo de la empresa.

## Requisitos

Para ejecutar este proyecto, necesitarás tener Python 3 instalado. Las dependencias de Python se listan en el archivo `requirements.txt`.

- Python 3.x
- PyQt6
- ReportLab
- Pandas
- Numpy

## Instalación y Ejecución

1. **Clona el repositorio:**

   ```bash
   git clone https://github.com/MiguelEstradaLopez/CFPythonPdf.git
   cd CFPythonPdf
   ```
2. **Crea un entorno virtual (recomendado):**

   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```
3. **Instala las dependencias:**

   ```bash
   pip install -r requirements.txt
   ```
4. **Ejecuta la aplicación:**

   ```bash
   python main.pyw
   ```

   Las facturas en PDF se guardarán en el directorio `output/`.

## Estructura del Proyecto

```
.
├── main.pyw                # Punto de entrada de la aplicación
├── requirements.txt        # Dependencias de Python
├── facturas.csv            # Base de datos de facturas
├── output/                 # Directorio para los PDFs generados
│   └── ...
└── src/
    ├── assets/             # Recursos como el logo
    │   └── logo.jpg
    ├── db/
    │   ├── database.py     # Lógica para interactuar con el CSV
    │   └── models.py       # Clases de datos (Factura, Cliente, Producto)
    ├── logic/
    │   └── invoice_manager.py # Lógica de negocio (validación, etc.)
    ├── pdf/
    │   └── pdf_generator.py # Lógica para crear los PDFs
    └── ui/
        ├── main_window.py  # Ventana principal de la GUI
        └── product_dialog.py # Diálogo para añadir productos
```
