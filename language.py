from multipledispatch import dispatch

class Script:
    pass
class Word:
    pass
class Phoneme:
    
    def __init__(self, ipa_symbol: str, *, stressed:bool=False):
        self.phoneme = ipa_symbol
        self.stressed = stressed
class Rule:
    # rules may apply to words, phonemes, etc.
    # we need some way of defining a context. E.g. maybe the rule only needs three words to apply, but some might need the entire text being used.
    pass

class LocalWordRule(Rule):

    def __init__(self, function):
        self.function = function

    def apply(self, word):
        return self.function(word)

class ContextWordRule(Rule):

    def __init__(self, function):
        self.function = function

    def apply(self, phrase: list[Word]):
        return self.function(phrase)

class Language:
    def __init__(self, name, phonemes, default_script=None):
        self.name = name
        self.phonemes = phonemes
        self.default_script = default_script

    def to_phonemes(self, word):
        # Map from orthography to IPA (if applicable)
        raise NotImplementedError

    def write(self, phonemes, script=None):
        match script, self.default_script:
            case None, None:
                raise ValueError("No script provided and no default script set for this language.")
            case None, _:
                script = self.default_script
            case _, _:
                script = script
        return script.render(phonemes)

class Word:
    
    def __init__(self, language: Language, phonemes: list[Phoneme]):
        self.langauge = language
        self.phonemes = phonemes
        if not self._is_valid_word():
            raise ValueError("Word contains phonemes not in language's phoneme set.")

    def _is_valid_word(self):
        for phoneme in self.phonemes:
            if phoneme not in self.langauge.phonemes:
                return False
        return True 



class Script:
    def __init__(self, name, phoneme_map, rules:list[Rule] = []):
        self.name = name
        self.phoneme_map = phoneme_map
        self.rules = rules 

    @dispatch(Script, list)
    def render(self, words):
        # we need to account for word-level rules here
        return ' '.join(self.render(word) for word in words)

    @dispatch(Script, Word)
    def render(self, word):
        # this needs changing because it may be that an indiviual phoneme is not supported, but that it is when in a small group.
        return ' '.join(self.phoneme_map.get(p,p) for p in word)

    @dispatch(Script, list)
    def apply_rules(self, phoneme):
        # apply phoneme-level rules here
        return phoneme
    
    @dispatch(Script, Word)
    def apply_rules(self, word):
        # apply word-level rules here
        return word