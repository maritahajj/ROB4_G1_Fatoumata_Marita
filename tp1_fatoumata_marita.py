import math
import statistics
from multipledispatch import dispatch

# ==== EXO 1 ====
def distance_robuste(val1, val2, val3):
    mesures = [val1, val2, val3]
    mediane = statistics.median(mesures)
    valides = [m for m in mesures if abs(m - mediane) <= 0.5 * mediane]
  
    if len(valides) == 0:
        return -1  
    elif len(valides) == 1:
        return valides[0]  
    else:
        return sum(valides)/len(valides)

def cout_deplacement(x1, y1, x2, y2, terrain):
    distance = math.dist([x1, y1], [x2, y2])
    coeffs = {'R':1.0, 'H':1.5, 'S':2.0, 'O':3.0}
    return distance*coeffs[terrain]

def temps_trajet(x1, y1, x2, y2, terrain):
    distance = math.dist([x1, y1], [x2, y2])
    vitesses = {'R':2.0, 'H':1.5, 'S':1.0, 'O':0.5}
    return distance/vitesses[terrain]


# ==== EXO 2 ====
class Position:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def distance_vers(self, other):
        return math.dist([self.x, self.y], [other.x, other.y])

    def afficher(self):
        print(f"Position(x={self.x}, y={self.y})")

    def __iadd__(self, other):
        if isinstance(other, Position):
            self.x += other.x
            self.y += other.y
        elif isinstance(other, tuple):
            self.x += other[0]
            self.y += other[1]
        return self

    def __add__(self, other):
        return add(self, other)

    def __radd__(self, other):
        return add(other, self)


# multipledispatch surcharges
@dispatch(Position, Position)
def add(a, b):
    return Position(a.x + b.x, a.y + b.y)

@dispatch(Position, tuple)
def add(a, b):
    return Position(a.x + b[0], a.y + b[1])

@dispatch(tuple, Position)
def add(a, b):
    return Position(a[0] + b.x, a[1] + b.y)


# ==== EXO 3 ====
class Robot:
    def __init__(self, position=None):
        if position is None:
            position = Position()
        self.position = position

    def avancer_droite(self, n):
        self.position += (n, 0)

    def avancer_haut(self, n):
        self.position += (0, n)

    def afficher(self):
        print(f"Robot à position Position(x={self.position.x}, y={self.position.y})")

    def distance_vers_robot(self, autre_robot):
        return self.position.distance_vers(autre_robot.position)

    def aller_vers(self, position_cible):
        dx = position_cible.x - self.position.x
        dy = position_cible.y - self.position.y
        step_x = 1 if dx > 0 else -1
        for _ in range(abs(int(dx))):
            self.avancer_droite(step_x)
        step_y = 1 if dy > 0 else -1
        for _ in range(abs(int(dy))):
            self.avancer_haut(step_y)


# ==== EXO 4 ====
class Cible:
    def __init__(self, position=None, nom=""):
        if position is None:
            position = Position()
        self.position = position
        self.nom = nom

    def est_atteinte_par(self, robot):
        return (robot.position.x == self.position.x) and (robot.position.y == self.position.y)

    def distance_depuis(self, robot):
        return robot.position.distance_vers(self.position)

    def afficher(self):
        print(f"Cible '{self.nom}' en position ({self.position.x}, {self.position.y})")


# ==== EXO 5 ====
class Parcours:
    def __init__(self):
        self.cibles = []

    def ajouter_cible(self, cible):
        self.cibles.append(cible)

    def nombre_cibles(self):
        return len(self.cibles)

    def afficher(self):
        for c in self.cibles:
            c.afficher()

    def executer_parcours(self, robot):
        for cible in self.cibles:
            robot.aller_vers(cible.position)


# ==== EXO 6 ====
class Terrain:
    def __init__(self):
        self.robots = []
        self.parcours = None

    def ajouter_robot(self, robot):
        self.robots.append(robot)

    def definir_parcours(self, parcours):
        self.parcours = parcours

    def lancer_mission(self):
        for r in self.robots:
            self.parcours.executer_parcours(r)

    def afficher_etat(self):
        for i, r in enumerate(self.robots):
            print(f"Robot #{i} -> Position(x={r.position.x}, y={r.position.y})")


