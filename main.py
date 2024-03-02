from catbook import Builder


def main():
    builder = Builder()
    builder.init()

    builder.files.OUTPUT = "./A Very Long Day.docx"
    builder.files.INPUT = "test/config/coda.bookfile"
    builder.files.FILES = "test/config/texts"

    builder.disable_inline_marks_and_metadata(False)

    builder.build()
    print(f"words: {builder.book.metadata.word_count}")


if __name__ == "__main__":
    main()
