from dataclasses import dataclass
from typing import Callable, Any, Set, Optional


@dataclass
class FiniteGroup:
    """
    A finite group represented by a set G and a binary operation *.

    A structure (G, *) is a group if it satisfies:

    1. Closure:
       For all a, b in G, a * b is also in G.

    2. Associativity:
       For all a, b, c in G,
       (a * b) * c = a * (b * c).

    3. Identity element:
       There exists an element e in G such that
       e * a = a and a * e = a for all a in G.

    4. Inverse element:
       For each a in G, there exists b in G such that
       a * b = e and b * a = e.
    """

    elements: Set[Any]
    operation: Callable[[Any, Any], Any]
    identity: Any
    name: str = "Finite Group"
    operation_symbol: str = "*"

    def __post_init__(self):
        if self.identity not in self.elements:
            raise ValueError("The identity element must belong to the set of elements.")

    def operate(self, a: Any, b: Any) -> Any:
        """
        Compute a * b.
        """
        if a not in self.elements:
            raise ValueError(f"{a} is not an element of the group.")

        if b not in self.elements:
            raise ValueError(f"{b} is not an element of the group.")

        return self.operation(a, b)

    def check_closure(self) -> bool:
        """
        Check whether the operation is closed on G.

        That is, for all a, b in G, a * b must also be in G.
        """
        for a in self.elements:
            for b in self.elements:
                result = self.operation(a, b)
                if result not in self.elements:
                    return False
        return True

    def check_associativity(self) -> bool:
        """
        Check associativity:

            (a * b) * c = a * (b * c)
        """
        for a in self.elements:
            for b in self.elements:
                for c in self.elements:
                    left = self.operation(self.operation(a, b), c)
                    right = self.operation(a, self.operation(b, c))

                    if left != right:
                        return False
        return True

    def check_identity(self) -> bool:
        """
        Check whether the given identity element works correctly.

        For every a in G:

            e * a = a
            a * e = a
        """
        e = self.identity

        for a in self.elements:
            if self.operation(e, a) != a:
                return False

            if self.operation(a, e) != a:
                return False

        return True

    def inverse_of(self, a: Any) -> Optional[Any]:
        """
        Find the inverse of an element a.

        The inverse of a is an element b such that:

            a * b = e
            b * a = e
        """
        if a not in self.elements:
            raise ValueError(f"{a} is not an element of the group.")

        e = self.identity

        for b in self.elements:
            if self.operation(a, b) == e and self.operation(b, a) == e:
                return b

        return None

    def check_inverses(self) -> bool:
        """
        Check whether every element has an inverse.
        """
        for a in self.elements:
            if self.inverse_of(a) is None:
                return False
        return True

    def is_abelian(self) -> bool:
        """
        Check whether the group is abelian.

        A group is abelian if:

            a * b = b * a

        for all a, b in G.
        """
        for a in self.elements:
            for b in self.elements:
                if self.operation(a, b) != self.operation(b, a):
                    return False
        return True

    def is_group(self) -> bool:
        """
        Check all group axioms.
        """
        return (
            self.check_closure()
            and self.check_associativity()
            and self.check_identity()
            and self.check_inverses()
        )

    def order(self) -> int:
        """
        Return the order of the group, that is, the number of elements in G.
        """
        return len(self.elements)

    def show_structure(self) -> None:
        """
        Display the main information about the finite group.
        """
        print(f"Group: {self.name}")
        print(f"G = {self._sorted_elements()}")
        print(f"Operation: {self.operation_symbol}")
        print(f"Identity element: {self.identity}")
        print(f"Order of the group: {self.order()}")

    def show_inverses(self) -> None:
        """
        Display the inverse of each element.
        """
        print("Inverses:")

        for a in self._sorted_elements():
            print(f"{a}^(-1) = {self.inverse_of(a)}")

    def show_verification(self) -> None:
        """
        Display whether the group axioms are satisfied.
        """
        print("Verification:")
        print(f"Closure: {self.check_closure()}")
        print(f"Associativity: {self.check_associativity()}")
        print(f"Identity: {self.check_identity()}")
        print(f"Inverses: {self.check_inverses()}")
        print(f"Is group: {self.is_group()}")
        print(f"Is abelian: {self.is_abelian()}")

    def _sorted_elements(self):
        """
        Return sorted elements when possible.
        """
        try:
            return sorted(self.elements)
        except TypeError:
            return list(self.elements)


# ------------------------------------------------------------
# Example: Z_5 under addition modulo 5
# ------------------------------------------------------------

def addition_mod_5(a: int, b: int) -> int:
    """
    Operation in Z_5:

        a * b = (a + b) mod 5
    """
    return (a + b) % 5


if __name__ == "__main__":
    Z5 = {0, 1, 2, 3, 4}

    group_Z5 = FiniteGroup(
        elements=Z5,
        operation=addition_mod_5,
        identity=0,
        name="Z_5 under addition modulo 5",
        operation_symbol="+ mod 5"
    )

    group_Z5.show_structure()
    print()

    group_Z5.show_verification()
    print()

    group_Z5.show_inverses()