import os
import platform
import subprocess
import sys
from setuptools import Extension
from setuptools import setup


def poppler_cpp_at_least(version):
    try:
        subprocess.check_call(
            ["pkg-config", "--exists", "poppler-cpp >= {}".format(version)]
        )
    except subprocess.CalledProcessError:
        return False
    except (FileNotFoundError, OSError):
        print("WARNING: pkg-config not found--guessing at poppler version.")
        print("         If the build fails, install pkg-config and try again.")
    return True


def brew_poppler_include():
    try:
        brew_list = subprocess.check_output(["brew", "list", "poppler"])
        try:
            brew_list = brew_list.decode()
        except (AttributeError, UnicodeDecodeError):
            pass
        include_dir = None
        library_dir = None
        for brew_file_line in brew_list.split("\n"):
            brew_file = brew_file_line.split("(")[0].strip()
            if brew_file.endswith("include/poppler/OptionalContent.h"):
                include_dir = os.path.dirname(os.path.dirname(brew_file))
            elif brew_file.endswith(".dylib"):
                library_dir = os.path.dirname(brew_file)
        return include_dir, library_dir
    except (FileNotFoundError, OSError, subprocess.CalledProcessError):
        return None, None


include_dirs = None
library_dirs = None

# On some BSDs, poppler is in /usr/local, which is not searched by default
if platform.system() in ["Darwin", "FreeBSD", "OpenBSD"]:
    include_dirs = ["/usr/local/include"]
    library_dirs = ["/usr/local/lib"]

# On Windows, only building with conda is tested so far
if platform.system() == "Windows":
    conda_prefix = os.getenv("CONDA_PREFIX")
    if conda_prefix is not None:
        include_dirs = [os.path.join(conda_prefix, r"Library\include")]
        library_dirs = [os.path.join(conda_prefix, r"Library\lib")]

extra_compile_args = ["-Wall"]
extra_link_args = []

# On macOS, some distributions of python build extensions for 10.6 by default,
# but poppler uses C++11 features that require at least 10.9
if platform.system() == "Darwin":
    extra_compile_args += ["-mmacosx-version-min=10.9", "-std=c++11"]
    extra_link_args += ["-mmacosx-version-min=10.9"]
    brew_include, brew_library = brew_poppler_include()
    if brew_include is not None:
        include_dirs.append(brew_include)
    if brew_library is not None:
        library_dirs.append(brew_library)

macros = [
    ("POPPLER_CPP_AT_LEAST_0_30_0", int(poppler_cpp_at_least("0.30.0"))),
    ("POPPLER_CPP_AT_LEAST_0_58_0", int(poppler_cpp_at_least("0.58.0"))),
    ("POPPLER_CPP_AT_LEAST_0_88_0", int(poppler_cpp_at_least("0.88.0"))),
]

module = Extension(
    "pdftotext",
    sources=["pdftotext.cpp"],
    libraries=["poppler-cpp"],
    include_dirs=include_dirs,
    library_dirs=library_dirs,
    define_macros=macros,
    extra_compile_args=extra_compile_args,
    extra_link_args=extra_link_args,
)

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="pdftotext",
    version="2.2.2",
    author="Jason Alan Palmer",
    author_email="jalanpalmer@gmail.com",
    description="Simple PDF text extraction",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jalan/pdftotext",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
    ext_modules=[module],
    test_suite="tests",
)
