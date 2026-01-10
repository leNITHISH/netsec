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
    msg = input();
    print("enter key:");
    k = input();
    enc = pf(msg, k);
    print(f"Message={msg}\tCipher={enc}");
    s.send(enc.encode(encoding="ascii", errors="ignore"));
    s.close();

def pf(txt, k):
    k = k.upper().replace("J", "I") + "ABCDEFGHIKLMNOPQRSTUVWXYZ";
    u = [];
    [u.append(x) for x in k if x not in u and x.isalpha()];
    m = np.array(u).reshape(5, 5);

    txt = txt.upper().replace("J", "I");
    t = "".join([c for c in txt if c.isalpha()]);
    d = [];
    i = 0;
    while i < len(t):
        a = t[i];
        if i + 1 >= len(t):
            d.append((a, 'X'));
            break;
        b = t[i+1];
        if a == b:
            d.append((a, 'X'));
            i += 1;
        else:
            d.append((a, b));
            i += 2;

    out = "";
    for a, b in d:
        p1 = np.where(m == a);
        r1, c1 = p1[0][0], p1[1][0];
        p2 = np.where(m == b);
        r2, c2 = p2[0][0], p2[1][0];

        if r1 == r2:
            out += m[r1, (c1+1)%5] + m[r2, (c2+1)%5];
        elif c1 == c2:
            out += m[(r1+1)%5, c1] + m[(r2+1)%5, c2];
        else:
            out += m[r1, c2] + m[r2, c1];
            
    return out;

sender();
