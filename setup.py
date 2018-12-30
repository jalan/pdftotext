import platform
import subprocess
from distutils.version import StrictVersion

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


def os_x_at_least_mojave():
    if platform.system() != "Darwin":
        return False

    darwin_platform_values = platform.platform().split("-")
    try:
        darwin_version_number_string = darwin_platform_values[1]
    except IndexError:
        return False
    os_x_mojave_version_string = "18.0.0"
    os_x_mojave_strict_version = StrictVersion(os_x_mojave_version_string)
    current_os_x_strict_version = StrictVersion(darwin_version_number_string)

    return current_os_x_strict_version >= os_x_mojave_strict_version


# On some BSDs, poppler is in /usr/local, which is not searched by default
if platform.system() in ["FreeBSD", "OpenBSD"] or os_x_at_least_mojave():
    include_dirs = ["/usr/local/include"]
else:
    include_dirs = None

# On OS X Mojave, poppler is in /usr/local/lib (when poppler is installed according to pdftotext's README)
if os_x_at_least_mojave():
    library_dirs = ["/usr/local/lib"]
else:
    library_dirs = None

macros = [
    ("POPPLER_CPP_AT_LEAST_0_30_0", int(poppler_cpp_at_least("0.30.0"))),
]

# On macOS, some distributions of python build extensions for 10.6 by default,
# but poppler uses C++11 features that require at least 10.9
if platform.system() == "Darwin":
    extra_compile_args = ["-Wall", "-mmacosx-version-min=10.9"]
    extra_compile_args += ["-std=c++11"] if os_x_at_least_mojave() else []
else:
    extra_compile_args = ["-Wall"]

module = Extension(
    "pdftotext",
    sources=["pdftotext.cpp"],
    libraries=["poppler-cpp"],
    library_dirs=library_dirs,
    include_dirs=include_dirs,
    define_macros=macros,
    extra_compile_args=extra_compile_args,
)

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="pdftotext",
    version="2.1.1",
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
