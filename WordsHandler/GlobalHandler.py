import json
import os
from warnings import warn

from Extractor import Extractor
from MyTranslator import MyTranslator
from AnkiConnector import AnkiConnector



class GlobalHandler:
    def __init__(self, json_file="data.json"):
        with open(json_file) as f:
            self.data = json.load(f)

        self.src_dir = self.data['src']['dir']
        self.files = self.data['src']['files']
        self.deck_labels = self.data['deckLabels']

        self.extractor = Extractor()
        self.translator = MyTranslator()
        self.connector = AnkiConnector()
        self.try_create_decks()

    def try_create_decks(self):
        for _, deck in self.deck_labels.items():
            try:
                self.connector.create_deck(deck)
            except Exception:
                pass


    def extract_and_add(self):
        for file in self.files:
            filename = os.sep.join([self.src_dir, file['name']])
            src_lang = file['src']
            dest_lang = file['dest']
            deck_label = self.deck_labels[file['deckLabel']]

            words = self.extractor.extract_words(filename)

            self.translator = MyTranslator(src_lang, dest_lang)
            translations = self.translator.translate_list(words)

            for word, translation in translations.items():
                try:
                    self.connector.add_flashcard(deck_label, word, translation)
                    self.connector.add_flashcard(deck_label, translation, word)
                except Exception as e:
                    if str(e).strip() == "cannot create note because it is a duplicate":
                        warn(f"Card duplicate {word}|{translation}")
                        continue
                    else:
                        raise e
                print(f"Added word '{word}' with translation '{translation}' to deck '{deck_label}'")
            open(filename, 'w').close()  # Clear file
