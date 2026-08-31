import subprocess
import os

def clear():
    subprocess.run("cls" if os.name == "nt" else "clear", shell=True)
