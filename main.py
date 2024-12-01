# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
'''
Pour les trois du fond qui exécutent dans le terminal intégré VSCode, la méthode filedialog.askopenfilename() ne fonctionnera pas
'''
import os
import argparse
import tkinter as tk
from interface import *
# récupérer ffmpeg
chemin_ffmpeg = os.path.dirname(os.path.abspath(__file__)) + os.pathsep + "lib"
# Ajouter au PATH
os.environ["PATH"] = chemin_ffmpeg + os.pathsep + os.environ["PATH"]

def main():

    # Création du parseur d'arguments
    parser = argparse.ArgumentParser(description='Lecteur vidéo avec interface graphique ou CLI')
    parser.add_argument('--cli', action='store_true', help='Utiliser l\'interface en ligne de commande')
    args = parser.parse_args()

    if args.cli:
        # Mode CLI
        InterfaceCLI.demarrer()
    else:
        # Mode GUI (par défaut)
        root = tk.Tk()
        InterfaceGUI(root)
        root.mainloop()




# 01001101 01100101 01110010 01100011 01101001 00100000 01100100 00100111 01100101 01111000 01110000 01110010 01101001 01101101 01100101
# 01110010 00100000 01101110 01101111 01110100 01110010 01100101 00100000 01101110 01101111 01110100 01100101 00100000 01100101 01101110
# 00100000 01100010 01100001 01110011 01100101 00100000 01100100 01100101 00100000 01001011 01101110 01110101 01110100 01101000 00100000
# 01101111 01110101 00100000 01100101 01101110 00100000 01100010 01100001 01110011 01100101 00100000 01110000 01101000 01101001 00101110
# SVP

# Point d'entrée du programme,
# Si le fichier est exécuté directement (et non importé), la fonction `main()` sera appelée
if __name__ == "__main__":
    print("""

                                         ___
                                     ,-""   `.
                                   ,'  _   e )`-._
                                  /  ,' `-._<.===-'
                                 /  /
                                /  ;
                    _          /   ;
       (`._    _.-"" ""--..__,'    |
       <_  `-""                     \\ 
        <`-                          :
         (__   <__.                  ;
           `-.   '-.__.      _.'    /
              \\      `-.__,-'    _,'
               `._    ,    /__,-'
                  ""._\\__,'< <____
                       | |  `----.`.
                       | |        \\ `.
                       ; |___      \\-``
                       \\   --<
                        `. `.<
                          `-'

— Notre Mission ?
— Sauver le monde. On sait pas encore comment mais ma cousine connait le naturopathe d’Elon Musk.
— #0101001001100101011100110111000001100101011000110111010001010100011010000110010101000011011011110110010001100101010100000110110001110011""")
    try:
        main()
    except Exception as e:
        print(f"Une erreur est survenue : {e} et tu vas galérer à réparer")

