import itertools
import numpy as np


class Formula:
    def __init__(self):
        pass

    def oblicz(self, zmienna):
        pass

    def __str__(self):
        pass

    def czy_taut(f):
        def znajdz(f):
            if f.__class__ is Zmienna:
                return [f.zmienna]

            if f.__class__ is Not:
                return znajdz(f.formula)

            if f.__class__ is not Prawda:
                ff1 = znajdz(f.formula1)
                ff2 = znajdz(f.formula2)
                if ff1 is not None and ff2 is not None:
                    return ff1 + ff2
                if ff1 is not None:
                    return ff1
                return ff2

        zmienne = np.unique(znajdz(f))
        all_poss = []
        for i in range(len(zmienne) + 1):
            all_poss.extend(list(itertools.combinations(zmienne, i)))

        for p in all_poss:
            if not f.oblicz({zm: zm in p for zm in zmienne}):
                return False
        return True


class Zmienna(Formula):
    def __init__(self, zmienna):
        self.zmienna = zmienna
        super().__init__()

    def oblicz(self, zmienne):
        return zmienne[self.zmienna]

    def __str__(self):
        return self.zmienna


class And(Formula):
    def __init__(self, f1, f2):
        self.formula1 = f1
        self.formula2 = f2
        super().__init__()

    def oblicz(self, zmienne):
        return self.formula1.oblicz(zmienne) and self.formula2.oblicz(zmienne)

    def __str__(self):
        return ' ( ' + str(self.formula1) + ' ) AND ( ' + str(self.formula2) + ' ) '


class Or(Formula):
    def __init__(self, f1, f2):
        self.formula1 = f1
        self.formula2 = f2
        super().__init__()

    def oblicz(self, zmienne):
        return self.formula1.oblicz(zmienne) or self.formula2.oblicz(zmienne)

    def __str__(self):
        return ' ( ' + str(self.formula1) + ' ) OR ( ' + str(self.formula2) + ' ) '


class Impl(Formula):
    def __init__(self, f1, f2):
        self.formula1 = f1
        self.formula2 = f2
        super().__init__()

    def oblicz(self, zmienne):
        return not self.formula1.oblicz(zmienne) or self.formula2.oblicz(zmienne)

    def __str__(self):
        return ' ( ' + str(self.formula1) + ' ) ==> ( ' + str(self.formula2) + ' ) '


class Rwn(Formula):
    def __init__(self, f1, f2):
        self.formula1 = f1
        self.formula2 = f2
        super().__init__()

    def oblicz(self, zmienne):
        return (self.formula1 and self.formula2) or (not self.formula1 and not self.formula2)

    def __str__(self):
        return ' ( ' + str(self.formula1) + ' ) <==> ( ' + str(self.formula2) + ' ) '


class Not(Formula):
    def __init__(self, f):
        self.formula = f
        super().__init__()

    def oblicz(self, zmienne):
        return not self.formula.oblicz(zmienne)

    def __str__(self):
        return ' NOT ( ' + str(self.formula) + ' ) '


class Prawda(Formula):
    def __init__(self):
        super().__init__()

    def oblicz(self, zmienne):
        return True

    def __str__(self):
        return ' TRUE '


class Falsz(Formula):
    def __init__(self):
        super().__init__()

    def oblicz(self, zmienne):
        return False

    def __str__(self):
        return ' FALSE '


a = Impl(Zmienna('x'), And(Zmienna('y'), Prawda()))
print(str(a))
print(a.oblicz({'x': True, 'y': True}))

b = And(Zmienna('x'), Not(Impl(Rwn(Zmienna('x'), Prawda()), Zmienna('y'))))
print(b)
print(b.czy_taut())

c = Or(Zmienna('x'), Not(Zmienna('x')))
print(c)
print(c.czy_taut())
