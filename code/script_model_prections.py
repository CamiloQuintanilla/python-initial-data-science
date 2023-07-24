import pandas as pd
import pickle
from scipy.stats import poisson

dict_tables = pickle.load(open('info/dict_tables','rb'))
df_historical_data = pd.read_csv('info/transforInfo/fifa_worldcup_historical_data.csv')
df_fixture_data = pd.read_csv('info/transforInfo/fifa_worldcup_fixture.csv')

df_home = df_historical_data[['HomeTeam','HomeGoal','AwayGoal']]
df_home = df_home.rename(columns={
    'HomeTeam':'Team',
    'HomeGoal':'GoalsScored',
    'AwayGoal':'GoalsConceded'
})

df_away = df_historical_data[['AwayTeam','HomeGoal','AwayGoal']]
df_away = df_away.rename(columns={
    'AwayTeam':'Team',
    'HomeGoal':'GoalsConceded',
    'AwayGoal':'GoalsScored'
})

df_average_team = pd.concat([df_home,df_away],ignore_index=True).groupby('Team').mean()

def predict_play (team_a:str,team_b:str):
    """
    funcion que mediante la Distribución de Poisson permite calcular el posible resultado de un partido de futbol

    Args:
        team_a: (str) nombre del equipo A
        team_b: (str) nombre del equipo B
    Returns:
        (list)
        Lista con la prediccion del partido de futbol
        Example:
            (1,5) -> en este caso ganaria el team_b
    """
    if team_a in df_average_team.index and team_b in df_average_team.index:
        lambda_a= df_average_team.at[team_a,'GoalsScored'] * df_average_team.at[team_b,'GoalsConceded']
        lambda_b= df_average_team.at[team_b,'GoalsScored'] * df_average_team.at[team_a,'GoalsConceded']
        probability_a,probability_b,probability_draw = 0,0,0
        for x in range(0,11):
            for y in range (0,11):
                p = poisson.pmf(x, lambda_a) * poisson.pmf(y,lambda_b)
                if x == y:
                    probability_draw += p 
                elif x > y:
                    probability_a += p
                else:
                    probability_b +=p
        points_a = 3 * probability_a + probability_draw
        points_b = 3 * probability_b + probability_draw
        return (points_a,points_b)  
    else:
        return (0,0)


df_fixture_group_48 = df_fixture_data[:48].copy()
df_fixture_knockout = df_fixture_data[48:56].copy()
df_fixture_quartier = df_fixture_data[56:60].copy()
df_fixture_semi = df_fixture_data[60:62].copy()
df_fixture_final = df_fixture_data[62:].copy()

for group in dict_tables:
    teams_in_group = dict_tables[group]['Team'].values
    df_fixture_group_6  = df_fixture_group_48[df_fixture_group_48['home_team'].isin(teams_in_group)]
    for index, row in df_fixture_group_6.iterrows():
        home, away = row['home_team'], row['away_team']
        points_home, points_away = predict_play(home, away)
        dict_tables[group].loc[dict_tables[group]['Team'] == home, 'Pts'] += points_home
        dict_tables[group].loc[dict_tables[group]['Team'] == away, 'Pts'] += points_away

    dict_tables[group] = dict_tables[group].sort_values('Pts', ascending=False).reset_index()
    dict_tables[group] = dict_tables[group][['Team', 'Pts']]
    dict_tables[group] = dict_tables[group].round(0)

for group in dict_tables:
    group_winner = dict_tables[group].loc[0, 'Team']
    runners_up = dict_tables[group].loc[1, 'Team']

    df_fixture_knockout.replace({
        f'Winners {group}': group_winner,
        f'Runners-up {group}':runners_up
    }, inplace=True)

df_fixture_knockout['winner'] = '?'

def get_winner (df_fixture_update):
    for index, row in df_fixture_update.iterrows():
        home, away = row['home_team'], row['away_team']
        points_a, points_b = predict_play(home,away)
        if points_a > points_b:
            winner = home
        else:
            winner = away
        df_fixture_update.loc[index, 'winner'] = winner
    return df_fixture_update

df_fixture_knockout = get_winner(df_fixture_knockout)

def update_table (df_fixture_round_1,df_fixture_round_2):
    for index, row in df_fixture_round_1.iterrows():
        winner = df_fixture_round_1.loc[index, 'winner']
        match = df_fixture_round_1.loc[index, 'score']
        df_fixture_round_2.replace({f'Winners {match}':winner}, inplace=True)
    df_fixture_round_2['winner'] = '?'
    return df_fixture_round_2

update_table(df_fixture_knockout,df_fixture_quartier)
get_winner(df_fixture_quartier)

update_table(df_fixture_quartier,df_fixture_semi)
get_winner(df_fixture_semi)

update_table(df_fixture_semi,df_fixture_final)
get_winner(df_fixture_final)
print(df_fixture_final)