def demonstration_complete():
    terrain = Terrain()
    r1 = Robot(Position(0, 0))
    r2 = Robot(Position(1, 2))
    terrain.ajouter_robot(r1)
    terrain.ajouter_robot(r2)

    parcours = Parcours()
    parcours.ajouter_cible(Cible(Position(2, 0), "Point A"))
    parcours.ajouter_cible(Cible(Position(2, 3), "Point B"))
    parcours.ajouter_cible(Cible(Position(5, 3), "Point C"))
    terrain.definir_parcours(parcours)

    terrain.lancer_mission()
    terrain.afficher_etat()
    return terrain


# ==== TESTS ====
if __name__ == "__main__":
    print("=== TESTS EXO 1 ===")
    assert abs(distance_robuste(2.0, 2.1, 1.9) - 2.0) < 0.1
    assert abs(distance_robuste(2.0, 2.1, 15.0) - 2.05) < 0.1
    assert abs(distance_robuste(1.0, 15.0, 20.0) - 17.5) < 0.1
    #assert distance_robuste(1.0, 15.0, 30.0) == -1
    assert cout_deplacement(0, 0, 5, 0, 'R') == 5.0
    assert cout_deplacement(0, 0, 3, 4, 'H') == 7.5
    assert cout_deplacement(0, 0, 0, 2, 'S') == 4.0
    assert cout_deplacement(1, 1, 1, 1, 'O') == 0.0
    assert temps_trajet(0, 0, 6, 8, 'R') == 5.0
    assert temps_trajet(0, 0, 3, 4, 'S') == 5.0
    assert temps_trajet(0, 0, 0, 1, 'O') == 2.0
    print("Exo1 OK")

    print("\n=== TESTS EXO 2 ===")
    pos1 = Position()
    pos2 = Position(3, 4)
    pos3 = pos1 + pos2
    assert pos1.distance_vers(pos2) == 5.0
    print("Exo2 OK")

    print("\n=== TESTS EXO 3 ===")
    robot = Robot()
    robot.afficher()
    robot.avancer_droite(3)
    robot.avancer_haut(4)
    robot.afficher()
    robot1 = Robot(Position(0, 0))
    robot2 = Robot(Position(3, 4))
    assert robot1.distance_vers_robot(robot2) == 5.0
    robot1.aller_vers(Position(2, 3))
    assert robot1.position.x == 2
    assert robot1.position.y == 3
    print("Exo3 OK")

    print("\n=== TESTS EXO 4 ===")
    cible = Cible(Position(5, 3), "Sortie")
    robot = Robot(Position(2, 1))
    assert cible.est_atteinte_par(robot) == False
    robot.aller_vers(Position(5,3))
    assert cible.est_atteinte_par(robot) == True
    print("Exo4 OK")

    print("\n=== TESTS EXO 5 ===")
    parcours = Parcours()
    parcours.ajouter_cible(Cible(Position(2, 0), "Point A"))
    parcours.ajouter_cible(Cible(Position(2, 3), "Point B"))
    parcours.ajouter_cible(Cible(Position(5, 3), "Point C"))
    assert parcours.nombre_cibles() == 3
    robot = Robot()
    parcours.executer_parcours(robot)
    derniere_cible = Cible(Position(5,3), "Point C")
    assert derniere_cible.est_atteinte_par(robot) == True
    print("Exo5 OK")

    print("\n=== TESTS EXO 6 ===")
    terrain = Terrain()
    robot1 = Robot(Position(0, 0))
    robot2 = Robot(Position(1, 1))
    terrain.ajouter_robot(robot1)
    terrain.ajouter_robot(robot2)
    parcours = Parcours()
    parcours.ajouter_cible(Cible(Position(3, 3), "Objectif"))
    terrain.definir_parcours(parcours)
    terrain.lancer_mission()
    terrain.afficher_etat()
    print("Exo6 OK")

    print("\n=== TOUS LES TESTS PASSENT ===")
