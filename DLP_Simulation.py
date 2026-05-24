# ============================================================
# Simulation: Discrete Logarithm Problem and Elliptic Curve DLP
# ============================================================
#
# This code is only for educational purposes.
# The numbers are intentionally small so that brute force search is possible.
# In real cryptographic systems, the parameters are much larger.

# ============================================================
# Part 1: Classical Discrete Logarithm Problem in Z_p^*
# ============================================================

def classical_dlp_bruteforce(p, alpha, beta):
    """
    Find x such that alpha^x = beta (mod p) by brute force.

    This is only feasible for very small p.
    """
    for x in range(p - 1):
        if pow(alpha, x, p) == beta:
            return x
    return None


def simulate_classical_dlp():
    print("===== Classical Discrete Logarithm Problem =====")

    # We work in the multiplicative group Z_11^*
    p = 11
    alpha = 2

    # Secret exponent
    x_secret = 8

    # Forward computation: beta = alpha^x mod p
    beta = pow(alpha, x_secret, p)

    print(f"Prime p = {p}")
    print(f"Generator alpha = {alpha}")
    print(f"Secret exponent x = {x_secret}")
    print(f"Computed beta = alpha^x mod p = {beta}")

    print("\nPower table:")
    for x in range(p - 1):
        value = pow(alpha, x, p)
        print(f"{alpha}^{x} mod {p} = {value}")

    # Reverse problem: recover x from alpha, beta, and p
    recovered_x = classical_dlp_bruteforce(p, alpha, beta)

    print("\nBrute force result:")
    print(f"Recovered x = {recovered_x}")
    print()


# ============================================================
# Part 2: Elliptic Curve Discrete Logarithm Problem
# Curve: y^2 = x^3 + ax + b over F_p
# ============================================================

POINT_AT_INFINITY = None


def inverse_mod(n, p):
    """
    Compute the modular inverse of n modulo p.
    That is, find n^{-1} such that n * n^{-1} = 1 mod p.
    """
    n = n % p
    if n == 0:
        raise ZeroDivisionError("0 has no modular inverse.")
    return pow(n, -1, p)


def is_on_curve(P, a, b, p):
    """
    Check whether point P lies on the elliptic curve:
        y^2 = x^3 + ax + b mod p
    """
    if P is POINT_AT_INFINITY:
        return True

    x, y = P
    left = (y * y) % p
    right = (x * x * x + a * x + b) % p
    return left == right


def point_add(P, Q, a, p):
    """
    Add two points P and Q on the elliptic curve over F_p.
    """
    if P is POINT_AT_INFINITY:
        return Q
    if Q is POINT_AT_INFINITY:
        return P

    x1, y1 = P
    x2, y2 = Q

    # Case: Q = -P, vertical line
    if x1 == x2 and (y1 + y2) % p == 0:
        return POINT_AT_INFINITY

    # Case 1: P != Q, point addition
    if P != Q:
        slope = ((y2 - y1) * inverse_mod(x2 - x1, p)) % p

    # Case 2: P = Q, point doubling
    else:
        if y1 % p == 0:
            return POINT_AT_INFINITY
        slope = ((3 * x1 * x1 + a) * inverse_mod(2 * y1, p)) % p

    x3 = (slope * slope - x1 - x2) % p
    y3 = (slope * (x1 - x3) - y1) % p

    return (x3, y3)


def scalar_multiply(k, P, a, p):
    """
    Compute kP using repeated point addition.
    This is the elliptic curve analogue of alpha^k.
    """
    result = POINT_AT_INFINITY

    for _ in range(k):
        result = point_add(result, P, a, p)

    return result


def ecdlp_bruteforce(P, Q, a, p, max_steps):
    """
    Find k such that Q = kP by brute force.

    This is only feasible for very small elliptic curves.
    """
    current = POINT_AT_INFINITY

    for k in range(1, max_steps + 1):
        current = point_add(current, P, a, p)

        if current == Q:
            return k

    return None


def simulate_ecdlp():
    print("===== Elliptic Curve Discrete Logarithm Problem =====")

    # Elliptic curve:
    # E: y^2 = x^3 + 2x + 2 over F_17
    p = 17
    a = 2
    b = 2

    # Public base point
    P = (3, 1)

    if not is_on_curve(P, a, b, p):
        raise ValueError("The base point P is not on the curve.")

    # Secret scalar
    k_secret = 7

    # Forward computation: Q = kP
    Q = scalar_multiply(k_secret, P, a, p)

    print(f"Curve: y^2 = x^3 + {a}x + {b} over F_{p}")
    print(f"Base point P = {P}")
    print(f"Secret scalar k = {k_secret}")
    print(f"Computed point Q = kP = {Q}")

    print("\nMultiples of P:")
    for k in range(1, 20):
        multiple = scalar_multiply(k, P, a, p)
        print(f"{k}P = {multiple}")

    # Reverse problem: recover k from P and Q
    recovered_k = ecdlp_bruteforce(P, Q, a, p, max_steps=30)

    print("\nBrute force result:")
    print(f"Recovered k = {recovered_k}")
    print()


# ============================================================
# Main program
# ============================================================

if __name__ == "__main__":
    simulate_classical_dlp()
    simulate_ecdlp()