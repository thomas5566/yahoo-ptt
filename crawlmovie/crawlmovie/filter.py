import pandas as pd
import django
import os, sys

sys.path.append(
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "..")
)
os.environ["DJANGO_SETTINGS_MODULE"] = "best_movies.settings"
django.setup()

from movieptt.models import PttMovie
from movieptt.models import Movie

movies = pd.read_csv("ptt.csv").dropna(how="all")
movies["title"] = movies["title"].astype("category")
titles = pd.read_csv("yahoo.csv")
key_word = titles.iloc[:, 7]
newDF = pd.DataFrame()
for key in key_word:
    mask = movies["title"].str.contains(key)  # string compare
    if mask.any() == True:
        movies["key_word"] = key  # Add new column
        newDF = newDF.append(movies[mask], ignore_index=True)
    else:
        pass

print(newDF)
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


# from django.conf import settings
# from sqlalchemy import create_engine
# import pandas as pd
# import django
# import os
# import sys
# import psycopg2 as p

# sys.path.append(os.path.join(os.path.dirname(
#     os.path.dirname(os.path.abspath(__file__))), ".."))
# os.environ['DJANGO_SETTINGS_MODULE'] = 'best_movies.settings'
# django.setup()

# # load database settings from django

# user = settings.DATABASES['default']['USER']
# password = settings.DATABASES['default']['PASSWORD']
# database_name = settings.DATABASES['default']['NAME']
# # host = settings.DATABASES['default']['HOST']
# # port = settings.DATABASES['default']['PORT']

# # database_url = 'postgresql://{user}:{password}@localhost:5432/{database_name}'.format(
# #     user=user,
# #     password=password,
# #     database_name=database_name,
# # )

# engine = conn=p.connect(dbname='db.sqlite3', user='thomas', host='127.0.0.1', password='5566', port=8000)

# movies = pd.read_csv("ptt.csv").dropna(how='all')
# movies["title"] = movies["title"].astype("category")
# titles = pd.read_csv("yahoo.csv")
# key_word = titles.iloc[:, 7]
# newDF = pd.DataFrame()
# for key in key_word:
#     mask = movies["title"].str.contains(key)  # string compare
#     movies["key_word"] = key  # Add new column
#     # for x in mask:
#     #     movies["key_word"] = key
#     # # data.append(movies[mask])
#     newDF = newDF.append(movies[mask], ignore_index=True)
# # write df into db
# newDF.to_sql("PttMovie", con=engine, if_exists="append", index=False, chunksize=500, method="multi")
