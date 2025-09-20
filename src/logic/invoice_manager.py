# src/logic/invoice_manager.py
# Este módulo contiene la lógica de negocio para la gestión de facturas.
# Separa las reglas de negocio (validación, numeración) de la interfaz de usuario y del acceso a datos.

import os
from typing import Optional
from datetime import datetime
from src.db import database
from src.db.models import Factura, Cliente, Producto


class InvoiceManager:
    """
    Gestiona la lógica de facturación, incluyendo la numeración automática,
    la validación de datos y la creación de objetos de factura.
    """

    def __init__(self):
        """
        Inicializa el gestor de facturas.
        Al crearse, se asegura de que la base de datos (el archivo CSV) esté lista para usarse.
        """
        # Llama a la función para crear el archivo CSV si no existe.
        database.inicializar_db()

    def obtener_siguiente_numero(self) -> int:
        """
        Calcula el próximo número de factura disponible.
        
        Returns:
            int: El número siguiente al de la última factura registrada.
        """
        # Obtiene el último número de factura de la base de datos.
        ultimo = database.obtener_ultimo_numero()
        # El nuevo número será el último más uno.
        return ultimo + 1

    def validar_cliente(self, cliente: Cliente) -> None:
        """
        Verifica que los datos esenciales del cliente no estén vacíos.
        Lanza un error si algún campo obligatorio falta.
        
        Args:
            cliente (Cliente): El objeto cliente a validar.
            
        Raises:
            ValueError: Si un campo obligatorio está vacío.
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
        Verifica que la lista de productos sea válida.
        
        Args:
            productos (list[Producto]): La lista de productos a validar.
            
        Raises:
            ValueError: Si la lista está vacía o si algún producto tiene datos inválidos.
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
        Orquesta la creación de una nueva factura.
        Valida los datos y asigna un número de factura si no se proporciona uno.
        
        Args:
            cliente (Cliente): El cliente de la factura.
            productos (list[Producto]): Los productos de la factura.
            numero (Optional[int]): El número de factura. Si es None, se genera automáticamente.
            fecha_emision (Optional[datetime]): La fecha de emisión. Si es None, se usa la actual.
            
        Returns:
            Factura: El objeto de factura recién creado y validado.
        """
        # Ejecuta las validaciones antes de crear el objeto.
        self.validar_cliente(cliente)
        self.validar_productos(productos)

        # Si no se pasa un número de factura, se obtiene el siguiente disponible.
        if numero is None:
            numero = self.obtener_siguiente_numero()

        # Crea y devuelve el objeto Factura final.
        return Factura(
            numero=numero,
            cliente=cliente,
            productos=productos,
            fecha_emision=fecha_emision,
        )