import sys

if sys.platform == "nspire":
    with open("/documents/apps/dmath.py.tns", "r") as file:
        exec(file.read())
else:
    from dmath import mod_table

n = int(input('n: '))
o = input('Operator (+, -, *): ')

mod_table(n, o)
