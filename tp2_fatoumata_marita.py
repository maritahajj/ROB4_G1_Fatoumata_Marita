from abc import ABC, abstractmethod
import random

class Carte(ABC):
    """
    Classe abstraite représentant une carte.
    Chaque carte doit implémenter la méthode jeu(joueur).
    """
    @abstractmethod
    def jeu(self, joueur):
        """
        Applique l'effet de la carte sur le joueur passé en argument.
        Doit être redéfinie dans les classes filles.
        """
        pass

class CarteNormale(Carte):
    """
    Carte Normale : ajoute un nombre aléatoire de points (1 à 10).
    """
    def jeu(self, joueur):
        points = random.randint(1, 10)
        joueur.score += points
        print("Effet : Ajoute", points, "points")


class CarteBonus(Carte):
    """
    Carte Bonus : double le score actuel du joueur.
    """
    def jeu(self, joueur):
        points = joueur.score
        joueur.score = 2*points
        print("Effet : Score doublé")


class CarteMalus(Carte):
    """
    Carte Malus : retire 5 points au joueur.
    """
    def jeu(self, joueur):
        joueur.score -= 5
        print("Effet : Perd 5 points")


class CarteChance(Carte):
    """
    Carte Chance : ajoute un nombre de points aléatoire entre -5 et 15.
    Peut donc ajouter, retirer ou ne rien changer.
    """
    def jeu(self, joueur):
        points = random.randint(-5, 15)
        joueur.score += points
        if points > 0:
            print(f"Effet : Ajoute {points} points")
        elif points < 0:
            print(f"Effet : Perd {-points} points")
        else:
            print("Effet : Rien")


class Joueur:
    """
    Classe représentant un joueur avec un nom et un score.
    """
    def __init__(self, nom, score=0):
        self.nom = nom
        self.score = score

    def jouer_carte(self, carte):
        """
        Tire une carte et applique son effet.
        Utilise le polymorphisme : peu importe le type de carte,
        on appelle carte.jeu(self).
        """
        print(f"{self.nom} tire une {carte.__class__.__name__}")
        carte.jeu(self)
        print(f"Score actuel de {self.nom} : {self.score}")


class Tricheur(Joueur):
    """
    Variante de joueur : le Tricheur ignore les cartes malus.
    Hérite de Joueur mais redéfinit jouer_carte().
    """
    def jouer_carte(self, carte):
        if isinstance(carte, CarteMalus):
            # Le tricheur n'est pas affecté par les malus
            print(f"{self.nom} (tricheur) ignore un malus !")
            print(f"Score actuel de {self.nom} : {self.score}")
        else:
            # Sinon, comportement identique au joueur normal
            print(f"{self.nom} (tricheur) tire une {carte.__class__.__name__}")
            carte.jeu(self)
            print(f"Score actuel de {self.nom} : {self.score}")


def creer_deck():
    """
    Crée le deck avec la composition suivante :
    - 30 cartes normales
    - 6 cartes bonus
    - 5 cartes malus
    - 15 cartes chance
    Puis mélange le paquet avant de le retourner.
    """
    deck = []

    # Ajout des cartes normales
    for i in range(30):
        deck.append(CarteNormale())

    # Ajout des cartes bonus
    for i in range(6):
        deck.append(CarteBonus())

    # Ajout des cartes malus
    for i in range(5):
        deck.append(CarteMalus())

    # Ajout des cartes chance
    for i in range(15):
        deck.append(CarteChance())

    # Mélanger le paquet
    random.shuffle(deck)
    return deck

def partie(joueur, nb_tour=5):
    """
    Lance une partie pour un joueur donné (Joueur ou Tricheur).
    Le joueur tire nb_tour cartes du deck.
    """
    deck = creer_deck()
    for i in range(nb_tour):
        if len(deck) < 1:
            deck = creer_deck()   # recrée un deck si vide
        carte = deck.pop()        # tirer une carte du paquet
        print(f"\nTour {i+1} :")
        joueur.jouer_carte(carte)
    print(f"\nScore final de {joueur.nom} : {joueur.score}")

if __name__ == "__main__":
    # Partie avec un joueur normal
    print("=== Partie Joueur normal ===")
    joueur1 = Joueur("Fatoumata")
    partie(joueur1, 5)

    # Partie avec un tricheur
    print("\n=== Partie Tricheur ===")
    joueur2 = Tricheur("Marita")
    partie(joueur2, 5)
