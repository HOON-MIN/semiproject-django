from django.shortcuts import render

def mainHome(reqeust):
    return render(reqeust, "main.html")