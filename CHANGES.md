# Changes

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
