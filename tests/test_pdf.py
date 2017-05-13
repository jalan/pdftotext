"""Tests for the PDF class."""

import io
import unittest

import pdftotext
from tests import abcde_pdf_file
from tests import blank_pdf_file
from tests import corrupt_page_file
from tests import corrupt_pdf_file
from tests import two_page_file


class InitTest(unittest.TestCase):
    """Test using and abusing __init__."""

    def setUp(self):
        self.abcde_pdf_file = io.BytesIO(abcde_pdf_file.getvalue())
        self.blank_pdf_file = io.BytesIO(blank_pdf_file.getvalue())
        self.corrupt_pdf_file = io.BytesIO(corrupt_pdf_file.getvalue())

    def test_double_init_success(self):
        pdf = pdftotext.PDF(self.abcde_pdf_file)
        pdf.__init__(self.blank_pdf_file)
        self.assertEqual(pdf.page_count, 1)

    def test_double_init_failure(self):
        pdf = pdftotext.PDF(self.blank_pdf_file)
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

    def test_init_corrupt_pdf_file(self):
        with self.assertRaises(pdftotext.Error):
            pdf = pdftotext.PDF(self.corrupt_pdf_file)

    def test_no_init(self):
        class BrokenPDF(pdftotext.PDF):
            def __init__(self):
                pass
        pdf = BrokenPDF()
        self.assertEqual(pdf.page_count, 0)


class ReadTest(unittest.TestCase):
    """Test the read method."""

    def setUp(self):
        self.abcde_pdf_file = io.BytesIO(abcde_pdf_file.getvalue())
        self.blank_pdf_file = io.BytesIO(blank_pdf_file.getvalue())
        self.corrupt_page_file = io.BytesIO(corrupt_page_file.getvalue())
        self.two_page_file = io.BytesIO(two_page_file.getvalue())

    def test_read(self):
        pdf = pdftotext.PDF(self.abcde_pdf_file)
        result = pdf.read(page_number=1)
        self.assertIn("abcde", result)

    def test_no_doc_to_read(self):
        class BrokenPDF(pdftotext.PDF):
            def __init__(self):
                pass
        pdf = BrokenPDF()
        with self.assertRaises(pdftotext.Error):
            pdf.read(1)

    def test_pdf_read_invalid_page_number(self):
        pdf = pdftotext.PDF(self.blank_pdf_file)
        with self.assertRaises(pdftotext.Error):
            pdf.read(100)

    def test_pdf_read_zero_args(self):
        pdf = pdftotext.PDF(self.blank_pdf_file)
        with self.assertRaises(TypeError):
            pdf.read()

    def test_pdf_read_one_arg(self):
        pdf = pdftotext.PDF(self.blank_pdf_file)
        result = pdf.read(1)
        self.assertIn("", result)

    def test_pdf_read_two_args(self):
        pdf = pdftotext.PDF(self.blank_pdf_file)
        with self.assertRaises(TypeError):
            pdf.read(0, 1)

    def test_pdf_read_wrong_arg_type(self):
        pdf = pdftotext.PDF(self.blank_pdf_file)
        with self.assertRaises(TypeError):
            pdf.read("wrong")

    def test_pdf_read_keyword_arg(self):
        pdf = pdftotext.PDF(self.blank_pdf_file)
        result = pdf.read(page_number=1)
        self.assertIn("", result)

    def test_pdf_read_wrong_keyword_arg(self):
        pdf = pdftotext.PDF(self.blank_pdf_file)
        with self.assertRaises(TypeError):
            pdf.read(wrong=0)

    def test_read_corrupt_page(self):
        pdf = pdftotext.PDF(self.corrupt_page_file)
        with self.assertRaises(pdftotext.Error):
            pdf.read(1)

    def test_read_page_two(self):
        pdf = pdftotext.PDF(self.two_page_file)
        result = pdf.read(2)
        self.assertIn("two", result)


class ReadAllTest(unittest.TestCase):
    """Test the read_all method."""

    def setUp(self):
        self.two_page_file = io.BytesIO(two_page_file.getvalue())

    def test_read_all_first_page(self):
        pdf = pdftotext.PDF(self.two_page_file)
        result = pdf.read_all()
        self.assertIn("one", result)

    def test_read_all_second_page(self):
        pdf = pdftotext.PDF(self.two_page_file)
        result = pdf.read_all()
        self.assertIn("two", result)

    def test_pdf_read_all_one_arg(self):
        pdf = pdftotext.PDF(self.two_page_file)
        with self.assertRaises(TypeError):
            pdf.read_all("wrong")
