# src/db/models.py
# Este módulo define las clases de datos (modelos) que representan las entidades
# principales de la aplicación, como Cliente, Producto y Factura.

from typing import List, Optional
from datetime import datetime

class Cliente:
    """Representa a un cliente con su información de contacto."""
    def __init__(self, nombre: str, identificacion: str, direccion: str, telefono: str):
        """
        Inicializa un objeto Cliente.
        
        Args:
            nombre (str): Nombre completo del cliente.
            identificacion (str): DNI, NIF, o identificador fiscal.
            direccion (str): Dirección de facturación.
            telefono (str): Número de teléfono de contacto.
        """
        self.nombre = nombre
        self.identificacion = identificacion
        self.direccion = direccion
        self.telefono = telefono


class Producto:
    """Representa un item (producto o servicio) en una factura."""
    def __init__(self, descripcion: str, cantidad: int, precio_unitario: float):
        """
        Inicializa un objeto Producto.
        
        Args:
            descripcion (str): Nombre o descripción del producto/servicio.
            cantidad (int): Número de unidades.
            precio_unitario (float): Costo por unidad.
        """
        self.descripcion = descripcion
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario
        # El subtotal se calcula automáticamente al crear el producto.
        self.subtotal = round(cantidad * precio_unitario, 2)


class Factura:
    """Representa una factura completa, asociando un cliente y una lista de productos."""
    def __init__(self, numero: int, cliente: Cliente, productos: List[Producto], fecha_emision: Optional[datetime] = None):
        """
        Inicializa un objeto Factura.
        
        Args:
            numero (int): Número identificador único de la factura.
            cliente (Cliente): El cliente al que se le emite la factura.
            productos (List[Producto]): Lista de productos incluidos en la factura.
            fecha_emision (Optional[datetime]): Fecha de emisión. Si es None, se usa la fecha y hora actual.
        """
        self.numero = numero
        # Si no se proporciona fecha de emisión, se asigna la fecha y hora actuales.
        self.fecha_emision = fecha_emision if fecha_emision else datetime.now()
        self.cliente = cliente
        self.productos = productos

    @property
    def total(self) -> float:
        """
        Calcula el monto total de la factura sumando los subtotales de todos los productos.
        Es una propiedad, por lo que se accede como 'factura.total' en lugar de 'factura.total()'.
        
        Returns:
            float: El total de la factura, redondeado a dos decimales.
        """
        return round(sum(p.subtotal for p in self.productos), 2)