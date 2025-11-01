import pandas as pd
import re
df = pd.read_csv("words_ipa.csv")
print(([k.split() for sub in   [list(i) for i in re.split(r' |\u2009',df['ipa'].iloc[1000])] for k in sub]))