from utils.Conversor import Conversor
from utils.Common import Common
class SAES(object):
    def __init__(self):
        self.sbox = [0x9,0x4,0xA,0xB,
                    0xD,0x1,0x8,0x5,
                    0x6,0x2,0x0,0x3,
                    0xC,0xE,0xF,0x7]
        self.conversor = Conversor()
        self.commons = Common()
        self._mensagem = ""

    def apresentation(self) -> str:
        return "\t\t\tS-AES\nSimplified - Advanced Encryption Standard\n"

    def mensagem_valida(self, texto: str) -> str:
        print("[DEBUG] Verificando se o tamanho da mensagem é válido...")
        if len(texto) % 2 != 0:
            print("[DEBUG] Tamanho válido ->", False, "\nAcrescentando '\x00' ao plaintext...")
            print("[DEBUG] Tamanho menor que 16 bits, acrescentando '\x00' ao plaintext...")
            texto += "\x00"
        print("[DEBUG] Tamanho válido ->", True)
        print("[DEBUG] Tamanho da mensagem:", len(texto), "bits")
        return texto

    def _get_mensagem(self) -> str:
        return self._mensagem

    def _get_key(self) -> str:
        return self._key

    def set_mensagem(self, nova_mensagem: str):
        self._mensagem = self.mensagem_valida(nova_mensagem)


if __name__ == "__main__":
    saes = SAES()
    print(saes.apresentation())
    texto_claro = input("Digite a mensagem:\n> ")
    saes.set_mensagem(texto_claro)
    bits = saes.conversor.texto_para_bits(saes._get_mensagem())
    nibbles = saes.conversor.bits_para_nibbles(bits)
    estado = saes.commons.add_round_key(nibbles)
