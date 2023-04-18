import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import MinMaxScaler

'''
Modify following class to develop your model
'''


class MyModel:
    '''
    Initialize the model and its parameters
    '''

    EPSILON = 4.484446606996052         # Model error
    IPL_2023_EPSILON = 8.5              # This IPL error

    def __init__(self):
        self._model = XGBRegressor()
        self.ct = ColumnTransformer(
            transformers=[('encoder', OneHotEncoder(handle_unknown='ignore', sparse=False), [1, 2, 3])],
            remainder='passthrough')
        self.mms = MinMaxScaler()


    def fit(self, training_data):

        # Preprocessing of Data
        df1 = training_data[0]
        df2 = training_data[1]
        df = pd.merge(df1, df2, on='ID')
        df.columns = [column.lower() for column in df.columns]
        df['runs'] = df.groupby(['id', 'innings'])['total_run'].cumsum()
        df.drop(columns=['id', 'innings', 'batter', 'bowler', 'non-striker', 'extra_type', 'batsman_run', 'extras_run',
                         'non_boundary', 'iswicketdelivery',
                         'player_out', 'kind', 'fielders_involved', 'city', 'matchnumber', 'tosswinner', 'tossdecision',
                         'superover', 'winningteam', 'wonby', 'margin', 'method',
                         'player_of_match', 'team1players', 'team2players', 'umpire1',
                         'umpire2', 'date', 'total_run'], inplace=True)
        df = df[df['overs'] < 6]
        df['battingteam'] = df['battingteam'].replace(
            {
                "Kings XI Punjab": "Punjab Kings",
                "Delhi Daredevils": "Delhi Capitals",
            }
        )
        df['team1'] = df['team1'].replace(
            {
                "Kings XI Punjab": "Punjab Kings",
                "Delhi Daredevils": "Delhi Capitals",
            }
        )
        df['team2'] = df['team2'].replace(
            {
                "Kings XI Punjab": "Punjab Kings",
                "Delhi Daredevils": "Delhi Capitals",
            }
        )
        team1_filter = df[df['battingteam'].isin(
            ['Deccan Chargers', 'Kochi Tuskers Kerala', 'Pune Warriors', 'Rising Pune Supergiants',
             'Rising Pune Supergiant', 'Gujarat Lions'])].index
        team2_filter = df[df['battingteam'].isin(
            ['Deccan Chargers', 'Kochi Tuskers Kerala', 'Pune Warriors', 'Rising Pune Supergiants',
             'Rising Pune Supergiant', 'Gujarat Lions'])].index
        df.drop(index=team1_filter & team2_filter, inplace=True)
        team1_filter = df[df['team1'].isin(
            ['Deccan Chargers', 'Kochi Tuskers Kerala', 'Pune Warriors', 'Rising Pune Supergiants',
             'Rising Pune Supergiant', 'Gujarat Lions'])].index
        team2_filter = df[df['team1'].isin(
            ['Deccan Chargers', 'Kochi Tuskers Kerala', 'Pune Warriors', 'Rising Pune Supergiants',
             'Rising Pune Supergiant', 'Gujarat Lions'])].index
        df.drop(index=team1_filter & team2_filter, inplace=True)
        team1_filter = df[df['team2'].isin(
            ['Deccan Chargers', 'Kochi Tuskers Kerala', 'Pune Warriors', 'Rising Pune Supergiants',
             'Rising Pune Supergiant', 'Gujarat Lions'])].index
        team2_filter = df[df['team2'].isin(
            ['Deccan Chargers', 'Kochi Tuskers Kerala', 'Pune Warriors', 'Rising Pune Supergiants',
             'Rising Pune Supergiant', 'Gujarat Lions'])].index
        df.drop(index=team1_filter & team2_filter, inplace=True)
        df = df.drop(columns=['ballnumber'])
        df = df.drop_duplicates()
        df = df.reset_index(drop=True)
        df['bowlingteam'] = df['team1']
        bowling_team_idx = df[df['battingteam'] == df['team1']].index
        df.loc[bowling_team_idx, 'bowlingteam'] = df['team2']
        df = df.drop(columns=['team1', 'team2'])
        df = df.iloc[:, [0, 1, 5, 3, 2, 4]]
        df['season'] = df['season'].replace(
            {'2020/21': 2020,
             '2009/10': 2010,
             '2007/08': 2008}
        )
        df['season'] = df['season'].astype(int)
        stadium_idx = df[df['venue'].str.contains(",")].index
        df.loc[stadium_idx, ['venue']] = df['venue'].str.split(",").str[0]

        # Model training
        X = df.iloc[:, :-1].values
        y = df.iloc[:, -1].values
        X = self.ct.fit_transform(X)
        X[:, 56:] = self.mms.fit_transform(X[:, 56:])
        y = y.reshape(-1, 1)
        self._model.fit(X, y)
        return self


    def predict(self, test_data):
        test_df = test_data
        test_df = test_df.drop(columns=['batsmen', 'bowlers', 'innings'])
        test_df['overs'] = 5
        test_df['season'] = 2023
        test_df.columns = ['venue', 'battingteam', 'bowlingteam', 'overs', 'season']
        test_df = test_df.iloc[:, [3, 1, 2, 0, 4]]
        test_df = self.ct.transform(test_df)
        test_df[:, 56:] = self.mms.transform(test_df[:, 56:])
        pred = self._model.predict(test_df)
        pred = pred + MyModel.IPL_2023_EPSILON + MyModel.EPSILON
        pred = pred.astype(int)
        return pred
