import sys
from os.path import dirname, join
from src import main

# Import local libs
sys.path.append(join(dirname(__file__), "libs"))

# Load the add-on
main.load()
