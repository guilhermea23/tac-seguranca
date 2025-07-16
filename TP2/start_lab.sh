#!/bin/bash

# Script para iniciar ambiente SQLi em Docker

echo "[INFO] Construindo containers..."
docker-compose up --build -d

echo "[INFO] Containers iniciados:"
docker ps

echo "[INFO] Acesse DVWA em: http://localhost:8080"
echo "[INFO] Monitoramento de logs ativo no container 'monitor'"
echo "[INFO] Snort rodando e escutando na interface eth0"

echo "[INFO] Use docker logs para verificar eventos. Exemplo:"
echo "       docker logs log_monitor"
echo "       docker logs snort"
