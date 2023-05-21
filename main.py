from tkinter.font import names
from flask import Flask, jsonify, request
from demographic_filtering import output
from content_filtering import get_recommendations
import pandas as pd

movies_data = pd.read_csv('final.csv')

app = Flask(__name__)

all_movies = movies_data[["original_title","poster_link","release_date","runtime","weighted_rating"]]

liked_movies = []
not_liked_movies = []
did_not_watch = []

def assign_val():
    m_data = {
        "original_title": all_movies.iloc[0,0],
        "poster_link": all_movies.iloc[0,1],
        "release_date": all_movies.iloc[0,2] or "N/A",
        "duration": all_movies.iloc[0,3],
        "rating":all_movies.iloc[0,4]/2
    }
    return m_data

@app.route("/movies")
def get_movie():
    movie_data = assign_val()

    return jsonify({
        "data": movie_data,
        "status": "success"
    })

@app.route("/like")
def liked_movie():
    global all_movies
    movie_data=assign_val()
    liked_movies.append(movie_data)
    all_movies.drop([0], inplace=True)
    all_movies = all_movies.reset_index(drop=True)
    return jsonify({
        "status": "success"
    })

# api to return list of liked movies
@app.route("/liked")
def liked_film():
    global liked_movies
    return jsonify({
        "status": "success",
        "data" : liked_movies
    })


@app.route("/dislike")
def unliked_movie():
    global all_movies

    movie_data=assign_val()
    not_liked_movies.append(movie_data)
    all_movies.drop([0], inplace=True)
    all_movies=all_movies.reset_index(drop=True)
    
    return jsonify({
        "status": "success"
    })

@app.route("/did_not_watch")
def did_not_watch_view():
    global all_movies

    movie_data=assign_val()
    did_not_watch.append(movie_data)
    all_movies.drop([0], inplace=True)
    all_movies=all_movies.reset_index(drop=True)
    
    return jsonify({
        "status": "success"
    })

# api to return list of popular movies
@app.route("/popular_movies")
def popular_movies():
    popular_array = []
    for i, r in output.iterrows():
        dict = {
            'original_title' :r["original_title"],
             'poster_link' :r["poster_link"],
              'runtime': r["runtime"],
               'release_date': r["release_date"] , 
               'weighted_rating': r["weighted_rating"]
        }
        popular_array.append(dict)
    return jsonify({
        "data" : popular_array,
        "status": "success"
    })

# api to return list of recommended movies
@app.route("/recommended_movies")
def recommended_movies():
    global liked_movies
    column_names = ['original_title' , 'poster_link' , 'runtime', 'release_date' , 'weighted_rating']
    all_recommended = pd.DataFrame(columns = column_names)
    for i in liked_movies:
        r = get_recommendations(i["original_title"])
        all_recommended = all_recommended.append(r)
    all_recommended.drop_duplicates(subset=["original_title"],inplace=True)

    recommended_array =[]
    for i,r in all_recommended.iterrows():
        dict = {
            'original_title' :r["original_title"],
             'poster_link' :r["poster_link"],
              'runtime': r["runtime"],
               'release_date': r["release_date"] , 
               'weighted_rating': r["weighted_rating"]
        }
        recommended_array.append(dict)
    return jsonify({
        "data" : recommended_array,
        "status": "success"
    })




if __name__ == "__main__":
  app.run()
