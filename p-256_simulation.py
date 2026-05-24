# Simulation of scalar multiplication on the NIST P-256 curve
# This example is for educational purposes.

# P-256 domain parameters
p = int("FFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFF", 16)

a = int("FFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFC", 16)

b = int("5AC635D8AA3A93E7B3EBBD55769886BC651D06B0CC53B0F63BCE3C3E27D2604B", 16)

Gx = int("6B17D1F2E12C4247F8BCE6E563A440F277037D812DEB33A0F4A13945D898C296", 16)
Gy = int("4FE342E2FE1A7F9B8EE7EB4A7C0F9E162BCE33576B315ECECBB6406837BF51F5", 16)

n = int("FFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551", 16)

O = None  # Point at infinity


def inverse_mod(k, p):
    """Return the modular inverse of k modulo p."""
    return pow(k, -1, p)


def is_on_curve(P):
    """Check whether a point P lies on the P-256 curve."""
    if P is O:
        return True

    x, y = P
    return (y * y - (x * x * x + a * x + b)) % p == 0


def point_add(P, Q):
    """Add two points P and Q on the elliptic curve."""
    if P is O:
        return Q
    if Q is O:
        return P

    x1, y1 = P
    x2, y2 = Q

    if x1 == x2 and (y1 + y2) % p == 0:
        return O

    if P != Q:
        lam = ((y2 - y1) * inverse_mod(x2 - x1, p)) % p
    else:
        lam = ((3 * x1 * x1 + a) * inverse_mod(2 * y1, p)) % p

    x3 = (lam * lam - x1 - x2) % p
    y3 = (lam * (x1 - x3) - y1) % p

    return (x3, y3)


def scalar_multiply(k, P):
    """Compute kP using the double-and-add method."""
    result = O
    addend = P

    while k > 0:
        if k & 1:
            result = point_add(result, addend)
        addend = point_add(addend, addend)
        k >>= 1

    return result


# Base point
G = (Gx, Gy)

print("Is G on the curve?", is_on_curve(G))

# Example private key
d = 123456789

# Public key Q = dG
Q = scalar_multiply(d, G)

print("Private key d:")
print(d)

print("\nPublic key Q = dG:")
print("Qx =", hex(Q[0]))
print("Qy =", hex(Q[1]))

print("\nIs Q on the curve?", is_on_curve(Q))
print("Is nG the point at infinity?", scalar_multiply(n, G) is O)
