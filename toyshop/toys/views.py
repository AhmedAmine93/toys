
from django.shortcuts import render
from .models import Toy
import time

timestamp = int(time.time())

def home(request):
   toys = Toy.objects.all()
   
   return render(request, 'toys/home.html', {'toys': toys, 'timestamp': timestamp})


def toy_list(request):
   toys = Toy.objects.all()
   return render(request, 'toys/toy_list.html', {'toys': toys, 'timestamp': timestamp})

def toy_detail(request, toy_id):
   toy = Toy.objects.get(id=toy_id)
   return render(request, 'toys/toy_detail.html', {'toy': toy, 'timestamp': timestamp})

def contact(request):
   return render(request, 'toys/contact.html',{'timestamp': timestamp})

def about(request):
   return render(request, 'toys/about.html',{ 'timestamp': timestamp})



# Create your views here.
