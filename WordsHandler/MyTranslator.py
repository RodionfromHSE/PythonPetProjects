from googletrans import Translator
import time
import random


class MyTranslator:
    def __init__(self, src="en", dest="ru", stop_count=40, time_range=(10, 16)):
        self.translator = Translator()
        self.src = src
        self.dest = dest
        self.stop_count = stop_count
        self.time_range = time_range

    def reset_lang(self, src, dest):
        self.src = src
        self.dest = dest

    def translate(self, text):
        return self.translator.translate(text, src=self.src, dest=self.dest).text

    def translate_list(self, words):
        trans = {}
        cnt = 1
        for word in words:
            if cnt % self.stop_count == 0:
                time.sleep(random.randint(*self.time_range))
            trans[word] = self.translate(word)
            print(word, "->", trans[word])
            cnt += 1
        return trans


