"""Tests for the PDF class."""

import io
import unittest

import pdftotext
from tests import test_pdf_file


class InitTest(unittest.TestCase):
    """Test using and abusing __init__."""

    def setUp(self):
        self.pdf_file = io.BytesIO(test_pdf_file.getvalue())
        self.another_pdf_file = io.BytesIO(test_pdf_file.getvalue())

    def test_double_init_success(self):
        pdf = pdftotext.PDF(self.pdf_file)
        pdf.__init__(self.another_pdf_file)
        self.assertEqual(pdf.page_count, 1)

    def test_double_init_failure(self):
        pdf = pdftotext.PDF(self.pdf_file)
        with self.assertRaises(AttributeError):
            pdf.__init__("wrong")

    def test_init_file_in_text_mode(self):
        text_file = io.StringIO("wrong")
        with self.assertRaises(TypeError):
            pdf = pdftotext.PDF(text_file)

    def test_init_invalid_pdf_file(self):
        pdf_file = io.BytesIO(b"wrong")
        with self.assertRaises(pdftotext.Error):
            pdf = pdftotext.PDF(pdf_file)

    def test_no_init(self):
        class BrokenPDF(pdftotext.PDF):
            def __init__(self):
                pass
        pdf = BrokenPDF()
        self.assertEqual(pdf.page_count, 0)
