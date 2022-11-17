from django.shortcuts import render
from .forms import SentimentForm
from .models import Movie, Sentiment
from .vectorizer import vect
import os
import pickle
import numpy as np 
# Create your views here.

classifier = pickle.load(
    open(os.path.join(
        "pkl_objects",
        "classifier.pkl"
    ), "rb"))

def classify(reviews):
    label = {0:"Negative", 1:"Positive"}
    X = vect.transform([reviews])
    pred = classifier.predict(X)[0]
    proba = np.max(classifier.predict_proba(X))
    return label[pred], proba

def train(review, y):
    X = vect.transform([review])
    classifier.partial_fit(X, [y])
    
def classify_review(request):
    form = SentimentForm(request.POST or None)
    if form.is_valid():
        reviews   = form.cleaned_data.get("reviews")
        gender    = form.cleaned_data.get("gender")
        age       = form.cleaned_data.get("age")
        country   = form.cleaned_data.get("country")
        movie     = form.cleaned_data.get("movie")
        my_result, my_proba = classify(reviews)
        
        context = {
            "result":my_result,
            "probability":round(my_proba),
            "review":reviews,
            "gender":gender,
            "age":age,
            "country":country,
            "movie":movie
        }
        return render(request, "classifiers/prediction.html", context)
    context = {"form":form}
    return render(request, "classifiers/movie_classify.html", context)
    
def feedback(request):
    feedback   = request.POST["feedback_button"]
    prediction = request.POST["result"]
    review     = request.POST["review"]
    gender     = request.POST["gender"]
    age        = request.POST["age"]
    country    = request.POST["country"]
    movie      = request.POST["movie"]
    
    inv_label  = {"Negative":0, "Positive":1}
    y = inv_label[prediction]
    
    if feedback == "Incorrect":
        y = int(not(y))
    train(review, y)
    my_movie = Movie.objects.filter(title=movie).first()
    sentiment = Sentiment(
        reviews=review, 
        result=y,
        gender=gender,
        age=age,
        country=country,
        movie=my_movie)
    sentiment.save()
    context = {}
    return render(request, "classifiers/thanks.html", context)

        