from setuptools import Extension
from setuptools import setup

module = Extension(
    "pdftotext",
    sources=["pdftotext/pdftotext.cpp"],
    libraries=["poppler-cpp"],
    extra_compile_args=["-Wall"],
)

setup(
    name="pdftotext",
    ext_modules=[module],
)
