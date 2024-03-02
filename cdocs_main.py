from catbook import Builder


def main():
    builder = Builder()
    builder.init()

    builder.files.OUTPUT = "./A Very Long Day.docx"
    #
    # cdocs requires the bookfile to be in the cdocs
    # root. it cannot live outside the cdocs; tho, it
    # presumably could live in a different root from the
    # files -- not yet tried.
    #
    builder.files.INPUT = "cdocs:bookfiles/coda"
    #
    # cdocs don't usually start with '/', though they can.
    # if you don't start the docpath to a top level doc
    # with '/', cdocs currently doesn't allow there to be
    # an extension. in that case, either use this form:
    #
    #      builder.files.INPUT = "cdocs:coda"
    #
    # setting 'bookfile' as the file type in the cdoc root
    # config. or use this form:
    #
    #      builder.files.INPUT = "cdocs:/coda.bookfile"
    #
    # this behavior is quirky and may change in the future.
    #
    builder.files.FILES = "cdocs:test/config/texts"

    builder.disable_inline_marks_and_metadata(False)
    builder.build()
    print(f"words: {builder.book.metadata.word_count}")


if __name__ == "__main__":
    main()
