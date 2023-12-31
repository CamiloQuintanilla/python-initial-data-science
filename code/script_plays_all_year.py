from bs4 import BeautifulSoup
import requests
import pandas as pd

list_years = [1930, 1934, 1938, 1942, 1946, 1950, 1954, 1958, 1962, 1966, 1970, 1974, 1978, 1982, 1986, 1990, 1994, 1998, 2002, 2006, 2010, 2014, 2018]

def get_matches (year:str):
    
    web = f'https://en.wikipedia.org/wiki/{year}_FIFA_World_Cup'
    response = requests.get(web)
    content = response.text
    soup = BeautifulSoup(content, 'lxml')

    matches = soup.find_all('div', class_ = 'footballbox')

    home_team:list = []
    score:list = []
    away_team = []

    for  match in matches:
        home_team.append(match.find('th', class_ = 'fhome').get_text())
        score.append(match.find('th', class_ = 'fscore').get_text())
        away_team.append(match.find('th', class_ = 'faway').get_text())

    dict_all_plays = {
        'home_team': home_team,
        'score': score,
        'away_team': away_team
    }

    df_football = pd.DataFrame(dict_all_plays)
    df_football['year'] = year

    return df_football

fifa = [get_matches(year) for year in list_years]
df_fifa = pd.concat(fifa, ignore_index=True)
df_fifa.to_csv('info/originInfo/fifa_worldcup_historical_data.csv', index=False)

df_fixture = get_matches('2022')
df_fixture.to_csv('info/originInfo/fifa_worldcup_fixture.csv', index=False)