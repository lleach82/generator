import os
from markdown_to_html import markdown_to_html_node, extract_title

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath="/"):
    for root, _, files in os.walk(dir_path_content):
        for filename in files:
            if not filename.endswith(".md"):
                continue

            from_path = os.path.join(root, filename)
            relative_path = os.path.relpath(from_path, dir_path_content)

            # Handle 'index.md' cleanly
            if filename == "index.md":
                relative_dir = os.path.dirname(relative_path)
            else:
                relative_dir = os.path.splitext(relative_path)[0]

            dest_dir = os.path.join(dest_dir_path, relative_dir)
            dest_path = os.path.join(dest_dir, "index.html")

            generate_page(from_path, template_path, dest_path, basepath)

def generate_page(from_path, template_path, dest_path, basepath="/"):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as f:
        markdown_content = f.read()

    with open(template_path, "r") as f:
        template_content = f.read()

    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()
    title = extract_title(markdown_content)

    final_html = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_content)
    final_html = final_html.replace('href="/', f'href="{basepath}')
    final_html = final_html.replace('src="/', f'src="{basepath}')
    
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(final_html)
