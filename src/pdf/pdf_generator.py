# src/pdf/pdf_generator.py
# Este módulo se encarga de crear una representación en PDF de una factura.
# Utiliza la librería ReportLab para dibujar el contenido del documento.

import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from src.db.models import Factura

# --- Definición de rutas ---
# BASE_DIR apunta a la carpeta 'src'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# ASSETS_DIR es la ruta a la carpeta de recursos (imágenes, etc.)
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
# OUTPUT_DIR es la ruta donde se guardarán los PDFs generados.
OUTPUT_DIR = os.path.join(BASE_DIR, "..", "output")


def generar_pdf(factura: Factura) -> str:
    """
    Genera un archivo PDF para una factura dada.
    
    Args:
        factura (Factura): El objeto de factura con todos los datos a imprimir.
        
    Returns:
        str: La ruta del archivo PDF generado.
    """
    # Asegura que el directorio de salida exista; si no, lo crea.
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # Define el nombre del archivo PDF usando el número de la factura.
    filename = os.path.join(OUTPUT_DIR, f"factura_{factura.numero}.pdf")
    
    # Crea un objeto Canvas, que es el "lienzo" sobre el que se dibuja el PDF.
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4  # Obtiene el ancho y alto de una página A4.

    # --- Dibuja el Logo de la Empresa ---
    logo_path = os.path.join(ASSETS_DIR, "logo.jpg")
    if os.path.exists(logo_path):
        # Dibuja la imagen en la esquina superior izquierda.
        # Las coordenadas (0,0) en ReportLab están en la esquina inferior izquierda.
        c.drawImage(logo_path, 30, height - 100, width=80, height=80, mask="auto")

    # --- Dibuja el Encabezado con los datos de la Empresa ---
    c.setFont("Helvetica-Bold", 16)
    c.drawString(120, height - 50, "Mi Empresa S.A.")
    c.setFont("Helvetica", 10)
    c.drawString(120, height - 65, "NIT: 123456789-0")
    c.drawString(120, height - 80, "Dirección: Calle Falsa 123")
    c.drawString(120, height - 95, "Teléfono: 555-1234")

    # --- Dibuja los Datos del Cliente y de la Factura ---
    c.setFont("Helvetica-Bold", 12)
    c.drawString(30, height - 130, f"Factura No: {factura.numero}")
    c.drawString(30, height - 150, "Cliente:")
    c.setFont("Helvetica", 10)
    c.drawString(100, height - 150, factura.cliente.nombre)
    c.drawString(100, height - 165, "ID: " + factura.cliente.identificacion)
    c.drawString(100, height - 180, factura.cliente.direccion)
    c.drawString(100, height - 195, factura.cliente.telefono)

    # --- Dibuja la Tabla de Productos ---
    # Posición vertical inicial para la tabla.
    y = height - 230
    c.setFont("Helvetica-Bold", 10)
    # Encabezados de la tabla
    c.drawString(30, y, "Descripción")
    c.drawString(250, y, "Cantidad")
    c.drawString(320, y, "Precio")
    c.drawString(400, y, "Subtotal")

    c.setFont("Helvetica", 10)
    # Itera sobre cada producto en la factura para dibujarlo en una fila.
    for p in factura.productos:
        y -= 20  # Mueve la posición vertical hacia abajo para la siguiente fila.
        c.drawString(30, y, p.descripcion)
        c.drawString(250, y, str(p.cantidad))
        c.drawString(320, y, f"${p.precio_unitario:.2f}")
        c.drawString(400, y, f"${p.subtotal:.2f}")

    # --- Dibuja el Total de la Factura ---
    y -= 40  # Añade un espacio antes del total.
    c.setFont("Helvetica-Bold", 12)
    c.drawString(320, y, "TOTAL:")
    c.drawString(400, y, f"${factura.total:.2f}")

    # Guarda el archivo PDF en el disco.
    c.save()
    
    # Devuelve la ruta completa del archivo generado.
    return filename