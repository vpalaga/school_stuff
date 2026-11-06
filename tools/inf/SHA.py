import random, math

p, q = 101, 107

n = p*q

phi = (p-1) * (q-1)

e = p
while math.gcd(e, n) != 1:
    e = random.randint(1, phi-1)
e = 669

d = pow(e, -1, phi)

print(f"{n=}, {phi=}, {e=}, {d=}")

def encrypt(m, e_pub, n_pub):
    c = pow(m, e_pub, n_pub)
    print(f"{c=}, {e_pub=}, {n_pub=}")

def decrypt(c):
    return pow(c, d, n)

encrypt(17, 5, 3*59)
print(decrypt(9357))