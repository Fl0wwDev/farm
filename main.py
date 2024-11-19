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
repository_name = "farm"  # Remplacez par le nom de votre dépôt

# Définir la configuration Git
subprocess.run(["git", "config", "--global", "user.name", user_name], check=True)
subprocess.run(["git", "config", "--global", "user.email", user_email], check=True)

# Créer un répertoire pour le projet si nécessaire
proj_dir = os.path.join(os.getcwd(), "farm")
if not os.path.exists(proj_dir):
    os.makedirs(proj_dir)
os.chdir(proj_dir)

# Fonction pour générer un "salt" aléatoire
def generate_salt():
    characters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(characters) for _ in range(20))

# Détecter la branche par défaut
default_branch = "main"  # Hypothèse par défaut
try:
    result = subprocess.run(["git", "ls-remote", "--symref", f"https://github.com/{github_username}/{repository_name}.git", "HEAD"],
                            capture_output=True, text=True, check=True)
    if "refs/heads/main" in result.stdout:
        default_branch = "main"
except subprocess.CalledProcessError:
    print("Impossible de détecter la branche par défaut. Utilisation de 'main'.")

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
        subprocess.run(["git", "init"], check=True)

        # Ajouter et committer le fichier
        subprocess.run(["git", "add", file_path], check=True)
        subprocess.run(["git", "commit", "-m", f"Add {file_name}"], check=True)

        # Configurer le dépôt distant
        github_repo_url = f"https://github.com/{github_username}/{repository_name}.git"
        try:
            remote_output = subprocess.run(["git", "remote", "get-url", "origin"], capture_output=True, text=True, check=True)
            if github_repo_url not in remote_output.stdout.strip():
                subprocess.run(["git", "remote", "set-url", "origin", github_repo_url], check=True)
        except subprocess.CalledProcessError:
            subprocess.run(["git", "remote", "add", "origin", github_repo_url], check=True)

        # Pousser les changements
        subprocess.run(["git", "pull", "origin", default_branch, "--allow-unrelated-histories"], check=True)
        subprocess.run(["git", "push", "-u", "origin", default_branch], check=True)

        print(f"Commit {file_name} ajouté et poussé.")
        time.sleep(random.randint(1, 3))  # Pause entre les commits
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution de Git : {e}")

print("Session de commits terminée.")
