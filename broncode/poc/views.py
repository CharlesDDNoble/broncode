from django.shortcuts import render

# Create your views here.
def thepage(request):
    return render(request, 'poc/thepage.html')