from typing import IO

from PyPDF2 import PdfFileReader
from PyPDF2.generic import Destination

from Header import Header


class PdfHeadersExtractor:
    """
    Class to extract headers from a pdf file.
    """

    _input_stream: IO = None
    _cached: bool = None
    _outlines: list = None
    _headers: list = None

    def __init__(self, file_path: str, cached: bool = True):
        self._input_stream = open(file_path, "rb")
        self._cached = cached

    def __del__(self):
        # Close input stream if it is opened
        if not self._input_stream.closed:
            self._input_stream.close()

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

    def extract_headers(self) -> list[Header]:
        # Return cached headers.
        if self._headers is not None and self._cached:
            return self._headers

        # Check headers existence.
        if not self.has_headers():
            raise ValueError("The passed file doesn't have headers!")

        # After call `has_headers` a `_outlines` must be not `None`.
        assert self._outlines is not None

        # Get headers.
        self._headers = self._convert_outlines_to_headers(0, self._outlines)

        return self._headers

    def _convert_outlines_to_headers(self, hierarchical_level: int, outlines: any) -> list[Header]:

        if type(outlines) is Destination:
            return [Header(hierarchical_level, outlines.title)]

        if type(outlines) is list:
            output = []
            for outline in outlines:
                headers = self._convert_outlines_to_headers(hierarchical_level + 1, outline)

                for header in headers:
                    output.append(header)
            return output

        assert False


extractor = PdfHeadersExtractor("test2.pdf")

if extractor.has_headers():
    extracted_headers = extractor.extract_headers()

    for header in extracted_headers:
        level_base = ['-' for i in range(header.get_level())]
        level_pointer = "".join(level_base) + ">"
        print(level_pointer + header.get_title())
else:
    print("Can't find headers.")
