# catbook

Catbook is very simple docx file builder. It was created to make managing book chapters simple. Think of Catbook as a poor writer's <a href='https://www.literatureandlatte.com/scrivener'>Scrivener</a>.

The goal was to create a minimal-markup way to concatenate text files into Word docs that could then be converted to epub, mobi, pdf, etc. using a tool like <a href='https://pandoc.org/'>Pandoc</a>.

Catbook:
* Allows chapters to be quickly rearranged
* Allows multi-section chapters
* Offers a trivially easy way to differentiate quotes, blocks, and special words
* Supports three levels of hierarchy
* Includes only the absolute minimum of markup and functionality
* Looks good enough for most purposes (e.g. sharing files with editors, previewing as an ebook, etc.)
* Makes it easy to get started and equally easy to move your content to another tool

Catbook is <a href='https://pypi.org/project/catbook/'>available on Pypi</a>.
___

## Bookfiles

Catbook reads a flat list of text files from a .bookfile and concatenates them into a Word doc. Files are identified by relative paths below a root folder.

The output doc may have up to three levels. The text files being concatenated indicate their level using the markup discussed below. Level titles use first, second, and third level built-in Word header styles. Using headers supports Word's navigation pane and TOC building features.

Metadata is collected during the compile. It is available from the Book object and from each Section object.

Bookfiles include:
* Paths to text files
* Comments with optional directives

The directives are:
* TITLE to be shown in the book's metadata
* AUTHOR to be shown in the book's metadata
* One or more INSERT directives to include preexisting docx
* PAGEBREAK to put a page break between the sections before and after the comment line
* A METADATA directive that inserts a page with a table containing the author, title, bookfile path, word count and other metadata. The metadata will only be complete at the end of the compile, so the typical place for this directive is at the end of the bookfile.

For e.g.
```
#
# this is a complete bookfile with title and author metadata:
# TITLE: This is my book
# AUTHOR: John Doe
#
# Let's insert a preexisting title page Word doc:
# INSERT: an-existing/title-page.docx
# PAGEBREAK
#
filesdir/section-1.txt
morefiles/section-2.txt
#
# let's insert another file here:
# INSERT: another/file.docx
#
still/morefiles/section-3.txt
filesdir/last-section-4.txt
#
# Let's drop the book build's metadata at the end:
# METADATA
#
```

___

## Text files

### Sections

Each text file that is concatenated into the docx is a "section". Sections have two parts:

- The first line
- All other lines

The first line is presented as a title. Titles are configured using the markup described below. Every other line becomes a paragraph.

Catbook skips blank lines. If the first line is blank the section will have no title to distinguish it from the section before it. A sequence of blank lines is no different than a single blank line.

Note that while in general, blank lines are skipped and have no effect, in rare cases a blank line at the bottom of the doc may cause Word to insert a trailing blank page. This can happens when the number of non-blank lines exactly fits the page. As it is not a consistent behavior, and depends on the Word render engine, trailing blank lines should be avoided.

### Comments

Any line that begins with a # is considered a comment. Comment lines are skipped. There can be any number of comment lines before the title line; the first non-comment line is considered the title line.

Each comment will be checked for the following directives:
* INCLUDE IMAGE
* METADATA
* MARK

The INCLUDE IMAGE directive includes an image. Images are centered in a paragraph. The directive is in the form:
```
# INCLUDE IMAGE: path/to/my/image.png
```

The METADATA directive prints the section metadata collected to that point. The information Catbook inserts is clearly visible in gray text. The directive looks like:
```
# METADATA
```

The MARK directive prints a file and line number. Marks are intended for debugging the bookfile and its text files. Adding a MARK to files is useful when the bookfile has a series of files without title lines. Use the directive like:
```
# MARK
```

MARKs and METADATAs can be disabled globally using the disable_inline_marks_and_metadata method on Builder.

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

A jump is on the first line of a text file. It takes the place of a title. Jumps create a break within a chapter by adding an untitled section. The section is separated from the preceding section by an indicator called an asterism. Most commonly the asterism is three widely spaced stars. The asterism text is configurable.
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

<img width="75%" height="75%" src="https://github.com/dk107dk/catbook/raw/main/output.png"/>

___

## Cdocs

Catbook supports <a href='https://pypi.org/project/cdocs/'>Cdocs</a> as a files source. Cdocs assembles and transforms content identified by abstract paths.

The main value to Catbook users would most likely be in token substitution. This capability might be helpful if, say, you wanted to include a character's name in one or more files but were concerned that it might change. In that case, you could define a variable in a tokens.json file called ```name``` and reference it as:

```
Who am I? My name is {{name}}!
```

The tokens.json file would live beside the file it is used in or in a folder above that within the cdocs root. Every file beside that tokens.json file or in lower folders would be able to use the same ```name``` variable.

See: ```cdocs_main.py```



