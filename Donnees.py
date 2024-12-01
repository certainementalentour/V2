# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
"""
Ce fichier sert a stocker les données :
Dictionnaire contenant : clé = numéro de la vidéo ; valeur = nom de la vidéo, chemin de la vidéo
"""
import json
import os
from tkinter import filedialog, ttk, Toplevel, StringVar


class donnees:
    # Attribut de classe permettant de partager le dictionnaire entre toutes les instances de la classe (et non en avoir une par appel)
    Video = {
        # Numéro de la vidéo: ("nom de la vidéo", 'chemin de la vidéo'),
        0: ("petit test pas du tout suspect", './ressources/debug.mp4'),
    }

    @staticmethod  # permet de ne pas instancier la classe dans les autres fichiers et évite les argument 'self' ou 'cls'
    def ajouter_donnees_video(numero, titre, chemin) -> None:
        """
        Ajoute une entrée de vidéo dans le dictionnaire `Video`.
        numero: Numéro de la vidéo.
        titre: Titre de la vidéo.
        chemin: Chemin du fichier vidéo.
        """
        donnees.Video[int(numero)] = (titre, chemin)  # ne pas oublier de stocker l'index sous forme d'entier
    
    @staticmethod
    def exportation() -> None:
        '''Exporte la liste de lecture dans un fichier'''
        
        # obtenir le chemin absolu du répertoire du fichier de sauvegarde
        chemin_actuel = os.path.dirname(os.path.abspath(__file__))
        chemin_fichier = os.path.join(chemin_actuel, 'ListeDeLecture.json')

        try:
            with open(chemin_fichier, 'w', encoding='utf-8') as liste:
                json.dump(donnees.Video, liste, ensure_ascii=False, indent=4)  
                # json.dump(données, fichier, remplacement des caractères non-ASCII, nombres d'espaces par indentation(si renseigné, des retours à la ligne seront automatiquement ajoutés))
                #print(f'{donnees.Video}, sauvegardés dans {liste.name}')  # debug
                print(f"liste exportée dans: {liste.name}")

        except Exception as e:
            print(f"Erreur lors de l'exportation : {e}")
    
    @staticmethod
    def importation() -> None:
        '''importe la liste de lecture précédemment enregistrée dans le fichier JSON situé dans le même répertoire que ce fichier Python'''
    
        chemin_actuel = os.path.dirname(os.path.abspath(__file__))
        chemin_fichier = os.path.join(chemin_actuel, 'ListeDeLecture.json')
        try:
            with open(chemin_fichier,'r', encoding='utf-8') as liste:
                # Convertir les clés du JSON (toujours des chaînes) en entiers
                donnees.Video = {int(k): v for k, v in json.load(liste).items()}
                print(f"liste de lecture chargée depuis {chemin_fichier}")
        
        except json.JSONDecodeError:
            print("Erreur : Le fichier JSON est corrompu. La liste de lecture sera réinitialisée.")
            donnees.Video = {}
        except FileNotFoundError:
            print("Aucun fichier JSON trouvé. Une nouvelle liste de lecture sera créée.")
            donnees.Video = {}
        except Exception as e:
            print(e, f"la liste n'a pas pu être importée depuis{liste.name}")


