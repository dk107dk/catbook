from catbook import Builder
from os.path import exists
from os import remove


def test_init_builder():
    builder = Builder()
    builder.init()


def test_output():
    output = "test/_scratch/a.docx"
    try:
        remove(output)
    except FileNotFoundError:
        pass

    builder = Builder()
    # create the config objects so we don't have to do it here
    builder.init()
    print("test_output: resetting output and input!")
    builder.files.OUTPUT = output
    builder.files.INPUT = "test/config/empty-contents.csv"
    builder.files.FILES = "test/config/texts"
    print(f"test_output: files are now {builder.files}")
    builder.build()

    assert exists(output)
    # not cleaning up the file because maybe someone wants to check it
