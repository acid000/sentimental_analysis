from django.shortcuts import render,redirect
from sentimental.models import Review,Brands
from textblob import TextBlob
from sendmail.views import sendmail
import schedule 
import time 
from threading import Timer
import threading
from django.contrib.auth.decorators import login_required
from time import *
def home(request):
    b=[]
    if request.method=='POST':
        name=request.POST['name']
        b=Brands.objects.filter(Name=name)  
    return render(request, 'base.html', {'reviews': b})


def analyze_sentiment(text,name):
    analysis = TextBlob(text)
    p=analysis.sentiment.polarity
    s=analysis.sentiment.subjectivity
    length=len(Brands.objects.filter(Name=name))
    curr_p=0.0
    curr_s=0.0
    print(length)
    if length==0:
        Brands.objects.create(Name=name,Avg_Polarity=p,Avg_Subjectivity=s,Recent_Comments=text,Number_of_Reviews=1)

    else:
        curr_p=Brands.objects.get(Name=name).Avg_Polarity
        curr_s=Brands.objects.get(Name=name).Avg_Subjectivity
        b=Brands.objects.get(Name=name)
        l=b.Number_of_Reviews
        b.Avg_Polarity=(float(curr_p)+p)/(l+1)
        b.Avg_Subjectivity=(float(curr_s)+s)/(l+1)
        b.Number_of_Reviews=l+1
        b.save()
    return 'positive' if analysis.sentiment.polarity > 0 else 'negative' if analysis.sentiment.polarity < 0 else 'neutral'


def add_review(request):
    if request.method == 'POST':
        name=request.POST['name']
        text = request.POST['text']
        sentiment = analyze_sentiment(text,name)
        return render(request,'home.html',{'sentiment':sentiment})
    return render(request, 'home.html')




def coundown():
    global time_left
    time_left=100
    while time_left>0:
        time_left=time_left-1
        sendmail()
        sleep(20)

t=threading.Thread(target=coundown)
t.start()

  
