import sys
from os.path import dirname, join

# Import local libs
sys.path.append(join(dirname(__file__), "libs"))

from . import main

# Load the add-on
main.load()
