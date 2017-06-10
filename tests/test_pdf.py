"""Tests for the PDF class."""

import io
import pkg_resources
import unittest

import pdftotext


file_names = [
    "abcde.pdf",
    "blank.pdf",
    "corrupt_page.pdf",
    "corrupt.pdf",
    "two_page.pdf",
]
test_files = {}
for file_name in file_names:
    file_path = pkg_resources.resource_filename("tests", file_name)
    with open(file_path, "rb") as open_file:
        test_files[file_name] = io.BytesIO(open_file.read())


def get_file(name):
    """Return a copy of the requested test file as if it were just opened."""
    return io.BytesIO(test_files[name].getvalue())


class InitTest(unittest.TestCase):
    """Test using and abusing __init__."""

    def test_double_init_success(self):
        pdf = pdftotext.PDF(get_file("abcde.pdf"))
        pdf.__init__(get_file("blank.pdf"))
        self.assertEqual(pdf.page_count, 1)

    def test_double_init_failure(self):
        pdf = pdftotext.PDF(get_file("blank.pdf"))
        with self.assertRaises(AttributeError):
            pdf.__init__("wrong")

    def test_init_file_in_text_mode(self):
        text_file = io.StringIO(u"wrong")
        with self.assertRaises((pdftotext.Error, TypeError)):
            pdftotext.PDF(text_file)

    def test_init_invalid_pdf_file(self):
        pdf_file = io.BytesIO(b"wrong")
        with self.assertRaises(pdftotext.Error):
            pdftotext.PDF(pdf_file)

    def test_init_corrupt_pdf_file(self):
        with self.assertRaises(pdftotext.Error):
            pdftotext.PDF(get_file("corrupt.pdf"))

    def test_no_init(self):
        class BrokenPDF(pdftotext.PDF):
            def __init__(self):
                pass
        pdf = BrokenPDF()
        self.assertEqual(pdf.page_count, 0)


class ReadTest(unittest.TestCase):
    """Test the read method."""

    def test_read(self):
        pdf = pdftotext.PDF(get_file("abcde.pdf"))
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
        pdf = pdftotext.PDF(get_file("blank.pdf"))
        with self.assertRaises(pdftotext.Error):
            pdf.read(100)

    def test_pdf_read_zero_args(self):
        pdf = pdftotext.PDF(get_file("blank.pdf"))
        with self.assertRaises(TypeError):
            pdf.read()

    def test_pdf_read_one_arg(self):
        pdf = pdftotext.PDF(get_file("blank.pdf"))
        result = pdf.read(1)
        self.assertIn("", result)

    def test_pdf_read_two_args(self):
        pdf = pdftotext.PDF(get_file("blank.pdf"))
        with self.assertRaises(TypeError):
            pdf.read(0, 1)

    def test_pdf_read_wrong_arg_type(self):
        pdf = pdftotext.PDF(get_file("blank.pdf"))
        with self.assertRaises(TypeError):
            pdf.read("wrong")

    def test_pdf_read_keyword_arg(self):
        pdf = pdftotext.PDF(get_file("blank.pdf"))
        result = pdf.read(page_number=1)
        self.assertIn("", result)

    def test_pdf_read_wrong_keyword_arg(self):
        pdf = pdftotext.PDF(get_file("blank.pdf"))
        with self.assertRaises(TypeError):
            pdf.read(wrong=0)

    def test_read_corrupt_page(self):
        with self.assertRaises(pdftotext.Error):
            pdf = pdftotext.PDF(get_file("corrupt_page.pdf"))
            pdf.read(1)

    def test_read_page_two(self):
        pdf = pdftotext.PDF(get_file("two_page.pdf"))
        result = pdf.read(2)
        self.assertIn("two", result)


class ReadAllTest(unittest.TestCase):
    """Test the read_all method."""

    def test_read_all_join(self):
        pdf = pdftotext.PDF(get_file("two_page.pdf"))
        result = pdf.read_all()
        self.assertIn("\n\n", result)

    def test_read_all_first_page(self):
        pdf = pdftotext.PDF(get_file("two_page.pdf"))
        result = pdf.read_all()
        self.assertIn("one", result)

    def test_read_all_second_page(self):
        pdf = pdftotext.PDF(get_file("two_page.pdf"))
        result = pdf.read_all()
        self.assertIn("two", result)

    def test_pdf_read_all_one_arg(self):
        pdf = pdftotext.PDF(get_file("blank.pdf"))
        with self.assertRaises(TypeError):
            pdf.read_all("wrong")


class PageCountTest(unittest.TestCase):
    """Test the page_count attribute."""

    def test_page_count_type(self):
        pdf = pdftotext.PDF(get_file("blank.pdf"))
        self.assertEqual(type(pdf.page_count), int)

    def test_page_count_one(self):
        pdf = pdftotext.PDF(get_file("blank.pdf"))
        self.assertEqual(pdf.page_count, 1)

    def test_page_count_two(self):
        pdf = pdftotext.PDF(get_file("two_page.pdf"))
        self.assertEqual(pdf.page_count, 2)


class IterationTest(unittest.TestCase):
    """Test iterating over pages."""

    def test_list_length(self):
        pdf = pdftotext.PDF(get_file("two_page.pdf"))
        result = list(pdf)
        self.assertEqual(len(result), 2)

    def test_list_first_element(self):
        pdf = pdftotext.PDF(get_file("two_page.pdf"))
        result = list(pdf)
        self.assertIn("one", result[0])

    def test_list_second_element(self):
        pdf = pdftotext.PDF(get_file("two_page.pdf"))
        result = list(pdf)
        self.assertIn("two", result[1])

    def test_stop_iteration(self):
        pdf = pdftotext.PDF(get_file("blank.pdf"))
        with self.assertRaises(StopIteration):
            next(pdf)
            next(pdf)

    def test_for_loop(self):
        pdf = pdftotext.PDF(get_file("two_page.pdf"))
        result = ""
        for page in pdf:
            result = result + page
        self.assertIn("one", result)
        self.assertIn("two", result)
