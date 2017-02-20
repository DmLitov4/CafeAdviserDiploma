from django.shortcuts import render

# Create your views here.
def start_page(request):
	return render(request, 'cafe/start_page.html', {})