# Usa uma imagem oficial do Python como base.
# Escolha a versão do Python que você precisa (ex: 3.9-slim-buster, 3.10-alpine, etc.)
FROM python:3.13.3

# Define o diretório de trabalho dentro do contêiner.
# Todos os comandos subsequentes serão executados neste diretório.
WORKDIR /app

# Copia o arquivo de requisitos para o diretório de trabalho.
# É uma boa prática copiar apenas este arquivo primeiro para aproveitar o cache do Docker.
COPY requirements.txt .

# Instala as dependências do Python.
# O --no-cache-dir evita que o pip armazene pacotes em cache, reduzindo o tamanho da imagem final.
# O --upgrade pip garante que o pip esteja atualizado.
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copia o restante do código da aplicação para o diretório de trabalho.
# O ponto final significa copiar tudo do diretório atual (local) para o WORKDIR (/app no contêiner).
COPY . .

# Expõe a porta em que a aplicação será executada.
# Por exemplo, se sua aplicação Flask/Django roda na porta 5000, você a expõe aqui.
EXPOSE 8080

# Comando para executar a aplicação quando o contêiner for iniciado.
CMD ["python", "app.py", "--host", "0.0.0.0", "--port", "8080"]
