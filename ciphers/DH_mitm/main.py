
import random

BLUE = "\033[94m"
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

def modexp(base, exp, mod):
    return pow(base, exp, mod)

p = int(input("Enter prime number (p): "))
g = int(input("Enter primitive root (g): "))

print(BLUE + "\n--- Alice ---")
Xa = random.randint(2, p-2)
Ya = modexp(g, Xa, p)
print("Alice private key:", Xa)
print("Alice public key:", Ya, RESET)

print(GREEN + "\n--- Bob ---")
Xb = random.randint(2, p-2)
Yb = modexp(g, Xb, p)
print("Bob private key:", Xb)
print("Bob public key:", Yb, RESET)

print(RED + "\n--- Attacker (Darth) ---")
Xd1 = random.randint(2, p-2)
Xd2 = random.randint(2, p-2)
Yd1 = modexp(g, Xd1, p)
Yd2 = modexp(g, Xd2, p)

print("Attacker private keys:", Xd1, Xd2)
print("Attacker public keys:", Yd1, Yd2, RESET)

Ka = modexp(Yd1, Xa, p)
Kb = modexp(Yd2, Xb, p)

Kd_a = modexp(Ya, Xd1, p)
Kd_b = modexp(Yb, Xd2, p)

print(BLUE + "\nAlice computes key with Darth: " + str(Ka) + RESET)
print(GREEN + "Bob computes key with Darth: " + str(Kb) + RESET)

print(RED + "\nDarth computes key with Alice: " + str(Kd_a) + RESET)
print(RED + "\nDarth computes key with Bob: " + str(Kd_b) + RESET)
