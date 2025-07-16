# Ataques

Esta pasta contém scripts para simulação de ataques de segurança.

## Ataques MITM

1. **ARP Spoofing**:
   ```bash
   docker build -t mitm-attacker ./mitm/
   docker run --network host --cap-add=NET_ADMIN mitm-attacker
   ```

2. **SSL Stripping**:
   ```bash
   python ssl_strip.py -t <target_ip> -g <gateway_ip>
   ```

## Ataques SQL Injection

1. **Testes básicos**:
   ```bash
   chmod +x basic_injection.sh
   ./basic_injection.sh
   ```

2. **Ataque UNION**:
   ```bash
   python union_attack.py -u http://localhost:8080
   ```

## Utilitários

- `network_scanner.py`: Varre a rede local
- `payload_generator.py`: Cria payloads para testes
