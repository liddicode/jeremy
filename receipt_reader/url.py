import requests
import pandas as pd
import string
def refresh_database(*,test=False):
    letters = list(string.ascii_lowercase)
    if test:
        letters = ["a", "b"]
    out_dfs = []
    for letter in letters:
        print(letter)
        url = f'http://seas3.elte.hu/cube/index.pl?s={letter}&bath=on&trick=on&goal=on&t=&syllcount=&maxout=9999999&wfreq=0-9&grammar='
        html = requests.get(url).content
        df_list = pd.read_html(html)
        #print(df_list[-1])
        out_dfs.append(df_list[-1].drop(0, axis=1))
    df = pd.concat(out_dfs).drop_duplicates(subset=1)
    df=df.astype({1:str, 2:str})
    df=df.sort_values(by=1, axis=0, key=lambda col: col.str.lower())
    df.to_csv('words_ipa.csv', index = False)   
refresh_database()