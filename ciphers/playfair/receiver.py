import numpy as np;
import socket;

def receiver():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
    s.bind(("localhost", 42069));
    s.listen(1);
    print("waiting...");
    c, addr = s.accept();
    msg = c.recv(1024).decode("ascii");
    print(f"Cipher={msg}");
    print("enter key:");
    k = input();
    dec = pf_d(msg, k);
    print(f"Decrypted={dec}");
    c.close();

def pf_d(txt, k):
    k = k.upper().replace("J", "I") + "ABCDEFGHIKLMNOPQRSTUVWXYZ";
    u = [];
    [u.append(x) for x in k if x not in u and x.isalpha()];
    m = np.array(u).reshape(5, 5);

    out = "";
    for i in range(0, len(txt), 2):
        a, b = txt[i], txt[i+1];
        p1 = np.where(m == a);
        r1, c1 = p1[0][0], p1[1][0];
        p2 = np.where(m == b);
        r2, c2 = p2[0][0], p2[1][0];

        if r1 == r2:
            out += m[r1, (c1-1)%5] + m[r2, (c2-1)%5];
        elif c1 == c2:
            out += m[(r1-1)%5, c1] + m[(r2-1)%5, c2];
        else:
            out += m[r1, c2] + m[r2, c1];
            
    return out;

receiver();
