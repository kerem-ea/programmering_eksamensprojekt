# C4 model: Context, Container, Component, Code
# OOP: Encapsulation, Inheritance, Polymorphism, Abstraction


# 1: 
# Lav et design til en klasse, der repræsenterer en geometrisk figur, f.eks. en cirkel, en firkant eller en trekant. 
# Klassen skal danne udgangspunkt for at kunne beregne areal og omkreds for de forskellige figurtyper.

# 2:
# Udvid designet, så resultatet af en beregning kan gemmes eller returneres på en tydelig måde.
# Forklar forskellen på at gemme en værdi i en attribut og at returnere en værdi fra en metode.

# 3:
# Lav klasserne Cirkel, Firkant og Trekant, der arver fra den geometriske figur-klasse.
# Forklar hvad super() bruges til. Implementer metoder til at beregne areal og omkreds for hver figurtype.

# 4:
# Vis hvordan du opretter instanser af Cirkel, Firkant og Trekant, 
# og hvordan du bruger objekterne til at beregne areal og omkreds for hver figur.

# 5: 
# Forklar hvad polymorfi betyder. 
# Vis med et eksempel hvordan man kan have flere figurobjekter i samme liste og kalde samme metode på dem.
import math
from abc import ABC, abstractmethod

class Figur(ABC):
    def __init__(self, navn: str):
        self.navn = navn

    @abstractmethod
    def areal(self):
        pass

    @abstractmethod
    def omkreds(self):
        pass

    def print_info(self):
        print(
            f"{self.navn} - "
            f"Areal: {self.areal():.2f}, "
            f"Omkreds: {self.omkreds():.2f}"
        )

class Cirkel(Figur):
    def __init__(self, radius: float):
        super().__init__("Cirkel")
        self.radius = radius

    def areal(self):
        return math.pi * self.radius ** 2

    def omkreds(self):
        return 2 * math.pi * self.radius

class Firkant(Figur):
    def __init__(self, a: float, b: float):
        super().__init__("Firkant")
        self.a = a
        self.b = b

    def areal(self):
        return self.a * self.b

    def omkreds(self):
        return 2 * (self.a + self.b)

class Trekant(Figur):
    def __init__(self, base: float, height: float, a: float, b: float, c: float):
        super().__init__("Trekant")
        self.base = base
        self.height = height
        self.a = a
        self.b = b
        self.c = c

    def areal(self):
        return 0.5 * self.base * self.height

    def omkreds(self):
        return self.a + self.b + self.c

cirkel = Cirkel(radius=1)
firkant = Firkant(a=4, b=6)
trekant = Trekant(base=4, height=5, a=3, b=4, c=5)

figurer = [cirkel, firkant, trekant]

for figur in figurer:
    figur.print_info()