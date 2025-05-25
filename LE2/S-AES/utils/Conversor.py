class Conversor:
    def texto_para_bits(self, texto: str) -> list:
        bits = []
        for caractere in texto:
            valor_binario = format(ord(caractere), "08b")
            bits.extend([int(b) for b in valor_binario])
        return bits

    def bits_para_texto(self, bits: list) -> str:
        texto = ""
        for i in range(0, len(bits), 8):
            byte = bits[i : i + 8]
            caractere = chr(int("".join(map(str, byte)), 2))
            texto += caractere
        return texto

    def bits_para_nibbles(self, bits: list) -> list:
        return [bits[i : i + 4] for i in range(0, len(bits), 4)]

    def nibbles_para_bits(self, nibbles: list) -> list:
        return [bit for nibble in nibbles for bit in nibble]
