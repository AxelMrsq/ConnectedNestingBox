from django.shortcuts import render
import os

# Create your views here.
def Home(request):
    return render(request, 'app/Home.html')

def test(request):
    # Ouvrir et lire le fichier
    chemin_fichier = os.path.join(os.path.dirname(__file__), 'data/test1.txt')

    with open(chemin_fichier, 'r') as fichier:
        contenu = fichier.readlines()

    # Dictionnaire pour stocker les valeurs extraites
    valeurs = {}

    # Parcourir chaque ligne et extraire les données
    for ligne in contenu:
        if ':' in ligne:  # Vérifie que la ligne contient un séparateur ':'
            cle, valeur = ligne.strip().split(':', 1)  # Séparer clé et valeur
            valeurs[cle.strip()] = valeur.strip()  # Supprimer les espaces inutiles

    return render(request, 'app/test.html', {'valeurs': valeurs})