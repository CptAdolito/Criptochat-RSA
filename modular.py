
def es_primo(n):
    if n == 1:
        return False

    i = 2
    while i*i <= n:
        if n % i == 0:
            return False
        i += 1
    return True

def lista_primos(a, b):
    return [n for n in range(a, b) if es_primo(n)]

def factorizar(n):
    factores = {}
    for i in range(2, int(n**0.5)+1):
        while n % i == 0:
            if i in factores:
                factores[i] += 1
            else:
                factores[i] = 1
            n //= i
    if n > 1:
        factores[n] = 1
    return factores

def mcd(a, b):
    if a == 0:
        return b
    return mcd(b % a, a)


def bezout(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        d, x, y = bezout(b % a, a)
        return (d, y - (b // a) * x, x)

def mcd_n(nlist):
    if len(nlist) == 1:
        return nlist[0]
    return mcd(nlist[0], mcd_n(nlist[1:]))

def bezout_n(nlist):
    if len(nlist) == 1:
        return (nlist[0], 0, 1)
    else:
        d, x, y = bezout_n(nlist[1:])
        return (d, y - (nlist[0] // d) * x, x)
    
def coprimos(a, b):
    return mcd(a, b) == 1

def potencia_mod_p(base, exp, p):
    if exp == 0:
        return 1
    if exp % 2 == 0:
        if exp < 0:
            return inversa_mod_p(potencia_mod_p(base, -exp//2, p)**2 % p, p)
        else:
            return potencia_mod_p(base, exp//2, p)**2 % p
    else:
        if exp > 0:
            return base * potencia_mod_p(base, exp-1, p) % p
        else:
            return inversa_mod_p(base * potencia_mod_p(base, -exp-1, p) % p, p)

def inversa_mod_p(n, p):
    d, x, _ = bezout(n, p)
    if d == 1:
        return x % p
    else:
        return "NE"

def euler(n):
    return len([x for x in range(1, n+1) if coprimos(x, n)])

def legendre(n, p):
    #return potencia_mod_p(n, (p-1)//2, p)
    r = potencia_mod_p(n, (p-1)//2, p)
    return (r-p if r > 1 else r)

def resolver_sistema_congruencias(alist, blist, plist):
    m = 1
    for p in plist:
        m *= p
    alist = [inversa_mod_p(alist[i], plist[i])*blist[i]%plist[i] for i in range(len(alist))]
    sol = 0
    for i in range(len(alist)):
        sol += alist[i]*m//plist[i]*inversa_mod_p(m//plist[i], plist[i])
    return sol % m, m

def cipolla(n, p):
    if legendre(n, p) != 1:
        return "NE"
    if p == 2:
        return 0, 1
    if p % 4 == 3:
        return potencia_mod_p(n, (p+1)//4, p), potencia_mod_p(n, 3*(p+1)//4, p)
    else:
        a = 1
        while legendre(a, p) != -1:
            a += 1
        t, u = p-1, 0
        while t % 2 == 0:
            t //= 2
            u += 1
        m = potencia_mod_p(a, t, p)
        c = potencia_mod_p(a, t//2, p)
        r = potencia_mod_p(n, (t+1)//2, p)
        d = potencia_mod_p(n, t, p)
        for i in range(1, u):
            if potencia_mod_p(d, 2**(u-i-1), p) == 1:
                b = potencia_mod_p(m, 2**(u-i-2), p)
                r = r * b % p
                c = c * b**2 % p
                m = m * b**2 % p
                d = d * b**4 % p
        return r, p-r


def raiz_mod_p(n, p):
    r = list()
    n = n % p
    if (p % 4 != 3) :
        x = 2
        while x in range (2, p) and len(r) != 2:
            if ((x * x) % p == n) :
                r.append(x)
            x += 1
        return r if len(r) == 2 else r[0] if len(r) == 1 else "NE"
    x = potencia_mod_p(n, (p + 1) // 4, p)
    if ((x * x) % p == n):
        return x

    x = p - x
    if ((x * x) % p == n):
        return x
    
    return "NE"


def ecuacion_cuadratica(a, b, c, p):
    try:
        x1 = ((raiz_mod_p(potencia_mod_p(b, 2, p) - 4*a*c, p) - b) * inversa_mod_p(2*a, p)) %p
        x2 = ((-raiz_mod_p(potencia_mod_p(b, 2, p) - 4*a*c, p) - b) * inversa_mod_p(2*a, p)) %p
        return (x1, x2) if x1 != x2 else x1
    except:
        return "NE"
            