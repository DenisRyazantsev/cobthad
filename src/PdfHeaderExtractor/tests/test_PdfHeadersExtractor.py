from unittest import TestCase
from anytree import Node
from PdfHeadersExtractor import PdfHeadersExtractor


class TestPdfHeadersExtractor(TestCase):
    _filepath_without_headers = "data/without_headers.pdf"
    _filepath_with_headers = "data/with_headers.pdf"

    # init
    def test_init_nonExistentFile_exceptionThrown(self):
        with self.assertRaises(FileNotFoundError):
            PdfHeadersExtractor("")

    # has_headers
    def test_hasHeaders_fileWithoutHeaders_false(self):
        extractor = PdfHeadersExtractor(self._filepath_without_headers)
        self.assertEqual(False, extractor.has_headers())

    def test_hasHeaders_fileWithHeaders_true(self):
        extractor = PdfHeadersExtractor(self._filepath_with_headers)
        self.assertEqual(True, extractor.has_headers())

    # extract_headers
    def test_extractHeaders_fileWithoutHeaders_exceptionThrown(self):
        extractor = PdfHeadersExtractor(self._filepath_without_headers)
        with self.assertRaises(ValueError):
            extractor.extract_headers()

    def test_extractHeaders_fileWithHeaders_AssertEquals(self):

        # Section a
        sub_paragraph_a = Node("SubParagraph AA.aa.a.a.a.a!")
        paragraph_a = Node("Paragraph AA.aa.a.a.a!", children=[sub_paragraph_a])
        sub_sub_section_a = Node("SubSubSection AA.aa.a.a!", children=[paragraph_a])
        seb_section_a = Node("SubSection AA.aa.a!", children=[sub_sub_section_a])
        section_a = Node("Section AA.aa!", children=[seb_section_a])

        # Section ab
        sub_paragraph_ab_1 = Node("SubParagraph AA.bb.a.a.a.a!")
        paragraph_ab_1 = Node("Paragraph AA.bb.a.a.a!", children=[sub_paragraph_ab_1])

        sub_paragraph_ab_2 = Node("SubParagraph AA.bb.a.a.b.a!")
        paragraph_ab_2 = Node("Paragraph AA.bb.a.a.b!", children=[sub_paragraph_ab_2])

        sub_paragraph_ab_3 = Node("SubParagraph AA.bb.a.a.c.a!")
        sub_paragraph_ab_4 = Node("SubParagraph AA.bb.a.a.c.b!")

        paragraph_ab_3 = Node("Paragraph AA.bb.a.a.c!", children=[sub_paragraph_ab_3, sub_paragraph_ab_4])
        sub_sub_section_ab = Node("SubSubSection AA.bb.a.a!", children=[paragraph_ab_1, paragraph_ab_2, paragraph_ab_3])

        sub_section_ab = Node("SubSection AA.bb.a!", children=[sub_sub_section_ab])
        section_ab = Node("Section AA.bb!", children=[sub_section_ab])

        # Chapter a
        chapter_a = Node("Chapter AA!", children=[section_a, section_ab])

        # Section b
        section_b = Node("Section BB.aa!")

        # Chapter b
        chapter_b = Node("Chapter BB!", children=[section_b])

        test_headers: Node = Node("with_headers", children=[chapter_a, chapter_b])

        extractor = PdfHeadersExtractor(self._filepath_with_headers)
        headers = extractor.extract_headers()

        self.assertEqual(test_headers.name, headers.name)
        self.assertEqual(test_headers.depth, headers.depth)
        self.assertEqual(test_headers.parent, headers.parent)

        test_descendants = test_headers.descendants
        descendants = headers.descendants

        for index in range(len(test_descendants)):
            test_header = test_descendants[index]
            header = descendants[index]

            self.assertEqual(test_header.name, header.name)
            self.assertEqual(test_header.depth, header.depth)
