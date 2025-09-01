import os
import streamlit as st
import pickle
import pandas as pd
import re


def clean_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name)  # remove invalid characters


# --- Fetch Poster from Local Folder ---
def fetch_poster(title):
    safe_title = clean_filename(title)
    poster_path = f"posters/{safe_title}.jpg"
    if os.path.exists(poster_path):
        return poster_path
    else:
        # fallback image if poster missing
        return "https://via.placeholder.com/500x750?text=No+Poster"

# --- Recommend Movies ---
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movies.iloc[i[0]].title))

    return recommended_movies, recommended_movies_posters

# --- Load Data ---
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# --- Page Title ---
st.markdown("<h1 style='text-align: center; color:#FF4B4B;'>🎬 Movie Recommendation System</h1>", unsafe_allow_html=True)

# --- Styled Dropdown Label ---
st.markdown(
    "<p style='margin:6px 0 2px 0; font-size:18px; color:#FAFAFA;'>🎯 Choose a movie to get recommendations:</p>",
    unsafe_allow_html=True
)

selected_movie_name = st.selectbox(
    label="🎯 Choose a movie to get recommendations:",
    options=movies['title'].values,
    label_visibility="collapsed",  # hide default label
    help="Start typing to search your movie"
)

# --- Recommend Button ---
clicked = st.button("Recommend", help="Click to generate 5 similar movies")

if clicked:
    names, posters = recommend(selected_movie_name)

    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.image(posters[i], use_container_width=True)   # ✅ local poster support
            st.markdown(f"<h4>{names[i]}</h4>", unsafe_allow_html=True)

# --- Custom CSS ---
st.markdown("""
<style>
/* 🔥 Fix background flicker on rerender */
html, body, [data-testid="stAppViewContainer"], .stApp {
    background: linear-gradient(to right, #141E30, #243B55) !important;
    color: #FAFAFA !important;
    height: 100%;
    margin: 0;
    padding: 0;
}

/* Center whole app vertically + horizontally */
.stApp {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh; /* use min-height instead of height for better scaling */
    padding: 0;
}

/* Keep content at nice width */
.block-container {
    max-width: 1100px;
    margin: auto;
}

/* Brighten selectbox labels */
div[data-testid="stSelectbox"] label,
div[data-baseweb="select"] label {
    color: #FAFAFA !important;
}

/* Button styling */
.stButton > button {
    background-color: #FF4B4B;
    color: #FFFFFF;
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 10px;
    padding: 0.5rem 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: transform .12s ease, box-shadow .12s ease, background-color .12s ease;
}
.stButton > button:hover {
    background-color: #ff5f5f;
    box-shadow: 0 4px 14px rgba(0,0,0,0.3);
    transform: translateY(-1px);
}
.stButton > button:active {
    background-color: #e33b3b;
    transform: translateY(0);
}
.stButton > button:focus {
    outline: 2px solid #FFD2D2;
    outline-offset: 2px;
}

/* Movie card */
h4 {
    font-size:16px !important;
    color:#FAFAFA !important;
    margin-top:10px;
    text-align: center;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
</style>
""", unsafe_allow_html=True)
