# book-segmentation

Code and trained models to segment the document structure of printed books and label each segment according to ten categories:

* Title page (including half titles)
* Ad card (advertisements)
* Publisher information
* Dedication
* Preface
* Table of contents
* Text
* Appendix
* Index
* N/A

Data, categorization system, and models described in more detail here:

Lara McConnaughey, Jennifer Dai and David Bamman (2017), "The Labeled Segmentation of Printed Books" (EMNLP 2017) [pdf](http://people.ischool.berkeley.edu/~dbamman/pubs/pdf/emnlp2017_book_segmentation.pdf)


This model makes use of data from Ted Underwood's [DataMunging repo](https://github.com/tedunderwood/DataMunging)

## Usage

To segment a book from the HathiTrust named `book.zip` using the default model:
`python code/segment_book.py book.zip models/labseg10/`

This should output a list of page numbers and labels for all pages in book.zip.

## Dependencies

Numpy (`pip install numpy --user`), scipy (`pip install scipy --user`) and [Tensorflow 1.0](https://www.tensorflow.org/install/)
