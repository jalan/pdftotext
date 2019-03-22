# pdftotext

[![PyPI Status](https://img.shields.io/pypi/v/pdftotext.svg)](https://pypi.python.org/pypi/pdftotext)
[![Build Status](https://travis-ci.org/jalan/pdftotext.svg?branch=master)](https://travis-ci.org/jalan/pdftotext)
[![Coverage Status](https://coveralls.io/repos/github/jalan/pdftotext/badge.svg?branch=master)](https://coveralls.io/github/jalan/pdftotext?branch=master)
[![Downloads](https://img.shields.io/pypi/dm/pdftotext.svg)](https://pypistats.org/packages/pdftotext)

Simple PDF text extraction

```python
import pdftotext

# Load your PDF
with open("lorem_ipsum.pdf", "rb") as f:
    pdf = pdftotext.PDF(f)

# If it's password-protected
with open("secure.pdf", "rb") as f:
    pdf = pdftotext.PDF(f, "secret")

# How many pages?
print(len(pdf))

# Iterate over all the pages
for page in pdf:
    print(page)

# Read some individual pages
print(pdf[0])
print(pdf[1])

# Read all the text into one string
print("\n\n".join(pdf))
```


## OS Dependencies

Debian, Ubuntu, and friends:

```
sudo apt-get update
sudo apt-get install build-essential libpoppler-cpp-dev pkg-config python-dev
```

Fedora, Red Hat, CentOS 7 and friends:

```
sudo yum install gcc-c++ pkgconfig poppler-cpp-devel python-devel redhat-rpm-config
```

CentOS 6: 

```
sudo yum install gcc-c++ pkgconfig python-devel redhat-rpm-config
```


On CentOS 6 the `libpoppler-cpp` library is not included with the system so we need to build from source. Following the instructions from [this link](https://github.com/ropensci/pdftools#building-from-source), note that recent versions of poppler require C++11 which is not available on CentOS, so we build a slightly older version of libpoppler.

    # Build dependencies
    sudo yum install wget xz libjpeg-devel openjpeg2-devel
    
    # Download and extract
    wget https://poppler.freedesktop.org/poppler-0.47.0.tar.xz
    tar -Jxvf poppler-0.47.0.tar.xz
    cd poppler-0.47.0
    
    # Build and install
    ./configure
    make
    sudo make install

By default libraries get installed in `/usr/local/lib` and `/usr/local/include`. On CentOS this is not a default search path so we need to set `PKG_CONFIG_PATH` and `LD_LIBRARY_PATH` to point R to the right directory:

    export LD_LIBRARY_PATH="/usr/local/lib"
    export PKG_CONFIG_PATH="/usr/local/lib/pkgconfig"

macOS:

```
brew install pkg-config poppler
```

Conda users may also need `libgcc`:

```
conda install libgcc
```

## Install

```
pip install pdftotext
```
