import pandas as pd
from surprise import BaselineOnly, Dataset, Reader, SVD, accuracy
from surprise import KNNBasic
from surprise.model_selection import cross_validate
from surprise import CoClustering
import joblib
import random
import numpy as np
from collections import defaultdict
import os
from sklearn.cluster import KMeans

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


def train_model(trainset, load=True, filedir="", model_name="model"):
    # cross_validate(BaselineOnly(), data, verbose=True)
    filename = f'{model_name}.joblib'
    filepath = os.path.join(filedir, filename)
    if load == True:
        algo = joblib.load(f'{filepath}.gz')
        return algo

    algo = SVD()
    algo.fit(trainset)

    joblib.dump(algo, f'{filepath}.gz', compress=('gzip', 3))
    return algo
def train_knn_model(trainset, load=True):
    # Specify the filename for saving the model
    filename = 'knn_model3m.joblib'
    
    try:
        algo = joblib.load(f'{filename}.gz')
    except EOFError as e:
        print(f"Error loading file: {e}")

    # Train the k-NN model
    algo = KNNBasic()
    algo.fit(trainset)

    # Save the trained model
    joblib.dump(algo, f'{filename}.gz', compress=('gzip', 3))
    
    return algo


def train_coclustering(trainset, load=True):
    # Specify the filename for saving the model
    filename = 'coclustering3m.joblib'
    
    try:
        algo = joblib.load(f'{filename}.gz')
    except EOFError as e:
        print(f"Error loading file: {e}")

    # Train the k-NN model
    algo = CoClustering()
    algo.fit(trainset)

    # Save the trained model
    joblib.dump(algo, f'{filename}.gz', compress=('gzip', 3))
    return algo
def train_knn_model(trainset, load=True):
    # Specify the filename for saving the model
    filename = 'knn_model300k.joblib'
    
    try:
        algo = joblib.load(f'{filename}.gz')
    except EOFError as e:
        print(f"Error loading file: {e}")

    # Train the k-NN model
    algo = KNNBasic()
    algo.fit(trainset)

    # Save the trained model
    joblib.dump(algo, f'{filename}.gz', compress=('gzip', 3))
    
    return algo


def train_coclustering(trainset, load=True):
    # Specify the filename for saving the model
    filename = 'coclustering3m.joblib'
    
    try:
        algo = joblib.load(f'{filename}.gz')
    except EOFError as e:
        print(f"Error loading file: {e}")

    # Train the k-NN model
    algo = CoClustering()
    algo.fit(trainset)

    # Save the trained model
    joblib.dump(algo, f'{filename}.gz', compress=('gzip', 3))
    return algo



def test_model(trainset, algo):
    testset = trainset.build_anti_testset()
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

def get_top_n_recommendations(predictions, n=10):
    # Sort the predictions by estimated ratings and return the top N
    predictions.sort(key=lambda x: x.est, reverse=True)
    return predictions[:n]

def get_all_anime_ids(filepath='../../../archive/anime_cleaned.csv'):
    anime_data = pd.read_csv(filepath)
    return set(anime_data['anime_id'])

def filter_unwatched_anime(all_anime_ids, user_anime_list):
    # Get all anime id's for any status in user_anime_list that is not "plan_to_watch"
    excluded_anime_ids = user_anime_list[user_anime_list["status"] != "plan_to_watch"]["anime_id"]

    return set(all_anime_ids - set(excluded_anime_ids))

def predict_ratings_for_unwatched(user, unwatched_anime_ids, algo):
    predictions = [algo.predict(user, anime_id) for anime_id in unwatched_anime_ids]
    return predictions


if __name__ == "__main__":

    LOAD = True
    set_seed(0)

    data = read_data(nrows=300000)
    trainset = data.build_full_trainset()
    # del data
    # algo = train_model(trainset, load=LOAD)
    algo2 = train_knn_model(trainset)
    predictions = test_model(trainset, algo2)
    top_n =  get_top_n(predictions)
    # Print the recommended items for each user
    # for uid, user_ratings in top_n.items():
    #     print(uid, [iid for (iid, _) in user_ratings])


    # ids = get_all_anime_ids()

    # from api import get_user_anime_list, get_anime_data

    # username = 'Damonashu'
    # user_anime_list = get_user_anime_list(username)

    # unwatched_anime_ids = filter_unwatched_anime(ids, user_anime_list)
    # predictions = predict_ratings_for_unwatched(username, unwatched_anime_ids, algo)

    # top_recommendations = get_top_n_recommendations(predictions)

    # for pred in top_recommendations:
    #     anime_data = get_anime_data(pred.iid)
    #     # print(anime_data)
    #     # print(f"Anime : {pred.iid}, Estimated Rating: {pred.est}")
    #     # print("\n\n")
    # # print([(pred.iid, pred.est) for pred in top_recommendations])

    

    # # predictions = predict_user_recommendations(user_anime_list, algo)
    # # top_n =  get_top_n(predictions)
    # # # Print the recommended items for each user
    # # for uid, user_ratings in top_n.items():
    # #     print(uid, [iid for (iid, _) in user_ratings])


