import sys

if sys.platform == "nspire":
    with open("/documents/apps/dmath.py.tns", "r") as file:
        exec(file.read())
else:
    from dmath import EEA

a = int(input('a: '))
b = int(input('b: '))

EEA(a, b)
