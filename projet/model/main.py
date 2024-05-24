import os
import subprocess

####################################################################################################################
##############################  pour lancer le netoyage et le model en 1 fois       ################################
####################################################################################################################

def main():
    """
    pour lancer le nettoyage et la création du model depuis la racine sans aller jusqu'au dossier model
    
    """

    # Changer le répertoire courant au dossier 'Model'   
    os.chdir(".\\Model")

    # Exécuter 'clean.py'
    subprocess.call("python clean.py", shell=True)

    # Exécuter 'Model.py'
    subprocess.call("python Model.py", shell=True)

# Appeler la fonction pour exécuter le code
if __name__ == "__main__":
    main()


