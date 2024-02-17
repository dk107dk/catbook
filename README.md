# catbook

A very simple docx file builder. Catbook was created to make managing book chapters simple. The goal was a minimal-markup way to concatenate text files into Word docs that could be converted to epub, mobi, pdf, etc.

The tool needed to:
* Allow chapters to be quickly rearranged
* Allow multi-section chapters
* Offer a trivially easy way to differentiate quotes, blocks, and special words
* Support three levels of hierarchy
* Include only the absolute minimum of markup and functionality

___

## Bookfiles

Catbook reads a flat list of text files from a .bookfile and concatenates them into a Word doc. The doc may have up to three levels. The levels are titled using Word styles.

Metadata about the files that are concatenated into the docx is available from the Book object and each section.

Bookfiles can include several things besides paths to text files.

* Comments as lines starting with #
* TITLE and AUTHOR to be shown in the book's metadata
* INCLUDE of preexisting docx
* A METADATA directive that inserts a page with a table containing the author, title, bookfile path, word count and other metadata.

For e.g.
```
#
# this is a complete bookfile
# TITLE: This is my book
# AUTHOR: John Doe
#
# INSERT: an-existing/file.docx
#
filesdir/section-1.txt
morefiles/section-2.txt
# INSERT: another/file.docx
still/morefiles/section-2.txt
#
# METADATA
#
```

___

## Text files

### Sections

Each text file that is concatenated into the docx is a "section". Sections have two parts:

- The first line
- All other lines

The first line is presented as a title, subject to the markup described below. Every other line becomes a paragraph. Catbook skips blank lines. If the first line is blank the section will have no title to distinguish it from the section before it.

### Markups

There are a very small number of markups to do things like italicize quotes, force a page break between sections, etc. Markup chars and fonts are minimally customizable using .ini files. See catbook/markup.py and catbook/fonts.py.


* Book title: ~~

A book title is the first line of a text file. The markup must be the first char. Book titles are the top grouping unit in the same way that a first-level heading in a docx is the top of a TOC. Book titles contain chapters and sections.
```
~~Book One: A New Hope
```

* Chapter title: ~

A title is the first line of a text file. The markup must be the first char. Chapter titles are a 2nd level grouping that is below a book and above section
```
~Chapter ten: In which a storm gathers
```

* Stand-alone section: >

This markup must be the first char of the first line of a text file. It forces the section to start on a new page
```
>1918: Vienna
In 1918 the empire slept...
```

* Jump: \***

A jump is on the first line of a text file. Jumps creates a break within a chapter by adding an untitled section. The section is separated from the preceding section by an indicator. As is often done, Catbook uses three widely spaced stars as the indicator. The jump is not configurable at this time.
```
***
In this section I will show that...
```

* Block: |

A block may start on any line. The markup must be the first char. Blocks are text that is set off from the rest of the paragraphs in a different font.
```
The letter said
|Dear Jack.
|I hope you've been well.

```

* Quoted line: "

A quote may start on any line. The markup must be the first char. A quote is another type of block. This markup is also useful for forcing a blank line. To make a blank line put the markup in the first char of an otherwise empty line.
```
"Hey!
Jack said. But it was quiet.

"
Eventually there was a sound.
```

* Highlighted text: |

Put pipes around any word or words to highlight them.  Assuming | is used for both highlights and blocks, if a highlight begins with the first word of a paragraph it looks like a block. In that case use a double highlight mark, as in:
```
||some highlighted words| that start a line.

There are more |highlighted words| in this line.
```

___

## Usage

For usage, see main.py and/or test/test_builder.py.

This code creates a docx file called My Book.docx in the working directory. It uses the charles.bookfile to know what text files to concatenate. The text files live in the directories below test/config/texts/charles and the bookfile refers to them relative to that path.

```
from catbook import Builder

def main():
    builder = Builder()
    builder.init()
    builder.files.OUTPUT = "./My Book.docx"
    builder.files.INPUT = "test/config/charles.bookfile"
    builder.files.FILES = "test/config/texts/charles"

    builder.build()
    print(f"words: {builder.book.metadata.word_count}")

if __name__ == "__main__":
    main()
```

The output looks like this:

<img width="75%" height="75%" src="https://raw.githubusercontent.com/catbook/cdocs/master/output.png"/>

