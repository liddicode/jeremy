import sys
from unicodedata import category

from language import Script, Language, Rule



B = "U+A7FA"
C = "U+03E5"
CH = "U+444"
SH = "U+64"
TH = "U+1D91"
Th = "U+257"
D = "U+0271"
F = "U+211C"
G = "U+0563"
H = "U+286"
J = "U+0282"
JJ = "U+73"
L = "U+3B6"
M = "U+05E2"
N = "U+27F"
NG = "U+1D77"
P = "U+77"
R = "U+3B3"
S = "U+292"
T = "U+6D"
V = "U+21D"
W = "U+1BF"
Y = "U+028E"
Z = "U+293"
SCHWA = "U+2202"
SCHWA_W = "U+294"
EH = "U+441"
EH_Y = "U+465"
O = "U+296"
O_W = "U+295"
OH = "U+6F"
OH_Y = "U+3ED"
A = "U+19E"
A_W = "U+1AA"
AH = "U+3B4"
AH_Y = "U+490"
I = "U+44C"
I_Y = "U+3D2"
OOW = "U+3C6"
UH = "U+3C5"


# Helper: convert a codepoint string like "U+03C5" or "03C5" to the
# corresponding Python character. Returns a tuple (char, original_codepoint_str).
def codepoint_to_char(codepoint):
    if not isinstance(codepoint, str):
        raise TypeError("codepoint must be a string")
    cp = codepoint.strip().upper()
    if cp.startswith("U+"):
        cp = cp[2:]
    try:
        value = int(cp, 16)
    except ValueError:
        raise ValueError(f"Invalid codepoint string: {codepoint}")
    return chr(value), f"U+{cp.zfill(4)}"


# Build a phoneme map that stores the actual character and records the
# source codepoint string so you can always see where the character came from.
phoneme_origins = {}
phoneme_map = {}

for name, var in {
    'b': B,
    'c': C,
    'tʃ': CH,
    'ʃ': SH,
    'ð': TH,
    'θ': Th,
    'd': D,
    'f': F,
    'g': G,
    'h': H,
    'dʒ': J,
    'ʒ': JJ,
    'l': L,
    'm': M,
    'n': N,
    'ŋ': NG,
    'p': P,
    'r': R,
    's': S,
    't': T,
    'v': V,
    'w': W,
    'j': Y,
    'z': Z,
    'ə': SCHWA,
    'əw': SCHWA_W,
    'ɛ': EH,
    'ɛj': EH_Y,
    'ɔ': O,
    'ɔw': O_W,
    'o': OH,
    'oj': OH_Y,
    'a': A,
    'aw': A_W,
    'ɑ': AH,
    'ɑj': AH_Y,
    'ɪ': I,
    'ɪj': I_Y,
'ʉ': OOW,
    'ʌ': UH,
    'ː': 'DOUBLE',
}.items():
    try:
        char, origin = codepoint_to_char(var)
    except Exception:
        # Keep the original string and mark origin as unknown if parsing fails.
        char = var
        origin = None
    phoneme_map[name] = char
    phoneme_origins[name] = origin



jubrish_script = Script(name="Jubrish", phoneme_map=phoneme_map)
jubrish = Language(name="Jubrish", phonemes=[], default_script=jubrish_script)
class UnknownPhonemeError(Exception):
    pass


class Rule:

    def __init__(self, rule):
        self._function = rule

    def apply(self, word):
        return self._function(word)

class PhonemeBasedScript:

    chrs = (chr(i) for i in range(sys.maxunicode + 1))
    PUNCTUATION = set(c for c in chrs if category(c).startswith("P"))

    def __init__(self, sounds_to_glyphs_dict, rules = [], to_ignore=PUNCTUATION):
        self.sounds_to_glyphs = sounds_to_glyphs_dict
        self.on_unknown = "keep_original"
        self.to_ignore = to_ignore
        self.rules = rules

    def phoneme_to_glyph(self, phoneme):
        try:
            return self.sounds_to_glyphs[phoneme]
        except KeyError as err:
            if self.on_unknown == "keep_original":
                return phoneme
            else:
                raise UnknownPhonemeError(f"Unrecognised phoneme: {phoneme}")
            
    def collapse(self, word):
        for rule in self.rules:
            word = rule.apply(word)
        return word

    def word_to_glyph(self, word, *, collapse=True):
        word = [self.phoneme_to_glyph(phoneme) for phoneme in word]
        return self.collapse(word) if collapse else word





