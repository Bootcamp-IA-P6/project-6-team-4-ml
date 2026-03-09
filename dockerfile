# 1. Imagen base de Python ligera
FROM python:3.11-slim

# 2. Directorio de trabajo dentro del contenedor
WORKDIR /app

# 3. Instalamos uv para gestionar las librerías
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# 4. Copiamos archivos de dependencias e instalamos
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen

# 5. Copiamos el código y los modelos
COPY models/ ./models/
COPY assets/ ./assets/
COPY app.py ./


# 6. Creamos la carpeta docs para el historial (el volumen se conectará aquí)
RUN mkdir -p docs

# 7. Exponemos el puerto que usa Streamlit
EXPOSE 8501

# 8. Comando para arrancar la aplicación
CMD ["uv", "run", "streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]