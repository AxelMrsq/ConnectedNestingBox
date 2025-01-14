from django.shortcuts import render
import os
import matplotlib
matplotlib.use('Agg')  # Utilise le backend 'Agg' sans interface graphique
import matplotlib.pyplot as plt
import io
import base64
from django.conf import settings

# Create your views here.
def Home(request):
    return render(request, 'app/Home.html')

def test(request):
    # Chemin du dossier contenant les fichiers txt
    dossier_data = os.path.join(settings.BASE_DIR, 'app/static', 'data/')

    # Listes pour stocker les données de T, H et W
    heures = []
    T_values = []
    H_values = []
    W_values = []

    # Lire chaque fichier .txt dans le dossier 'data'
    for filename in os.listdir(dossier_data):
        if filename.endswith('.txt'):
            chemin_fichier = os.path.join(dossier_data, filename)
            with open(chemin_fichier, 'r') as fichier:
                contenu = fichier.readlines()

            # Extraire les données de chaque fichier
            for ligne in contenu:
                if ':' in ligne:
                    cle, valeur = ligne.strip().split(':', 1)
                    if cle.strip() == 'T':
                        T_values.append(float(valeur.strip()))
                    elif cle.strip() == 'H':
                        H_values.append(float(valeur.strip()))
                    elif cle.strip() == 'W':
                        W_values.append(float(valeur.strip()))
            
            # Associer chaque fichier à une heure (par exemple, 'test1.txt' -> 1h)
            heure = int(filename.replace('test', '').replace('.txt', ''))
            heures.append(heure)

    # Vérification des longueurs des listes
    print(f"Heures: {len(heures)}, T_values: {len(T_values)}, H_values: {len(H_values)}, W_values: {len(W_values)}")

    # Vérification de la correspondance des dimensions
    if len(heures) == len(T_values) == len(H_values) == len(W_values):
        # Créer une figure avec 3 sous-graphiques
        fig, axs = plt.subplots(3, 1, figsize=(10, 15))  # 3 lignes, 1 colonne

        # Graphique pour T
        axs[0].plot(heures, T_values, label="T", marker='o', color='r')
        axs[0].set_xlabel('Heure')
        axs[0].set_ylabel('T')
        axs[0].set_title('Évolution de T au fil du temps')
        axs[0].legend()

        # Graphique pour H
        axs[1].plot(heures, H_values, label="H", marker='o', color='g')
        axs[1].set_xlabel('Heure')
        axs[1].set_ylabel('H')
        axs[1].set_title('Évolution de H au fil du temps')
        axs[1].legend()

        # Graphique pour W
        axs[2].plot(heures, W_values, label="W", marker='o', color='b')
        axs[2].set_xlabel('Heure')
        axs[2].set_ylabel('W')
        axs[2].set_title('Évolution de W au fil du temps')
        axs[2].legend()

        # Ajuster l'espacement entre les graphiques
        plt.tight_layout()

        # Convertir les graphiques en image base64 pour l'affichage dans la page HTML
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        image_base64 = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()

        return render(request, 'app/test.html', {'image_base64': image_base64})
    else:
        return render(request, 'app/test.html', {'error': 'Les données sont incohérentes. Vérifiez les fichiers.'})

def test_audio(request):
    # Chemin du dossier contenant les fichiers .wav
    dossier_data = os.path.join(settings.BASE_DIR, 'app/static', 'data')

    fichiers_mp3 = [f for f in os.listdir(dossier_data) if f.endswith('.mp3')]

    return render(request, 'app/test_audio.html', {'fichiers_mp3': fichiers_mp3})