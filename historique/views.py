from django.shortcuts import render
from .models import Historique

def historique(request):
    historiques = Historique.objects.all().order_by('-date')
    return render(request, 'historique.html',{'historiques':historiques})
# Create your views here.
