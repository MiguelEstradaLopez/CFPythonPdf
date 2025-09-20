# src/logic/invoice_manager.py
import os
from typing import Optional
from datetime import datetime
from src.db import database
from src.db.models import Factura, Cliente, Producto

class InvoiceManager:
    """
    Clase para manejar la lógica de facturación:
    - Numeración automática
    - Validación de datos
    - Creación de facturas
    """

    def __init__(self):
        # Asegura que la base de datos esté inicializada
        database.inicializar_db()

    def obtener_siguiente_numero(self) -> int:
        """
        Obtiene el próximo número de factura basado en las facturas guardadas.
        """
        ultimo = database.obtener_ultimo_numero()
        return ultimo + 1

    def validar_cliente(self, cliente: Cliente) -> None:
        """
        Valida que los campos obligatorios del cliente no estén vacíos.
        """
        if not cliente.nombre.strip():
            raise ValueError("El nombre del cliente es obligatorio.")
        if not cliente.identificacion.strip():
            raise ValueError("La identificación del cliente es obligatoria.")
        if not cliente.direccion.strip():
            raise ValueError("La dirección del cliente es obligatoria.")
        if not cliente.telefono.strip():
            raise ValueError("El teléfono del cliente es obligatorio.")

    def validar_productos(self, productos: list[Producto]) -> None:
        """
        Valida que haya al menos un producto y que todos tengan cantidad y precio válidos.
        """
        if not productos:
            raise ValueError("Debe agregar al menos un producto a la factura.")
        for p in productos:
            if not p.descripcion.strip():
                raise ValueError("La descripción del producto no puede estar vacía.")
            if p.cantidad <= 0:
                raise ValueError(f"La cantidad del producto '{p.descripcion}' debe ser mayor que cero.")
            if p.precio_unitario <= 0:
                raise ValueError(f"El precio unitario del producto '{p.descripcion}' debe ser mayor que cero.")

    def crear_factura(
        self,
        cliente: Cliente,
        productos: list[Producto],
        numero: Optional[int] = None,
        fecha_emision: Optional[datetime] = None,
    ) -> Factura:
        """
        Crea una factura nueva validando datos y generando número automático si no se pasa.
        """
        self.validar_cliente(cliente)
        self.validar_productos(productos)

        if numero is None:
            numero = self.obtener_siguiente_numero()

        return Factura(
            numero=numero,
            cliente=cliente,
            productos=productos,
            fecha_emision=fecha_emision,
        )
