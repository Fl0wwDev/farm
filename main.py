import os
import subprocess
import random
import string
import time

# Configuration statique
github_username = "Fl0wwDev"
user_name = "mahe"
user_email = "mafradin@hotmail.fr"
repository_name = "farm"  # Nom de votre dépôt

def run_command(command, check=True, capture_output=False):
    """Exécuter une commande système avec gestion des erreurs."""
    try:
        time.sleep(1)  # Pause avant chaque commande
        return subprocess.run(
            command,
            check=check,
            capture_output=capture_output,
            text=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Erreur : La commande '{' '.join(command)}' a échoué.")
        print(f"Code de retour : {e.returncode}")
        if capture_output:
            print(f"Sortie d'erreur : {e.stderr}")
        raise

# Configuration Git
try:
    run_command(["git", "config", "--global", "user.name", user_name])
    run_command(["git", "config", "--global", "user.email", user_email])
    print("Configuration Git définie avec succès.")
except Exception as e:
    print("Impossible de configurer Git. Vérifiez votre installation.")
    exit(1)

# Pause pour simuler le traitement
time.sleep(2)

# Créer un répertoire pour le projet si nécessaire
proj_dir = os.path.join(os.getcwd(), "farm")
if not os.path.exists(proj_dir):
    os.makedirs(proj_dir)
    print(f"Dossier '{proj_dir}' créé.")
time.sleep(1)

os.chdir(proj_dir)

# Initialisation Git si nécessaire
if not os.path.exists(".git"):
    run_command(["git", "init"])
    print("Dépôt Git initialisé.")
time.sleep(1)

# Vérifier ou basculer sur la branche 'main'
try:
    run_command(["git", "checkout", "-b", "main"])
    print("Branche 'main' créée et activée.")
except subprocess.CalledProcessError:
    run_command(["git", "checkout", "main"])
    print("Branche 'main' activée.")
time.sleep(1)

# Pull pour synchroniser la branche locale avec la branche distante
try:
    run_command(["git", "pull", "origin", "main", "--allow-unrelated-histories"])
    print("Pull réalisé avec succès.")
except subprocess.CalledProcessError:
    print("Aucun pull n'a été réalisé. La branche 'main' est probablement à jour.")

# Nombre aléatoire de commits pour la session
num_commits = random.randint(3, 25)
print(f"Nombre de commits à effectuer aujourd'hui : {num_commits}")
time.sleep(2)

# Boucle pour les commits
for _ in range(num_commits):
    try:
        # Génération d'un fichier temporaire unique
        file_name = f"Temp-{''.join(random.choices(string.ascii_lowercase + string.digits, k=10))}.txt"
        with open(file_name, "w") as f:
            f.write("Hello, World!\n")
        print(f"Fichier {file_name} créé.")
        time.sleep(1)

        # Ajout et commit
        run_command(["git", "add", file_name])
        print(f"Fichier {file_name} ajouté à l'index.")
        time.sleep(1)

        run_command(["git", "commit", "-m", f"Add {file_name}"])
        print(f"Commit effectué pour {file_name}.")
        time.sleep(1)

        # Push forcé (plus sûr avec --force-with-lease)
        run_command(["git", "push", "--force-with-lease", "-u", "origin", "main"])
        print(f"Commit {file_name} poussé avec succès.")
        time.sleep(random.randint(5, 10))  # Pause aléatoire entre les commits

    except Exception as e:
        print(f"Erreur lors de l'exécution d'un commit ou d'une commande Git : {e}")
        time.sleep(2)
        continue

print("Session de commits terminée.")
