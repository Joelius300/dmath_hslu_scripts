import sys

if sys.platform == "nspire":
    with open("/documents/apps/dmath.py.tns", "r") as file:
        exec(file.read())
else:
    from dmath import chinesischer_restsatz

print('Formel der Form: x === r mod m')
r = [int(ri) for ri in input("r's (Reste, Kommagetrennt): ").split(',')]
m = [int(mi) for mi in input("m's (Modulobasen, Kommagetrennt): ").split(',')]

chinesischer_restsatz(r, m, prompt_steps=True)
