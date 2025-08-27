# Usar imagem slim do Python 3.12
FROM python:3.12-slim

# Definir variáveis de ambiente para evitar prompts interativos
ENV DEBIAN_FRONTEND=noninteractive

# Instalar dependências de sistema para o Playwright (necessárias para o Chromium)
RUN apt-get update && apt-get install -y \
    libnss3 \
    libxss1 \
    libasound2 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libpango-1.0-0 \
    libcairo2 \
    libatspi2.0-0 \
    fonts-dejavu \
    fonts-noto \
    fonts-unifont \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Definir diretório de trabalho
WORKDIR /app

# Copiar arquivo de requisitos e instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Instalar apenas o navegador Chromium, sem reinstalar dependências
RUN playwright install chromium

# Copiar arquivos do projeto
COPY . .

# Comando para executar a aplicação
CMD ["python", "src/bot.py"]