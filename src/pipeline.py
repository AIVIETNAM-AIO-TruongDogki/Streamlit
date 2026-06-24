import langcodes
from deep_translator import GoogleTranslator
from langdetect import DetectorFactory, LangDetectException, detect
from nltk.tokenize import TreebankWordDetokenizer, wordpunct_tokenize
from spellchecker import SpellChecker

DetectorFactory.seed = 0
MIN_INPUT_LENGTH = 3

SPELL_LANGS = {
    "en", "es", "fr", "pt", "de",
    "ru", "ar", "eu", "lv", "nl"
}

TARGET_LANGS = {
    "Vietnamese" : "vi",
    "English" : "en",
    "French" : "fr",
    "Japanese" : "ja",
    "Chinese" : "zh-CN",
    "Korean" : "ko",
    "Spanish" : "es",
    "German" : "de"
}

EXAMPLES_T = [
    "Every morning, I drink a cup of coffee.",
    "Bonjour, comment allez-vous?",
    "Xin chao, hom nay troi dep qua.",
]

EXAMPLES_S = [
"Yesturday, I recieveed a mesage from my freind.",
"Definately a great oppurtunity.",
"Je voudraiis allerr au marchee.",
]

def get_spellchecker(code):
    return SpellChecker(language=code)

def language_name(code):
    try:
        return langcodes.Language.get(code).display_name()
    except Exception:
        return code or "Unknown"
    
def detect_language(raw):
    try:
        return detect(raw)
    except LangDetectException:
        return None
    
def fix_typos(text, code):
    spell = get_spellchecker(code)
    tokens = wordpunct_tokenize(text)
    fixed = []

    for token in tokens:
        if token.isalpha() and len(token) > 1:
            suggestion = spell.correction(token.lower()) or token
            suggestion = suggestion.title() if token.istitle() else suggestion
            suggestion = suggestion.isupper() if token.isupper() else suggestion
            fixed.append(suggestion)
        else:
            fixed.append(token)
    
    return TreebankWordDetokenizer().detokenize(fixed), fixed != tokens

def run_translation(text, target_code):
    raw = text.strip()

    if len(raw) < MIN_INPUT_LENGTH:
        return  {"ok": False, "error": f"Nhập tối thiểu {MIN_INPUT_LENGTH} ký tự."}
    
    source = detect_language(raw)

    if source is None:
        return  {"ok": False, "error": f"Không nhận diện được ngôn ngữ."}
    
    if source == target_code:
        return {
            "ok" : True,
            "source" : language_name(source),
            "target" : language_name(target_code),
            "translated" : raw,
            "note" : "Câu đã ở ngôn ngữ đích, không cần dịch.",
        }

    # Using GoogleTranslator: RAW : source -> target (language)
    try:
        translated = GoogleTranslator(source=source, target=target_code).translate(raw)
    except Exception as e:
        return {"ok" : False,
                "error" : "Lỗi dịch: {e}"}
    
    return {
        "ok" : True,
        "source" : language_name(source),
        "target" : language_name(target_code),
        "translated" : translated,
    }

def run_spellcheck(text):
    raw = text.strip()

    if len(raw) < MIN_INPUT_LENGTH:
        return  {"ok": False, "error": f"Nhập tối thiểu {MIN_INPUT_LENGTH} ký tự."}
    
    code = detect_language(text)

    if code is None:
        return {"ok": False, "error": "Không nhận diện được ngôn ngữ."}
    
    if code not in SPELL_LANGS:
        return {
                "ok": False,
                "error": f"pyspellchecker chưa hỗ trợ {language_name(code)} ({code}).",
        }
    fixed, changed = fix_typos(raw, code)

    return {
        "ok" : True,
        "language": language_name(text),
        "fixed" : fixed,
        "changed" : changed,
    }