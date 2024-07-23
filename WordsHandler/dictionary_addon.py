from aqt.qt import QShortcut, QKeySequence, QProcess, QDesktopServices, QUrl
from aqt import mw
from aqt.utils import showInfo

def onDictionaryLookup(lang):
    if mw.state != "review":
        return
    text = mw.reviewer.web.page().selectedText()
    if text != "":
        dict_type = "english" if lang == "en" else "german-english"
        url = f"https://dictionary.cambridge.org/dictionary/{dict_type}/{text}"
        QDesktopServices.openUrl(QUrl(url))


def onDictionaryLookupEN():
    onDictionaryLookup("en")

def onDictionaryLookupDE():
    onDictionaryLookup("de")


QShortcut(QKeySequence("Ctrl+S"),
          mw, activated=onDictionaryLookupEN)
QShortcut(QKeySequence("Ctrl+D"),
          mw, activated=onDictionaryLookupDE)
