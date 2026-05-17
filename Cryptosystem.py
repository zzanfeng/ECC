from dataclasses import dataclass
from typing import Callable, Any, Set


@dataclass
class Cryptosystem:
    """
    A general cryptosystem represented by the five-tuple:

        (P, C, K, E, D)

    where:
        P = plaintext space
        C = ciphertext space
        K = key space
        E = encryption function
        D = decryption function

    Correctness condition:

        D_k(E_k(p)) = p
    """

    plaintext_space: Set[Any]
    ciphertext_space: Set[Any]
    key_space: Set[Any]
    encryption_function: Callable[[Any, Any], Any]
    decryption_function: Callable[[Any, Any], Any]
    name: str = "Cryptosystem"

    def encrypt(self, key: Any, plaintext: Any) -> Any:
        """
        Encrypt plaintext p using key k.
        """
        if key not in self.key_space:
            raise ValueError(f"Invalid key: {key}")

        if plaintext not in self.plaintext_space:
            raise ValueError(f"Invalid plaintext: {plaintext}")

        ciphertext = self.encryption_function(key, plaintext)

        if ciphertext not in self.ciphertext_space:
            raise ValueError(f"Invalid ciphertext produced: {ciphertext}")

        return ciphertext

    def decrypt(self, key: Any, ciphertext: Any) -> Any:
        """
        Decrypt ciphertext c using key k.
        """
        if key not in self.key_space:
            raise ValueError(f"Invalid key: {key}")

        if ciphertext not in self.ciphertext_space:
            raise ValueError(f"Invalid ciphertext: {ciphertext}")

        plaintext = self.decryption_function(key, ciphertext)

        if plaintext not in self.plaintext_space:
            raise ValueError(f"Invalid plaintext recovered: {plaintext}")

        return plaintext

    def verify_correctness(self, key: Any, plaintext: Any) -> bool:
        """
        Verify the correctness condition:

            D_k(E_k(p)) = p
        """
        ciphertext = self.encrypt(key, plaintext)
        recovered_plaintext = self.decrypt(key, ciphertext)

        return recovered_plaintext == plaintext

    def show_five_tuple(self) -> None:
        """
        Display the five components of the cryptosystem.
        """
        print(f"Cryptosystem: {self.name}")
        print(f"P = {self.plaintext_space}")
        print(f"C = {self.ciphertext_space}")
        print(f"K = {self.key_space}")
        print("E = encryption function")
        print("D = decryption function")


# ------------------------------------------------------------
# Example: Shift cipher over Z_26
# ------------------------------------------------------------

def shift_encrypt(key: int, plaintext: int) -> int:
    """
    E_k(p) = (p + k) mod 26
    """
    return (plaintext + key) % 26


def shift_decrypt(key: int, ciphertext: int) -> int:
    """
    D_k(c) = (c - k) mod 26
    """
    return (ciphertext - key) % 26


if __name__ == "__main__":
    Z26 = set(range(26))

    shift_cipher = Cryptosystem(
        plaintext_space=Z26,
        ciphertext_space=Z26,
        key_space=Z26,
        encryption_function=shift_encrypt,
        decryption_function=shift_decrypt,
        name="Shift Cipher"
    )

    shift_cipher.show_five_tuple()

    key = 3
    plaintext = 7

    ciphertext = shift_cipher.encrypt(key, plaintext)
    recovered_plaintext = shift_cipher.decrypt(key, ciphertext)

    print()
    print(f"Key k = {key}")
    print(f"Plaintext p = {plaintext}")
    print(f"Ciphertext E_k(p) = {ciphertext}")
    print(f"Recovered plaintext D_k(E_k(p)) = {recovered_plaintext}")
    print(f"Correctness verified: {shift_cipher.verify_correctness(key, plaintext)}")