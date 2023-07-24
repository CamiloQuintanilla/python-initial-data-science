import pandas as pd

df_historic_data=pd.read_csv('info/originInfo/fifa_worldcup_historical_data.csv')
df_fixture_data=pd.read_csv('info/originInfo/fifa_worldcup_fixture.csv')


df_fixture_data['home_team']=df_fixture_data['home_team'].str.strip()
df_fixture_data['away_team']=df_fixture_data['away_team'].str.strip()

df_historic_data.drop_duplicates(inplace=True)
df_historic_data.sort_values('year', inplace=True)

index_to_elimine = df_historic_data[df_historic_data['home_team'].str.contains('Sweden') & df_historic_data['away_team'].str.contains('Austria')].index

df_historic_data.drop(index=index_to_elimine, inplace=True)
df_historic_data['score'] = df_historic_data['score'].str.replace('[^\d–]','', regex=True)
df_historic_data['home_team']=df_historic_data['home_team'].str.strip()
df_historic_data['away_team']=df_historic_data['away_team'].str.strip()

df_historic_data[['HomeGoal','AwayGoal']] = df_historic_data['score'].str.split('–', expand=True)
df_historic_data.drop('score', axis=1, inplace=True)

df_historic_data.rename(columns={'home_team':'HomeTeam','score':'Score','away_team':'AwayTeam','year':'Year'}, inplace=True)

df_historic_data=df_historic_data.astype({
    'HomeGoal':int,
    'AwayGoal':int,
    'Year':int
})

df_historic_data['TotalGoals'] = df_historic_data['HomeGoal'] + df_historic_data['AwayGoal']

df_historic_data.to_csv('info/transforInfo/fifa_worldcup_historical_data.csv', index=False)
df_fixture_data.to_csv('info/transforInfo/fifa_worldcup_fixture.csv', index=False)

