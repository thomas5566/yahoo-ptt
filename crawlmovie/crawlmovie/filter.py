
import pandas as pd
import django
import os
import sys
from collections import Counter

sys.path.append(
    os.path.join(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))), "..")
)
os.environ["DJANGO_SETTINGS_MODULE"] = "best_movies.settings"
django.setup()

from movieptt.models import PttMovie
from movieptt.models import Movie

movies = pd.read_csv("ptt.csv").dropna(how="all")
movies["title"] = movies["title"].astype("category")

titles = pd.read_csv("yahoomovie.csv")
key_word = titles.iloc[:, 0]

newDF = pd.DataFrame()

for key in key_word:
    mask = movies["title"].str.contains(key)  # string compare
    movies["key_word"] = key  # Add new column
    newDF = newDF.append(movies[mask], ignore_index=True)

for key in key_word:
    if movies["title"].str.contains(key).any() == True:
        print(movies["title"].str.count('好雷'))

newDF.to_csv('output.csv')

df_records = newDF.to_dict("records")
model_instances = [
    PttMovie(
        author=record["author"],
        contenttext=record["contenttext"],
        date=record["date"],
        title=record["title"],
        key_word=Movie.objects.get(title=record["key_word"]),
    )
    for record in df_records
]

PttMovie.objects.bulk_create(model_instances)
