from catbook import Builder


def main():
    builder = Builder()
    builder.init()

    builder.files.OUTPUT = "./A Cold Hard Material.docx"
    builder.files.INPUT = "test/config/charles.bookfile"
    builder.files.FILES = "test/config/texts/charles"

    builder.build()
    print(f"words: {builder.book.metadata.word_count}")

    """
    count = 0
    keys = builder.book.metadata.words()
    for k in sorted(keys.keys()):
        if keys[k] > 50:
            print(f"{count}: {k} = {keys[k]}")
        count = count + 1
    """


if __name__ == "__main__":
    main()
