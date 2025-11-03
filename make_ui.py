import os
import subprocess


def make_ui(source:str,dest:str):
    dest_folder = os.path.dirname(dest)
    os.makedirs(dest_folder,exist_ok=True)
    os.system(f"pyuic6 -x {source} -o {dest}")

def make_rc(source:str,dest:str):
    result = subprocess.run(
        ["rcc","-g","python",source],
        stdout=subprocess.PIPE,  
        stderr=subprocess.PIPE,  
        text=True,               
        check=False           
    )
    data = result.stdout.replace("PySide6","PyQt6")
    with open(dest,"w") as f:
        f.write(data)

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
    make_rc("resources/resources.qrc","ui/resources/resources.py")