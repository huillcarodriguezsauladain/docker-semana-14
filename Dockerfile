# Imagen base oficial ligera (slim)
FROM python:3.11-slim

# Variables de entorno no sensibles (evita .pyc y muestra logs en tiempo real)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=5000

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar e instalar dependencias primero (aprovecha caché de capas)
COPY requirements.txt .
RUN pip install --no-cache-dir \
    --trusted-host pypi.org \
    --trusted-host pypi.python.org \
    --trusted-host files.pythonhosted.org \
    -r requirements.txt

# Copiar código fuente
COPY . .

# Ejecutar tests durante el build (garantiza calidad antes de empaquetar)
RUN python -m unittest discover -s . -p "test_*.py" -v

# Crear usuario no-root para ejecución segura (buena práctica de producción)
RUN useradd --create-home appuser && chown -R appuser:appuser /app
USER appuser

# Puerto expuesto por la aplicación
EXPOSE 5000

# Comando al iniciar el contenedor
CMD ["python", "app.py"]
