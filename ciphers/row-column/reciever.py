import socket
import math

def reciever():
    reci = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    reci.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    reci.bind(("localhost", 42069))
    reci.listen(1)
    print("Listening on port 42069...")
    
    conn, addr = reci.accept()

    payload = conn.recv(1024 * 1024).decode() 
    
    print(f"bro literrally said \"{payload.strip()}\"")

    try:
        k = int(input("enter the key to decrypt the message: "))
    except ValueError:
        print("Invalid key!")
        return
    
    n = len(payload) 
    cols = k
    
    rows = math.ceil(n / cols)
    
    if rows == 0:
        print("Error: Key implies 0 rows. Unable to decrypt.")
        conn.close()
        reci.close()
        return

    grid = [["" for _ in range(cols)] for _ in range(rows)]
    
    idx = 0
    try:
        for c in range(cols):
            for r in range(rows):
                if idx < n:
                    grid[r][c] = payload[idx]
                    idx += 1
    except IndexError:
        print("Grid mismatch error.")

    res = []
    for r in range(rows):
        res.append("".join(grid[r]))
        
    print(f"decrypted message: {''.join(res).strip()}")

    conn.close()
    reci.close()

reciever()
