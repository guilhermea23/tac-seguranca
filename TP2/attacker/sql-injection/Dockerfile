FROM debian:bullseye-slim

# Instalar dependências
RUN apt-get update && \
    apt-get install -y curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Criar diretório de trabalho
WORKDIR /app

# Copiar o script de SQLi
COPY basic_injection.sh .

# Tornar o script executável
RUN chmod +x basic_injection.sh

# Comando padrão do contêiner
CMD ["./basic_injection.sh"]
