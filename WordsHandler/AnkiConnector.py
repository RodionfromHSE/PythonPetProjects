import json
import requests
from warnings import warn


class AnkiConnector:
    def __init__(self, url="http://localhost:8765", version=6):
        self.url = url
        self.version = version
        try:
            self.check_server()
        except Exception:
            # TODO: Make error output less verbose
            raise RuntimeError("Can't connect to Anki. Maybe you forgot to open Anki or to download the needed "
                               "extension?")

    def check_server(self):
        headers = {"Content-Type": "application/json"}
        payload = {
            "action": "ping",
            "version": self.version,
        }
        try:
            response = requests.post(self.url, data=json.dumps(payload), headers=headers)
            response.raise_for_status()
            print('AnkiConnect is running')
        except requests.exceptions.RequestException:
            raise RuntimeError('AnkiConnect is not running')

    def add_flashcard(self, deck_name, front, back):
        headers = {"Content-Type": "application/json"}
        payload = {
            "action": "addNote",
            "version": self.version,
            "params": {
                "note": {
                    "deckName": deck_name,
                    "modelName": "Basic",
                    "fields": {
                        "Front": front,
                        "Back": back
                    }
                }
            }
        }
        response = requests.post(self.url, data=json.dumps(payload), headers=headers)
        response.raise_for_status()
        result = response.json()
        if result.get("error"):
            raise Exception(result["error"])
        return result["result"]

    def create_deck(self, deck_name):
        # Connect to AnkiConnect API
        headers = {"Content-Type": "application/json"}
        payload = {
            "action": "createDeck",
            "version": self.version,
            "params": {
                "deck": deck_name
            }
        }

        # Send request to create deck
        response = requests.post(self.url, data=json.dumps(payload), headers=headers)
        response.raise_for_status()

        # Check response status and return result
        result = response.json()
        if result.get("error"):
            if result["error"] == "Deck already exists":
                print(f"Warning: Deck '{deck_name}' already exists.")
            else:
                raise Exception(result["error"])
        return result["result"]





if __name__ == '__main__':
    anki = AnkiConnector()
    anki.create_deck("German")
    try:
        anki.add_flashcard("German", 'Yes', 'Done')
        anki.add_flashcard("German", 'Yes', 'Done')
    except Exception as e:
        if str(e).strip() == "cannot create note because it is a duplicate":
            warn(f"Card duplicate")
