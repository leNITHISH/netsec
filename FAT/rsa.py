import random
import math


def isPrime(n):
    if n<2: return False
    for i in range(2, int(n**0.5)+1):
        if n%i==0: return False
    return True

def generate_primes():
    r = random.randint(100, 500)
    p=0
    q=0
    for i in reversed(range(2, r)):
        if isPrime(i):
            if p==0:
                p=i
            else:
                q=i
                break
    return p, q
def generate_keys(p, q):
    n = p*q # ignore fo now ig 
    phi = (p-1)*(q-1)
    e=0
    while e==0:
        r = random.randint(2, phi-1)
        if math.gcd(r, phi)==r:
            e=r;
            break;

    d = pow(e, -1, phi)

    return e, d

def encrypt(M, e, n):
    C = pow(M, e, n);
    return C;
def decrypt(C, d, n):
    M = pow(C, d, n);
    return M;
def some_hash(m):
    return sum(map(ord, m));
def sign(M, d, n):
    H = some_hash(M)
    S = pow(H, d, n)
    return S;
def verify(M, S, e, n):
    H_prm = some_hash(M);
    H = pow(S, e, n);
    return H_prm == H;

            
