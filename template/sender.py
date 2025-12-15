import socket;

def sender():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);

    try:
        s.connect(("localhost", 42069));
        print("checkout mah website, localhost:3000");
    except ConnectionRefusedError:
        print("Hey the passwords are stored in plaintext");
        return;

    msd = "'sup 'lil bro";
    s.send(msd.encode());
    print(f"Let me tell you something: \"{msd}\"");

    s.close();

sender();
