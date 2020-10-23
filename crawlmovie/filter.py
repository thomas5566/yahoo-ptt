import os, sys, django
# sys.path.append(
#     os.path.join(os.path.dirname(
#         os.path.dirname(os.path.abspath(__file__))), "..")
# )
sys.path.append("..")
os.environ["DJANGO_SETTINGS_MODULE"] = "best_movies.settings"
django.setup()
from movieptt.models import PttMovie
from movieptt.models import Movie
from movieptt.models import CountGoodAndBad

import pandas as pd
import numpy as np

from collections import Counter

class FilterAndInsertData():
    movies = pd.read_csv("ptt.csv").dropna(how="all")
    movies["title"] = movies["title"].astype("category")

    titles = pd.read_csv("yahoomovie.csv")
    key_word = titles.iloc[:, 7]

    # 找到含有相同電影名稱的title 並新增一個新欄位'key_word' 最後insert to database
    newDF = pd.DataFrame()
    for key in key_word:
        mask = movies["title"].str.contains(key)  # string compare
        movies["key_word"] = key  # Add new column
        newDF = newDF.append(movies[mask], ignore_index=True)
    newDF.to_csv('output.csv')

    # Insert Data to DataBase
    # df_records = newDF.to_dict("records")
    # model_instances = [
    #     PttMovie(
    #         author=record["author"],
    #         contenttext=record["contenttext"],
    #         date=record["date"],
    #         title=record["title"],
    #         key_word=Movie.objects.get(title=record["key_word"]), # foreign key
    #     )
    #     for record in df_records
    # ]
    # PttMovie.objects.bulk_create(model_instances)

    # count title欄位 有包含 '好雷' and '負雷' 字眼的標題
    ptt_coun_ray = pd.DataFrame()
    ptt_coun_ray['title'] = titles.iloc[:, 7]

    # To assign as a column use transform
    newDF['good_ray'] = newDF.groupby(['key_word'])['title'].transform(lambda x: x[x.str.contains('好雷')].count())
    newDF['bad_ray'] = newDF.groupby(['key_word'])['title'].transform(lambda x: x[x.str.contains('負雷')].count())

    # merge newDF and title DataFrame and duplicates title
    df = ptt_coun_ray.merge(newDF, left_on='title', right_on='key_word', how='left').drop(['author', 'key_word', 'contenttext', 'date', 'title_y'], axis=1)
    df2 = df.drop_duplicates(subset=['title_x'])
    df2 = df2.fillna(0) # Transfer NaN to 0
    df2.to_csv('count_good_or_bad.csv')

    # df_records2 = df2.to_dict('records2')
    # model_instances = [
    #     CountGoodAndBad(
    #         good_ray=record["good_ray"],
    #         bad_ray=record["bad_ray"],
    #         movie=Movie.objects.get(title=record["title_x"]),
    #     )
    #     for record in df_records2
    # ]
    # CountGoodAndBad.objects.bulk_create(model_instances)
