# Imagen de Python
FROM python:3.13-slim

# Herramientas del sistema que necesita Python para conectarse a MySQL
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential pkg-config default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Primero las librerías (así Docker las guarda en caché)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Después el código del backend
COPY . .

EXPOSE 8000

# Crea las tablas en MySQL y arranca el servidor en todas las redes
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
