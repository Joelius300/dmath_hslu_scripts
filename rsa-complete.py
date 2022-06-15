import sys

if sys.platform == "nspire":
    with open("/documents/apps/dmath.py.tns", "r") as file:
        exec(file.read())
else:
    from dmath import rsa_complete

p = int(input('p (Primzahl): '))
q = int(input('q (andere Primzahl): '))
e = int(input('e (teilerfremd zu phi(pq)={}): '.format((p - 1) * (q - 1))))
m = [int(mi) for mi in input("m's (Geheimtexte, Kommagetrennt): ").split(',')]

rsa_complete(p, q, e, m)
