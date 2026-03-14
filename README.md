# Ferremas

Ferremas es una aplicación web desarrollada con Django que simula un e-commerce de ferretería.  
Incluye catálogo de productos, autenticación de usuarios, carrito de compras y procesamiento de pagos mediante Mercado Pago.


## Demo

**Aplicación en vivo:**  
https://examen-integracion.onrender.com/

### Credenciales de prueba

Cliente  
usuario: Prueba  
password: prueba  

Administrador  
usuario: admin  
password: admin



---

## Screenshots

![Home](Ferremas/docs/home.png)
![Catalogo](Ferremas/docs/catalogo.png)
![Carrito](Ferremas/docs/carrito.png)
![Agregar Producto](Ferremas/docs/agregar_producto.png)

---

## Stack tecnológico

Backend
- Python
- Django
- SQLite

Frontend
- HTML
- CSS
- JavaScript
- Bootstrap 5

Servicios externos
- Mercado Pago API

---

## Arquitectura

La aplicación sigue una arquitectura basada en el framework Django.

Cliente (HTML / Bootstrap / JavaScript)
        ↓
Django Views
        ↓
Modelos ORM
        ↓
SQLite Database

Para el procesamiento de pagos se integra la API de Mercado Pago
mediante generación de preferencias de pago y redirección al checkout.

---

## Desafíos técnicos

- Integración de Mercado Pago para generar preferencias de pago.
- Implementación de autenticación personalizada con `AbstractUser`.
- Gestión de roles (`admin` y `cliente`).
- Sistema de carrito con actualización dinámica de cantidades.
- Implementación del flujo completo de compra: carrito → creación de orden → pago → confirmación de compra.

---

## Funcionalidades

- Catálogo de productos con stock e imágenes.
- Registro e inicio de sesión de usuarios.
- Carrito de compras.
- Procesamiento de pagos con Mercado Pago.
- Panel de administración para agregar productos

---

## Instalación

```bash
git clone https://github.com/AngelCzu/Examen_Integracion
cd Ferremas
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

---

## Autor

Angel Gabriel Cea Zúñiga

Desarrollador de Software Junior
Ingeniería en Informática – Duoc UC

GitHub: https://github.com/AngelCzu