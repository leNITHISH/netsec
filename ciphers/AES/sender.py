import socket

SBOX = [
    99, 124, 119, 123, 242, 107, 111, 197, 48, 1, 103, 43, 254, 215, 171, 118,
    202, 130, 201, 125, 250, 89, 71, 240, 173, 212, 162, 175, 156, 164, 114, 192,
    183, 253, 147, 38, 54, 63, 247, 204, 52, 165, 229, 241, 113, 216, 49, 21,
    4, 199, 35, 195, 24, 150, 5, 154, 7, 18, 128, 226, 235, 39, 178, 117,
    9, 131, 44, 26, 27, 110, 90, 160, 82, 59, 214, 179, 41, 227, 47, 132,
    83, 209, 0, 237, 32, 252, 177, 91, 106, 203, 190, 57, 74, 76, 88, 207,
    208, 239, 170, 251, 67, 77, 51, 133, 69, 249, 2, 127, 80, 60, 159, 168,
    81, 163, 64, 143, 146, 157, 56, 245, 188, 182, 218, 33, 16, 255, 243, 210,
    205, 12, 19, 236, 95, 151, 68, 23, 196, 167, 126, 61, 100, 93, 25, 115,
    96, 129, 79, 220, 34, 42, 144, 136, 70, 238, 184, 20, 222, 94, 11, 219,
    224, 50, 58, 10, 73, 6, 36, 92, 194, 211, 172, 98, 145, 149, 228, 121,
    231, 200, 55, 109, 141, 213, 78, 169, 108, 86, 244, 234, 101, 122, 174, 8,
    186, 120, 37, 46, 28, 166, 180, 198, 232, 221, 116, 31, 75, 189, 139, 138,
    112, 62, 181, 102, 72, 3, 246, 14, 97, 53, 87, 185, 134, 193, 29, 158,
    225, 248, 152, 17, 105, 217, 142, 148, 155, 30, 135, 233, 206, 85, 40, 223,
    140, 161, 137, 13, 191, 230, 66, 104, 65, 153, 45, 15, 176, 84, 187, 22
]

RCON = [1, 2, 4, 8, 16, 32, 64, 128, 27, 54]

def xtime(a):
    return ((a << 1) ^ 27) & 255 if a & 128 else (a << 1)

def print_state(label, s):
    print(f"{label}: {''.join(f'{x:02X}' for x in s)}")

def mixcol(c):
    u0, u1, u2, u3 = c[0], c[1], c[2], c[3]
    c[0] = xtime(u0) ^ (xtime(u1) ^ u1) ^ u2 ^ u3
    c[1] = u0 ^ xtime(u1) ^ (xtime(u2) ^ u2) ^ u3
    c[2] = u0 ^ u1 ^ xtime(u2) ^ (xtime(u3) ^ u3)
    c[3] = (xtime(u0) ^ u0) ^ u1 ^ u2 ^ xtime(u3)

def keyexp(k):
    w = [k[i:i+4] for i in range(0, 16, 4)]
    for i in range(4, 44):
        t = w[i-1][:]
        if i % 4 == 0:
            t = t[1:] + t[:1]
            t = [SBOX[x] for x in t]
            t[0] ^= RCON[i // 4 - 1]
        w.append([w[i-4][j] ^ t[j] for j in range(4)])
    return w

def addround(s, k):
    for i in range(16): s[i] ^= k[i]

def subbytes(s):
    for i in range(16): s[i] = SBOX[s[i]]

def shiftrows(s):
    s[1], s[5], s[9], s[13] = s[5], s[9], s[13], s[1]
    s[2], s[6], s[10], s[14] = s[10], s[14], s[2], s[6]
    s[3], s[7], s[11], s[15] = s[15], s[3], s[7], s[11]

def mixcols(s):
    for i in range(0, 16, 4):
        col = s[i:i+4]
        mixcol(col)
        s[i:i+4] = col

def encrypt(block, key):
    s = block[:]
    w = keyexp(key)
    print_state("IP", s)
    addround(s, sum(w[:4], []))
    for r in range(1, 10):
        subbytes(s)
        shiftrows(s)
        mixcols(s)
        addround(s, sum(w[r*4:(r+1)*4], []))
        print_state(f"Round {r}", s)
    subbytes(s)
    shiftrows(s)
    addround(s, sum(w[40:], []))
    print_state("Round 10", s)
    return s

msg = input("Message: ").ljust(16)[:16]
key = input("Key: ").ljust(16)[:16]
ct = encrypt([ord(x) for x in msg], [ord(x) for x in key])
cipher_hex = ''.join(f"{x:02X}" for x in ct)
print("Cipher Text:", cipher_hex)

s = socket.socket()
s.connect(("localhost", 42069))
s.send(cipher_hex.encode())
s.close()
