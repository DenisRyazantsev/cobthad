# import the main window object (mw) from aqt

from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo, qconnect
# import all of the Qt GUI library
from aqt.qt import *


# We're going to add a menu item below. First we want to create a function to
# be called when the menu item is activated.
from desk_creator import create_desk


def testFunction() -> None:
    create_desk()


# create a new menu item, "test"
action = QAction("test", mw)
# set it to call testFunction when it's clicked
qconnect(action.triggered, testFunction)
# and add it to the tools menu
mw.form.menuTools.addAction(action)
