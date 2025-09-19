FROM python:3.11-slim

WORKDIR /app

# Copiar APENAS o backend
COPY backend/requirements.txt .
COPY backend/ .

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]