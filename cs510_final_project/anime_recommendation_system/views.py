from django.shortcuts import render
from django.http import HttpResponse
from anime_recommendation_system.api.api import generate_html_table
from anime_recommendation_system.api.api import get_anime_data
from anime_recommendation_system.api.api import get_user_anime_list
from django.views.decorators.csrf import ensure_csrf_cookie
@ensure_csrf_cookie
def my_view(request):
    # Logic to process the request
    
    # Render the 'my_template.html' template
    return render(request, 'home_page.html')

def search(request):
    if request.method == 'POST':
        query = request.POST.get('query', '')
        anime_list = get_user_anime_list(query)
        print(anime_list)
        anime_data_list = get_anime_data()  # Fetch anime data
        if anime_data_list:
            html_table = generate_html_table(anime_data_list)  # Generate HTML table
            return render(request, 'results.html', {'html_table': html_table})  # Render template with HTML table
   
    return render(request, 'home_page.html')