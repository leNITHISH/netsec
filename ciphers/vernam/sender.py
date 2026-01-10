import socket;

def sender():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
    try:
        s.connect(("localhost", 42069));
    except ConnectionRefusedError:
        print("toodles");
        return;
    print("Enter the message you wanna send: ");
    string = input();
    print("Enter the key phrase to encrypt: ");
    key  = input();
    msg = ver_e(string, key);
    s.send(msg.encode(encoding="ascii", errors="ignore"));
    s.close();

def ver_e(string, key):
    ret = [];
    n = len(string);
    m = len(key);

    for i, c in enumerate(string):
        ret.append(chr((ord(c)^ord(key[127 & i]))%128));
    return "".join(ret);

sender();
