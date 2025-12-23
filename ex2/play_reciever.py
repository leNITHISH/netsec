import socket

def reciever():
    reci = socket.socket(socket.AF_INET, socket.SOCK_STREAM);

    reci.bind(("localhost", 42069));
    reci.listen(1);
    print("Listenin'...");
    conn, addr = reci.accept();
    print("Connected!");

    payload = conn.recv(1024).decode("ascii");
    print(f"encrypted message: \"{payload}\"\n\nenter key to decrypt:");
    key = int(input());
    msd = caesar_d(payload, key);
    print(f"recieved message: \"{msd}\"");

    conn.close();
    reci.close();

def caesar_d(string, key):
    ret = [];
    for c in string:
        ret.append(chr((ord(c)-key)%128));

    return "".join(ret);
reciever();
