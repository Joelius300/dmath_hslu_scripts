import sys

if sys.platform == "nspire":
    with open("/documents/apps/dmath.py.tns", "r") as file:
        exec(file.read())
else:
    from dmath import mod_square

n = int(input('n: '))
p = input('Primitive (Z*_n = ja, sonst Z_n) ([y]/n): ').upper() != 'N'

mod_square(n, p)
