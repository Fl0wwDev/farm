import os
import subprocess
import random
import string
import time
from datetime import datetime

# Configuration statique
github_username = "Fl0wwDev"
user_name = "mahe"
user_email = "mafradin@hotmail.fr"
repository_name = "farm"  # Nom de votre dépôt

# Fonction pour exécuter une commande et gérer les erreurs
def run_command(command, check=True, capture_output=False):
    try:
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
    run_command(["git", "config", "--global", "pull.rebase", "false"])  # Force la fusion automatique par défaut
    print("Configuration Git définie avec succès.")
except Exception as e:
    print("Impossible de configurer Git. Vérifiez votre installation.")
    exit(1)

# Créer un répertoire pour le projet si nécessaire
proj_dir = os.path.join(os.getcwd(), "farm")
if not os.path.exists(proj_dir):
    os.makedirs(proj_dir)
    print(f"Dossier '{proj_dir}' créé.")
os.chdir(proj_dir)

# Fonction pour générer un "salt" aléatoire
def generate_salt():
    characters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(characters) for _ in range(20))

# Détecter la branche par défaut
default_branch = "main"  # Hypothèse par défaut
try:
    result = run_command(
        ["git", "ls-remote", "--symref", f"https://github.com/{github_username}/{repository_name}.git", "HEAD"],
        capture_output=True
    )
    if "refs/heads/main" in result.stdout:
        default_branch = "main"
    elif "refs/heads/master" in result.stdout:
        default_branch = "master"
    print(f"Branche par défaut détectée : {default_branch}")
except Exception:
    print("Impossible de détecter la branche par défaut. Utilisation de 'main'.")

# Configurer le remote si nécessaire
github_repo_url = f"git@github.com:{github_username}/{repository_name}.git"
try:
    remote_output = run_command(["git", "remote", "get-url", "origin"], capture_output=True)
    if github_repo_url not in remote_output.stdout.strip():
        run_command(["git", "remote", "set-url", "origin", github_repo_url])
except subprocess.CalledProcessError:
    run_command(["git", "remote", "add", "origin", github_repo_url])

# Configurer le suivi de branche
try:
    run_command(["git", "branch", "--set-upstream-to=origin/main", default_branch])
except subprocess.CalledProcessError:
    print("Impossible de configurer la branche distante.")

# Nombre aléatoire de commits pour la session
num_commits = random.randint(3, 25)
print(f"Nombre de commits à effectuer aujourd'hui : {num_commits}")

# Commencer les commits
for _ in range(num_commits):
    try:
        # Choisir un fichier aléatoire à créer
        file_types = {
            "dart": "void main() {\n  print('Hello world!');\n}\n",
            "cpp": "#include <iostream>\n\nint main() {\n    std::cout << 'Hello, World!' << std::endl;\n    return 0;\n}\n",
            "c": "#include <stdio.h>\n\nint main() {\n    printf('Hello, world!\\n');\n    return 0;\n}\n",
            "py": "print('Hello, world!')\n",
            "js": "console.log('Hello, world!');\n",
            "ts": "console.log('Hello, world!');\n",
            "bf": "++++++++++[>+++++++>++++++++++>+++>+<<<<-]>++.>+.+++++++..+++.>++.<<+++++++++++++.>++++.--------.++++++++++++.--------.--------.\n"
        }
        file_extension = random.choice(list(file_types.keys()))
        file_content = file_types[file_extension]

        # Générer un nom de fichier unique
        salt = generate_salt()
        file_name = f"Temp-{salt}.{file_extension}"
        file_path = os.path.join(proj_dir, file_name)

        # Créer le fichier
        with open(file_path, "w") as file:
            file.write(file_content)

        # Initialiser Git si ce n'est pas déjà fait
        run_command(["git", "init"])

        # Ajouter et committer le fichier
        run_command(["git", "add", file_path])
        run_command(["git", "commit", "-m", f"Add {file_name}"])

        # Gérer les pulls avec gestion des conflits
        try:
            run_command(["git", "pull", "origin", default_branch, "--allow-unrelated-histories"])
        except subprocess.CalledProcessError:
            print("Conflit détecté. Tentative de résolution automatique...")
            run_command(["git", "merge", "--strategy-option", "ours", "-m", "Merge unrelated histories - resolved with 'ours' strategy"])  # Résolution automatique avec un message

        # Pousser les changements
        run_command(["git", "push", "-u", "origin", default_branch])

        print(f"Commit {file_name} ajouté et poussé.")
        time.sleep(random.randint(1, 3))  # Pause entre les commits
    except Exception as e:
        print(f"Erreur lors de l'exécution d'un commit ou d'une commande Git : {e}")
        continue

print("Session de commits terminée.")
