import streamlit as st
import pandas as pd
import pickle
import requests
import time
session= requests.Session()
session.headers.update({'User-Agent': 'MovieApp/1.0'})
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    params={
        'api_key':"815dc2caf22568da88c2d6434c174e6f",
        'language':"en-US"
    }
    for attempt in range(3):
        try:
            response = session.get(url.format(movie_id), params=params)
            response.raise_for_status()
            data=response.json()
            poster_path = data.get('poster_path', None)
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        except requests.exceptions.RequestException:
            if attempt<2:
                time.sleep(1)
                continue
            raise



    response= requests.get("https://api.themoviedb.org/3/movie/{movie_id}?api_key=815dc2caf22568da88c2d6434c174e6f&language=en.US")
    movie_data= response.json()
    poster_path= movie_data.get('poster_path', None)
    return "https://image.tmdb.org/t/p/w500/"+ data['poster_path']
def recommend(movie):
    movie_index = movies[movies['title']== movie].index[0]
    distances= similarity[movie_index]
    movie_list= sorted(list(enumerate(distances)), reverse= True, key= lambda x:x[1])[1:6]
    recommended_movies=[]
    recommended_movies_poster= []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_poster

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies= pd.DataFrame(movies_dict)

similarity= pickle.load(open('similarity.pkl', 'rb'))
st.title('Movie Recommendation')
select_movie_name = st.selectbox('Enter the name of  Movie to recommend', movies['title'].values)
if st.button('Recommended'):
    recommendation= recommend(select_movie_name)
    for i in recommendation:
        names,posters= recommend(select_movie_name)
        col1,col2,col3,col4,col5= st.columns(5)
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


