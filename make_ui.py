import os

def make_ui(source:str,dest:str):
    dest_folder = os.path.dirname(dest)
    os.makedirs(dest_folder,exist_ok=True)
    os.system(f"pyuic6 -x {source} -o {dest}")

def make_ui_whole_folder(source_dir:str,dest_dir:str):
    for filename in os.listdir(source_dir):
        name, ext = os.path.splitext(filename)
        if ext != ".ui": continue

        source_path = os.path.join(source_dir,filename)
        dest_path = os.path.join(dest_dir,name+".py")
        print(f"Processing {name}")
        make_ui(source_path,dest_path)

if __name__ == "__main__":
    SRC = "ui/forms"
    DST = "ui/forms_uic"
    
    make_ui_whole_folder(SRC,DST)