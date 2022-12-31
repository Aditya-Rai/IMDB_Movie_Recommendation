# Importing the Libraries
import streamlit as st
import pickle
import requests

# Making a function that take a movie name as a input and find its similarity matrix and returns the nearest five movies

def recommend(selected_movie):

    selected_movie_index = movies_df[movies_df["title"] == selected_movie].index[0]
    current_similarity = similarity[selected_movie_index]

    similar_movies = sorted(list(enumerate(current_similarity)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_poster = []
    for similar_movie in similar_movies:
        similar_movie_index = similar_movie[0]
        similar_movie_id = movies_df.loc[similar_movie_index, "id"]

        # Fetching Poster using API
        recommended_movies_poster.append(fetch_poster(similar_movie_id))
        recommended_movies.append(movies_df.loc[similar_movie_index, "title"])
        # print(recommended_movies)
    return recommended_movies,recommended_movies_poster


def fetch_poster(similar_movie_id):
    # print(similar_movie_id)
    responses = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=c76ecdd9cd32b410b0839a7f68b288b1&language=en-US".format(similar_movie_id))
    # print(responses)
    data = responses.json()

    image_path = data["poster_path"]
    if image_path == None:
        return "https://bitsofco.de/content/images/2018/12/broken-1.png"

    
    return "https://image.tmdb.org/t/p/w500" + data["poster_path"]

# Importing the pickle and taking as an dataframe

movies_df= pickle.load(open("final_movies.pkl","rb"))
similarity = pickle.load(open("final_similarity.pkl","rb"))


# Title
st.title('Movie Recommendation System')

# Movie List to show when user type a movie name
movies_list = movies_df["title"].values

selected_movie_name = st.selectbox("Enter the Movie Name",movies_list)

if st.button("Recommend"):
    # print(selected_movie_name)
    recommended_movie_names,recommended_posters = recommend(selected_movie_name)

    col1,col2,col3,col4,col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_posters[1])
    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_posters[4])
