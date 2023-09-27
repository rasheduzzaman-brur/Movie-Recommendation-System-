import pickle
import pandas as pd
import requests


movieDict = pickle.load(open('model/movieDict.pkl','rb')) #it is a dictionary where movie name is used as key and movie id is used as value
movieLink = pickle.load(open('model/movieLink.pkl','rb')) #it is a dictionary where movie Id is used as key and  Linkid of tmdb movie id is used as value

model = pd.DataFrame()
model = pickle.load(open('model/model.pkl','rb'))  # it is a model of pearson correlation

def fetch_poster(movie_id):   # fetching poster for all similar movies form tmdb using tmdb api
    movie_id = movieLink[movie_id]
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=b8df2890780a1db0bb839e00f4203426&append_to_response=videos'.format(movie_id))
    data = response.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def get_similar(moveilist,rating): # Get the all similar movies for a selected movie
    movie_list = []
    df = pd.DataFrame()
    for movie in moveilist:
        similar_movies = model[movie]*(rating[0]-2.5) # return movie based on previous movies rating
        similar_movies = similar_movies.sort_values(ascending=False)
        df = pd.concat([df, pd.DataFrame([similar_movies])])
    df = df.sum(axis=0).sort_values(ascending=False) ## sum all movies similarity
    similar_movies = similar_movies.index # get the movei name
    
    for i in range(len(similar_movies)): # return top 10 similar movies
        if i==10:
          break
        movie_list.append(similar_movies[i])

    recommend_poster = [] #fetch poster for each movie
    for i in movie_list:
        movieId = movieDict[i]
        recommend_poster.append(fetch_poster(movieId))
    return movie_list , recommend_poster