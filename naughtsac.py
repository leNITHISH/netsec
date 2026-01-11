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

    recv_cmd = (
        f'freeze --execute '
        f'"bash -c \'printf \\"{key}\\n\\" | python {receiver} | sed -r \\"s/[\\x00-\\x1F\\x7F]//g\\"\'' 
        f'" -o {outdir}/recv.png'
    )

    send_cmd = (
        f'freeze --execute '
        f'"bash -c \'printf \\"{plaintext}\\n{key}\\n\\" | python {sender} | sed -r \\"s/[\\x00-\\x1F\\x7F]//g\\"\'' 
        f'" -o {outdir}/send.png'
    )

    subprocess.Popen(recv_cmd, shell=True)
    time.sleep(1)
    subprocess.run(send_cmd, shell=True)


def run_cipher_cinematic(cipher, key, plaintext):
    base = os.path.abspath(f"ciphers/{cipher}")
    outdir = f"output/{cipher}"
    os.makedirs(outdir, exist_ok=True)

    # switch to workspace 10
    subprocess.run("xdotool key Super_L+0", shell=True)
    time.sleep(0.5)

    # open first terminal
    subprocess.run("i3-msg exec alacritty", shell=True)
    time.sleep(0.5)

    # type receiver
    subprocess.run(f'xdotool type "cd {base} && python receiver.py"', shell=True)
    subprocess.run("xdotool key Return", shell=True)

    time.sleep(1)

    # split + new terminal
    subprocess.run("i3-msg split v", shell=True)
    subprocess.run("i3-msg exec alacritty", shell=True)
    time.sleep(0.5)

    # type sender
    subprocess.run(f'xdotool type "cd {base} && python sender.py"', shell=True)
    subprocess.run("xdotool key Return", shell=True)
    time.sleep(0.5)

    # type plaintext
    subprocess.run(f'xdotool type "{plaintext}"', shell=True)
    subprocess.run("xdotool key Return", shell=True)
    time.sleep(0.2)

    # type key
    subprocess.run(f'xdotool type "{key}"', shell=True)
    subprocess.run("xdotool key Return", shell=True)

    time.sleep(1)

    # screenshot sender
    subprocess.run(f'freeze --execute "sleep 0.1" -o {outdir}/send.png', shell=True)

    time.sleep(0.5)

    # focus receiver pane
    subprocess.run("i3-msg focus left", shell=True)
    time.sleep(0.5)

    subprocess.run(f'freeze --execute "sleep 0.1" -o {outdir}/recv.png', shell=True)

    # leave workspace
    subprocess.run("xdotool key Super_L+Left", shell=True)

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
