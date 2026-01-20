import socket
import math

def letsencrypt():
    s = input("enter the message you wanna send: ")
    
    while True:
        try:
            k = int(input("enter the key (width) you wanna encrypt the message in: "))
            if k == 0:
                print("Key cannot be 0. Try again.")
                continue
            break
        except ValueError:
            print("Key must be an integer.")

    n = len(s)
    cols = k
    rows = math.ceil(n / cols)
    
    padded_s = s.ljust(rows * cols, ' ')
    
    grid = []
    for i in range(0, len(padded_s), cols):
        grid.append(padded_s[i:i+cols])
        
    rails = []
    for c in range(cols):
        column_str = ""
        for r in range(rows):
            column_str += grid[r][c]
        rails.append(column_str)
        
    return "".join(rails)

def sender():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.connect(("localhost", 42069))
    except ConnectionRefusedError:
        print("Connection failed. Is the receiver running?")
        return
        
    msd = letsencrypt()
    
    s.send(msd.encode())
    print(f"encrypted text sent: \"{msd}\"")

    s.close()

if __name__ == "__main__":
    sender()
