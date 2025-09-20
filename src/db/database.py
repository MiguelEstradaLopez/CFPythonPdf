# src/db/database.py
# Este módulo gestiona la persistencia de datos utilizando un archivo CSV como base de datos.
# Se encarga de inicializar, guardar y leer información de las facturas.

import os
import csv
from src.db.models import Factura

# Define el nombre del archivo que actuará como base de datos.
DB_FILE = "facturas.csv"


def inicializar_db():
    """
    Asegura que la base de datos (archivo CSV) exista.
    Si el archivo no existe, lo crea y escribe la fila de encabezado.
    """
    # Comprueba si el archivo de la base de datos ya existe en el disco.
    if not os.path.exists(DB_FILE):
        # Si no existe, lo abre en modo escritura ('w') para crearlo.
        with open(DB_FILE, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            # Escribe los nombres de las columnas en la primera fila.
            writer.writerow([
                "numero",
                "fecha_emision",
                "cliente_nombre",
                "cliente_identificacion",
                "cliente_direccion",
                "cliente_telefono",
                "productos",  # Los productos se guardarán como una cadena de texto.
                "total"
            ])


def guardar_factura(factura: Factura):
    """
    Añade una nueva fila al archivo CSV para guardar una factura.
    
    Args:
        factura (Factura): El objeto de la factura que se va a guardar.
    """
    # Abre el archivo en modo 'append' ('a') para añadir datos sin sobreescribir.
    with open(DB_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        # Prepara una lista de cadenas con los datos de la factura para escribirla en una fila.
        writer.writerow([
            factura.numero,
            factura.fecha_emision.strftime("%Y-%m-%d %H:%M:%S"),
            factura.cliente.nombre,
            factura.cliente.identificacion,
            factura.cliente.direccion,
            factura.cliente.telefono,
            # Serializa la lista de productos en una sola cadena de texto.
            "; ".join([f"{p.descripcion} x{p.cantidad} @ {p.precio_unitario}" for p in factura.productos]),
            f"{factura.total:.2f}"
        ])


def obtener_ultimo_numero() -> int:
    """
    Lee el archivo CSV para encontrar el número de factura más alto utilizado.
    
    Returns:
        int: El último número de factura encontrado, o 0 si no hay ninguna.
    """
    # Si el archivo no existe, no hay facturas, por lo que el último número es 0.
    if not os.path.exists(DB_FILE):
        return 0
    
    # Abre el archivo en modo lectura ('r').
    with open(DB_FILE, mode="r", newline="", encoding="utf-8") as f:
        # Usa DictReader para leer las filas como diccionarios (clave: nombre de columna).
        reader = csv.DictReader(f)
        # Crea una lista de todos los números de factura, convirtiéndolos a enteros.
        numeros = [int(row["numero"]) for row in reader if row.get("numero")]
        # Devuelve el número más alto de la lista, o 0 si la lista está vacía.
        return max(numeros) if numeros else 0