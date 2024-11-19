import os
import subprocess
import random
import string
import time

def run_command(command):
    """Exécuter une commande shell et afficher les erreurs si elles surviennent."""
    try:
        subprocess.run(command, check=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Erreur : La commande '{' '.join(command)}' a échoué avec le code {e.returncode}.")

# Nombre aléatoire de commits pour la session
num_commits = random.randint(3, 10)
print(f"Nombre de commits à effectuer aujourd'hui : {num_commits}")

for _ in range(num_commits):
    try:
        # Générer un fichier temporaire unique
        file_name = f"Temp-{''.join(random.choices(string.ascii_lowercase + string.digits, k=10))}.txt"
        with open(file_name, "w") as f:
            f.write("Hello, World!\n")
        print(f"Fichier {file_name} créé.")

        # Ajouter, committer et pousser
        run_command(["git", "add", file_name])
        run_command(["git", "commit", "-m", f"Add {file_name}"])
        run_command(["git", "push"])
        print(f"Commit {file_name} poussé avec succès.")

        # Pause aléatoire entre les commits
        time.sleep(random.randint(5, 10))
    except Exception as e:
        print(f"Erreur : {e}")
        continue

print("Session de commits terminée.")
