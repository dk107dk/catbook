# catbook

A very simple docx file builder.

Catbook takes a list of text files in a bookfile and concationates them into a Word doc. The doc may have up to three levels. The levels are titled using Word styles.

There is a very small number of markups to do things like italicize quotes, force a page break between sections, etc. Markup chars and fonts are minimally customizable using .ini files. See catbook/markup.py and catbook/fonts.py.

Metadata about the files that are concationated as sections of the doc is available from the Book object. Bookfiles can specify title and author using directives in comment lines starting with #. Preexisting docx files may be inserted using insert directives in the bookfile.

For usage, see main.py and/or test/test_builder.py.




