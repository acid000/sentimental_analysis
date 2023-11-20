from django.shortcuts import render
from django.core.mail import send_mail
from django.shortcuts import HttpResponse
from django.contrib.auth.models import User
from sentimental.models import Brands

d={}
l=Brands.objects.all()
for i in l:
    d[i.Name]=i.Avg_Polarity

def sendmail():
    newlist=Brands.objects.all()
    for i in newlist:
        name=i.Name
        avsP=i.Avg_Polarity
        userlist=User.objects.all()
        maillist=[]
        for mail in userlist:
            maillist.append(mail.email)
        if d[name]!=avsP:
            d[name]=avsP
            send_mail('hello sir/mam the polarity of the brand is changed ','this is from sachin','sr719499@gmail.com',maillist,fail_silently=False)
    print("i am called")
