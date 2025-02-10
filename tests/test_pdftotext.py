"""Tests for the pdftotext module."""

import importlib.resources
import io
import unittest

import pdftotext


test_files = {}
directory = importlib.resources.files("tests")
for f in directory.iterdir():
    if f.name.endswith(".pdf"):
        test_files[f.name] = io.BytesIO(f.read_bytes())


def get_file(name):
    """Return a copy of the requested test file as if it were just opened."""
    return io.BytesIO(test_files[name].getvalue())


class InitTest(unittest.TestCase):
    """Test using and abusing __init__."""

    def test_double_init_success(self):
        pdf = pdftotext.PDF(get_file("abcde.pdf"))
        pdf.__init__(get_file("blank.pdf"))
        self.assertEqual(len(pdf), 1)

    def test_double_init_failure(self):
        pdf = pdftotext.PDF(get_file("blank.pdf"))
        with self.assertRaises(AttributeError):
            pdf.__init__("wrong")

    def test_init_file_in_text_mode(self):
        text_file = io.StringIO("wrong")
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
        self.assertEqual(len(pdf), 0)

    def test_locked_with_only_user_password(self):
        with self.assertRaises(pdftotext.Error):
            pdftotext.PDF(get_file("user_password.pdf"))

    def test_locked_with_only_user_password_user_unlock(self):
        pdf = pdftotext.PDF(get_file("user_password.pdf"), "user_password")
        self.assertIn("secret", pdf[0])

    def test_locked_with_both_passwords(self):
        with self.assertRaises(pdftotext.Error):
            pdftotext.PDF(get_file("both_passwords.pdf"))

    def test_locked_with_both_passwords_user_unlock(self):
        pdf = pdftotext.PDF(get_file("both_passwords.pdf"), "user_password")
        self.assertIn("secret", pdf[0])

    def test_locked_with_both_passwords_owner_unlock(self):
        pdf = pdftotext.PDF(get_file("both_passwords.pdf"), "owner_password")
        self.assertIn("secret", pdf[0])


class GetItemTest(unittest.TestCase):
    """Test the __getitem__ method."""

    def test_read(self):
        pdf = pdftotext.PDF(get_file("abcde.pdf"))
        result = pdf[0]
        self.assertIn("abcde", result)

    def test_read_portrait(self):
        pdf = pdftotext.PDF(get_file("portrait.pdf"))
        result = pdf[0]
        self.assertIn("a", result)
        self.assertIn("b", result)
        self.assertIn("c", result)
        self.assertIn("d", result)

    def test_read_landscape_0(self):
        pdf = pdftotext.PDF(get_file("landscape_0.pdf"))
        result = pdf[0]
        self.assertIn("a", result)
        self.assertIn("b", result)
        self.assertIn("c", result)
        self.assertIn("d", result)

    def test_read_landscape_90(self):
        pdf = pdftotext.PDF(get_file("landscape_90.pdf"))
        result = pdf[0]
        self.assertIn("a", result)
        self.assertIn("b", result)
        self.assertIn("c", result)
        self.assertIn("d", result)

    def test_read_columns(self):
        pdf = pdftotext.PDF(get_file("three_columns.pdf"))
        page = pdf[0]
        col1_index = page.index("column 1")
        one_index = page.index("one")
        col2_index = page.index("column 2")
        two_index = page.index("two")
        col3_index = page.index("column 3")
        three_index = page.index("three")
        self.assertLess(col1_index, one_index)
        self.assertLess(one_index, col2_index)
        self.assertLess(col2_index, two_index)
        self.assertLess(two_index, col3_index)
        self.assertLess(col3_index, three_index)

    def test_no_doc_to_read(self):
        class BrokenPDF(pdftotext.PDF):
            def __init__(self):
                pass

        pdf = BrokenPDF()
        with self.assertRaises(IndexError):
            pdf[0]

    def test_pdf_read_invalid_page_number(self):
        pdf = pdftotext.PDF(get_file("blank.pdf"))
        with self.assertRaises(IndexError):
            pdf[100]

    def test_pdf_read_wrong_arg_type(self):
        pdf = pdftotext.PDF(get_file("blank.pdf"))
        with self.assertRaises(TypeError):
            pdf["wrong"]

    def test_read_corrupt_page(self):
        with self.assertRaises((pdftotext.Error, IndexError)):
            pdf = pdftotext.PDF(get_file("corrupt_page.pdf"))
            pdf[0]

    def test_read_page_two(self):
        pdf = pdftotext.PDF(get_file("two_pages.pdf"))
        result = pdf[1]
        self.assertIn("two", result)


