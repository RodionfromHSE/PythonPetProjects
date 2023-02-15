from ftfy import fix_encoding as fe


class Extractor:
    def __init__(self):
        self.wrong_fix = {'Гј': 'ü', 'Гџ': 'ß', 'Гњ': 'Ü'}

    def fix_text(self, txt):  # Well... I actually didn't need this function. Guys, just use UTF-8:)
        txt = fe(txt.strip())
        for wrong, right in self.wrong_fix.items():
            txt = txt.replace(wrong, right)
        return txt

    def extract_words(self, filename):
        with open(filename, encoding='utf-8') as f:
            lines = f.readlines()
            words = [l.strip() for l in lines if l.strip()]
        return words


# Here is text format dependent code


if __name__ == '__main__':
    filename = 'germanLetters.txt'
    extractor = Extractor()
    words = extractor.extract_words(filename)
    print('\n'.join(words))
    # translator = MyTranslator('de', 'en')
    # trans = translator.translate_list(words)
    #
    # text = "\n\n".join(["\n".join([word, tran]) for word, tran in trans.items()])
    # print(text)
    # output_file = "out.txt"
    # with open(output_file, mode='a', encoding="utf-8") as f:
    #     f.write(text)
