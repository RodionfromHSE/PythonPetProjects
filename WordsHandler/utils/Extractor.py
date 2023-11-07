class Extractor:
    def extract_words_from_text(self, text):
        lines = text.split('\n')
        words = [l.strip() for l in lines if l.strip()]
        return words

    def extract_words_from_file(self, filename):
        with open(filename, encoding='utf-8') as f:
            text = f.read()
            return self.extract_words_from_text(text)


def main():
    filename = 'germanLetters.txt'
    extractor = Extractor()
    words = extractor.extract_words_from_file(filename)
    print('\n'.join(words))

if __name__ == '__main__':
    main()
