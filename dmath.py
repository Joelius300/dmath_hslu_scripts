# this code is mostly terrible. it's quick and dirty and designed for micropython 2014

# does the extended euclidian algorithm and returns the relevant results from the last line before b becomes 0.
# in addition, the last u and v values (which are returned in slot 1 and 2) are made positive and returned in slot 3 and 4.
# this lets you get the first positive multiplicative inverse of a to b and b to a as well.
def EEA(a, b):
    if a < b:
        print('a < b in EEA, may not work!')
    #     print('a < b in euklidischem Algorithmus, swapping them and proceeding')
    #     print('a = {} | b = {}'.format(a, b))
    #     a, b = b, a

    orig_a = a
    orig_b = b

    u_old, u = 1, 0
    v_old, v = 0, 1
    print('{0:>5}     - {1:>5} {2:>5}'.format(a, u_old, v_old))
    while b:
        q = a // b
        u, u_old = u_old - q * u, u
        v, v_old = v_old - q * v, v
        a, b = b, a % b
        print('{0:>5}{1:>6}{2:>6}{3:>6}'.format(a, q, u_old, v_old))

    print()
    print('{} * {} + {} * {} = 1'.format(u_old, orig_a, v_old, orig_b))

    x = None
    y = None
    if a == 1:  # a & b sind teilerfremd, höchstwahrscheinlich EEA für die modulare inverse verwendet -> positiv machen
        x = u_old
        while x < 0:
            x += orig_b
        y = v_old
        while y < 0:
            y += orig_a

        print('Falls Modulare Inv gesucht: ')
        print('   {0} * {1} === 1 mod {2}'.format(x, orig_a, orig_b))
        print('   {0} * {1} === 1 mod {2}'.format(y, orig_b, orig_a))

    return a, u_old, v_old, x, y


# returns the first positive modular inverse for z
# uses ggT which is basically EEA without printing, makes sure it's positiv, then returns so it's redundant to the last two parameters of EEA
def mod_inv(base, z):
    y = ggT(base, z)[2]
    while y < 0:
        y += base
    print('{0} * {1} === 1 mod {2}'.format(z, y, base))

    return y


# I think redundant as it does the same as EEA just without printing
def ggT(a, b):
    if a < b:
        print('a < b in ggT calc, may not work!')
        # print('a < b in ggT calc, swapping them and proceeding')
        # a, b = b, a

    if b == 0:
        return a, 1, 0
    else:
        g, u, v = ggT(b, a % b)
        q = a // b
        return g, v, u - q * v


