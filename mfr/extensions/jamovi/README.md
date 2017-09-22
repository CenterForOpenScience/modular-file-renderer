
# jamovi .omv file renderer

`.omv` is the native file format for the free and open source [jamovi statistical spreadsheet](https://www.jamovi.org). an `.omv` file is a 'compound' file format, containing data, analyses and results.

`.omv` files created by recent versions of jamovi, contain an `index.html` file which represents the results of the analyses performed. the jamovi `.omv` file renderer extracts the contents of `index.html` from the archive, and replaces image paths from the archive with equivalent data URIs. This, then serves as the rendered content.
