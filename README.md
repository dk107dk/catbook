# catbook

A very simple docx file builder.

Catbook reads a list of text files from a "bookfile" and concatenates them into a Word doc. The doc may have up to three levels. The levels are titled using Word styles.

There is a very small number of markups to do things like italicize quotes, force a page break between sections, etc. Markup chars and fonts are minimally customizable using .ini files. See catbook/markup.py and catbook/fonts.py.

Metadata about the files that are concatenated as sections of the doc is available from the Book object. Bookfiles can specify title and author using directives in comment lines starting with #. Preexisting docx files may be inserted using insert directives in the bookfile.

For usage, see main.py and/or test/test_builder.py.

___

Catbook was created to make managing book chapters simple. The goal was to have a minimal-markup way to concatenate text files into Word docs that could be converted to epub, mobi, pdf, etc.

The concatenation tool needed to:
* Allow chapters to be quickly rearranged
* Provide ways to separate sections to create longer, multi-file chapters
* Offer a trivially easy way to differentiate quotes, blocks, and special words
* Support three levels of hierarchy
* Include only the absolute minimum of markup and functionality





