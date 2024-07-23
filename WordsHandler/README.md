# Anki Translator

> This app allows you to automize process of creation Anki decks.
> All that you need is to create list of sentences you want to learn
> and, woolya, you have this sentences translated in your Anki app


## Usage
1. Download Anki from [here](https://apps.ankiweb.net/)
2. Download Anki-connect with instruction [here](https://ankiweb.net/shared/info/2055492159)
3. Fill files with sentences and add them to data.json

## "Show in the dictionary" (for Windows users)

* Download the `1287554547` extension.
* Go to the `C:\Users\%USERNAME%\AppData\Roaming\Anki2\addons21\1287554547` directory.
* Change the init.py file to the `dictionary_addon.py` file.


## Issues

1. Deep Translators library has bug in implementation of Yandex translator `translate` method.
To fix it change return statement from `return response["text"]` to `return response["text"][0]` in file `$DIRECTORY/deep_translator/yandex.py`

You can find the needed directory by using command `pip show deep-translator`

2. While translating the files is fast, adding them to Anki is slow. I need to add some kind of progress bar and coroutines to speed up the process.

## Future features
1. Definition + example sentence for all highlighted words
I \_fell in love_ with her
 |
 |
 v
Front: I \_fell in love_ with her
Back: to fall in love with someone (влюбиться в кого-либо)

2. More user-friendly UX
