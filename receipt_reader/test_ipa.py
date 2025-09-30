import pandas as pd
import re
df = pd.read_csv("words_ipa.csv")
print(([k for sub in   [list(i) for i in re.split(r' |\u2009',df['2'].iloc[1000])] for k in sub]))