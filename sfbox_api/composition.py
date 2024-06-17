from typing import List

import sympy


class Composition:
    LIB = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789()[]")
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def __init__(self, topological_script: str):
        report = Composition.check_script(topological_script)
        if report != "No errors":
            raise SyntaxError(report)
        self.topological_script = topological_script
        try:
            self.N: int = self._mol_mass()
        except SyntaxError:
            raise SyntaxError(f"{topological_script}: braces placed incorrectly")

    def types_list(self) -> List[str]:
        lst: List = []
        brace_open: bool = False
        position: int
        for i in range(len(self.topological_script)):
            if self.topological_script[i] == "(":
                brace_open = True
                position = i + 1
            if self.topological_script[i] == ")":
                if brace_open:
                    lst.append(self.topological_script[position:i])
                    brace_open = False
        return list(set(lst))

    def _mol_mass(self) -> int:
        formula = ""
        for s in self.topological_script:
            if s.isdigit() or s in "()":
                formula += s
        formula = formula.replace("()", "+")
        formula = formula.replace("(", "+(")
        formula = formula.replace(")", ")*")
        formula = formula.replace("*)", "*1)")
        formula = formula.replace("(+", "(")
        formula = formula.replace("*+", "+")
        return sympy.sympify(formula[1:])

    @staticmethod
    def check_script(script: str) -> str:
        if set(script).difference(Composition.LIB) != set():
            return f"{script}: Invalid symbol(s): {set(script).difference(Composition.LIB)}"
        if script.count("(") != script.count(")"):
            return f"{script}: Number of ) != number of ("
        if script.count("[") != script.count("]"):
            return f"{script}:Number of ] != number of ["
        if script[0] != "(":
            return f"{script}: First symbol is not ("
        if not script[-1].isdigit():
            return f"{script}: Last symbol is not digit"
        if script.count(")(") != 0:
            return f"{script}: There is )("
        if script.count("()") != 0:
            return f"{script}: There is ()"
        for i in range(len(script) - 1):
            if script[i] == "]" and script[:i].count("[") < 1:
                return f"{script}: before ] less than 1 ["
            if script[i] == "]" and script[script[:i].rfind("[") : i].count(
                "("
            ) != script[script[:i].rfind("[") : i].count(")"):
                return f"{script}: in [] number ( > number )"
            if script[i] == ")":
                for j in range(i + 1, len(script)):
                    if script[j] in "()[]":
                        break
                    else:
                        if not script[j].isdigit():
                            return f"{script}: After ) there is no digit"
            if script[i] == ")" and script[i + 1] == "0":
                return f"{script}: 0 after )"
            if script[i] == "(" and script[i + 1].isdigit():
                return f"{script}: digit after ("
            if script[i] == "[" and script[i + 1] != "(":
                return f"{script}: After [ must be ("
            if script[i] == "]" and script[i + 1].isdigit():
                return f"{script}: digit after ]"
            if script[i] == "[" and script[:i].count(")") <= 1:
                return f"{script}: ) must be before first ["
            if script[i] in Composition.alphabet and script[i + 1] in "[](":
                return f"{script}: character before []("
            if script[i] in "[])" and script[i + 1] in Composition.alphabet:
                return f"{script}: []) before character"
        return "No errors"
