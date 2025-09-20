# src/pdf/pdf_generator.py
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # carpeta src
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
OUTPUT_DIR = os.path.join(BASE_DIR, "..", "output")


def generar_pdf(factura):
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    filename = os.path.join(OUTPUT_DIR, f"factura_{factura.numero}.pdf")
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    # --- Logo ---
    logo_path = os.path.join(ASSETS_DIR, "logo.jpg")
    if os.path.exists(logo_path):
        # Dibuja el logo en la parte superior izquierda
        c.drawImage(logo_path, 30, height - 100, width=80, height=80, mask="auto")

    # --- Encabezado Empresa ---
    c.setFont("Helvetica-Bold", 16)
    c.drawString(120, height - 50, "Mi Empresa S.A.")
    c.setFont("Helvetica", 10)
    c.drawString(120, height - 65, "NIT: 123456789-0")
    c.drawString(120, height - 80, "Dirección: Calle Falsa 123")
    c.drawString(120, height - 95, "Teléfono: 555-1234")

    # --- Datos cliente ---
    c.setFont("Helvetica-Bold", 12)
    c.drawString(30, height - 130, f"Factura No: {factura.numero}")
    c.drawString(30, height - 150, "Cliente:")
    c.setFont("Helvetica", 10)
    c.drawString(100, height - 150, factura.cliente.nombre)
    c.drawString(100, height - 165, "ID: " + factura.cliente.identificacion)
    c.drawString(100, height - 180, factura.cliente.direccion)
    c.drawString(100, height - 195, factura.cliente.telefono)

    # --- Tabla productos ---
    y = height - 230
    c.setFont("Helvetica-Bold", 10)
    c.drawString(30, y, "Descripción")
    c.drawString(250, y, "Cantidad")
    c.drawString(320, y, "Precio")
    c.drawString(400, y, "Subtotal")

    c.setFont("Helvetica", 10)
    for p in factura.productos:
        y -= 20
        c.drawString(30, y, p.descripcion)
        c.drawString(250, y, str(p.cantidad))
        c.drawString(320, y, f"${p.precio_unitario:.2f}")
        c.drawString(400, y, f"${p.subtotal:.2f}")

    # --- Total ---
    y -= 40
    c.setFont("Helvetica-Bold", 12)
    c.drawString(320, y, "TOTAL:")
    c.drawString(400, y, f"${factura.total:.2f}")

    c.save()
    return filename
