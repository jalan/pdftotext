import subprocess
from setuptools import Extension
from setuptools import setup


def poppler_cpp_at_least(version):
    try:
        subprocess.check_call([
            "pkg-config",
            "--exists",
            "poppler-cpp >= {}".format(version),
        ])
    except subprocess.CalledProcessError:
        return False
    except OSError:
        print("WARNING: pkg-config not found--guessing at poppler version.")
        print("         If the build fails, install pkg-config and try again.")
    return True


macros = [
    ("POPPLER_CPP_AT_LEAST_0_30_0", int(poppler_cpp_at_least("0.30.0"))),
]

module = Extension(
    "pdftotext",
    sources=["pdftotext/pdftotext.cpp"],
    libraries=["poppler-cpp"],
    define_macros=macros,
    extra_compile_args=["-Wall"],
)

setup(
    name="pdftotext",
    version="1.0.0",
    description="Simple PDF text extraction",
    url="https://github.com/jalan/pdftotext",
    author="Jason Alan Palmer",
    author_email="jalanpalmer@gmail.com",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
    ext_modules=[module],
    test_suite="tests",
)
