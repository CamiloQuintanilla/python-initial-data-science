import pandas as pd
import json
import pickle
from string import ascii_uppercase as abecedary

tables:list = pd.read_html('https://en.wikipedia.org/wiki/2022_FIFA_World_Cup')

dict_tables = {}

for letter,i in zip(abecedary,range(9, 59, 7)):
    df_tables = tables[i]
    df_tables.rename(columns={df_tables.columns[1]: 'Team'}, inplace=True)
    df_tables.pop('Qualification')
    dict_tables[f'Grupo {letter}'] = df_tables

with open ('info/dict_tables','wb') as output:
    pickle.dump(dict_tables, output)
# format_dict = json.dumps(dict_tables, indent=4)
# with open ('dict_tables.json','w') as output:
#     output.write(format_dict)
