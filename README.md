# SoftPoli - Sistema de Gestión de Flota y Servicios

SoftPoli es una aplicación web desarrollada en Django para la gestión integral de vehículos, servicios de mantenimiento, piezas, técnicos y requerimientos (TDRs) en una organización.

## Características principales

- **Gestión de Vehículos:** Registro, edición y seguimiento de vehículos y su estado operativo.
- **Gestión de Servicios:** Creación y control de servicios de mantenimiento preventivo y correctivo, con cálculo automático de kilometraje.
- **Gestión de Piezas:** Control de stock, punto de reorden y movimientos de piezas utilizadas en servicios.
- **Gestión de Técnicos y Personal:** Asignación de técnicos y responsables a cada servicio.
- **Gestión de TDRs:** Consolidación y generación de reportes PDF de requerimientos.
- **Dashboard visual:** Indicadores clave, gráficos de servicios por mes, vehículos por estado y lista de piezas bajo stock.
- **Seguridad:** Acceso restringido mediante login, solo usuarios autorizados pueden operar el sistema.

## Requisitos

- Python 3.10+
- Django 4.x+
- [django-autocomplete-light](https://django-autocomplete-light.readthedocs.io/)
- Chart.js (CDN incluido en el template)
- Bootstrap 5 (CDN incluido en el template)
- Otros paquetes según requirements.txt

## Instalación

1. **Clona el repositorio:**
   ```bash
   git clone https://github.com/tuusuario/softpoli.git
   cd softpoli

2. python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

3. pip install -r requirements.txt

4. python manage.py migrate

5. python manage.py createsuperuser

6. python manage.py runserver

---

## 🇬🇧 English

# SoftPoli - Fleet and Services Management System

SoftPoli is a web application developed in Django for the comprehensive management of vehicles, maintenance services, parts, technicians, and requirements (TDRs) in an organization.

## Main Features

- **Vehicle Management:** Register, edit, and track vehicles and their operational status.
- **Service Management:** Create and control preventive and corrective maintenance services, with automatic mileage calculation.
- **Parts Management:** Stock control, reorder point, and tracking of parts used in services.
- **Technician and Staff Management:** Assign technicians and responsible staff to each service.
- **TDR Management:** Consolidation and PDF report generation of requirements.
- **Visual Dashboard:** Key indicators, monthly service charts, vehicle status charts, and a list of low-stock parts.
- **Security:** Restricted access via login; only authorized users can operate the system.

## Requirements

- Python 3.10+
- Django 4.x+
- [django-autocomplete-light](https://django-autocomplete-light.readthedocs.io/)
- Chart.js (CDN included in the template)
- Bootstrap 5 (CDN included in the template)
- Other packages as listed in requirements.txt

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/youruser/softpoli.git
   cd softpoli

