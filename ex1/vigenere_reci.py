import socket

def reciever(): #{
    r = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
    r.bind(("localhost", 42069));
    r.listen(1);
    print("Listenin'...");
    conn, addr = r.accept();
    print("Connected!");

    pl = conn.recv(1024).decode("ascii");
    print(f"Encrypted message: \"{pl}\"\nenter key to decrypt:");
    key = input();
    msg = ver_d(pl, key);
    print(f"decrypted message: \"{msg}\"");
    conn.close();
    r.close();
#}
def ver_d(inp, key): #{
    ret = [];
    n = len(inp);
    m = len(key);

    for i, c in enumerate(inp): 
        ret.append(chr((ord(c)-ord(key[i%m]))%128));

    return "".join(ret);
#}
reciever();
