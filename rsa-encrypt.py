import sys

if sys.platform == "nspire":
    with open("/documents/apps/dmath.py.tns", "r") as file:
        exec(file.read())
else:
    from dmath import rsa_encrypt

m = int(input('m (Klartext): '))
e = int(input('e (Teil des oeffentlichen Schluessels): '))
n = int(input('n (Teil des oeffentlichen Schluessels (n=pq): '))

c = rsa_encrypt(m, e, n)