print(phoneme_map.values)
# --- pronunciation lookup and conversion utilities ---
import csv
import re
import unicodedata
from pathlib import Path

CSV_PRON_PATH = Path(__file__).parent / 'receipt_reader' / 'my data.csv'


def load_pron_dict(csv_path=CSV_PRON_PATH):
    """Load the pronunciation CSV into a dict mapping normalized words -> ipa string.

    The CSV's first column contains entries like "word ▶"; we strip trailing
    arrows and whitespace and normalize to lowercase for lookup.
    """
    pron = {}
    try:
        with open(csv_path, newline='', encoding='utf-8') as fh:
            reader = csv.reader(fh)
            for row in reader:
                if not row:
                    continue
                # Expect two columns: word-like and ipa
                word_raw = row[0]
                ipa = row[1] if len(row) > 1 else ''
                # strip trailing arrow marker and whitespace
                word = re.sub(r"\s*▶\s*$", '', word_raw).strip().lower()
                if word:
                    pron[word] = ipa.strip()
    except FileNotFoundError:
        # return empty dict if file missing
        return {}
    return pron


# small utility to normalize an IPA token to a base form
def normalize_ipa_token(tok):
    # decompose and remove combining marks (accents)
    s = unicodedata.normalize('NFD', tok)
    s = ''.join(ch for ch in s if unicodedata.category(ch) != 'Mn')
    # remove length markers and stress marks
    s = s.replace('ː', '').replace('ˈ', '').replace('ˌ', '').replace('ˑ', '')
    s = s.strip()
    return s


def ipa_string_to_tokens(ipa_string):
    """Split an IPA string into tokens and return list of (orig, base).

    orig is the original token from the CSV (with diacritics), base is a
    normalized form used for lookup (diacritics and stress removed). The
    conversion will prefer the normalized form when looking up in
    `phoneme_map`, but if absent will print the original token.
    """
    if not ipa_string:
        return []
    tokens = re.split(r'\s+', ipa_string.strip())
    out = []
    for tok in tokens:
        if not tok:
            continue
        base = normalize_ipa_token(tok)
        out.append((tok, base))
    return out


def phoneme_tokens_to_glyphs(tokens, phoneme_map_local=None):
    """Convert a sequence of (orig, base) tokens to glyph characters.

    Lookup order: base (normalized) -> orig (raw) -> fall back to orig string.
    Returns a concatenated string of glyphs / fallbacks.
    """
    if phoneme_map_local is None:
        phoneme_map_local = phoneme_map
    out = []
    for orig, base in tokens:
        # try normalized base first
        glyph = None
        if base in phoneme_map_local:
            glyph = phoneme_map_local[base]
        elif orig in phoneme_map_local:
            glyph = phoneme_map_local[orig]
        if glyph is not None:
            out.append(glyph)
        else:
            # missing mapping: append original IPA token so it's visible
            out.append(orig)
    return ''.join(out)


def text_to_jubrish(text, pron_dict):
    """Convert input text to Jubrish glyphs using the pron_dict and phoneme_map.

    The function tries full-text lookup first; if not found it looks up each
    whitespace-separated word individually and concatenates the resulting glyphs
    with spaces between words.
    """
    text_norm = text.strip().lower()
    # direct full-text lookup
    if text_norm in pron_dict:
        ipa = pron_dict[text_norm]
        tokens = ipa_string_to_tokens(ipa)
        return phoneme_tokens_to_glyphs(tokens)

    # otherwise split into words
    words = re.findall(r"\b[\w'’]+\b", text_norm)
    parts = []
    for w in words:
        ipa = pron_dict.get(w)
        if not ipa:
            parts.append(w)  # fallback: include the original word
            continue
    tokens = ipa_string_to_tokens(ipa)
    parts.append(phoneme_tokens_to_glyphs(tokens))
    return ' '.join(parts)


if __name__ == '__main__':
    # simple CLI: either take the rest of argv as the string or prompt the user
    import sys
    pron = load_pron_dict()
    if len(sys.argv) > 1:
        inp = ' '.join(sys.argv[1:])
    else:
        inp = input('Enter text to convert: ')
    out = text_to_jubrish(inp, pron)
    print(out)
