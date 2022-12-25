from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from .models import Frappe, Review
from .forms import ReviewForm
from django.contrib.auth.decorators import   login_required

#def home(request):
#   searchTerm = request.GET.get('searchFrappe')
 #   if searchTerm:
 #       frappes =Frappe.objects.filter(title__icontains=searchTerm)
 #   else:
  #      frappes = Frappe.objects.all()
   # 
    #return render(request, 'home.html',{'searchTerm':searchTerm, 'frappes': frappes})


def home(request):
    searchTerm = request.GET.get('searchFrappe')    
    if searchTerm:
        frappes = Frappe.objects.filter(title__icontains=searchTerm)    
    else:        
        frappes = Frappe.objects.all()    
    return render(request, 'home.html',      {'searchTerm':searchTerm, 'frappes': frappes})

def about(request):
    return HttpResponse('<h1>Welcome to About Page</h1>')

def detail(request, frappe_id):
    frappe = get_object_or_404(Frappe,pk=frappe_id)
    reviews = Review.objects.filter(frappe = frappe)
    return render(request,'detail.html',{'frappe':frappe, 'reviews': reviews})


#def signup(request):    
    email = request.GET.get('email')    
    return render(request, 'signup.html', {'email':email})

@login_required
def createreview(request, frappe_id):    
    frappe = get_object_or_404(Frappe,pk=frappe_id)
    if request.method == 'GET':        
        return render(request, 'createreview.html',{'form':ReviewForm(), 'frappe':frappe})    
    else:        
        try:
            form = ReviewForm(request.POST)
            newReview = form.save(commit=False) 
            newReview.user = request.user
            newReview.frappe = frappe
            newReview.save()            
            return redirect('detail', newReview.frappe.id)
        except ValueError:            
            return render(request,'createreview.html',{'form':ReviewForm(),'error':'bad data passed in'})

@login_required
def updatereview(request, review_id):    
    review = get_object_or_404(Review,pk=review_id,user=request.user)    
    if request.method == 'GET':        
        form = ReviewForm(instance=review)        
        return render(request, 'updatereview.html', {'review': review,'form':form})    
    else:        
        try: 
            form = ReviewForm(request.POST, instance=review) 
            form.save()            
            return redirect('detail', review.frappe.id)
        except ValueError:            
            return render(request,'updatereview.html', {'review': review,'form':form,  'error':'Bad data in form'})

@login_required
def deletereview(request, review_id):    
    review = get_object_or_404(Review, pk=review_id,user=request.user)    
    review.delete()    
    return redirect('detail', review.frappe.id)