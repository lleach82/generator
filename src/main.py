import os
import shutil


def move_contents(src="../static", dest="../public"):
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
    move_contents()

if __name__ == "__main__":
    main()
