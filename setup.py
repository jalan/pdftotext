import os
import platform
import subprocess
import sys
from setuptools import Extension
from setuptools import setup

include_dirs = None
library_dirs = None


def poppler_cpp_at_least(version):
    # return True if platform is windows plus include and library dirs
    # are non-empty. pkg-config may not be avaiable in windows systems
    if platform.system() == "Windows":
        if include_dirs and library_dirs:
            return True
        else:
            print("         On windows platform, install via conda or make sure")
            print("         POPPLER_PREFIX environmental variable points to the")
            print("         folder where you've put the poppler build containing")
            print("         bin, include and library dirs. In the later case add")
            print("         %POPPLER_PREFIX%\\bin to your environmantal PATH")
            print("         variable.")
            return False
    try:
        subprocess.check_call(
            ["pkg-config", "--exists", "poppler-cpp >= {}".format(version)]
        )
    except subprocess.CalledProcessError:
        return False
    except OSError:
        print("WARNING: pkg-config not found--guessing at poppler version.")
        print("         If the build fails, install pkg-config and try again.")
    return False


# On some BSDs, poppler is in /usr/local, which is not searched by default
if platform.system() in ["Darwin", "FreeBSD", "OpenBSD"]:
    include_dirs = ["/usr/local/include"]
    library_dirs = ["/usr/local/lib"]

# On Windows, only building with conda is tested so far
if platform.system() == "Windows":
    conda_prefix = os.getenv("CONDA_PREFIX")
    poppler_prefix = os.getenv("POPPLER_PREFIX")
    if conda_prefix is not None:
        include_dirs = [os.path.join(conda_prefix, r"Library\include")]
        library_dirs = [os.path.join(conda_prefix, r"Library\lib")]
    elif poppler_prefix is not None:
        include_dirs = [os.path.join(poppler_prefix, r"include")]
        library_dirs = [os.path.join(poppler_prefix, r"lib")]


extra_compile_args = ["-Wall"]
extra_link_args = []

# On macOS, some distributions of python build extensions for 10.6 by default,
# but poppler uses C++11 features that require at least 10.9
if platform.system() == "Darwin":
    extra_compile_args += ["-mmacosx-version-min=10.9", "-std=c++11"]
    extra_link_args += ["-mmacosx-version-min=10.9"]

macros = [("POPPLER_CPP_AT_LEAST_0_30_0", int(poppler_cpp_at_least("0.30.0")))]

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
    version="2.1.5",
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
