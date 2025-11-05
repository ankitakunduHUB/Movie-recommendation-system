import streamlit as st
import pickle
import os

# --- Safe pickle loader with better error messages ---
def safe_load_pickle(path):
    try:
        with open(path, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        st.error(f"❌ File not found: {path}")
        st.stop()
    except pickle.UnpicklingError:
        st.error(f"⚠️ File {path} is not a valid pickle. Recreate or check the file content.")
        st.stop()
    except Exception as e:
        st.error(f"Unexpected error while loading {path}: {e}")
        st.stop()


# --- Movie recommendation logic ---
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []

    for i in distances[1:6]:
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names


# --- Streamlit UI setup ---
st.set_page_config(page_title="🎬 Movie Recommender System", layout="wide")
st.title("🎥 Movie Recommender System")
st.write("Select a movie, and get 5 recommendations based on similarity.")

# --- Resolve correct model file paths ---
base_path = os.path.dirname(__file__)  # directory where app.py is located
movie_list_path = os.path.join(base_path, 'movie_list.pkl')
similarity_path = os.path.join(base_path, 'similarity.pkl')

# --- Load data ---
movies = safe_load_pickle(movie_list_path)
similarity = safe_load_pickle(similarity_path)

# --- Dropdown to select movie ---
movie_list = movies['title'].values
selected_movie = st.selectbox("🎞️ Type or select a movie from the dropdown", movie_list)

# --- Show recommendations ---
if st.button('Show Recommendation'):
    recommended_movie_names = recommend(selected_movie)
    st.subheader("Recommended Movies:")
    for name in recommended_movie_names:
        st.write(f"🎬 {name}")