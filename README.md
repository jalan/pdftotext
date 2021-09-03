# pdftotext

[![PyPI Status](https://img.shields.io/pypi/v/pdftotext.svg)](https://pypi.python.org/pypi/pdftotext)
[![Azure Status](https://dev.azure.com/jalanpalmer/jalanpalmer/_apis/build/status/jalan.pdftotext?branchName=master)](https://dev.azure.com/jalanpalmer/jalanpalmer/_build/latest?definitionId=1&branchName=master)
[![AppVeyor status](https://ci.appveyor.com/api/projects/status/uwcjxgu31kirkiuj/branch/master?svg=true)](https://ci.appveyor.com/project/jalan/pdftotext/branch/master)
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

These instructions assume you're using Python 3 on a recent OS. Package names
may differ for Python 2 or for an older OS.

### Debian, Ubuntu, and friends

```
sudo apt install build-essential libpoppler-cpp-dev pkg-config python3-dev
```

### Fedora, Red Hat, and friends

```
sudo yum install gcc-c++ pkgconfig poppler-cpp-devel python3-devel
```

### macOS

```
brew install pkg-config poppler python
```

### Windows

Currently tested only when using conda:

 - Install the Microsoft Visual C++ Build Tools
 - Install poppler through conda:
   ```
   conda install -c conda-forge poppler
   ```


## Install

```
pip install pdftotext
```
