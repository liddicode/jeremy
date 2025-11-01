class Script:

    
    symbols_to_phonemes = {"Y": 'j',
                            "OOW": 'ʉ',
                            "DOUBLE": 'ː',
                            "SH": 'ʃ',
                            "NG": 'ŋ', 
                            "Th": 'ɵ', 
                            "J": 'ʤ', 
                            "H": 'h', 
                            "D": 'd', 
                            "N": 'n', 
                            "C": 'k', 
                            "W": 'w', 
                            "S": 's', 
                            "L": 'l', 
                            "CH": 'ʧ', 
                            "UH": 'ʌ', 
                            "I": 'ɪ', 
                            "R": 'r', 
                            "O": 'o', 
                            "F": 'f', 
                            "SCHWA": 'ə', 
                            "TH" : 'ð', 
                            "JJ": 'ʒ', 
                            "V" : 'v', 
                            "Z" : 'z', 
                            "STRESS": '́', 
                            "B" : 'b',
                            "Th" : 'θ',
                            "O" : 'ɔ', 
                            "AH" : 'ɑ', 
                            "P": 'p', 
                            "G":  'g', 
                            "T":  't', 
                            "EH" : 'ɛ', 
                            "M" : 'm', 
                            "A": 'a'}
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

    def __init__(self, ipa_symbol, *, stressed=False):
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

