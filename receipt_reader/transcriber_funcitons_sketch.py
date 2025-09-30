class Script:

    
    symbols_to_phonemes = {0: 'j',
                            1: 'ʉ',
                            2: 'ː',
                            3: 'ʃ',
                            4: 'ŋ', 
                            5: 'ɵ', 
                            6: 'ʤ', 
                            7: 'h', 
                            8: 'd', 
                            9: 'n', 
                            10: 'k', 
                            11: 'w', 
                            12: 's', 
                            13: 'l', 
                            14: 'ʧ', 
                            15: 'ʌ', 
                            16: 'ɪ', 
                            17: 'r', 
                            18: 'o', 
                            19: 'f', 
                            20: 'ə', 
                            21: 'ð', 
                            22: 'ʒ', 
                            23: 'v', 
                            24: 'z', 
                            25: '́', 
                            26: 'b',
                            27: 'θ',
                            28: 'ɔ', 
                            29: 'ɑ', 
                            30: 'p', 
                            31: 'g', 
                            32: 't', 
                            33: 'ɛ', 
                            34: 'm', 
                            35: 'a'}
    class Phoneme:

        def __init__(self, character):
            self.character = character

        @classmethod
        def of_ipa(character):
            return Phoneme(character)
        
class Symbol:

        def __init__(unicode_char):
            self.symbol = unicode_char


class Phoneme:

    def __init__(ipa_symbol, *, stressed=False):
        self.phoneme = ipa_symbol
        self.stressed = stressed


def next_symbol(phonemes, *, method = "max"):
    '''Return next symbol from a list of phonemes'''
    match method:
        case "max":
            count = 1
            while Phoneme.list_has_symbol(phonemes[0:count+1]):
                count+=1
            return Symbol.of_phonemes(phonemes[0:count]), phonemes[count::]
        case "min":
            return [Symbol.of_phoneme(phoneme) for phoneme in phonemes]
        case _:
            raise ValueError(f"Method {method} not recognised in next_symbol.")
    

def phonemes_to_symbols(phonemes, *, method = "max"):
    '''Return a list of symbols from a list of phonemes following a provided conversion method'''
    symbols = []
    while phonemes:
        next, phonemes = next_symbol(phonemes, method=method)
        symbols.append(next)
    return symbols



