import pickle
import streamlit as st
import requests
import pandas as pd
import difflib

# Function to fetch movie posters using OMDB API
def fetch_omdb_poster(movie_name):
    api_key = "96960fd"  # Replace with your OMDB API key
    url = f"http://www.omdbapi.com/?t={movie_name}&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    if 'Poster' in data and data['Poster'] != "N/A":
        return data['Poster']  # Poster URL
    return None

# Function to fetch IMDb rating using OMDB API
def fetch_omdb_rating(movie_name):
    api_key = "96960fd"  # Replace with your OMDB API key
    url = f"http://www.omdbapi.com/?t={movie_name}&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    if 'imdbRating' in data and data['imdbRating'] != "N/A":
        return float(data['imdbRating'])
    return 0.0

# Function to find closest matches for user input
def get_closest_matches(query, movie_list, n=5):
    return difflib.get_close_matches(query, movie_list, n=n)

# Function to recommend movies
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:  # Top 5 recommendations
        movie_title = movies.iloc[i[0]].title
        recommended_movie_names.append(movie_title)
        recommended_movie_posters.append(fetch_omdb_poster(movie_title))
    return recommended_movie_names, recommended_movie_posters

# Streamlit UI
st.set_page_config(page_title="Movie Recommender System", page_icon="🎬", layout="wide")
st.title('🎬 Movie Recommender System')

# Load data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity_compressed.pkl', 'rb'))

# Search bar with auto-complete
search_query = st.text_input("🔍 Search for a movie:", "", placeholder="Enter a movie name...")

# Movie recommendation
if search_query:
    matched_movies = get_closest_matches(search_query, movies['title'].values)
    selected_movie = st.selectbox("Select a movie", matched_movies)
else:
    selected_movie = st.selectbox("Select a movie from the list", movies['title'].values)

# Display recommendations when the button is clicked
min_rating = st.slider("Select Minimum IMDb Rating", 0.0, 10.0, 7.0, 0.1)

if st.button('🎯 Show Recommendations'):
    # Get recommended movies based on selected movie
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    # Filter movies based on IMDb rating
    filtered_movies = [
        movie for movie in recommended_movie_names if fetch_omdb_rating(movie) >= min_rating
    ]

    # Show recommendations
    st.subheader("Recommended Movies")
    cols = st.columns(5)  # Create 5 columns for displaying recommendations
    for col, movie_name in zip(cols, filtered_movies):
        poster_url = fetch_omdb_poster(movie_name)
        with col:
            st.markdown(f"**{movie_name}**", unsafe_allow_html=True)  # Display movie name
            if poster_url:
                st.image(poster_url, use_column_width=True)  # Display movie poster
            else:
                st.write("Poster not found")  # Handle missing posters

# Adding Custom Styling
def add_bg_from_url():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("https://wallpapers.com/images/hd/netflix-background-gs7hjuwvv2g0e9fj.jpg");
            background-size: cover;
        }}
        .stButton>button {{
            background-color: #1db954;
            color: white;
            font-size: 18px;
            font-weight: bold;
            border-radius: 10px;
            padding: 12px 30px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
            transition: 0.3s;
        }}
        .stButton>button:hover {{
            background-color: #1ed760;
        }}
        .stTextInput>div>input {{
            font-size: 16px;
            padding: 10px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
add_bg_from_url()
