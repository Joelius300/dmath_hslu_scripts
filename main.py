def EEA(a, b):
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
    return a, u_old, v_old


def ggT(a, b):
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


def chain(*iterables):
    for it in iterables:
        for each in it:
            yield each


def modInverse(a, m):
    for x in range(1, m):
        if (((a % m) * (x % m)) % m == 1):
            return x
    return -1


def modInvSteps(mod, Z):
    for i in Z:
        y = ggT(mod, i)[2]
        while y < 0:
            y += mod
        print('{0} * {1} ** -1 = 1 mod {2}'.format(i, y, mod))


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


def phi_m(n):
    faktoren = faktorisiere(n)
    r = Counter(faktoren)

    phi = 1
    for i in r:
        phi *= (i - 1) * i ** (r[i] - 1)
        print('({1} - 1) * {1}^{0}'.format(r[i] - 1, i), end=' ')
        if not i == faktoren[-1]:
            print('*', end=' ')

    print('= {0}'.format(phi), end='')
    print()
    return phi


def generateKeys(p, q, e):
    n = p * q
    phi_n = (p - 1) * (q - 1)
    t, x, d = EEA(phi_n, e)

    while d < 0:
        d += n

    print('ggT({0}, {1}) = {2}\n'.format(phi_n, e, t))
    print('d = {0}, da {0} * {1} = 1 mod {2}\n'.format(d, e, phi_n))

    return (n, e), d


def encrypt(m, e, n):
    print('{0} ** {1} mod {2} ='.format(m, e, n), m ** e % n)
    return m ** e % n


def decrypt(c, d, n):
    print('{0} ** {1} mod {2} ='.format(c, d, n), c ** d % n)
    return c ** d % n


def cryptoSys(p, q, e, m):
    keys = generateKeys(p, q, e)
    n = keys[0][0]
    d = keys[1]

    print('Verschlüsselung')
    c = list()
    for i in range(len(m)):
        c.append(encrypt(m[i], e, n))

    print()
    print('Entschlüsselung')
    for i in range(len(c)):
        decrypt(c[i], d, n)


def zTable(n, operator):
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


def zSq(n, primitiv):
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
    for i in range(len(z)):
        res = (z[i] ** 2) % n
        r.append(res)
        print('{0:>3}'.format(res), end=' ')
    print()

    # Restklassen
    rest = list()
    n_rest = list()

    for i in r:
        if (i in z) and (r.count(i) == 4):
            rest.append(i)
        else:
            n_rest.append(i)

    for i in z:
        if not i in r:
            n_rest.append(i)

    print()
    print('Quadratischer Rest: {0}\n'.format(set(rest)))
    print('Quadratischer nicht Rest: {0}'.format(set(n_rest)))


def QAndM(m, e, n, o=None, x=0):
    if o == None:
        o = bin(e)[3:]
    if x == 0:
        x = m

    print(x)

    if not o:
        return x
    elif o[0] == '1':
        print(x ** 2 % n)
        return QAndM(m, e, n, o[1:], x ** 2 * m % n)
    elif o[0] == '0':
        return QAndM(m, e, n, o[1:], x ** 2 % n)


def CR(r, m):
    x_all = list()
    M_all = list()
    m_all = 1
    for i in m:
        m_all *= i
        print(i, end=' ')
        if not i == m[-1]:
            print('*', end=' ')

    print('= {0} = m \n'.format(m_all))

    for i in range(len(r)):
        M = m_all / m[i]
        print('M_{0} = {2}/{1} = {3} \n'.format(i + 1, m[i], m_all, M))

        M_all.append(M)
        t, x, y = EEA(M, m[i])
        while x < 0:
            x += m[i]
        x_all.append(x)

        print('{1} * {2} = 1 mod {0} \n'.format(m[i], M, x))

    X = 0
    for i in range(len(M_all)):
        X += r[i] * M_all[i] * x_all[i]
        print('{0} * {1} * {2}'.format(r[i], M_all[i], x_all[i]), end=' ')
        if i < len(M_all) - 1:
            print('+', end=' ')
    print()
    print('{1} = {0} mod({2})'.format(X % m_all, X, m_all))


def sqm(basis, potenz, mod):
    binary = bin(potenz)
    print('binary: ', binary[2:])
    qm_string = ''
    result = ''
    temp_result = basis
    for s in binary[2:]:
        if s == '1':
            qm_string += 'QM'
        else:
            qm_string += 'Q'

    qm_string = qm_string[2:]
    print('QM_String', qm_string)

    for s in qm_string:
        if s == 'Q':
            result += '{0} Q-> '.format(temp_result)
            temp_result_squared = temp_result ** 2
            temp_result = (temp_result_squared) % mod
            result += '{0} = '.format(temp_result_squared)
        else:
            result += '{0} M-> '.format(temp_result)
            temp_result_multiplied = temp_result * basis
            temp_result = (temp_result_multiplied) % mod
            result += '{0} = '.format(temp_result_multiplied)
    result += '{0}'.format(temp_result % mod)

    print(result)


if __name__ == '__main__':
    # Erweiterter Euklidischer Algorithmus
    print("--- Erweiterter Euklidischer Algorithmus ---")
    print(EEA(199, 74))

    # Modulare Inverse
    print("--- Mod inverse (1) ---")
    print(modInverse(5, 9))
    print("--- Mod inverse (2) ---")
    modInvSteps(9, (5,))

    # ggT
    print("--- ggT ---")
    print(ggT(9, 15))

    # Faktorisieren
    print("--- Faktorisieren ---")
    print(faktorisiere(120))

    # Eulersche Phi Funktion TODO mit Modulo? wieso das _m
    print("--- Phi ---")
    print(phi_m(20))

    # RSA Public private key generation
    # e muss teilerfremd zu phi von n=pq ist
    print("--- RSA Manuell ---")
    (n, e), d = generateKeys(5, 7, 17)
    print("n={0}, e={1}, d={2}".format(n, e, d))

    # RSA encryption
    c = encrypt(999, e, n)
    print("c=", c)

    # RSA decryption
    print(decrypt(c, d, n))

    # RSA durchgespielt
    print("--- RSA ---")
    cryptoSys(5, 7, 17, (999,))

    # Modulare Rechentabelle aufzeigen
    print("--- Mod Rechentabelle ---")
    zTable(5, 'a')  # [a]addition, [s]ubtraction, [m]ultiplication

    # Quadrat in Zn* oder Zn
    print("--- Quadrat in Zn* oder Zn ---")
    zSq(23, primitiv=True)

    # Square-and-multiply
    print("--- Square-and-multiply (1) ---")
    print(QAndM(89, 72, 191))
    print("--- Square-and-multiply (2) ---")
    sqm(89, 72, 191)

    # Chinesischer Restsatz
    print("--- Chinesischer Restsatz ---")
    CR((1, 3), (2, 4))
