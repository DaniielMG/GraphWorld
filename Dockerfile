# Imagen base de Python
FROM python:3.11-slim

# Directorio de trabajo
WORKDIR /app

# Copiar archivos necesarios
COPY requirements.txt .
COPY api.py .
COPY procesamiento.py .
COPY analisis_grafo.py .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto que usa FastAPI
EXPOSE 8000

# Comando para arrancar la API
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]