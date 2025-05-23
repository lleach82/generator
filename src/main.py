import os
import sys
import shutil
from markdown_to_html import markdown_to_html_node, extract_title
from gencontent import generate_pages_recursive

def move_contents():
    script_dir = os.path.dirname(os.path.abspath(__file__))  # /path/to/generator/src
    src = os.path.join(script_dir, "../static")
    dest = os.path.join(script_dir, "../docs")

    src = os.path.abspath(src)
    dest = os.path.abspath(dest)

    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.mkdir(dest)

    def recursive_copy(src_path, dest_path):
        for item in os.listdir(src_path):
            src_item = os.path.join(src_path, item)
            dest_item = os.path.join(dest_path, item)
            if os.path.isdir(src_item):
                os.mkdir(dest_item)
                recursive_copy(src_item, dest_item)
            else:
                shutil.copy(src_item, dest_item)
                print(f"Copied file: {dest_item}")

    recursive_copy(src, dest)

def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    output_dir = "docs"
    move_contents()
    generate_pages_recursive("content", "template.html", output_dir, basepath)

if __name__ == "__main__":
    main()
