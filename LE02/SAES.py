import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
import time

class SAES:
    def __init__(self, chave):
        self.s_box = {
            0x0: 0x9, 0x1: 0x4, 0x2: 0xA, 0x3: 0xB,
            0x4: 0xD, 0x5: 0x1, 0x6: 0x8, 0x7: 0x5,
            0x8: 0x6, 0x9: 0x2, 0xA: 0x0, 0xB: 0x3,
            0xC: 0xC, 0xD: 0xE, 0xE: 0xF, 0xF: 0x7
        }
        self.inv_s_box = {v: k for k, v in self.s_box.items()}
        self.mix_columns_matrix = [[1, 4], [4, 1]]
        self.chave = chave
        self.round_keys = self.key_expansion(chave)

    def add_round_key(self, bloco, chave):
        return [b ^ k for b, k in zip(bloco, chave)]

    def sub_nibbles(self, bloco):
        return [self.s_box[n] for n in bloco]

    def shift_rows(self, bloco):
        return [bloco[0], bloco[1], bloco[3], bloco[2]]

    def mix_columns(self, bloco):
        def mult(a, b):
            p = 0
            for _ in range(4):
                if b & 1: p ^= a
                hi_bit = a & 0x8
                a = (a << 1) & 0xF
                if hi_bit: a ^= 0x3
                b >>= 1
            return p

        return [
            mult(self.mix_columns_matrix[0][0], bloco[0]) ^ mult(self.mix_columns_matrix[0][1], bloco[2]),
            mult(self.mix_columns_matrix[0][0], bloco[1]) ^ mult(self.mix_columns_matrix[0][1], bloco[3]),
            mult(self.mix_columns_matrix[1][0], bloco[0]) ^ mult(self.mix_columns_matrix[1][1], bloco[2]),
            mult(self.mix_columns_matrix[1][0], bloco[1]) ^ mult(self.mix_columns_matrix[1][1], bloco[3]),
        ]

    def key_expansion(self, chave):
        return [chave[:4], chave[4:]] 

    def encrypt_block(self, bloco):
        print("\nBloco original:", bloco)
        bloco = self.add_round_key(bloco, self.round_keys[0])
        print("AddRoundKey 1:", bloco)
        bloco = self.sub_nibbles(bloco)
        print("SubNibbles:", bloco)
        bloco = self.shift_rows(bloco)
        print("ShiftRows:", bloco)
        bloco = self.mix_columns(bloco)
        print("MixColumns:", bloco)
        bloco = self.add_round_key(bloco, self.round_keys[1])
        print("AddRoundKey 2:", bloco)
        bloco = self.sub_nibbles(bloco)
        bloco = self.shift_rows(bloco)
        bloco = self.add_round_key(bloco, self.round_keys[0]) 
        print("Bloco cifrado:", bloco)
        return bloco

    def texto_para_nibbles(self, texto):
        bits = ''.join(f'{ord(c):08b}' for c in texto)
        return [int(bits[i:i+4], 2) for i in range(0, len(bits), 4)]

    def nibbles_para_base64(self, nibbles):
        bits = ''.join(f'{n:04b}' for n in nibbles)
        byte_array = int(bits, 2).to_bytes((len(bits) + 7) // 8, byteorder='big')
        return base64.b64encode(byte_array).decode()

def encrypt_saes_ecb(texto, chave):
    saes = SAES(chave)
    nibbles = saes.texto_para_nibbles(texto)
    blocos = [nibbles[i:i+4] for i in range(0, len(nibbles), 4)]
    resultado = []
    for bloco in blocos:
        if len(bloco) < 4:
            bloco += [0] * (4 - len(bloco))
        resultado += saes.encrypt_block(bloco)
    return saes.nibbles_para_base64(resultado)

def aes_encrypt_real(mensagem, modo):
    chave = get_random_bytes(16)
    iv = get_random_bytes(16)
    mensagem_bytes = pad(mensagem.encode(), 16)
    modos = {
        'ECB': AES.MODE_ECB,
        'CBC': AES.MODE_CBC,
        'CFB': AES.MODE_CFB,
        'OFB': AES.MODE_OFB,
        'CTR': AES.MODE_CTR
    }
    modo_aes = modos[modo]
    if modo == 'ECB':
        cipher = AES.new(chave, modo_aes)
    elif modo == 'CTR':
        cipher = AES.new(chave, modo_aes)
    else:
        cipher = AES.new(chave, modo_aes, iv=iv)
    inicio = time.time()
    cifrado = cipher.encrypt(mensagem_bytes)
    fim = time.time()
    tempo = fim - inicio
    print(f"Modo: {modo} | Tempo: {tempo:.6f}s")
    print("Base64:", base64.b64encode(cifrado).decode())
    return cifrado

if __name__ == '__main__':
    texto = input("Entre com a mensagem a ser criptografada: \n> ")
    print("=== PARTE 1 ===")
    chave_simples = [0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8] 
    print("=== PARTE 2 ===\nTexto base64 (ECB S-AES):", encrypt_saes_ecb(texto, chave_simples))

    print("\n=== PARTE 3 ===")
    for modo in ['ECB', 'CBC', 'CFB', 'OFB', 'CTR']:
        aes_encrypt_real("Mensagem secreta AES", modo)
