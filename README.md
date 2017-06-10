# pdftotext

Simple PDF text extraction

```python
import pdftotext

with open("lorem_ipsum.pdf", "rb") as f:
    pdf = pdftotext.PDF(f)

# Iterate over all the pages
for page in pdf:
    print(page)

# Just read the second page
print(pdf.read(2))

# Or read all the text at once
print(pdf.read_all())
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


## Install

```
pip install pdftotext
```
