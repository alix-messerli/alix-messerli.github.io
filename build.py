"""Génère le CV statique dans le dossier `website/` à partir des fichiers YAML de `data/`."""
import hashlib
import os
import shutil
from datetime import date

import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape

DATA_DIR = "data"
TEMPLATES_DIR = "templates"
OUTPUT_DIR = "website"
ASSETS = ["static", "assets"]


def load_data(directory=DATA_DIR):
    """Charge chaque fichier YAML ; la clé principale porte le nom du fichier."""
    data = {}
    for file in sorted(os.listdir(directory)):
        if not file.endswith((".yml", ".yaml")):
            continue
        subject = os.path.splitext(file)[0]
        with open(os.path.join(directory, file), encoding="utf-8") as f:
            content = yaml.safe_load(f) or {}
        if subject not in content:
            raise ValueError(f"{file} : la clé '{subject}' est introuvable")
        data[subject] = content[subject]
    return data


def build():
    env = Environment(
        loader=FileSystemLoader(TEMPLATES_DIR),
        autoescape=select_autoescape(["html"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    # Empreinte du CSS : force les navigateurs à recharger le style après chaque modification
    with open("static/css/styles.css", "rb") as f:
        css_version = hashlib.md5(f.read()).hexdigest()[:8]
    html = env.get_template("base.html").render(**load_data(), updated=date.today(), css_version=css_version)

    if os.path.isdir(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    for item in ASSETS:
        shutil.copytree(item, os.path.join(OUTPUT_DIR, item))
    # Empêche GitHub Pages de passer le site par Jekyll
    open(os.path.join(OUTPUT_DIR, ".nojekyll"), "w").close()
    print(f"Site généré dans '{OUTPUT_DIR}/'.")


if __name__ == "__main__":
    build()
