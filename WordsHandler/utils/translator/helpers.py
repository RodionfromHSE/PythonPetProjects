from deep_translator import GoogleTranslator, YandexTranslator, DeeplTranslator
from omegaconf import OmegaConf
# each translator has methods: translate, translate_batch, translate_file

from enum import Enum
from dataclasses import dataclass
import typing as tp

class TranslatorType(Enum):
    YANDEX = "yandex"
    GOOGLE = "google"
    DEEPL = "deepl"

@dataclass
class LanguageMapper:
    src_map: tp.Dict[str, str]
    dest_map: tp.Dict[str, str]

    def map_src(self, lang: str) -> str:
        if lang not in self.src_map:
            raise ValueError(f"Unknown language: {lang}\n")
        return self.src_map[lang]
    
    def map_dest(self, lang: str) -> str:
        return self.dest_map[lang]
    
class TranslatorMapper:
    YANDEX = LanguageMapper(
        src_map={
            "ru": "ru",
            "en": "en",
            "de": "de",
        },
        dest_map={
            "ru": "ru",
            "en": "en",
            "de": "de",
        }
    )
    GOOGLE = LanguageMapper(
        src_map={
            "ru": "ru",
            "en": "en",
            "de": "de",
        },
        dest_map={
            "ru": "ru",
            "en": "en",
            "de": "de",
        }
    )
    DEEPL = LanguageMapper(
        src_map={
            "ru": "ru",
            "en": "en",
            "de": "de",
        },
        dest_map={
            "ru": "ru",
            "en": "en",
            "de": "de",
        }
    )

def get_translator(file_config: OmegaConf):
    src, dest = file_config.src, file_config.dest
    translator_type = file_config.translator
    match translator_type:
        case TranslatorType.YANDEX.value:
            return YandexTranslator(
                source=TranslatorMapper.YANDEX.map_src(src),
                target=TranslatorMapper.YANDEX.map_dest(dest),
            )
        case TranslatorType.GOOGLE.value:
            return GoogleTranslator(
                source=TranslatorMapper.GOOGLE.map_src(src),
                target=TranslatorMapper.GOOGLE.map_dest(dest),
            )
        case TranslatorType.DEEPL.value:
            return DeeplTranslator(
                source=TranslatorMapper.DEEPL.map_src(src),
                target=TranslatorMapper.DEEPL.map_dest(dest),
            )
        case _:
            raise ValueError(f"Unknown translator type: {translator_type}")
