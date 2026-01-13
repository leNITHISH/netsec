import socket

P10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
P8  = [6, 3, 7, 4, 8, 5, 10, 9]
IP  = [2, 6, 3, 1, 4, 8, 5, 7]
EP  = [4, 1, 2, 3, 2, 3, 4, 1]
P4  = [2, 4, 3, 1]
IP_INV = [4, 1, 3, 5, 7, 2, 8, 6]

S0 = [[1, 0, 3, 2], [3, 2, 1, 0], [0, 2, 1, 3], [3, 1, 3, 2]]
S1 = [[0, 1, 2, 3], [2, 0, 1, 3], [3, 0, 1, 0], [2, 1, 0, 3]]

def h2b(hex_str, n_bits):
    return list(bin(int(hex_str, 16))[2:].zfill(n_bits))

def b2h(bits):
    return hex(int("".join(bits), 2))[2:].upper()

def permutate(bits, table):
    return [bits[i-1] for i in table]

def shift(bits, n):
    return bits[n:] + bits[:n]

def xor(a, b):
    return [str(int(x) ^ int(y)) for x, y in zip(a, b)]

def b2d(b):
    return int("".join(b), 2)

def d2b(d, size):
    return list(bin(d)[2:].zfill(size))

def generate_keys(key_bits):
    key = list(key_bits)
    p10 = permutate(key, P10)
    l, r = p10[:5], p10[5:]
    
    l, r = shift(l, 1), shift(r, 1)
    k1 = permutate(l + r, P8)
    
    l, r = shift(l, 2), shift(r, 2)
    k2 = permutate(l + r, P8)
    
    return k1, k2

def s_box_search(bits, sbox):
    row = b2d([bits[0], bits[3]])
    col = b2d([bits[1], bits[2]])
    return d2b(sbox[row][col], 2)

def fk(bits, subkey):
    l, r = bits[:4], bits[4:]
    ep = permutate(r, EP)
    xor_res = xor(ep, subkey)
    
    l_xor, r_xor = xor_res[:4], xor_res[4:]
    s0_out = s_box_search(l_xor, S0)
    s1_out = s_box_search(r_xor, S1)
    
    p4 = permutate(s0_out + s1_out, P4)
    return xor(l, p4) + r 

def sender():
    msg_hex = input("enter message(8 bit hex): ")
    key_hex = input("enter key(10 bit hex): ")

    bits = h2b(msg_hex, 8)
    key_bits = h2b(key_hex, 10)

    k1, k2 = generate_keys(key_bits)
    print(f"Subkey 1: {b2h(k1)}")
    print(f"Subkey 2: {b2h(k2)}")

    ip_res = permutate(bits, IP)
    print(f"IP Result: {b2h(ip_res)}")

    fk1 = fk(ip_res, k1)
    
    switched = fk1[4:] + fk1[:4]
    print(f"Round 1 (after switch): {b2h(switched)}")

    fk2 = fk(switched, k2)
    print(f"Round 2 (pre-IP inverse): {b2h(fk2)}")

    ciphertext_bits = permutate(fk2, IP_INV)
    final_cipher_hex = b2h(ciphertext_bits)
    
    print(f"encrypted text: \"{final_cipher_hex}\"")

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect(("localhost", 42069))
        s.send(final_cipher_hex.encode())
        print("Message sent to receiver.")
    except ConnectionRefusedError:
        print("Error: Could not connect to receiver.")
    finally:
        s.close()

if __name__ == "__main__":
    sender()
