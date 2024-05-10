# AnimeRex: Anime Recommender System

This project aims to curate a web application for anime enthusiasts out there which utilises an anime recommendation system that harnesses the power of machine learning to curate personalized anime selections tailored to individual preferences. By analyzing user ratings, viewing history, and metadata from thousands of anime titles, this system can predict and recommend new anime that viewers are likely to enjoy, enhancing their viewing experience and exploring new genres seamlessly.

## Getting Started

### Dependencies
- scikit-surprise
- Django
- Pandas
- Joblib

```bash
pip install -r requirements.txt
```

### Data
The data used in this project is from the Kaggle dataset [MyAnimeList Dataset](https://www.kaggle.com/azathoth42/myanimelist). Download and extract the data into the `archive` directory on the root level.

### API Key
Create a MyAnimeList account and obtain an API key from [MyAnimeList API](https://myanimelist.net/apiconfig). Create a `.env` file in the root directory and add the following line:
```bash
MYANIMELIST_CLIENT_ID=<your_client_id>
```

### Usage
```bash
cd cs510_final_project
python manage.py runserver
```

## Retrain and Replace Model


### Retrain and Evaluate the Model
In order to use a different algorithm, modify `cs510_final_project/anime_recommendation_system/api/recommend.py` and create a new method to train the model, which uses a new `algo` variable as well as a different filename for the model.

Running the following script will train the model, run the evaluation, and save the model. This script can be ran exclusive from Django.
```bash
python recommend.py
```

### Replace the Model
To replace the model, change the `model_name` parameter for the `ALGO` variable in `cs510_final_project/anime_recommendation_system/views.py`.