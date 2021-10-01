# Changes

## 2.2.1 - 2021-10-01

 - Improve support for building on Apple M1 systems


## 2.2.0 - 2021-08-15

 - Change the default layout behavior to match what poppler recommends
 - Add an option to use physical layout mode, which matches the previous
   default behavior


## 2.1.6 - 2021-05-14

 - Fix an issue with detecting the bounding box on some pages


## 2.1.5 - 2020-08-14

 - Pass `-mmacosx-version-min=10.9` to the linker on macOS


## 2.1.4 - 2020-01-25

 - Pass `-std=c++11` when building on macOS


## 2.1.3 - 2020-01-06

 - Support building on Windows when using conda


## 2.1.2 - 2019-08-06

 - Improve documentation
 - Search in `/usr/local` when building on macOS


## 2.1.1 - 2018-10-07

 - For macOS, require at least version 10.9


## 2.1.0 - 2018-05-30

 - Support reading PDFs in raw layout mode


## 2.0.2 - 2018-02-19

 - Search in `/usr/local` when building on some BSDs


## 2.0.1 - 2017-08-09

 - Fix some text being missed on certain landscape pages


## 2.0.0 - 2017-07-23

 - Remove `PDF.page_count`, `PDF.read`, and `PDF.read_all`
 - Support password-protected PDFs


## 1.1.0 - 2017-07-17

 - Make `PDF` implement the sequence protocol (`__len__` and `__getitem__`)
 - Mark `PDF.page_count`, `PDF.read`, and `PDF.read_all` as deprecated in favor
   of the above
 - Handle keyboard interrupts in `PDF.read_all`


## 1.0.0 - 2017-06-10

 - Initial release
