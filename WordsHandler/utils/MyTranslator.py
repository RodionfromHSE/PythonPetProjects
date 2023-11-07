# from googletrans import Translator # legacy
from deepl import Translator
import time
import random
import os
from omegaconf import OmegaConf

class MyTranslator:
    def __init__(self, src, dest, auth_key, stop_count=40, time_range=(10, 16), batch_size=10):
        self.translator = Translator(auth_key=auth_key)
        self.src = src
        self.dest = dest
        self.stop_count = stop_count
        self.time_range = time_range
        self.batch_size = batch_size
        self.sep = ";;;"

    def reset_lang(self, src, dest):
        self.src = src
        self.dest = dest

    def translate(self, text):
        if not text.strip():
            raise RuntimeError("Empty String in translator")
        return self.translator.translate_text(text, source_lang=self.src, target_lang=self.dest).text

    def translate_list(self, sentences):
        trans = {}
        cnt = 1
        for sentence in sentences:
            if cnt % self.stop_count == 0:
                time.sleep(random.randint(*self.time_range))
            try:
                trans[sentence] = self.translate(sentence)
            except Exception as e:
                # TODO: add to missing sentences
                print(f"Error translating '{sentence}', skipping")
                print("Error: ", str(e))
                continue
            print(sentence, "->", trans[sentence])
            cnt += 1
        return trans
    
    def translate_file(self, infile, outfile):
        self.translator.translate_document_from_filepath(infile, outfile, source_lang=self.src, target_lang=self.dest)


if __name__ == '__main__':
    sentences = ['Wie oft saugen Sie?', 'Das ist ein Test', 'Ich bin ein Berliner', 'Der Freund von Anna betrügt sie aber sie hat Tomaten auf den Augen']
    translator = MyTranslator(src="de", dest="en-us")
    print(translator.translate_list(sentences))