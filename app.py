import streamlit as st
import pickle
import pandas as pd
import requests

API = '64c9e20da415a1fac8924e814e7c7764'

# https://api.themoviedb.org/3/movie/65?api_key=64c9e20da415a1fac8924e814e7c7764&language=en-US

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=64c9e20da415a1fac8924e814e7c7764&language=en-US'.format(movie_id))
    data = response.json()
    print(data)
    return  "http://image.tmdb.org/t/p/w500/"+data['poster_path']

similarity = pickle.load(open('similarity.pkl', 'rb'))
movies = pickle.load(open('movies.pkl' , 'rb'))

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
 
    movies_list = sorted(list(enumerate(distances)) , reverse = True , key = lambda x: x[1])[1:6]

    recommend_movies = []
    recommend_posters=[]
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        
        recommend_movies.append(movies.iloc[i[0]].title)
        recommend_posters.append(fetch_poster(movie_id))
        
    return recommend_movies, recommend_posters


st.title('Movie Recommender System')



selected_movie_names = st.selectbox(
    "Select a Movie",
    (movies['title'].values),
)

if st.button("Recommend"):
    names,posters = recommend(selected_movie_names)
    
    col1, col2, col3, col4 ,col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])

