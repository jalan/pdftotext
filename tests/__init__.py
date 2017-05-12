"""Shared test assets."""

import io
import pkg_resources


abcde_pdf_path = pkg_resources.resource_filename("tests", "abcde.pdf")
with open(abcde_pdf_path, "rb") as open_file:
    abcde_pdf_file = io.BytesIO(open_file.read())

blank_pdf_path = pkg_resources.resource_filename("tests", "blank.pdf")
with open(blank_pdf_path, "rb") as open_file:
    blank_pdf_file = io.BytesIO(open_file.read())

corrupt_page_path = pkg_resources.resource_filename("tests", "corrupt_page.pdf")
with open(corrupt_page_path, "rb") as open_file:
    corrupt_page_file = io.BytesIO(open_file.read())

corrupt_pdf_path = pkg_resources.resource_filename("tests", "corrupt.pdf")
with open(corrupt_pdf_path, "rb") as open_file:
    corrupt_pdf_file = io.BytesIO(open_file.read())

two_page_path = pkg_resources.resource_filename("tests", "two_page.pdf")
with open(two_page_path, "rb") as open_file:
    two_page_file = io.BytesIO(open_file.read())
