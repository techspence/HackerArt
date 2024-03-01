import os
from jinja2 import Environment, FileSystemLoader

def create_directory(path):
    try:
        os.makedirs(path, exist_ok=True)
    except OSError as error:
        print(f"Creation of the directory {path} failed with error: {error}")
        return False
    return True

def write_to_file(path, content):
    try:
        with open(path, 'w') as file:
            file.write(content)
    except IOError as error:
        print(f"Writing to file {path} failed with error: {error}")
        return False
    return True

def main():
    ascii_art_dir = 'ASCII/'
    docs_dir = 'HackerArt-io/docs/'
    templates_dir = './bin/jinja2_templates'

    # Jinja2 environment
    env = Environment(loader=FileSystemLoader(templates_dir))

    # Load templates
    try:
        art_template = env.get_template('ascii_art_template.md.j2')
        index_template = env.get_template('index_template.md.j2')
    except Exception as error:
        print(f"Loading templates failed with error: {error}")
        return

    arts = []

    # Create directories if they do not exist
    if not create_directory(docs_dir) or not create_directory(os.path.join(docs_dir, 'ascii-art')):
        return

    for filename in os.listdir(ascii_art_dir):
        if filename.endswith('.txt'):
            art_path = os.path.join(ascii_art_dir, filename)
            md_filename = filename.replace('.txt', '.md')
            md_path = os.path.join(docs_dir, 'ascii-art', md_filename)

            try:
                with open(art_path, 'r') as file:
                    art_content = file.read()
            except IOError as error:
                print(f"Reading file {art_path} failed with error: {error}")
                continue

            # Render and write individual art markdown
            rendered_art = art_template.render(content=art_content)
            if not write_to_file(md_path, rendered_art):
                continue

            arts.append({'title': filename[:-4], 'filename': md_filename})

    # Render and write index markdown
    rendered_index = index_template.render(arts=arts)
    if write_to_file(os.path.join(docs_dir, 'index.md'), rendered_index):
        print("Markdown files generated successfully.")

if __name__ == "__main__":
    main()