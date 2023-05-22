import json
import os
from warnings import warn
from pprint import pprint

from Extractor import Extractor
from MyTranslator import MyTranslator
from AnkiConnector import AnkiConnector



class GlobalHandler:
    def __init__(self, json_file="data.json"):
        with open(json_file) as f:
            self.data = json.load(f)
        # pprint(self.data)

        self.src_dir = self.data['src']['dir']
        self.files = self.data['src']['files']
        self.deck_labels = self.data['deckLabels']
        # pprint(self.deck_labels)

        self.extractor = Extractor()
        self.connector = AnkiConnector()
        self.try_create_decks()

    def try_create_decks(self):
        for _, deck in self.deck_labels.items():
            try:
                self.connector.create_deck(deck)
            except Exception:
                pass


    def extract_and_add(self):
        tmp_file = "tmp.txt"
        for file in self.files:
            filename = os.sep.join([self.src_dir, file['name']])
            
            src_lang = file['src']
            dest_lang = file['dest']
            # TO-DO: Why do I init translator here? I should init it once and use it in loop
            translator = MyTranslator(src_lang, dest_lang)
            
            src_words = self.extractor.extract_words(filename)
            if not src_words:
                warn(f"No words extracted from file '{filename}'")
                continue
            translator.translate_file(filename, tmp_file)
            
            dest_words = self.extractor.extract_words(tmp_file)
            print(f"Translated file '{filename}', extracted words: {len(dest_words)}, original words: {len(src_words)}")
            if len(dest_words) != len(src_words):
                print(f"Warning: number of words in file '{filename}' is different after translation")

            deck_label = self.deck_labels[file['deckLabel']]
            
            # print(f"Extracting words from file '{filename}', src_lang='{src_lang}', dest_lang='{dest_lang}', deck_label='{deck_label}'")
            # print(f"Words: {words}")
            # print(f"Translations: {translations}")

            for word, translation in zip(src_words, dest_words):
                # print(f"Adding word '{word}' with translation '{translation}' to deck '{deck_label}'")
                try:
                    self.connector.add_flashcard(deck_label, word, translation)
                    self.connector.add_flashcard(deck_label, translation, word)
                except Exception as e:
                    if str(e).strip() == "cannot create note because it is a duplicate":
                        warn(f"Card duplicate {word}|{translation}")
                        continue
                    else:
                        print(f"Error adding card {word}|{translation}, {e}")
                        raise e
                # print(f"Added word '{word}' with translation '{translation}' to deck '{deck_label}'")
    
    def clear(self):
        for file in self.files:
            filename = os.sep.join([self.src_dir, file['name']])
            open(filename, 'w').close()  # Clear file
