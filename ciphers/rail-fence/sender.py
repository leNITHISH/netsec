import socket;

def sender():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);

    s.connect(("localhost", 42069));
    msd = letsencrypt();
    s.send(msd.encode());
    print(f"encrypted text: \"{msd}\"");

    s.close();


def letsencrypt():
    s = input("enter the message you wanna send: ");
    k = int(input("enter the key you wanna encrypt the message in: "));
    
    rails = [""]*k;
    
    row = 0;
    sig = 1;
    
    def inc_row():
        nonlocal row, sig;
        if row==0:
            sig=1;
        elif row==k-1:
            sig=-1;
        row+=sig;

    for c in s:
        rails[row]+=c;
        inc_row();


    return "".join(rails);

sender();
