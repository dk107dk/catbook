from catbook import Builder


def main():
    builder = Builder()
    builder.init()

    print("test_output: resetting output and input!")
    builder.files.OUTPUT = "./test.docx"
    builder.files.INPUT = (
        "/Users/davidkershaw/Desktop/desktop/new/space/builds/charles.csv"
    )
    builder.files.FILES = "/Users/davidkershaw/Desktop/desktop/new/space/texts/charles"

    print(f"\n>>>>>> test_output: files are now {builder.files}")
    builder.build()


if __name__ == "__main__":
    main()
