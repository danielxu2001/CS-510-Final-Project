from django.shortcuts import render
from django.http import HttpResponse
from anime_recommendation_system.api.api import generate_html_table
from anime_recommendation_system.api.api import get_anime_data
from anime_recommendation_system.api.api import get_user_anime_list
from django.views.decorators.csrf import ensure_csrf_cookie
from anime_recommendation_system.api.recommend import predict_ratings_for_unwatched, get_top_n_recommendations, filter_unwatched_anime, get_all_anime_ids, train_model
import pandas as pd

ALL_IDS = get_all_anime_ids(filepath='../archive/anime_cleaned.csv')
ALGO = train_model(trainset=None, load=True, filedir='anime_recommendation_system/api/', model_name='model_svd_300k')

@ensure_csrf_cookie
def my_view(request):
    # Logic to process the request
    
    # Render the 'my_template.html' template
    return render(request, 'home_page.html')

def search(request):
    if request.method == 'POST':
        query = request.POST.get('query', '')
        user_anime_list = get_user_anime_list(query)

        unwatched_anime_ids = filter_unwatched_anime(ALL_IDS, user_anime_list)
        predictions = predict_ratings_for_unwatched(query, unwatched_anime_ids, ALGO)

        top_recommendations = get_top_n_recommendations(predictions, n=25)

        anime_data_list = []
        for pred in top_recommendations:
            anime_id = pred.iid
            est = pred.est

            # print(f"Anime : {anime_id}, Estimated Rating: {est}")
            anime_data = get_anime_data(anime_id)  # Fetch anime data
            anime_data['estimated_rating'] = est 
            
            anime_data_list.append(anime_data)
        
        anime_data_df = pd.DataFrame(anime_data_list)
        
        html_table = generate_html_table(anime_data_df)  # Generate HTML table
        return render(request, 'results.html', {'html_table': html_table})  # Render template with HTML table
   
    return render(request, 'home_page.html')