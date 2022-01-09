import os
from typing import Optional

from PyPDF2 import PdfFileReader
from PyPDF2.generic import Destination

from anytree import Node


class PdfHeadersExtractor:

    def __init__(self, file_path: str, cached: bool = True):
        """
        Class to extract headers from a pdf file.

        :param file_path: of a pdf file.
        :param cached: if true then a file will be read only once.
        """
        self._input_stream = open(file_path, "rb")
        self._cached = cached
        self._title: str = str(os.path.basename(file_path)).replace(".pdf", "")
        self._outlines: Optional[list] = None
        self._headers: Optional[Node] = None

    def __del__(self):
        try:
            # Close input stream if it is opened
            if not self._input_stream.closed:
                self._input_stream.close()
        except:
            pass

    def has_headers(self) -> bool:
        """
        Returns if a pdf file has headers.

        :return: if a pdf file has headers.
        """
        # Return cached condition.
        if self._outlines is not None and self._cached:
            return len(self._outlines) > 0

        # Construct a reader.
        reader = PdfFileReader(self._input_stream)

        # Set raw headers.
        self._outlines = reader.outlines

        # Close input stream if it is opened and if cached is false
        if not self._cached and not self._input_stream.closed:
            self._input_stream.close()

        return len(self._outlines) > 0

    def extract_headers(self) -> Node:
        """
        To extract headers from a pdf file.

        :return: list of headers.
        """
        # Return cached headers.
        if self._headers is not None and self._cached:
            return self._headers

        # Check headers existence.
        if not self.has_headers():
            raise ValueError("The passed file doesn't have headers!")

        # After call `has_headers` a `_outlines` must be not `None`.
        assert self._outlines is not None

        # Get headers.
        headers = self._convert_outlines_to_headers(self._outlines)

        # Root node.
        self._headers = Node(self._title)

        # Make hierarchy.
        self._headers.children = headers

        return self._headers

    def _convert_outlines_to_headers(self, outlines: any) -> list[Node]:
        output = []
        for outline in outlines:

            if type(outline) is Destination:
                output.append(Node(outline.title))
                continue

            if type(outline) is list:
                headers = self._convert_outlines_to_headers(outline)
                if len(output) > 0:
                    output[-1].children = headers
                else:
                    output.append(headers)
                continue

        return output
