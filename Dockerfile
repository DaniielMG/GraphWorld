<<<<<<< HEAD
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
COPY api.py .
COPY procesamiento.py .
COPY analisis_grafo.py .
COPY elestats.csv .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

=======
# Imagen base de Python
FROM python:3.11-slim

# Directorio de trabajo
WORKDIR /app

# Copiar archivos necesarios
COPY requirements.txt .
COPY api.py .
COPY procesamiento.py .
COPY analisis_grafo.py .
# Nota: Si no subiste el CSV a GitHub, el despliegue fallará. 
# Para la prueba de AWS, asegúrate de tener una versión pequeña de elestats.csv
COPY elestats.csv .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto que usa FastAPI
EXPOSE 8000

# Comando para arrancar la API
>>>>>>> 578b0a74ddcf2c8eb15d54920d3bd461a1441912
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]