from aqt import mw
from aqt.qt import *
from aqt.utils import showInfo

from .HeadersFormatter.HeadersFormatter import *
from .PdfHeaderExtractor.PdfHeadersExtractor import *
from PyQt5 import QtCore, QtWidgets

def convert_pdf_file_to_deck() -> None:

    # Request a file.
    file, _ = QtWidgets.QFileDialog.getOpenFileName(
        QtWidgets.QMainWindow(),
        "Pdf Files",
        QtCore.QDir.homePath(),
        "Pdf Files (*.pdf)"
    )

    if not file:
        return

    try:
        extractor = PdfHeadersExtractor(file)
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


def load():
    # Create a new menu item.
    action = QAction("Convert a PDF file to a hierarchical deck", mw)
    # Set it to call convert_pdf_file_to_deck when it's clicked.
    qconnect(action.triggered, convert_pdf_file_to_deck)
    # And add it to the tools menu.
    mw.form.menuTools.addAction(action)
