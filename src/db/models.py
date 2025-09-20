# src/db/models.py

from typing import List, Optional
from datetime import datetime

class Cliente:
    def __init__(self, nombre: str, identificacion: str, direccion: str, telefono: str):
        self.nombre = nombre
        self.identificacion = identificacion
        self.direccion = direccion
        self.telefono = telefono


class Producto:
    def __init__(self, descripcion: str, cantidad: int, precio_unitario: float):
        self.descripcion = descripcion
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario
        self.subtotal = round(cantidad * precio_unitario, 2)


class Factura:
    def __init__(self, numero: int, cliente: Cliente, productos: List[Producto], fecha_emision: Optional[datetime] = None):
        self.numero = numero
        self.fecha_emision = fecha_emision if fecha_emision else datetime.now()
        self.cliente = cliente
        self.productos = productos

    @property
    def total(self) -> float:
        return round(sum(p.subtotal for p in self.productos), 2)
