# Imagen de Node.js
FROM node:24-alpine

WORKDIR /app

# Primero las dependencias de React
COPY package*.json ./
RUN npm ci

# Después el código del frontend
COPY . .

EXPOSE 5173

# --host 0.0.0.0: el servidor escucha en todas las redes para que el navegador
# pueda entrar desde fuera del contenedor (si no, la página sale en blanco)
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
