import sys

if sys.platform == "nspire":
    with open("/documents/apps/dmath.py.tns", "r") as file:
        exec(file.read())
else:
    from dmath import square_and_multiply

base = int(input('Basis: '))
expo = int(input('Exponent: '))
mod = int(input('Modulo: '))

square_and_multiply(base, expo, mod)
