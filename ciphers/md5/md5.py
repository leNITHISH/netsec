import struct
import math

T = [int(2**32 * abs(math.sin(i + 1))) & 0xFFFFFFFF for i in range(64)]

SHIFT = [
    7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
    5,  9, 14, 20, 5,  9, 14, 20, 5,  9, 14, 20, 5,  9, 14, 20,
    4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
    6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21,
]

def left_rotate(x, n):
    return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF

def pad_message(msg_bytes):
    orig_len_bits = len(msg_bytes) * 8
    msg_bytes += b'\x80'
    while len(msg_bytes) % 64 != 56:
        msg_bytes += b'\x00'
    msg_bytes += struct.pack('<Q', orig_len_bits)
    return msg_bytes

def md5(message):
    msg_bytes = message.encode('utf-8')
    print(f"Number of characters in input: {len(message)}")

    padded = pad_message(bytearray(msg_bytes))

    A0 = 0x67452301
    B0 = 0xEFCDAB89
    C0 = 0x98BADCFE
    D0 = 0x10325476

    num_blocks = len(padded) // 64

    for block_idx in range(num_blocks):
        block = padded[block_idx * 64:(block_idx + 1) * 64]
        M = list(struct.unpack('<16I', block))

        print(f"\nBlock {block_idx + 1}")
        print(f"Initial State: A={A0:08X} B={B0:08X} C={C0:08X} D={D0:08X}")

        A, B, C, D = A0, B0, C0, D0

        for round_num in range(4):
            print(f"\nRound {round_num + 1}")

            for i in range(16):
                step = round_num * 16 + i

                if round_num == 0:
                    F = (B & C) | (~B & D)
                    g = i
                elif round_num == 1:
                    F = (D & B) | (~D & C)
                    g = (5 * i + 1) % 16
                elif round_num == 2:
                    F = B ^ C ^ D
                    g = (3 * i + 5) % 16
                else:
                    F = C ^ (B | ~D)
                    g = (7 * i) % 16

                F = F & 0xFFFFFFFF
                temp = (A + F + T[step] + M[g]) & 0xFFFFFFFF
                temp = left_rotate(temp, SHIFT[step])
                temp = (temp + B) & 0xFFFFFFFF

                A, B, C, D = D, temp, B, C

                print(f"  Step {step+1:2d}: A={A:08X} B={B:08X} C={C:08X} D={D:08X}")

            print(f"End of Round {round_num + 1}: A={A:08X} B={B:08X} C={C:08X} D={D:08X}")

        A0 = (A0 + A) & 0xFFFFFFFF
        B0 = (B0 + B) & 0xFFFFFFFF
        C0 = (C0 + C) & 0xFFFFFFFF
        D0 = (D0 + D) & 0xFFFFFFFF

        print(f"After Block {block_idx + 1}: A={A0:08X} B={B0:08X} C={C0:08X} D={D0:08X}")

    digest = struct.pack('<4I', A0, B0, C0, D0)
    hash_hex = digest.hex()

    print(f"\nFinal Hash Value: {hash_hex}")
    return hash_hex

message = input("Enter message: ")
print(f"Input: \"{message}\"")
md5(message)
