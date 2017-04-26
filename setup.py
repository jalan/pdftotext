from setuptools import Extension
from setuptools import setup

pdftotext_module = Extension(
    "pdftotext",
    sources=["pdftotext.cpp"],
    libraries=["poppler-cpp"],
    extra_compile_args=["-Wall"],
)

setup(
    name="pdftotext",
    ext_modules=[
        pdftotext_module,
    ],
)
