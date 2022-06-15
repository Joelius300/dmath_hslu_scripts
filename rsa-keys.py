from dmath import generate_rsa_keys

p = int(input('p (Primzahl): '))
q = int(input('q (andere Primzahl): '))
e = int(input('e (teilerfremd zu phi(pq)={}): '.format((p - 1) * (q - 1))))

(n, e), d = generate_rsa_keys(p, q, e)

print('Public key: ({}, {})  |  Private key: {}'.format(n, e, d))
