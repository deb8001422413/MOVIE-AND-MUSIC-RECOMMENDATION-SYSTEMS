import streamlit as st
import pickle
import pandas as pd
import json

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Movie & Music Recommender",
    layout="centered"
)

# ---------------- CSS ----------------
st.markdown("""
<style>

/* Fade-in animation */
.fade-in {
    animation: fadeIn 0.8s ease-in-out;
}
@keyframes fadeIn {
    from {opacity: 0; transform: translateY(15px);}
    to {opacity: 1; transform: translateY(0);}
}

/* Card container */
.rainbow-card {
    position: relative;
    padding: 14px;
    margin: 12px 0;
    border-radius: 14px;
    background:  red;
    color: white;
    overflow: hidden;
    isolation: isolate;
}

/* Animated rainbow border for cards */
.rainbow-card::before {
    content: "";
    position: absolute;
    inset: 0;
    border-radius: 14px;
    padding: 2px;
    background: conic-gradient(
        #00ff7f,
        #00c8ff,
        #ff00ff,
        #ff9800,
        #00ff7f
    );
    animation: spin 5s linear infinite;

    -webkit-mask:
        linear-gradient(#000 0 0) content-box,
        linear-gradient(#000 0 0);
    -webkit-mask-composite: xor;
            mask-composite: exclude;
}

/* Spin animation */
@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

/* Card hover */
.rainbow-card:hover {
    background: #0b2e1a;
    box-shadow: 0 0 20px rgba(0,255,127,0.6);
    transform: scale(1.03);
    transition: all 0.3s ease;
}

/* -------- BUTTON RAINBOW BORDER -------- */
div.stButton > button {
    position: relative;
    padding: 0.6em 1.5em;
    font-size: 16px;
    font-weight: 600;
    color: white;
    background:  rgba(0,255,127,0.6);
    border-radius: 14px;
    border: none;
    cursor: pointer;
    overflow: hidden;
    z-index: 0;
}

/* Button rainbow border */
div.stButton > button::before {
    content: "";
    position: absolute;
    inset: -2px;
    border-radius: 16px;
    background: conic-gradient(
        #00ff7f,
        #00c8ff,
        #ff00ff,
        #ff9800,
        #00ff7f
    );
    animation: spin 4s linear infinite;
    z-index: -1;
}

/* Button inner background */
div.stButton > button::after {
    content: "";
    position: absolute;
    inset: 2px;
    border-radius: 12px;
    background: #111;
    z-index: -1;
}

/* Button hover effect */
div.stButton > button:hover::after {
    background: linear-gradient(135deg, #00ff7f, #00c8ff);
}

div.stButton > button:hover {
    box-shadow: 0 0 18px rgba(0,255,127,0.7);
    transform: scale(1.05);
    transition: all 0.3s ease;

}
/* ===== STATIC RAINBOW BORDER FOR INPUT / SELECT BOX ===== */

div[data-baseweb="select"],
div[data-baseweb="input"] {
    position: relative;
    border-radius: 30px;
    padding: 2px;
    background: linear-gradient(
        135deg,
        #00ff7f,
        #00c8ff,
        #ff00ff,
        #ff9800,
        #00ff7f
    );
}

/* Inner input */
div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div {
    border-radius: 12px !important;
    background: #111 !important;
}

/* Text color */
div[data-baseweb="select"] *,
div[data-baseweb="input"] * {
    color: white !important;
}

/* Hover glow */
div[data-baseweb="select"]:hover,
div[data-baseweb="input"]:hover {
    box-shadow: 0 0 15px rgba(0,255,127,0.6);
}

.stApp {
    background-color:lightyellow;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------
movies_dict = pickle.load(open("movies_dict.pkl", "rb"))
movies = pd.DataFrame(movies_dict)

new_df = pd.DataFrame(pickle.load(open("movies_data.pkl", "rb")))
music = pd.DataFrame(pickle.load(open("music_dict.pkl", "rb")))

similarity = pickle.load(open("similarity.pkl", "rb"))
music_similarity = pickle.load(open("music_similarity.pkl", "rb"))

# ---------------- MOVIE RECOMMENDER ----------------
def recommend_movie(movie_title):
    index = new_df[new_df['title'] == movie_title].index[0]
    distances = similarity[index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    st.markdown(f"###  Movies like **{movie_title}**")

    for i in movies_list:
        st.markdown(
            f"""
            <div class="rainbow-card fade-in">
                🎞️ <b>{new_df.iloc[i[0]]['title']}</b>
            </div>
            """,
            unsafe_allow_html=True
        )

# ---------------- MUSIC RECOMMENDER ----------------
def recommend_music(song_name):
    index = music[music['track_name'] == song_name].index[0]
    artist = music.iloc[index]['track_artist']

    distances = music_similarity[index]
    sorted_songs = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )

    st.markdown(f"### 🎵 Songs like **{song_name}**")

    count = 0
    for i, _ in sorted_songs:
        track = music.iloc[i]['track_name']
        art = music.iloc[i]['track_artist']

        if track == song_name and art == artist:
            continue

        st.markdown(
            f"""
            <div class="rainbow-card fade-in">
                <b>{track}</b><br>
                {art}
            </div>
            """,
            unsafe_allow_html=True
        )

        count += 1
        if count == 5:
            break

# ---------------- UI ----------------
st.title(" Movie &  Music Recommendation System")

tabs = st.tabs([" Movies", " Music"])

# -------- MOVIE TAB --------
with tabs[0]:
    movie = st.selectbox("Select a movie", movies["title"].values)
    if st.button("Recommend Movies"):
        recommend_movie(movie)

# -------- MUSIC TAB --------
with tabs[1]:
    song = st.selectbox("Select a song", music["track_name"].values)
    if st.button("Recommend Songs "):
        recommend_music(song)
