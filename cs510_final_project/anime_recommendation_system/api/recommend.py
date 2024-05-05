import pandas as pd
from surprise import BaselineOnly, Dataset, Reader, SVD, accuracy
from surprise.model_selection import cross_validate
import joblib
import random
import numpy as np
from collections import defaultdict

def set_seed(seed):
    random.seed(seed)
    np.random.seed(seed)

def read_data(nrows=None):
    user_ratings = pd.read_csv('../../../archive/animelists_cleaned.csv', nrows=nrows)

    # Only consider shows that user has completed
    user_ratings = user_ratings[user_ratings["my_status"] == 2]

    # Filter out columns that are not needed
    user_ratings = user_ratings[["username", "anime_id", "my_score"]]

    print(user_ratings)

    reader = Reader(rating_scale=(1, 10))
    data = Dataset.load_from_df(user_ratings, reader)
    return data


def train_model(trainset, load=True):
    # cross_validate(BaselineOnly(), data, verbose=True)
    filename = 'model.joblib'
    if load == True:
        algo = joblib.load(f'{filename}.gz')
        return algo

    algo = SVD()
    algo.fit(trainset)

    joblib.dump(algo, f'{filename}.gz', compress=('gzip', 3))
    return algo

def test_model(trainset, algo):
    testset = trainset.build_testset()
    predictions = algo.test(testset)
    # RMSE should be low as we are biased
    accuracy.rmse(predictions, verbose=True)  # ~ 0.68 (which is low)

    return predictions

def predict_user_recommendations(user_anime_list, algo):
    # Predict the ratings for the user
    predictions = []
    for _, row in user_anime_list.iterrows():
        uid = row["username"]
        iid = row["anime_id"]
        pred = algo.predict(uid, iid)
        predictions.append(pred)

    return predictions

# From Surprise Docs
def get_top_n(predictions, n=10):
    """Return the top-N recommendation for each user from a set of predictions.

    Args:
        predictions(list of Prediction objects): The list of predictions, as
            returned by the test method of an algorithm.
        n(int): The number of recommendation to output for each user. Default
            is 10.

    Returns:
    A dict where keys are user (raw) ids and values are lists of tuples:
        [(raw item id, rating estimation), ...] of size n.
    """

    # First map the predictions to each user.
    top_n = defaultdict(list)
    for uid, iid, true_r, est, _ in predictions:
        top_n[uid].append((iid, est))

    # Then sort the predictions for each user and retrieve the k highest ones.
    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[uid] = user_ratings[:n]

    return top_n



if __name__ == "__main__":
    LOAD = True
    set_seed(0)

    data = read_data(nrows=1000)
    trainset = data.build_full_trainset()

    algo = train_model(trainset, load=LOAD)
    predictions = test_model(trainset, algo)
    top_n =  get_top_n(predictions)
    # Print the recommended items for each user
    for uid, user_ratings in top_n.items():
        print(uid, [iid for (iid, _) in user_ratings])

    from api import get_user_anime_list

    username = 'Damonashu'
    user_anime_list = get_user_anime_list(username)
    print(user_anime_list)

    predictions = predict_user_recommendations(user_anime_list, algo)
    top_n =  get_top_n(predictions)
    # Print the recommended items for each user
    for uid, user_ratings in top_n.items():
        print(uid, [iid for (iid, _) in user_ratings])
