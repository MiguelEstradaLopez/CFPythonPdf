# src/db/database.py
import os
import csv
from src.db.models import Factura

DB_FILE = "facturas.csv"


def inicializar_db():
    """Crea el archivo CSV si no existe, con encabezados."""
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "numero",
                "fecha_emision",
                "cliente_nombre",
                "cliente_identificacion",
                "cliente_direccion",
                "cliente_telefono",
                "productos",  # guardado como texto
                "total"
            ])


def guardar_factura(factura: Factura):
    """Guarda una factura en el archivo CSV."""
    with open(DB_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            factura.numero,
            factura.fecha_emision.strftime("%Y-%m-%d %H:%M:%S"),
            factura.cliente.nombre,
            factura.cliente.identificacion,
            factura.cliente.direccion,
            factura.cliente.telefono,
            "; ".join([f"{p.descripcion} x{p.cantidad} @ {p.precio_unitario}" for p in factura.productos]),
            f"{factura.total:.2f}"
        ])


def obtener_ultimo_numero() -> int:
    """Devuelve el último número de factura registrado en el CSV."""
    if not os.path.exists(DB_FILE):
        return 0
    with open(DB_FILE, mode="r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        numeros = [int(row["numero"]) for row in reader if row.get("numero")]
        return max(numeros) if numeros else 0
