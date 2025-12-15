import socket

def reciever():
    reci = socket.socket(socket.AF_INET, socket.SOCK_STREAM);

    reci.bind(("localhost", 42069));
    reci.listen(1);
    print("lmao ded this thing actually listening");
    conn, addr = reci.accept();
    print(f"Look who's connected {addr}");

    payload = conn.recv(1024).decode();
    print(f"bro literrally said \"{payload}\"");

    conn.close();
    reci.close();
reciever();
