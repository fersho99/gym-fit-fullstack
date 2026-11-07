# Gym Fit

Aplicación full stack del gimnasio Gym Fit: backend con Django, DRF y JWT, y frontend con React y Vite.
Resultado de Aprendizaje de las Unidades 2 y 3 de Desarrollo Web Integral.

## Funciones

- Login con JWT, registro de usuarios y sesión persistente con `AuthContext`.
- Dashboard protegido con los datos del usuario (`/auth/me/`).
- Widget de clima que consume la API de [Open-Meteo](https://open-meteo.com/) con `fetch`.
- Endpoint que consume el servicio SOAP público CountryInfoService con `zeep`.

## Requisitos

- Python 3.14
- Node.js 24

## Instalación del backend

```bash
cd backend
python -m venv venv
./venv/Scripts/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

El backend queda en `http://localhost:8000`, y la documentación de la API en `http://localhost:8000/swagger/`.

## Instalación del frontend

En otra terminal:

```bash
cd frontend
cp .env.example .env
npm install
npm run dev
```

El frontend queda en `http://localhost:5173`.

## Endpoints principales

| Ruta | Acceso | Descripción |
| --- | --- | --- |
| `POST /api/v1/auth/register/` | Público | Crea una cuenta |
| `POST /api/v1/auth/token/` | Público | Login con email y contraseña; devuelve los tokens |
| `POST /api/v1/auth/token/refresh/` | Público | Renueva el token de acceso |
| `GET /api/v1/auth/me/` | Con token | Datos del usuario que inició sesión |
| `GET /api/v1/soap/country/<código ISO>/` | Con token | Datos de un país, obtenidos por SOAP; por ejemplo `MX` |
| `/api/v1/users/` | Administradores | CRUD de usuarios |

## Pruebas

```bash
cd backend
python manage.py test
```
