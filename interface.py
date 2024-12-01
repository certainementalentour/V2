# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox
from Donnees import GestionPlaylist, donnees
from LecteurVideo import LecteurVideo

if sys.platform == 'win32':
    import winreg
def recuperer_theme():
    """détecte le thème windows"""
    try:
        registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
        key = winreg.OpenKey(registry, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize")
        value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
        return "light" if value == 1 else "dark"
        #return 0  # debug
    except:
        return "light"  # Par défaut le thème sera clair

class InterfaceGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("[Insérer un titre]")
        self.root.geometry("1200x260")  # proportions initiales de l'interface
        self.root.minsize(565, 200)

        # Ajouter l'icône
        emplacement_icone = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ressources", "logoColore.ico")
        if os.path.exists(emplacement_icone):
            self.root.iconbitmap(emplacement_icone)

         # Appliquer le thème
        theme = recuperer_theme()
        style = ttk.Style()

        if theme == "dark":
            self.root.configure(bg='black')
            style.configure(".", background="black", foreground="white")  # Configuration globale
            style.configure("TLabel", background="black", foreground="white")
            style.configure("TFrame", background="black")
            style.configure("Treeview", 
            background="black", 
            foreground="white",
            fieldbackground="black"
            )
            #  Configuration spécifique aux boutons sombres
            style.configure("TButton",
                background="#333333",
                foreground="grey",
                bordercolor="#555555",
                relief="flat",
                padding=5
            )
            # bouton survolé
            style.map("TButton", background=[("active", "#444444")], foreground= [("active", "black")], bordercolor=[("active", "#666666")])
            # Configuration spécifique pour la zone de texte
            text_bg = 'black'
            text_fg = 'white'
        else:
            self.root.configure(bg='white')
            style.configure("TFrame", background="white")
            # boutons clairs
            style.configure("TButton", background="#0080ff", foreground="black", bordercolor="#cccccc", relief="flat", padding=5)
            
            # Configuration spécifique pour la zone de texte
            text_bg = 'white'
            text_fg = 'black'

        # Configurer le redimensionnement de la grille (rendre l'interface responsive)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Frame principale
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")

        # Configurer le redimensionnement dans main_frame
        main_frame.grid_columnconfigure(1, weight=1)  # La colonne avec le Text widget s'étendra
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_rowconfigure(2, weight=1)
        main_frame.grid_rowconfigure(3, weight=1)
        
        # Boutons
        ttk.Button(main_frame, text="Afficher la playlist", 
                  command=self.afficher_playlist).grid(row=0, column=0, pady=5, padx=5, sticky="ew")
        ttk.Button(main_frame, text="Ajouter une vidéo", 
				  command=lambda: GestionPlaylist.ajouter_video(self.root)).grid(row=1, column=0, pady=5, padx=5, sticky="ew")
        ttk.Button(main_frame, text="Lire une vidéo", 
                  command=self.lire_video).grid(row=2, column=0, pady=5, padx=5, sticky="ew")
        ttk.Button(main_frame, text="Ne pas Appuyer", 
                  command=self.perdu).grid(row=3, column=0, pady=5, padx=5, sticky="ew")
        ttk.Button(main_frame, text="Quitter", 
                  command=self.quitter).grid(row=4, column=0, pady=5, padx=5, sticky="ew")
        
        # Zone d'affichage de la playlist
        self.playlist_text = tk.Text(main_frame, height=10, width=50,
                                    bg=text_bg, fg=text_fg)
        self.playlist_text.configure(insertbackground=text_fg)  # colore aussi l'arrière-plan des lignes vides
        if theme == "dark":
            self.playlist_text.configure(selectbackground="#0080ff", selectforeground="white")
        self.playlist_text.grid(row=0, column=1, rowspan=4, padx=5, sticky="nsew")
        
        # Charger la playlist au démarrage
        donnees.importation()
        self.afficher_playlist()

    def afficher_playlist(self):
        self.playlist_text.delete(1.0, tk.END)
        for numero, (titre, chemin) in donnees.Video.items():
            self.playlist_text.insert(tk.END, f"{numero}: {titre} ({chemin})\n")

    def lire_video(self):
        chemin = GestionPlaylist.choisir_video(self.root)  # self.root sert à rattacher à l'interface principale
        if chemin:
            if os.path.exists(chemin):
                LecteurVideo(chemin)
                donnees.exportation()
            else:
                messagebox.showerror("erreur", "le fichier n'existe pas")

    def quitter(self):
        donnees.exportation()
        self.root.quit()

    def perdu(self):
        messagebox.showerror("perdu", "NE PAS CLIQUER !")

class InterfaceCLI:
    @staticmethod
    def demarrer():

		# Charger la liste de lecture
        donnees.importation()
		
        while True:
            print("\n1: Afficher la playlist")
            print("2: Ajouter une vidéo à la playlist")
            print("3: Lire une vidéo")
            print("4: Quitter")

            choix = input("Votre choix : ")

            if choix == "1":
                GestionPlaylist.afficher_playlist()
            elif choix == "2":
                GestionPlaylist.ajouter_video()
            elif choix == "3":
                chemin = GestionPlaylist.choisir_video()
                if chemin:
                    LecteurVideo(chemin)
                    donnees.exportation()
            elif choix == "4":
                donnees.exportation()
                print("Programme quitté.")
                break
            else:
                print("Choix invalide.")
