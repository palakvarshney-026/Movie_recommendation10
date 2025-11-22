import streamlit as st
import pandas as pd
import pickle
def recommend(movie):
    movie_index = movies[movies['title']== movie].index[0]
    distances= similarity[movie_index]
    movie_list= sorted(list(enumerate(distances)), reverse= True, key= lambda x:x[1])[1:6]
    recommended_movies=[]
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies= pd.DataFrame(movies_dict)

similarity= pickle.load(open('similarity.pkl', 'rb'))
st.title('Movie Recommendation')
select_movie_name = st.selectbox('Enter the name of  Movie to recommend', movies['title'].values)
if st.button('Recommend'):
    recommendation= recommend(select_movie_name)
    for i in recommendation:
        st.write(i)
