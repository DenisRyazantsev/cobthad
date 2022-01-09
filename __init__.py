import tkinter
from tkinter import filedialog
from aqt import mw
from aqt.qt import *
from aqt.utils import showInfo

from .HeadersFormatter.HeadersFormatter import *
from .PdfHeaderExtractor.PdfHeadersExtractor import *


def test_function() -> None:
    # Hide a tkinter window.
    root = tkinter.Tk()
    root.withdraw()

    # Request a file.
    file = filedialog.askopenfile(mode='r', filetypes=[('Pdf Files', '*.pdf')], initialdir=os.path.expanduser("~"))

    if str(file) == "None":
        return

    # Close an input stream. We need only a file name.
    file.close()

    try:
        extractor = PdfHeadersExtractor(file.name)
    except ValueError as e:
        showInfo(str(e))
        return

    if not extractor.has_headers():
        showInfo("No headers found. ¯\\_(ツ)_/¯")
        return

    headers = extractor.extract_headers()
    format_for_anki(headers, True)
    _create_hierarchical_deck(headers)

    showInfo("Deck is created.")


def _create_hierarchical_deck(headers: Node):
    # Make correct deck names.
    leaves: list[Node] = headers.leaves
    sub_deck_names = []
    for leave in leaves:
        deck_name = leave.name
        while True:
            leave_parent = leave.parent
            if leave_parent is not None:
                deck_name = leave_parent.name + "::" + deck_name
                leave = leave_parent
            else:
                sub_deck_names.append(deck_name)
                break

    # Create a root deck.
    mw.col.decks.id(headers.root.name)

    for deck_name in sub_deck_names:
        # Create a sub-deck.
        mw.col.decks.id(deck_name)


# create a new menu item, "test"
action = QAction("test", mw)
# set it to call testFunction when it's clicked
qconnect(action.triggered, test_function)
# and add it to the tools menu
mw.form.menuTools.addAction(action)
