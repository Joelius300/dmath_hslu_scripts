import sys

if sys.platform == "nspire":
    with open("/documents/apps/dmath.py.tns", "r") as file:
        exec(file.read())
else:
    from dmath import rsa_decrypt

c = int(input('c (Geheimtext): '))
d = int(input('d (Privater Schluessel): '))
n = int(input('n (Teil des oeffentlichen Schluessels (n=pq): '))

m = rsa_decrypt(c, d, n)
