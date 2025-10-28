# backend/Dockerfile

FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    dos2unix \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 1. Define o diretório de trabalho principal
WORKDIR /code

# 2. Copia PRIMEIRO o ficheiro de requisitos e instala as dependências
#    Isto aproveita o cache do Docker. A instalação só corre de novo se o requirements.txt mudar.
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir -r /code/requirements.txt

# 3. Copia a sua pasta 'app' com todo o código para dentro do WORKDIR
COPY . .

RUN dos2unix /code/entrypoint.sh
RUN chmod +x /code/entrypoint.sh
# 4. Expõe a porta
EXPOSE 8000

ENTRYPOINT ["/code/entrypoint.sh"]
# 5. O comando para iniciar a aplicação.
#    Agora, a partir de /code, o Python vai encontrar a pasta 'app' e tudo o que está dentro dela.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]