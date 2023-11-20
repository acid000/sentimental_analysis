from django.shortcuts import render,redirect
from sentimental.models import Brands
from textblob import TextBlob
from sendmail.views import sendmail
import threading
from time import *
import requests
from bs4 import BeautifulSoup


    #print(mydivs)

def home(request):
    b=[]
    net_polarity=0.0
    user_avg=0.0
    user_size=0
    if request.method=='POST':
        name=request.POST['name']
        b=Brands.objects.filter(Name=name)  
        global var
        var=name
        var.lower()
        lst= page_authentication() # from internet
        for i in b:
            user_avg=float(i.Avg_Polarity)
            user_size=i.Number_of_Reviews

        net_sum=lst[0]+user_avg*user_size
        net_polarity=net_sum/(lst[1]+user_size)
        for i in b:
            if i.Avg_Polarity!=net_polarity:
                i.Avg_Polarity=net_polarity
                i.save()
            if i.Number_of_Reviews!=user_size+lst[1]:
                i.Number_of_Reviews=user_size+lst[1]
                i.save()    

    return render(request, 'base.html', {'avs_polarity':net_polarity})

def page_authentication():
    url='https://www.ambitionbox.com/reviews/'+var+'-'+'reviews'

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'}
    response = requests.get(url, headers=headers)
    print(response)
    if response.status_code < 200 or response.status_code > 299:
        raise Exception(f'Failed to load the page {url}')
    page_content = response.text
    webpage =  BeautifulSoup(page_content, 'html.parser')
    mydivs = webpage.find_all("p", {"class": "body-medium overflow-wrap"})
    l=[]
    for i in mydivs:
        title=i.text
        l.append(title)
        #print(title)
    number_of_reviews=0
    sum_of_polarity=0    
    for comment in l:
        analysis = TextBlob(comment)
        p=analysis.sentiment.polarity
        s=analysis.sentiment.subjectivity
        sum_of_polarity=sum_of_polarity+p
        number_of_reviews=number_of_reviews+1
        print("p ->", p)
        sum_of_polarity
    
    return [sum_of_polarity,number_of_reviews]


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
        b.Avg_Polarity=(float(curr_p)*l+p)/(l+1)
        b.Avg_Subjectivity=(float(curr_s)*l+s)/(l+1)
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
    time_left=10
    while time_left>0:
        time_left=time_left-1
        sendmail()
        sleep(1)

t=threading.Thread(target=coundown)
t.start()

  
