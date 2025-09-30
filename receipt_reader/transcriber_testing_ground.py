# we need to determine rules for the gluing of IPA symbols
import pandas as pd
import re
unique_symbols = set()

df = pd.read_csv("words_ipa.csv")

ipa_col = df["ipa"]
for count, ipa_set in enumerate(ipa_col):
    unique_symbols=unique_symbols.union(([k for sub in   [list(i) for i in re.split(r' |\u2009',ipa_set)] for k in sub]))
    if 'K' in [k for sub in   [list(i) for i in re.split(r' |\u2009',ipa_set)] for k in sub]:
        print(ipa_set, count)
print({i:symbol for i, symbol in enumerate(unique_symbols)})