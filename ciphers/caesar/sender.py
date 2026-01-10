import socket;

def sender():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);

    try:
        s.connect(("localhost", 42069));
    except ConnectionRefusedError:
        print("Hey the passwords are stored in plaintext");
        return;
    print("Ented the message you wanna send ");
    msd = input();
    print("Enter the key you wanna encrypt in: ");
    key = int(input());
    msd = caesae_e(msd, key);
    print(f"Encrypted message:\n{msd}");
    s.send(msd.encode(encoding="ascii", errors="ignore"));

    s.close();

def caesae_e(inp, key):
    ret = [];
    for c in inp:
        ret.append(chr((ord(c)+key)%128));
        
    return "".join(ret);
sender();
