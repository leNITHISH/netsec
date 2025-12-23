import numpy as np;
import socket;

def sender():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
    try:
        s.connect(("localhost", 42069));
    except ConnectionRefusedError:
        print("toodles");
        return;
    print("enter message:");
    string = input();
    key = np.array([[3, 3], [2, 5]]);
    msg = hill_e(string, key);
    print(f"Message={string}\tCipher={msg}");
    s.send(msg.encode(encoding="ascii", errors="ignore"));
    s.close();

def hill_e(string, key_matrix):
    n = len(key_matrix);
    while len(string)%n !=0:
        string+= 'x';

    numbers = [ord(c.upper())-65 for c in string if c.isalpha()];
    cipher = [];

    for i in range(0, len(numbers), n):
        block = np.array(numbers[i:i+n]);
        t = np.dot(key_matrix, block)%26;
        cipher.extend(t);

    return "".join([chr(int(num)+65) for num in cipher]);
    
sender();
