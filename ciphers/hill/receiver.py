import socket
import numpy as np

def modInverse(a, m):
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def hill_d(ciphertext, key_matrix):
    n = len(key_matrix)
    
    det = int(np.round(np.linalg.det(key_matrix)))
    det_inv = modInverse(det % 26, 26)
    
    if det_inv is None:
        return "ERROR: Key matrix not invertible"

    adjugate = np.array([
        [key_matrix[1, 1], -key_matrix[0, 1]],
        [-key_matrix[1, 0], key_matrix[0, 0]]
    ])
    
    inverse_key = (det_inv * adjugate) % 26

    numbers = [ord(c.upper()) - 65 for c in ciphertext]
    plain = []
    for i in range(0, len(numbers), n):
        block = np.array(numbers[i:i+n])
        t = np.dot(inverse_key, block) % 26
        plain.extend(t)

    return "".join([chr(int(np.round(num)) + 65) for num in plain])

def receiver():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", 42069))
    server.listen(1)
    print("Waiting for sender...")
    
    conn, addr = server.accept()
    data = conn.recv(1024).decode()
    
    if data:
        key = np.array([[3, 3], [2, 5]])
        decrypted_msg = hill_d(data, key)
        print(f"Received (Cipher): {data}")
        print(f"Decrypted Message: {decrypted_msg}")
    
    conn.close()
    server.close()

if __name__ == "__main__":
    receiver()
