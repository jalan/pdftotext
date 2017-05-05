"""Shared test assets."""

import io
import pkg_resources


test_pdf_path = pkg_resources.resource_filename("tests", "test.pdf")
with open(test_pdf_path, "rb") as open_file:
    test_pdf_file = io.BytesIO(open_file.read())
