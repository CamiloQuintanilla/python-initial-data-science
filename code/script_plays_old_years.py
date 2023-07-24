import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


path = 'C:/Users/cami2/Downloads/chromedriver'
service =Service(executable_path=path)
driver = webdriver.Chrome(service=service)

driver.get('https://en.wikipedia.org/wiki/1982_FIFA_World_Cup')

matches = driver.find_elements(by='xpath', value='//th[@class="fhome"]/..')

home_team_list:list = []
score_list:list = []
away_team_list:list = []

for match in matches:
    home_team_list.append(match.find_element(by='xpath', value='./th[@class="fhome"]').text)
    score_list.append(match.find_element(by='xpath', value='./th[@class="fscore"]').text)
    away_team_list.append(match.find_element(by='xpath', value='./th[@class="faway"]').text)

dict_all_plays = {
        'home_team': home_team_list,
        'score': score_list,
        'away_team': away_team_list
    }

df_football = pd.DataFrame(dict_all_plays)
df_football['year'] = 1982
df_football.to_csv('info/originInfo/test_1982.csv', index=False)


driver.quit()