# ============================================================
# ElGamal Cryptosystem Simulation over Z_p^*
# ============================================================
# This simulation illustrates the basic working process of the
# ElGamal cryptosystem:
#
# 1. Key generation
# 2. Encryption
# 3. Decryption
# 4. Verification that the decrypted message equals the original one
#
# The parameters are intentionally small for educational purposes.
# They are not secure for real cryptographic applications.
# ============================================================


def elgamal_key_generation(p, alpha, private_key):
    """
    Generate the public key for the ElGamal cryptosystem.

    Parameters:
        p: a prime number
        alpha: a generator of the multiplicative group Z_p^*
        private_key: the receiver's private key a

    Returns:
        public_key: y = alpha^a mod p
    """
    public_key = pow(alpha, private_key, p)
    return public_key


def elgamal_encrypt(message, p, alpha, public_key, random_k):
    """
    Encrypt a message using the ElGamal cryptosystem.

    Encryption formulas:
        gamma = alpha^k mod p
        delta = message * public_key^k mod p

    Parameters:
        message: plaintext message represented as an integer modulo p
        p: prime number
        alpha: generator of Z_p^*
        public_key: receiver's public key y
        random_k: random temporary integer chosen by the sender

    Returns:
        ciphertext: the pair (gamma, delta)
    """
    gamma = pow(alpha, random_k, p)
    masking_value = pow(public_key, random_k, p)
    delta = (message * masking_value) % p

    return gamma, delta


def elgamal_decrypt(ciphertext, p, private_key):
    """
    Decrypt an ElGamal ciphertext.

    Decryption formula:
        message = delta * (gamma^a)^(-1) mod p

    Parameters:
        ciphertext: the pair (gamma, delta)
        p: prime number
        private_key: receiver's private key a

    Returns:
        decrypted_message: the recovered plaintext message
    """
    gamma, delta = ciphertext

    shared_value = pow(gamma, private_key, p)
    shared_value_inverse = pow(shared_value, -1, p)

    decrypted_message = (delta * shared_value_inverse) % p

    return decrypted_message


def print_table(headers, rows):
    """
    Print a simple table without using external libraries.
    """
    table = [headers] + rows
    column_widths = [
        max(len(str(row[i])) for row in table)
        for i in range(len(headers))
    ]

    def format_row(row):
        return " | ".join(
            str(row[i]).ljust(column_widths[i])
            for i in range(len(row))
        )

    print(format_row(headers))
    print("-+-".join("-" * width for width in column_widths))

    for row in rows:
        print(format_row(row))


# ============================================================
# 1. Public parameters
# ============================================================

p = 23
alpha = 5

# ============================================================
# 2. Receiver key generation
# ============================================================

private_key = 6
public_key = elgamal_key_generation(p, alpha, private_key)

print("ElGamal Cryptosystem Simulation")
print("================================")
print(f"Prime number p: {p}")
print(f"Generator alpha: {alpha}")
print(f"Private key a: {private_key}")
print(f"Public key y = alpha^a mod p: {public_key}")
print()


# ============================================================
# 3. Encryption and decryption examples
# ============================================================

messages = [3, 7, 11, 15, 19]
random_values_k = [2, 4, 7, 10, 13]

rows = []

for message, k in zip(messages, random_values_k):
    ciphertext = elgamal_encrypt(
        message=message,
        p=p,
        alpha=alpha,
        public_key=public_key,
        random_k=k
    )

    decrypted_message = elgamal_decrypt(
        ciphertext=ciphertext,
        p=p,
        private_key=private_key
    )

    gamma, delta = ciphertext

    rows.append([
        message,
        k,
        gamma,
        delta,
        f"({gamma}, {delta})",
        decrypted_message,
        message == decrypted_message
    ])


headers = [
    "Message m",
    "Random k",
    "gamma",
    "delta",
    "Ciphertext",
    "Decrypted m",
    "Correct"
]

print_table(headers, rows)