class LengthTest(unittest.TestCase):
    """Test the __len__ method."""

    def test_length_one(self):
        pdf = pdftotext.PDF(get_file("blank.pdf"))
        self.assertEqual(len(pdf), 1)

    def test_length_two(self):
        pdf = pdftotext.PDF(get_file("two_pages.pdf"))
        self.assertEqual(len(pdf), 2)

    def test_length_no_doc(self):
        class BrokenPDF(pdftotext.PDF):
            def __init__(self):
                pass

        pdf = BrokenPDF()
        self.assertEqual(len(pdf), 0)


class ListTest(unittest.TestCase):
    """Test iterating over pages."""

    def test_list_first_element(self):
        pdf = pdftotext.PDF(get_file("two_pages.pdf"))
        self.assertIn("one", pdf[0])

    def test_list_second_element(self):
        pdf = pdftotext.PDF(get_file("two_pages.pdf"))
        self.assertIn("two", pdf[1])

    def test_list_invalid_element(self):
        pdf = pdftotext.PDF(get_file("two_pages.pdf"))
        with self.assertRaises(IndexError):
            pdf[2]

    def test_list_last_element(self):
        pdf = pdftotext.PDF(get_file("two_pages.pdf"))
        self.assertIn("two", pdf[-1])

    def test_for_loop(self):
        pdf = pdftotext.PDF(get_file("two_pages.pdf"))
        result = ""
        for page in pdf:
            result = result + page
        self.assertIn("one", result)
        self.assertIn("two", result)


class RawTest(unittest.TestCase):
    """Test reading in raw layout."""

    def test_raw_vs_not(self):
        filename = "table.pdf"
        pdf = pdftotext.PDF(get_file(filename))
        raw_pdf = pdftotext.PDF(get_file(filename), raw=True)
        self.assertNotEqual(pdf[0], raw_pdf[0])

    def test_raw_invalid_type(self):
        with self.assertRaises(TypeError):
            pdftotext.PDF(get_file("blank.pdf"), raw="")

    def test_raw_invalid_value(self):
        with self.assertRaises(ValueError):
            pdftotext.PDF(get_file("blank.pdf"), raw=100)

    def test_raw_is_not_default(self):
        filename = "table.pdf"
        pdf_default = pdftotext.PDF(get_file(filename))
        pdf_raw_false = pdftotext.PDF(get_file(filename), raw=False)
        self.assertEqual(pdf_default[0], pdf_raw_false[0])


class PhysicalTest(unittest.TestCase):
    """Test reading in physical layout."""

    def test_physical_vs_not(self):
        filename = "three_columns.pdf"
        pdf = pdftotext.PDF(get_file(filename))
        physical_pdf = pdftotext.PDF(get_file(filename), physical=True)
        self.assertNotEqual(pdf[0], physical_pdf[0])

    def test_physical_invalid_type(self):
        with self.assertRaises(TypeError):
            pdftotext.PDF(get_file("blank.pdf"), physical="")

    def test_physical_invalid_value(self):
        with self.assertRaises(ValueError):
            pdftotext.PDF(get_file("blank.pdf"), physical=-10)

    def test_physical_is_not_default(self):
        filename = "three_columns.pdf"
        pdf_default = pdftotext.PDF(get_file(filename))
        pdf_physical_false = pdftotext.PDF(get_file(filename), physical=False)
        self.assertEqual(pdf_default[0], pdf_physical_false[0])

    def test_raw_and_physical(self):
        with self.assertRaises(ValueError):
            pdftotext.PDF(get_file("blank.pdf"), raw=True, physical=True)

    def test_raw_vs_physical(self):
        filename = "three_columns.pdf"
        pdf_raw = pdftotext.PDF(get_file(filename), raw=True)
        pdf_physical = pdftotext.PDF(get_file(filename), physical=True)
        self.assertNotEqual(pdf_raw[0], pdf_physical[0])
