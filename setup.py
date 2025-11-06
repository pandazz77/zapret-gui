from setuptools import setup, find_packages, Command
from core.globals import VERSION

import os
import subprocess

class RCCCommand(Command):
    description = "Compile rcc"

    def initialize_options(self):
        self.source = "resources/resources.qrc"
        self.dest = "ui/resources/resources.py"

    def finalize_options(self):
        ...

    def run(self):
        RCCCommand.make_rc(self.source,self.dest)

    @staticmethod
    def make_rc(source:str,dest:str):
        """RCC"""
        print(f"Processing resource {source}")
        result = subprocess.run(
            ["pyside6-rcc","-g","python",source],
            stdout=subprocess.PIPE,  
            stderr=subprocess.PIPE,  
            text=True,               
            check=False           
        )
        data = result.stdout
        with open(dest,"w") as f:
            f.write(data)


class UICCommand(Command):
    description = 'Compile .ui files'

    def initialize_options(self):
        self.ui_dir = "ui/forms"
        self.out_dir = "ui/forms_uic"

    def finalize_options(self):
        ...

    def run(self):
        UICCommand.make_ui_whole_folder(self.ui_dir,self.out_dir)

    @staticmethod
    def make_ui(source:str,dest:str):
        """UIC"""
        dest_folder = os.path.dirname(dest)
        os.makedirs(dest_folder,exist_ok=True)
        print(f"Processing UI {source}")
        os.system(f"pyside6-uic {source} -o {dest}")

    @staticmethod
    def make_ui_whole_folder(source_dir:str,dest_dir:str):
        """UIC WHOLE FOLDER"""
        for filename in os.listdir(source_dir):
            name, ext = os.path.splitext(filename)
            if ext != ".ui": continue

            source_path = os.path.join(source_dir,filename)
            dest_path = os.path.join(dest_dir,name+".py")
            UICCommand.make_ui(source_path,dest_path)

class NuitkaCompile(Command):
    description = 'Compile with nuitka'

    def initialize_options(self):
        self.build_dir = "nuitka_build"
    
    def finalize_options(self):
        ...

    def run(self):
        os.makedirs(self.build_dir,exist_ok=True)
        os.chdir(self.build_dir)
        os.system("nuitka --onefile --windows-console-mode=disable --enable-plugin=pyside6 ../main.py -o zapret_gui.exe")

if __name__ == "__main__":
    setup(
        name='zapret_gui',
        version=VERSION,
        packages=find_packages(),
        py_modules=['main'],
        cmdclass={
            "uic":UICCommand,
            "rcc":RCCCommand,
            "nuitka": NuitkaCompile
        },
        entry_points={
            'console_scripts': [
                'zapret_gui=main:main',
            ],
        },
        install_requires=[],
        author='pandazz77',
        description='GUI for zapret'
    )