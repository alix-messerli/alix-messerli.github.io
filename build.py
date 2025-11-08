import yaml
import os
import shutil
from jinja2 import Environment, FileSystemLoader

def remove_extension(filename):
    name, _ = os.path.splitext(filename)
    return name

def getInformations(directory="data"):
    data = {}
    for file in os.listdir(directory):
        if file.endswith(".yml") or file.endswith(".yaml"):
            subject = remove_extension(file)
            with open(os.path.join(directory, file), 'r', encoding="utf-8") as f:
                content = yaml.safe_load(f)
            if isinstance(content, dict) and subject in content:
                data[subject] = content[subject]
    return data

def copy_file_or_directory(src, dest):
    if os.path.isdir(src):
        dest_dir = os.path.join(dest, os.path.basename(src))
        shutil.copytree(src, dest_dir, dirs_exist_ok=True)
    elif os.path.isfile(src):
        shutil.copy2(src, dest)

def generate_site(data_dir="data", output_dir="website", addtional_lang=""):
    
    if addtional_lang:
        data_dir = os.path.join(data_dir, addtional_lang)
        output_dir = os.path.join(output_dir, addtional_lang)
        templates_dir = os.path.join('templates', addtional_lang)
        if not os.path.isdir(templates_dir):
            templates_dir = 'templates'
    else:
        templates_dir = 'templates'

    env = Environment(loader=FileSystemLoader(templates_dir))

    base_template = env.get_template('base.html')
    cv_section = env.get_template('cv.html')
    cv_portfolio = env.get_template('portfolio.html')

    data = getInformations(data_dir)

    # Render sub-sections
    cv_content = cv_section.render(data)
    portfolio_content = cv_portfolio.render(data)

    output = base_template.render(data, cv_content=cv_content, portfolio_content=portfolio_content)

    os.makedirs(output_dir, exist_ok=True)

    output_file_path = os.path.join(output_dir, 'index.html')
    with open(output_file_path, 'w', encoding="utf-8") as file:
        file.write(output)

    print(f"Site generated successfully in '{output_dir}'.")



# Automatically generate sites for each language subdirectory in data_dir

def generate_all_sites(data_dir="data", output_dir="website"):
    # Generate the default site (no additional language)
    generate_site(data_dir=data_dir, output_dir=output_dir, addtional_lang="")
    # Copy static assets
    files_to_copy = ['static', 'assets', 'CNAME']
    for item in files_to_copy:
        copy_file_or_directory(item, "website")

    # List all subdirectories in data_dir (excluding files)
    for entry in os.listdir(data_dir):
        sub_path = os.path.join(data_dir, entry)
        if os.path.isdir(sub_path):
            generate_site(data_dir=data_dir, output_dir=output_dir, addtional_lang=entry)



# Call the function to generate all sites
generate_all_sites()