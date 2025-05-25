class Common:
    def add_round_key(estado, chave_round):
        print(f"[DEBUG] Passando pela função add_round_key com as seguintes propriedades:\n - Estado: {estado} bits\n - Chave: {chave_round}")
        return [s ^ k for s, k in zip(estado, chave_round)]

    def sub_nibbles(estado, sbox):
        print(f'[DEBUG] Passando pela função sub_nibbles com as seguintes propriedades:\n - Estado: {estado} bits\n -S-Box: {sbox}')
        return [sbox[nibble] for nibble in estado]

    def shift_rows(estado):
        print(f'[DEBUG] Passando pela função shift_rows com as seguintes propriedades:\n - Estado: {estado}')
        return [estado[0], estado[1], estado[3], estado[2]]

    def mix_columns(estado):
        def mult(a, b):
            p = 0
            for _ in range(4):
                if b & 1:
                    p ^= a
                carry = a & 0x8
                a = (a << 1) & 0xF
                if carry:
                    a ^= 0x3  # x^4 + x + 1 irreducível: 0b0011
                b >>= 1
            return p & 0xF

        s0 = estado[0]
        s1 = estado[1]
        s2 = estado[2]
        s3 = estado[3]

        return [
            mult(1, s0) ^ mult(4, s2),
            mult(1, s1) ^ mult(4, s3),
            mult(4, s0) ^ mult(1, s2),
            mult(4, s1) ^ mult(1, s3),
        ]
