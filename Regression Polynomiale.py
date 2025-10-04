import numpy as np

# Données
pas_moteur = np.array([135.3533402869855, 154.61721890913964, 172.0594087170174, 185.2434794596085, 195.32890802875067, 219.10192412731516, 232.57959698068922])
longueur_onde = np.array([256, 312, 365, 404, 435, 546, 577])

# Calcul des coefficients de la régression polynomiale d'ordre 4
coefficients = np.polyfit(pas_moteur,longueur_onde,  2)

print("Coefficients de la régression polynomiale d'ordre 4 :", coefficients)