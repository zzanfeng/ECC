from dataclasses import dataclass
from math import gcd
from typing import List


@dataclass
class ZnRing:
    """
    The ring of integers modulo n.

    Z_n = {0, 1, 2, ..., n-1}

    In this ring, addition and multiplication are performed modulo n:

        a + b mod n
        a * b mod n

    This class is designed for educational purposes. It shows how
    arithmetic works inside Z_n and verifies some basic ring properties.
    """

    n: int

    def __post_init__(self):
        if self.n <= 1:
            raise ValueError("n must be an integer greater than 1.")

    def elements(self) -> List[int]:
        """
        Return the elements of Z_n.
        """
        return list(range(self.n))

    def add(self, a: int, b: int) -> int:
        """
        Addition in Z_n:

            (a + b) mod n
        """
        self._validate_element(a)
        self._validate_element(b)

        return (a + b) % self.n

    def multiply(self, a: int, b: int) -> int:
        """
        Multiplication in Z_n:

            (a * b) mod n
        """
        self._validate_element(a)
        self._validate_element(b)

        return (a * b) % self.n

    def additive_inverse(self, a: int) -> int:
        """
        Return the additive inverse of a in Z_n.

        The additive inverse of a is an element b such that:

            a + b ≡ 0 mod n
        """
        self._validate_element(a)

        return (-a) % self.n

    def has_multiplicative_inverse(self, a: int) -> bool:
        """
        Check whether a has a multiplicative inverse in Z_n.

        An element a has a multiplicative inverse modulo n if and only if:

            gcd(a, n) = 1
        """
        self._validate_element(a)

        return gcd(a, self.n) == 1

    def multiplicative_inverse(self, a: int) -> int:
        """
        Return the multiplicative inverse of a in Z_n.

        The inverse of a is an element b such that:

            a * b ≡ 1 mod n

        This exists only when gcd(a, n) = 1.
        """
        self._validate_element(a)

        if not self.has_multiplicative_inverse(a):
            raise ValueError(f"{a} has no multiplicative inverse in Z_{self.n}.")

        for b in self.elements():
            if self.multiply(a, b) == 1:
                return b

        raise ValueError(f"Could not find the multiplicative inverse of {a}.")

    def check_additive_identity(self) -> bool:
        """
        Check whether 0 is the additive identity.

        For every a in Z_n:

            a + 0 = a
            0 + a = a
        """
        for a in self.elements():
            if self.add(a, 0) != a:
                return False

            if self.add(0, a) != a:
                return False

        return True

    def check_multiplicative_identity(self) -> bool:
        """
        Check whether 1 is the multiplicative identity.

        For every a in Z_n:

            a * 1 = a
            1 * a = a
        """
        for a in self.elements():
            if self.multiply(a, 1) != a:
                return False

            if self.multiply(1, a) != a:
                return False

        return True

    def check_distributive_property(self) -> bool:
        """
        Check the distributive property.

        For all a, b, c in Z_n:

            a * (b + c) = a*b + a*c
        """
        for a in self.elements():
            for b in self.elements():
                for c in self.elements():
                    left = self.multiply(a, self.add(b, c))
                    right = self.add(self.multiply(a, b), self.multiply(a, c))

                    if left != right:
                        return False

        return True

    def show_structure(self) -> None:
        """
        Display the ring Z_n.
        """
        print(f"Ring: Z_{self.n}")
        print(f"Elements: {self.elements()}")
        print("Addition: (a + b) mod n")
        print("Multiplication: (a * b) mod n")

    def show_operation_examples(self, a: int, b: int) -> None:
        """
        Display examples of addition and multiplication in Z_n.
        """
        self._validate_element(a)
        self._validate_element(b)

        print(f"In Z_{self.n}:")
        print(f"{a} + {b} ≡ {self.add(a, b)} (mod {self.n})")
        print(f"{a} * {b} ≡ {self.multiply(a, b)} (mod {self.n})")

    def show_additive_inverses(self) -> None:
        """
        Display the additive inverse of each element.
        """
        print(f"Additive inverses in Z_{self.n}:")

        for a in self.elements():
            print(f"-{a} ≡ {self.additive_inverse(a)} (mod {self.n})")

    def show_multiplicative_inverses(self) -> None:
        """
        Display the multiplicative inverses that exist in Z_n.
        """
        print(f"Multiplicative inverses in Z_{self.n}:")

        for a in self.elements():
            if self.has_multiplicative_inverse(a):
                print(f"{a}^(-1) ≡ {self.multiplicative_inverse(a)} (mod {self.n})")
            else:
                print(f"{a} has no multiplicative inverse in Z_{self.n}")

    def show_verification(self) -> None:
        """
        Display basic verification results.
        """
        print("Verification:")
        print(f"Additive identity 0: {self.check_additive_identity()}")
        print(f"Multiplicative identity 1: {self.check_multiplicative_identity()}")
        print(f"Distributive property: {self.check_distributive_property()}")

    def _validate_element(self, a: int) -> None:
        """
        Check whether a belongs to Z_n.
        """
        if a not in self.elements():
            raise ValueError(f"{a} is not an element of Z_{self.n}.")


# ------------------------------------------------------------
# Example: Z_5
# ------------------------------------------------------------

if __name__ == "__main__":
    Z5 = ZnRing(5)

    Z5.show_structure()
    print()

    Z5.show_operation_examples(3, 4)
    print()

    Z5.show_verification()
    print()

    Z5.show_additive_inverses()
    print()

    Z5.show_multiplicative_inverses()