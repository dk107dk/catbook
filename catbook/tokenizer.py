from typing import List


class Tokenizer:
    @staticmethod
    def get_words(text: str) -> List[str]:
        """finds words.
        not included: numbers.
        included: hyphenated words, contractions
        """
        text = text.strip()
        text = text.lower()
        # we're lowering now, so we don't need the caps
        alpha = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        joiners = "'-"
        words = []
        word_start = 0
        pointer = -1

        def back(index):
            while index > -1 and text[index - 1] not in alpha:
                index = index - 1
            return index

        def forward(index):
            while index < len(text) - 1 and text[index] not in alpha:
                index = index + 1
            return index

        def take_a_word(f, b, call):
            # shouldn't happen. but if it does, -1 wraps.
            if b == -1:
                # print("b is -1. returning ''")
                return ""
            fw = forward(f)
            bk = back(b)
            # can happen on back-to-back special chars. if it does, -1 wraps.
            if bk == -1:
                # print("bk is -1. returning ''")
                return ""

            word = text[fw:bk]
            word = word.strip()
            if word != "":
                words.append(word)
            """
            print(f"\ncall: {call}")
            print(  f"f,b: {f},{b}")
            print(  f"fw,bk: {fw},{bk}")
            print(  f"found word: {word} ")
            print(  f"in {text}")
            """
            return word

        for c in text:
            pointer = pointer + 1
            if c == " " and pointer > word_start:
                take_a_word(word_start, pointer, 41)
                word_start = pointer + 1
            elif c in alpha:
                continue
            elif c in joiners:
                if pointer == 0:
                    continue
                elif pointer == len(text) - 1:
                    continue
                elif text[pointer - 1] in alpha and text[pointer + 1] in alpha:
                    continue
                else:
                    if pointer - 1 > word_start:
                        take_a_word(word_start, pointer, 54)
                        word_start = pointer
                    else:
                        word_start = pointer
                        continue
            else:
                continue

        if word_start < pointer:
            take_a_word(word_start, pointer + 1, 63)

        return words
