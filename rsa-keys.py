import sys

if sys.platform == "nspire":
    with open("/documents/apps/dmath.py.tns", "r") as file:
        exec(file.read())
else:
    from dmath import generate_rsa_keys

p = int(input('p (Primzahl): '))
q = int(input('q (andere Primzahl): '))
e = int(input('e (teilerfremd zu phi(pq)={}): '.format((p - 1) * (q - 1))))

(n, e), d = generate_rsa_keys(p, q, e)

print('Public key: (n={}, e={})  |  Private key: d={}'.format(n, e, d))