class GestionPlaylist:
    @staticmethod
    def afficher_playlist():
        """Affiche les vidéos disponibles dans la playlist."""

        print("\nPlaylist actuelle :")
        for numero, (titre, chemin) in donnees.Video.items():
            print(f"{numero}: {titre} ({chemin})")

    @staticmethod
    def ajouter_video(parent_window=None):
        """Ajoute une vidéo à la playlist avec interface graphique."""
        
        if parent_window:  # Mode GUI
            # Créer une fenêtre de dialogue
            dialog = Toplevel(parent_window)
            dialog.title("Ajouter une vidéo")
            dialog.geometry("300x110")
            # Appliquer le thème
            if parent_window.cget('bg') == 'black':  # Si le thème parent est sombre
                dialog.configure(bg='black')
                style = ttk.Style()
                style.configure("Dark.TLabel", background="black", foreground="white")
                style.configure("Dark.TEntry", fieldbackground="black", foreground="white")
                style.configure("Dark.TButton", background="#333333", foreground="white")
            
            # Champ pour le titre
                ttk.Label(dialog, text="Titre de la vidéo:", style="Dark.TLabel").pack(pady=5)
            else:
                dialog.configure(bg='white')
                ttk.Label(dialog, text="Titre de la vidéo:").pack(pady=5)

            titre_var = StringVar()
            titre_entry = ttk.Entry(dialog, textvariable=titre_var)
            titre_entry.pack(pady=5)
            
            def valider():
                titre = titre_var.get()
                if titre:
                    # Ouvre le sélecteur de fichier
                    chemin = filedialog.askopenfilename(
                        parent=dialog,
                        filetypes=[("Fichiers vidéo", "*.mp4 *.avi *.mov *.mkv *.webm *.flv")]
                    )
                    if chemin and os.path.exists(chemin):
                        numero = max(donnees.Video.keys(), default=0) + 1  # permet de retrouver le dernier élément de la liste puis ajoute la nouvelle vidéo juste après
                        donnees.ajouter_donnees_video(numero, titre, chemin)
                        dialog.destroy()
                    else:
                        print("Fichier invalide ou non sélectionné.")

            ttk.Button(dialog, text="Valider", command=valider).pack(pady=10)
            pass  # permet de ne plus perdre le focus en CLI

        else:  # Mode CLI
            titre = input("Entrez le titre de la vidéo : ")
            chemin = input("Entrez le chemin complet du fichier vidéo : ")
            
            if os.path.exists(chemin):
                numero = max(donnees.Video.keys(), default=0) + 1  # permet de retrouver le dernier élément de la liste puis ajoute la nouvelle vidéo juste après
                donnees.ajouter_donnees_video(numero, titre, chemin)
                print(f"Vidéo '{titre}' ajoutée avec succès !")
            else:
                print("Chemin invalide.")

    @staticmethod
    def choisir_video(parent_window=None):
        """Permet de sélectionner une vidéo à lire."""
        if not donnees.Video:  # Si la playlist est vide
            print("La playlist est vide. Veuillez ajouter une vidéo avant de continuer.")
            return None
            
        if parent_window:  # Mode GUI
            dialog = Toplevel(parent_window)
            dialog.title("Choisir une vidéo")

            # Appliquer le thème
            if parent_window.cget('bg') == 'black':  # Si le thème parent est sombre
                dialog.configure(bg='black')
                style = ttk.Style()
                style.configure("Dark.Treeview",
                    background="black",
                    foreground="white",
                    fieldbackground="black")
                style.configure("Dark.Treeview.Heading",
                    background="black",
                    foreground="white")
                style.map("Dark.Treeview.Heading",
                          background=[('active', 'black')],
                          foreground=[('active', 'white')])
                style.map("Dark.Treeview",
                          background=[('selected', '#0080ff')],
                          foreground=[('selected', 'white')])
                style.configure("Dark.TButton",
                    background="#333333",
                    foreground="white")
                listbox = ttk.Treeview(dialog, columns=("Numéro", "Titre", "Chemin"), 
                                 show="headings", style="Dark.Treeview")
            else:
                dialog.configure(bg='white')
                listbox = ttk.Treeview(dialog, columns=("Numéro", "Titre", "Chemin"), 
                                      show="headings")
        
            # Variable pour stocker le chemin sélectionné
            chemin_selectionne = [None]
            
            # Créer une "listbox" pour afficher les vidéos
            listbox.heading("Numéro", text="Numéro")
            listbox.heading("Titre", text="Titre")
            listbox.heading("Chemin", text="Chemin")
            
            # Remplir la "listbox"
            for numero, (titre, chemin) in donnees.Video.items():
                listbox.insert("", "end", values=(numero, titre, chemin))
            
            listbox.pack(pady=10, padx=10, fill="both", expand=True)
            
            def on_select():
                selection = listbox.selection()
                if selection:
                    item = listbox.item(selection[0])
                    chemin_selectionne[0] = item['values'][2]  # Stocker le chemin
                    dialog.destroy()
            
            ttk.Button(dialog, text="Sélectionner", command=on_select).pack(pady=5)
            
            # Attendre que la fenêtre soit fermée
            parent_window.wait_window(dialog)
            return chemin_selectionne[0]
            
        else:  # Mode CLI
            GestionPlaylist.afficher_playlist()
            choix = input("Entrez le numéro de la vidéo à lire : ").strip()  # retire les espaces et retours à la ligne
            if not choix.isdigit():  # Vérifie que l'entrée est un entier (mais le laisse en tant que chaîne de caractères)
                print("Veuillez entrer un numéro valide.")
                return None
            choix = int(choix)
            if choix in donnees.Video:  # Vérifie si le numéro existe
                return donnees.Video[choix][1]  # Retourne le chemin de la vidéo
            else:
                print("Numéro invalide.")  # Si la clé n'existe pas
                return None
