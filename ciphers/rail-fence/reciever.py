import socket

def reciever():
    reci = socket.socket(socket.AF_INET, socket.SOCK_STREAM);

    reci.bind(("localhost", 42069));
    reci.listen(1);
    conn, addr = reci.accept();

    payload = conn.recv(1024).decode();
    print(f"\"{payload}\"");

    k = int(input("enter the key to decrypt the message: "));
    
    if k == 1:
        print(f"decrypted message: {payload}");
    else:
        n = len(payload);
        rail_counts = [0] * k;
        row = 0;
        sig = 1;
        
        for _ in range(n):
            rail_counts[row] += 1;
            if row == 0: sig = 1;
            elif row == k - 1: sig = -1;
            row += sig;

        rails = [];
        idx = 0;
        for count in rail_counts:
            rails.append(list(payload[idx:idx + count]));
            idx += count;

        result = [];
        row = 0;
        sig = 1;
        for _ in range(n):
            result.append(rails[row].pop(0));
            if row == 0: sig = 1;
            elif row == k - 1: sig = -1;
            row += sig;
            
        print(f"decrypted message: {''.join(result)}");

    conn.close();
    reci.close();

reciever();
