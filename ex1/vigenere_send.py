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
    msg = vig_e(string, key);
#   print(msg);
    s.send(msg.encode(encoding="ascii", errors="ignore"));
    s.close();

def vig_e(string, key):
    ret = [];
    n = len(string);
    m = len(key);

    for i in range(n):
        ret.append(chr((ord(string[i])+ord(key[i%m]))%128));
    return "".join(ret);

sender();
