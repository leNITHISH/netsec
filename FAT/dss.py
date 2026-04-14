import random

def isPrime(n):
    if n<2: return False;
    for i in range(2, int(n**0.5)+1): 
        if n%i==0: return False;
    return True;

def generate_primes():
	primes = [];
	for i in reversed(range(500, 1000)):
		if len(primes)==20:
			break;
		if(isPrime(i)):
			primes.append(i);
	p = random.choice(primes);
	factors = [];
	for i in range(1, p-1):
		if isPrime(i) and (p-1)%i==0:
			factors.append(i);
	q = max(factors);
	g=0;
	for h in reversed(range(2, p-2)):
		g = pow(h, (p-1)//q, p);
		if g>1:
			break;
	return p, q, g;

def generate_private_key(q):
	return random.choice(range(2, q-1));

def generate_public_key(g, x, p):
	return pow(g, x, p);

def hash_as(msg):
	return sum(map(ord, msg));

def generate_sign(h, k, x, p, q, g):
	r = pow(pow(g, k, p), 1, q);
	kinv = pow(k, -1, q);
	s = pow((kinv*(h+x*r)), 1, q);
	return s, r;
def verify_sign(s, r, msg, p, q, g, y):
    w = pow(s, -1, q)
    u1 = (hash_as(msg) * w) % q
    u2 = (w * r) % q
    v = ((pow(g, u1, p) * pow(y, u2, p)) % p) % q
    return r == v


