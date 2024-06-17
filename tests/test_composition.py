from typing import List

import pytest

from sfbox_api import Composition


@pytest.mark.parametrize(
    "script, expected_result",
    [
        ("(H)2(S)1(O)4", ["H", "S", "O"]),
        ("(X)1(A2)30(([(A1)33])3(G3)8)3", ["X", "A1", "A2", "G3"]),
        ("(a120z)10", ["a120z"]),
    ],
)
def test_types_list(script: str, expected_result: List[str]) -> None:
    comp = Composition(script)
    assert set(comp.types_list()) == set(expected_result)


@pytest.mark.parametrize(
    "script, expected_result",
    [
        ("(X)1(G)99", 100),
        ("(X)1(A)2([(A1)3(G)5])2(B)10", 29),
        ("(x)1(a)1[(a)1[(a)1](a)1](a)1[(a)1](a)1", 8),
        ("(a)1(g)2[(a1)1(g)2[(a)1(g)2](a)1(g)2](a1)1(g)2[(a)1(g)2](a)1(g)2", 21),
        ("(x)1(a)2(([(a)2])3)2(a)10", 25),
    ],
)
def test_mol_mass(script: str, expected_result: int) -> None:
    comp = Composition(script)
    assert comp.N == expected_result


@pytest.mark.parametrize(
    "script_with_error",
    [
        ("(X-x)1(G)99"),
        ("(Xx)1 (G)99"),
        ("(X))1(G)99"),
        ("(X)1[(G)99"),
        ("x(X)1(G)99"),
        ("(X)1(G)99x"),
        ("(X)1(G)(A)99"),
        ("()1(G)99"),
        ("(X)1(A)x(G)1"),
        ("(X)1(A)02(G)1"),
        ("(1X)1(A)2(G)1"),
        ("(X)1[A]2(G)1"),
        ("(X)1[(A)2](G)1"),
        ("(X)1(a)1[(x)1)1A((b)2](G)1"),
        ("(X)1(a)1[(A)1a](a)2(G)1"),
        ("(X)1(a)1[(A)1a1](a)2(G)1"),
        ("(X)1(a)1[(A](a)2)1(G)1"),
    ],
)
def test_check_script(script_with_error: str) -> None:
    with pytest.raises(SyntaxError) as err:
        assert Composition(script_with_error)
    if err:
        print(str(err.value))
