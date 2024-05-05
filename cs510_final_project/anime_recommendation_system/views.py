from django.shortcuts import render
from django.http import HttpResponse
def my_view(request):
    # Logic to process the request
    
    # Render the 'my_template.html' template
    return render(request, 'home_page.html')