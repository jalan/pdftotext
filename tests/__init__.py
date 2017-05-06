"""Shared test assets."""

import io
import pkg_resources


blank_pdf_path = pkg_resources.resource_filename("tests", "blank.pdf")
with open(blank_pdf_path, "rb") as open_file:
    blank_pdf_file = io.BytesIO(open_file.read())

abcde_pdf_path = pkg_resources.resource_filename("tests", "abcde.pdf")
with open(abcde_pdf_path, "rb") as open_file:
    abcde_pdf_file = io.BytesIO(open_file.read())
