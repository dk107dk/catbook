from catbook import Builder


def main():
    builder = Builder()
    builder.init()
    builder.files.OUTPUT = "The Rulers Of All Things.docx"
    builder.files.INPUT = "test/config/half.bookfile"
    builder.files.FILES = "test/config/texts/half"
    builder.build()


if __name__ == "__main__":
    main()