def faktorisiere(n):
    l = list()  # Lösungsmenge
    # Auf Teilbarkeit durch 2, und alle ungeraden Zahlen von 3..n/2 testen
    for i in chain([2], range(3, n // 2 + 1, 2)):
        # Ein Teiler kann mehrfach vorkommen (z.B. 4 = 2 * 2), deswegen:
        while n % i == 0:
            l.append(i)
            n = n // i
        if i > n:  # Alle Teiler gefunden? Dann Abbruch.
            break
    return l


# itertools polyfill
def chain(*iterables):
    for it in iterables:
        for each in it:
            yield each


# non-updatable, very very very simple Counter polyfill
class Counter:
    def __init__(self, iterable):
        self._counts = dict()
        for x in iterable:
            if self._counts.get(x):
                self._counts[x] += 1
            else:
                self._counts[x] = 1

    def __iter__(self):
        # return keys of counted items, sorted by their count descending
        return (x for (x, _) in sorted(self._counts.items(), key=lambda item: item[1], reverse=True))

    def __getitem__(self, item):
        return self._counts.__getitem__(item)


def phi(n):
    faktoren = faktorisiere(n)
    r = Counter(faktoren)

    p = 1
    for i in r:
        p *= (i - 1) * i ** (r[i] - 1)
        print('({1} - 1) * {1}^{0}'.format(r[i] - 1, i), end=' ')
        if not i == faktoren[-1]:
            print('*', end=' ')

    print('= {0}'.format(p), end='')
    print()
    return p


def generate_rsa_keys(p, q, e):
    n = p * q
    phi_n = (p - 1) * (q - 1)
    t, _, _, _, d = EEA(phi_n, e)
    # t=ggt, d=inv of e to mod phi_n

    print('# unnötig: ', end='')
    if phi_n != phi(n):
        print('ERROR (p-1)*(q-1) gibt nicht phi(n) ALSO SIND P UND/ODER Q KEINE PRIMZAHLEN')
        return None

    print('ggT({0}, {1}) = {2}\n'.format(phi_n, e, t))
    if t != 1:
        print('ERROR e ({}) IST NICHT TEILERFREMD ZU PHI VON n (phi({}) = {})!!'.format(e, n, phi_n))
        return None

    print('d = {0}, da {0} * {1} = 1 mod {2}\n'.format(d, e, phi_n))

    return (n, e), d


def rsa_encrypt(m, e, n):
    print('{0} ** {1} mod {2} ='.format(m, e, n), m ** e % n)
    return m ** e % n


def rsa_decrypt(c, d, n):
    print('{0} ** {1} mod {2} ='.format(c, d, n), c ** d % n)
    return c ** d % n


# Spielt RSA einmal durch mit Schlüsselgenerierung, Ver- und Entschlüsselung
def rsa_complete(p, q, e, m):
    keys = generate_rsa_keys(p, q, e)
    n = keys[0][0]
    d = keys[1]

    print('Verschlüsselung')
    c = list()
    for i in range(len(m)):
        c.append(rsa_encrypt(m[i], e, n))

    print()
    print('Entschlüsselung')
    for i in range(len(c)):
        rsa_decrypt(c[i], d, n)


# Modulare Rechentabelle für [a]addition, [s]ubtraction, [m]ultiplication
def mod_table(n, operator):
    for i in range(-1, n):
        print('{0:>3}'.format(i), end=' ')
    print()
    for i in range(n):
        print('{0:>3}'.format(i), end=' ')
        for x in range(n):
            if operator == 'a':
                print('{0:>3}'.format((x + i) % n), end=' ')
            elif operator == 'm':
                print('{0:>3}'.format((x * i) % n), end=' ')
            elif operator == 's':
                print('{0:>3}'.format((x - i) % n), end=' ')

        print()


# Modulares Quadrieren mit quadratischen Resten und Nichtresten. Entweder für alle in Z_n oder nur in den primitiven Elementen Z*_n
def mod_square(n, primitiv):
    z = list()
    r = list()
    # x Zeile
    for i in range(1, n):
        if primitiv:
            if ggT(n, i)[0] == 1:
                z.append(i)
                print('{0:>3}'.format(i), end=' ')
        else:
            z.append(i)
            print('{0:>3}'.format(i), end=' ')

    # x *mod x Zeile
    print()
    for i in z:
        res = (i ** 2) % n
        r.append(res)
        print('{0:>3}'.format(res), end=' ')
    print()

    # Restklassen
    rest = list()
    n_rest = list()

    for i in r:
        if i in z:  # checking for how many times they appear could tell you whether n is prime or a product of two primes
            rest.append(i)
        else:
            n_rest.append(i)

    for i in z:
        if i not in r:
            n_rest.append(i)

    print()
    print('Quadratischer Rest: {0}\n'.format(set(rest)))
    print('Quadratischer nicht Rest: {0}'.format(set(n_rest)))


def square_and_multiply(basis, potenz, mod):
    binary = bin(potenz)
    print('binary: ', binary[2:])  # cut off prefix
    qm_string = ''
    result = ''
    temp_result = basis
    for s in binary[2:]:  # cut off prefix
        if s == '1':
            qm_string += 'QM'
        else:
            qm_string += 'Q'

    qm_string = qm_string[2:]  # cut off first QM (first bit is always 1)
    print('QM_String', qm_string)

    for s in qm_string:
        if s == 'Q':
            result += '{0} Q-> '.format(temp_result)
            temp_result_squared = temp_result ** 2
            temp_result = temp_result_squared % mod
            result += '{0} = '.format(temp_result_squared)
        else:
            result += '{0} M-> '.format(temp_result)
            temp_result_multiplied = temp_result * basis
            temp_result = temp_result_multiplied % mod
            result += '{0} = '.format(temp_result_multiplied)
    result += '{0}'.format(temp_result % mod)

    print(result)


def chinesischer_restsatz(r, m):
    y_all = list()
    M_all = list()
    m_all = 1
    for i in m:
        m_all *= i
        print(i, end=' ')
        if not i == m[-1]:
            print('*', end=' ')

    print('= {0} = m \n'.format(m_all))

    for i in range(len(r)):
        Mi = m_all // m[i]
        print('M_{0} = {1}/{2} = {3} \n'.format(i + 1, m_all, m[i], Mi))

        M_all.append(Mi)
        _, _, _, y, _ = EEA(Mi, m[i])
        # y = mod_inv(Mi, m[i])
        y_all.append(y)
        print()

    x = 0
    for i in range(len(M_all)):
        x += r[i] * M_all[i] * y_all[i]
        print('{0} * {1} * {2}'.format(r[i], M_all[i], y_all[i]), end=' ')
        if i < len(M_all) - 1:
            print('+', end=' ')
    print('=')
    print('{0} = {1} mod({2})'.format(x, x % m_all, m_all))

    return x


if __name__ == '__main__':
    # Erweiterter Euklidischer Algorithmus
    print("--- Erweiterter Euklidischer Algorithmus ---")
    print(EEA(199, 74))

    # Modulare Inverse
    print("--- Mod inverse ---")
    mod_inv(9, 5)

    # ggT
    print("--- ggT ---")
    print(ggT(9, 15))

    # Faktorisieren
    print("--- Faktorisieren ---")
    print(faktorisiere(120))

    # Eulersche Phi Funktion
    print("--- Phi ---")
    print(phi(491 * 223))

    # RSA Public private key generation
    # e muss teilerfremd zu phi von n=pq ist
    print("--- RSA Manuell ---")
    (n, e), d = generate_rsa_keys(5, 7, 17)
    print("n={0}, e={1}, d={2}".format(n, e, d))

    # RSA encryption
    c = rsa_encrypt(999, e, n)
    print("c=", c)

    # RSA decryption
    print(rsa_decrypt(c, d, n))

    # RSA durchgespielt
    print("--- RSA ---")
    rsa_complete(5, 7, 17, (999,))

    # Modulare Rechentabelle aufzeigen
    print("--- Mod Rechentabelle ---")
    mod_table(5, 'a')  # [a]addition, [s]ubtraction, [m]ultiplication

    # Quadrat in Zn* oder Zn
    print("--- Quadrat in Zn* oder Zn mit resten und nichtresten ---")
    mod_square(19, primitiv=True)

    # Square-and-multiply
    print("--- Square-and-multiply ---")
    square_and_multiply(89, 72, 191)

    # Chinesischer Restsatz
    print("--- Chinesischer Restsatz ---")
    chinesischer_restsatz((1, 2, 3, 4), (2, 3, 5, 11))
