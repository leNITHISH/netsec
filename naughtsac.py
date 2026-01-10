import time
import os, sys

TEMPLATE_SENDER = """import socket

def encrypt(msg, key):
    # TODO: implement
    return msg

msg = input("Enter plaintext: ")
key = input("Enter key: ")

enc = encrypt(msg, key)
print("Encrypted message:", enc)

s = socket.socket()
s.connect(("localhost",42069))
s.send(enc.encode("ascii", errors="ignore"))
s.close()
"""

TEMPLATE_RECEIVER = """import socket

def decrypt(msg, key):
    # TODO: implement
    return msg

r = socket.socket()
r.bind(("localhost",42069))
r.listen(1)
c,_ = r.accept()

cipher = c.recv(1024).decode("ascii")
print("Encrypted message:", cipher)

key = input("Enter key: ")
print("Decrypted message:", decrypt(cipher, key))
"""

def new_cipher(name):
    path = f"ciphers/{name}"
    os.makedirs(path, exist_ok=True)

    with open(f"{path}/sender.py","w") as f:
        f.write(TEMPLATE_SENDER)

    with open(f"{path}/receiver.py","w") as f:
        f.write(TEMPLATE_RECEIVER)

    print(f"Created cipher '{name}' in {path}")


import subprocess, yaml

def run_cipher(cipher, key, plaintext):
    outdir = f"output/{cipher}"
    os.makedirs(outdir, exist_ok=True)

    sender = f"ciphers/{cipher}/sender.py"
    receiver = f"ciphers/{cipher}/receiver.py"

    send_cmd = f'printf "{plaintext}\\n{key}\\n" | freeze --wait --command "python {sender}" --output {outdir}/send.png'
    recv_cmd = f'printf "{key}\\n" | freeze --wait --command "python {receiver}" --output {outdir}/recv.png'

    subprocess.Popen(recv_cmd, shell=True)
    time.sleep(1)
    subprocess.run(send_cmd, shell=True)

def build(exid):
    cfg = yaml.safe_load(open("experiments.yaml"))
    exp = cfg["experiments"][exid]

    md = []
    s = cfg["student"]

    md.append(f"# {s['course']}")
    md.append(f"**Name:** {s['name']}  ")
    md.append(f"**Reg No:** {s['regno']}  ")
    md.append(f"**Course Code:** {s['course_code']}  ")
    md.append(f"**Faculty:** {s['faculty']}\n")

    md.append(f"# {exid}\n")

    for cipher, data in exp.items():
        key = data["key"]
        plaintext = cfg["defaults"]["plaintext"]

        run_cipher(cipher, key, plaintext)

        md.append(f"## {cipher.capitalize()} Cipher\n")

        md.append("### Sender")
        md.append("```python")
        md.append(open(f"ciphers/{cipher}/sender.py").read())
        md.append("```")

        md.append("### Receiver")
        md.append("```python")
        md.append(open(f"ciphers/{cipher}/receiver.py").read())
        md.append("```")

        md.append("### Output")
        md.append(f"![send]( {cipher}/send.png )")
        md.append(f"![recv]( {cipher}/recv.png )\n")

    open(f"output/{exid}.md","w").write("\n".join(md))
    print(f"📄 Generated output/{exid}.md")

if __name__ == "__main__":
    if sys.argv[1] == "new":
        new_cipher(sys.argv[2])
    else:
        build(sys.argv[1])
