import os, sys, django
# sys.path.append(
#     os.path.join(os.path.dirname(
#         os.path.dirname(os.path.abspath(__file__))), "..")
# )
sys.path.append("..")
os.environ["DJANGO_SETTINGS_MODULE"] = "best_movies.settings"
django.setup()

from movieptt.models import PttMovie, Movie, CountGoodAndBad

import pandas as pd
import numpy as np

class FilterAndInsertData():
    movies = pd.read_csv("ptt_movies.csv").dropna(how="all")
    titles = pd.read_csv("yahoomovie.csv")

    movies["title"] = movies["title"].astype("category")
    key_word = titles.iloc[:, 7]

    # 找到含有相同電影名稱的title 並新增一個新欄位'key_word' 最後insert to database
    newDF = pd.DataFrame()
    for key in key_word:
        mask = movies["title"].str.contains(key)  # string compare
        movies["key_word"] = key  # Add new column
        newDF = newDF.append(movies[mask], ignore_index=True)
    newDF.to_csv('output.csv')

    # Insert ptt comment Data to DataBase
    df_records = newDF.to_dict("records")
    for record in df_records:
        identifyer = PttMovie.objects.filter(author=record['author'], title=record['title']).exists()

        if identifyer:
            print('Data is already exists!!')
        else:
            PttMovie.objects.create(
                author=record["author"],
                contenttext=record["contenttext"],
                date=record["date"],
                title=record["title"],
                key_word=Movie.objects.get(title=record["key_word"]), # foreign key
            )
            # print('Not exist')

        # identifyer_title = PttMovie.objects.get(title=record['title'])
        # identifyer_author = PttMovie.objects.get(author=record['author'])
        # identifyer_key_word = Movie.objects.get(title=record["key_word"])
        # movie_key_word = Movie.objects.filter(title=record["key_word"]).first()
        # pttmovie, created = PttMovie.objects.get_or_create(
        #     # key_word=identifyer_key_word,
        #     author=PttMovie.objects.filter(author=record['author']).first(),
        #     title=PttMovie.objects.filter(title=record['title']).first(),
        #     defaults={
        #         "author": record['author'],
        #         "contenttext": record['contenttext'],
        #         'date': record['date'],
        #         'title': record['title'],
        #         'key_word': movie_key_word,
        #     }
        # )
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
    df = ptt_coun_ray.merge(newDF, left_on='title', right_on='key_word', how='left').drop(
            ['author', 'key_word', 'contenttext', 'date', 'title_y'], axis=1)
    df2 = df.drop_duplicates(subset=['title_x'])
    df2 = df2.fillna(0) # Transfer NaN to 0
    df2.to_csv('count_good_or_bad.csv')

    # df_records2 = df2.to_dict('records2')
    # for record in df_records2:
    #     # get Movie TABLE title as identify
    #     identifyer = Movie.objects.get(title=record["title_x"])
    #     CountGoodAndBad.objects.update_or_create(
    #         movie=identifyer,
    #         defaults={
    #             'movie': identifyer,
    #             'good_ray': record['good_ray'],
    #             'bad_ray': record['bad_ray'],
    #         }
    #     )

    # model_instances2 = [
    #     CountGoodAndBad(
    #         good_ray=record["good_ray"],
    #         bad_ray=record["bad_ray"],
    #         movie=Movie.objects.get(title=record["title_x"]),
    #     )
    #     for record in df_records2
    # ]
    # CountGoodAndBad.objects.bulk_create(model_instances2)
    # CountGoodAndBad.objects.update_or_create()
