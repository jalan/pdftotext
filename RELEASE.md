This document details my release process. Maybe someday I'll automate it.

1. Commit updated versions of `CHANGES.md` and `setup.py`
2. Make sure the directory is clean: `git status` shows nothing
3. Create a new virtual environment and install twine and setuptools
4. Run `python setup.py sdist`
5. Upload to PyPI with `twine upload dist/pdftotext-X.X.X.tar.gz`
6. Tag the release on GitHub
