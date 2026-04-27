import math
from typing import List
import random
class Frac:
    def __init__(self, a:int|float, b:int|float, c=0)->None:
        self.a, self.b = a, b
    def __repr__(self)->str:
        return f"Frac: {self.a} / {self.b}"
    def to_float(self)->float:
        return self.a / self.b
    def simplify(self,r=True):
        """r: return a Frac object"""
        if isinstance(self.a, int) and isinstance(self.b, int):
            gcd = math.gcd(self.a,self.b)
            if gcd > 0:
                self.a //= gcd
                self.b //= gcd
        if r:
            return self
        return None
    def __mul__(self, other):
        if isinstance(other, Frac):
            return Frac(self.a*other.a,self.b*other.b).simplify()
        elif isinstance(other, int) or isinstance(other, float):
            return Frac(self.a*other, self.b).simplify()
        return NotImplemented
    def __add__(self, other):
        if isinstance(other,Frac):
            return Frac(self.a*other.b + other.a*self.b, self.b*other.b).simplify()
        elif isinstance(other, int|float):
            return Frac(other*self.b + self.a, self.b).simplify()
        return NotImplemented
    def __sub__(self, other):
        if isinstance(other, Frac):
            return Frac(self.a*other.b - other.a*self.b, self.b*other.b).simplify()
        elif isinstance(other, int | float):
            return Frac(other * self.b - self.a, self.b).simplify()
        return NotImplemented
    def __truediv__(self, other):
        if isinstance(other, Frac):
            return self.__mul__(Frac(other.b,other.a))
        elif isinstance(other, int | float):
            return self.__mul__(Frac(1,other))

        return NotImplemented

class Expersion:
    numbers = [str(n) for n in range(10)]
    expressions = ["+","-","*","/"]

    def __init__(self, term:str|list[str|int])->None:
        self.term:List[int|str|float] = []
        self.term_string = ""

        if isinstance(term, str):
            self.to_lst(term)
            self.term_string = term
        else:
            self.term = term
            self.to_str(term)

        self.add_missing_multipliers()

    def __repr__(self)->str:
        return f"{self.term_string}"

    def to_str(self, raw:list[int|str]):
        string = ""
        for i in raw:
            string += str(i)
        self.term_string = string

    def to_lst(self, raw:str)->None:
        elements = list(raw)
        i = 0

        while i < len(elements):
            print(i)
            if elements[i] in Expersion.numbers:
                i = self.collect_integers(elements, i)
            else:
                self.term.append(elements[i])
            i+=1
    def collect_integers(self,source:list[str], from_i:int)->int:
        i = from_i
        number = ""

        while source[i] in Expersion.numbers or source[i] == ".":
            number += source[i]
            i+=1

            if not i < len(source):
                self.term.append(float(number))
                return i

        self.term.append(float(number))
        return i - 1

    def is_a_variable(self, x:str|float|int)->bool:
        if not isinstance(x, str):
            return False
        if x not in Expersion.numbers and x not in Expersion.expressions:
            return True
        return False

    def add_missing_multipliers(self)->None:
        for i in range(len(self.term)-1):
            if isinstance(self.term[i], float) and self.is_a_variable(self.term[i+1]):
                self.term.insert(i+1, "*")

e1 = Expersion(term=[2, "x", "+", 2])
e2 = Expersion(term="22.7x+1")
print(e2)
print(e2.term)