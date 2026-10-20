"""n° 340 THE CUBIC KNIGHT'S TOUR : un tour fermé sur les 384 cases, avec les deux conventions de saut aux coins
du cube. Une demi-minute environ."""
import subprocess, sys, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
subprocess.run([sys.executable, "cube.py", "prudent"], check=True)
subprocess.run([sys.executable, "cube.py"], check=True)
