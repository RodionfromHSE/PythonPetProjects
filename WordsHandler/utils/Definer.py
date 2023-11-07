# import libraries to give definition of words in english

import requests
import json
import sys
import os
import time
import re
import urllib

# make function to get definition of word in english
def get_definition(word):
    # make url to get definition of word
    url = "https://api.dictionaryapi.dev/api/v2/entries/en/" + word
    # get response from url
    response = requests.get(url)
    # get json data from response
    data = json.loads(response.text)
    # print json data in beautiful format
    print(json.dumps(data, indent=4, sort_keys=True))
    # get definition of word from json data
    definition = data[0]["meanings"][0]["definitions"][0]["definition"]
    # return definition of word
    return definition

if __name__ == "__main__":
    # get word from command line argument
    words = ["hello", "world"] 
    # get definition of word
    for word in words:
        definition = get_definition(word)
        # print definition of word
        print(definition)