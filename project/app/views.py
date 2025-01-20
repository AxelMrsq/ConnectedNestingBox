from django.shortcuts import render
import os
import matplotlib
matplotlib.use('Agg')  # Utilise le backend 'Agg' sans interface graphique
import matplotlib.pyplot as plt
import io
import base64
from django.conf import settings
import re

# Create your views here.
def index(request):
    return render(request, 'app/index.html')

def about(request):
    return render(request, 'app/about.html')

def app(request):
    return render(request, 'app/app.html')

def hourlydata(request):
    # Chemin du dossier contenant les fichiers txt
    dossier_data = os.path.join(settings.BASE_DIR, 'app/static', 'data/')

    # Listes pour stocker les données de T, H et W
    heures = []
    T_values = []
    H_values = []
    W_values = []

    # Lister et trier les fichiers par ordre décroissant
    fichiers = [f for f in os.listdir(dossier_data) if f.startswith('data_') and f.endswith('.txt')]
    fichiers = sorted(fichiers, key=lambda x: int(x.replace('data_', '').replace('.txt', '')), reverse=True)

    # Lire chaque fichier dans le nouvel ordre
    for filename in fichiers:
        chemin_fichier = os.path.join(dossier_data, filename)
        with open(chemin_fichier, 'r') as fichier:
            contenu = fichier.readlines()

        # Extraire les données
        for ligne in contenu:
            if ':' in ligne:
                cle, valeur = ligne.strip().split(':', 1)
                if cle.strip() == 'T':
                    T_values.append(float(valeur.strip()))
                elif cle.strip() == 'H':
                    H_values.append(float(valeur.strip()))
                elif cle.strip() == 'W':
                    W_values.append(float(valeur.strip()))

        # Associer chaque fichier à une heure basée sur son numéro
        heure = int(filename.replace('data_', '').replace('.txt', ''))
        heures.append(heure)

    # Vérifier la cohérence des listes
    if len(heures) == len(T_values) == len(H_values) == len(W_values):
        images_base64 = {}

        # Fonction pour générer un graphique
        def generer_graphique(x, y, label, couleur):
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(x, y, label=label, marker='o', color=couleur)
            ax.set_xlabel('Hour')
            ax.set_ylabel(label)
            ax.set_title(f'Evolution of {label}')
            ax.legend()
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            graph_b64 = base64.b64encode(buf.read()).decode('utf-8')
            buf.close()
            plt.close(fig)
            return graph_b64

        images_base64['graph_T'] = generer_graphique(heures, T_values, "T", 'r')
        images_base64['graph_H'] = generer_graphique(heures, H_values, "H", 'g')
        images_base64['graph_W'] = generer_graphique(heures, W_values, "W", 'b')

        return render(request, 'app/hourlydata.html', {'images': images_base64})
    else:
        return render(request, 'app/hourlydata.html', {'error': 'Data are incorrect. Verify the files.'})

def recordedaudio(request):
    dossier_data = os.path.join(settings.BASE_DIR, 'app/static', 'data')
    
    # Liste des fichiers .mp3
    fichiers_mp3 = [f for f in os.listdir(dossier_data) if f.endswith('.mp3')]

    # Séparer les fichiers great-tit_X et redstart_X des autres
    pattern = re.compile(r'^(great-tit|redstart)_(\d+)\.mp3$')

    fichiers_prioritaires = []
    autres_fichiers = []

    for fichier in fichiers_mp3:
        match = pattern.match(fichier)
        if match:
            fichiers_prioritaires.append((fichier, int(match.group(2))))
        else:
            autres_fichiers.append(fichier)

    # Trier les fichiers prioritaires du plus grand au plus petit
    fichiers_prioritaires.sort(key=lambda x: x[1], reverse=True)

    # Extraire uniquement les noms de fichiers triés
    fichiers_mp3_trie = [f[0] for f in fichiers_prioritaires] + autres_fichiers

    return render(request, 'app/recordedaudio.html', {'fichiers_mp3': fichiers_mp3_trie})