import pandas as pd
from mymodelfile import MyModel

if __name__ == '__main__':

    # path
    ball_by_ball_scores_file = "IPL_Ball_by_Ball_2008_2022.csv"
    match_results_file = "IPL_Matches_Result_2008_2022.csv"
    test_data_file = "input_test_file.csv"

    # model instantiate
    a_model = MyModel()

    # reading data
    ball_by_ball_scores_data = pd.read_csv(ball_by_ball_scores_file)
    match_results_data = pd.read_csv(match_results_file)
    test_data = pd.read_csv(test_data_file)

    # model fitting
    a_model.fit([ball_by_ball_scores_data, match_results_data])

    # prediction using fitted model
    predictions = a_model.predict(test_data)

    # submission file creation
    submissions_df = pd.DataFrame(data=predictions, columns=['predicted_runs'])
    submissions_df.to_csv('submission.csv', index_label='id')
