import json
import os
from warnings import warn
from pprint import pprint

from Extractor import Extractor
from translator.helpers import get_translator
from AnkiConnector import AnkiConnector



class GlobalHandler:
    def __init__(self, config):
        self.src_dir = config['src']['dir']
        self.files = config['src']['files']
        self.deck_labels = config['deckLabels']

        self.extractor = Extractor()
        self.connector = AnkiConnector()
        self.try_create_decks()

    def try_create_decks(self):
        for _, deck in self.deck_labels.items():
            try:
                self.connector.create_deck(deck)
            except Exception:
                print(f"Deck {deck!r} already exists")
                pass


    def extract_and_add(self):
        tmp_file = "tmp.txt"
        for file in self.files:
            filename = os.sep.join([self.src_dir, file['name']])
            translator = get_translator(file)
            
            src_words = self.extractor.extract_words_from_file(filename)
            if not src_words:
                warn(f"No words extracted from file '{filename}'")
                continue
            translated_text = translator.translate_file(filename)
            # print(translated_text)
            dest_words = self.extractor.extract_words_from_text(translated_text)
            # print(dest_words)

            print(f"Translated file '{filename}', extracted words: {len(dest_words)}, original words: {len(src_words)}")
            if len(dest_words) != len(src_words):
                print(f"Warning: number of words in file '{filename}' is different after translation")
                print(f"Original words: {src_words}")
                print(f"Translated words: {dest_words}")

            deck_label = self.deck_labels[file['deckLabel']]
            

            for word, translation in zip(src_words, dest_words):
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
    
    def clear(self):
        for file in self.files:
            filename = os.sep.join([self.src_dir, file['name']])
            open(filename, 'w').close()  # Clear file
