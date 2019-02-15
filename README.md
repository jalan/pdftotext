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

Fedora, Red Hat, and friends:

```
sudo yum install gcc-c++ pkgconfig poppler-cpp-devel python-devel redhat-rpm-config
```

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
