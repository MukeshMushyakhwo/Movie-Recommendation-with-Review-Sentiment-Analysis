import streamlit as st
import joblib
import pandas as pd
import requests
import re
import string
import os

api_key = os.environ.get('API_KEY')

st.title("Movie Recommendation and Review Analysis System") 

movies_title = joblib.load('Model/movies_data.joblib')
similarity = joblib.load('Model/similarity.joblib')
sentiment_model = joblib.load('Model/sentiment_analysis_model.pkl')
vectorizer  = joblib.load('Model/tfidf_vectorizer.pkl')

movies_title = pd.DataFrame(movies_title)

def search_movie_title(movie_data):
    select = st.selectbox("Search", movie_data["title"].values)
    return select


select = search_movie_title(movies_title)

def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()

    # Remove links (http/https)
    text = re.sub(r'http\S+', '', text)

    # Remove HTML tags
    text = re.sub(r'<.*?>', '', text)

    # Remove punctuation
    text = text.translate(str.maketrans("", "", string.punctuation))

    # Remove numbers
    text = re.sub(r'\d+', '', text)

    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()

    return text




# Function to perform sentiment analysis
def analyze_sentiment(review):
    # Preprocess the review text and transform it using the vectorizer
    processed_review = preprocess_text(review)  # You need to define the preprocess_text function
    vectorized_review = vectorizer.transform([processed_review])
    
    # Predict sentiment using the loaded model
    sentiment = sentiment_model.predict(vectorized_review)[0]

    # Convert the sentiment prediction to a label (positive/negative)
    if sentiment == 1:
        sentiment_label = "positive"
    else:
        sentiment_label = "negative"

    return sentiment_label



def poster(movie_id):
    get_img = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-Us")
    data = get_img.json()
    
    if 'poster_path' in data:
        return "https://image.tmdb.org/t/p/original/" + data['poster_path']
    else:
        return "No poster available"
    
    
def get_movie_reviews(movie_id):
    reviews_url = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}/reviews?api_key={api_key}") 
    data = reviews_url.json()
    reviews = []
    
    for review in data.get("results", []):
        author = review.get("author", "Unknown")
        content = review.get("content", "")
        reviews.append({"author": author, "content": content})
    
    return reviews
    
    
def recommend(movie):
    movie_index = movies_title[movies_title['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:11]  
    recommended_movies = []
    recommended_movies_posters = []
          
    for i in movies_list:
        movie_id = movies_title.iloc[i[0]].id
        recommended_movies.append(movies_title.iloc[i[0]].title)
        recommended_movies_posters.append(poster(movie_id))
    return recommended_movies, recommended_movies_posters


if select:
    names, posters = recommend(select)
    
    # Assuming `movies_title` is a DataFrame containing movie information
    id = movies_title.loc[movies_title['title'] == select, 'id'].values[0]
    overview = movies_title.loc[movies_title['id'] == id, 'overview'].values[0]
    genre = movies_title.loc[movies_title['id'] == id, 'genres'].values[0]
    casts = movies_title.loc[movies_title['id'] == id, 'cast'].values[0]
    crew = movies_title.loc[movies_title['id'] == id, 'crew'].values[0]
    release_date =  movies_title.loc[movies_title['id'] == id, 'release_date'].values[0]
    rating = movies_title.loc[movies_title['id'] == id, 'vote_average'].values[0]


    
    # Create two columns layout
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.image(poster(id), use_column_width=True, width='100%')  # Full width of the screen
         
    
    with col2:
        st.write(f'### {select}')
        st.write(f"**Genre:** {genre}")
        st.write(f"**Cast:** {casts}")
        st.write(f"**Director:** {crew}")
        st.write(f"**Release Date:** {release_date}")
        st.write(f"**Rating:** `{rating}`")
        
    st.warning(overview)


    # Fetch and display movie reviews
    st.write("#### Reviews:")
    movie_reviews = get_movie_reviews(id)
    
    # Create a scrollable container for reviews
    with st.container():
        
        if not movie_reviews:
            st.write("No reviews available.")
        else:
            # Display the first review
            st.write(f"**Author:** {movie_reviews[0]['author']}")
            st.write(movie_reviews[0]['content'])
            sentiment = analyze_sentiment(movie_reviews[0]['content'])
            
            # Display sentiment with emoji
            if sentiment == 'positive':
                emoji_html = '<span style="font-size: 25px;">👍</span>'
                st.write(f"##### `Review:` {sentiment.capitalize()} {emoji_html}", unsafe_allow_html=True)
            else:
                emoji_html = '<span style="font-size: 25px;">👎</span>'
                st.write(f"##### `Review:` {sentiment.capitalize()} {emoji_html}", unsafe_allow_html=True)

            st.write("-" * 40)


        # Flag to track if all reviews have been shown
        all_reviews_shown = False

        # Load more reviews on button click
        if len(movie_reviews) > 1:
            if not all_reviews_shown:
                if st.button("Show More Reviews"):
                    for review in movie_reviews[1:]:
                        st.write(f"**Author:** {review['author']}")
                        st.write(review['content'])
                        sentiment = analyze_sentiment(review['content'])
                        # Display sentiment with emoji
                        if sentiment == 'positive':
                            emoji_html = '<span style="font-size: 25px;">👍</span>'
                            st.write(f"##### `Review:` {sentiment.capitalize()} {emoji_html}", unsafe_allow_html=True)
                        else:
                            emoji_html = '<span style="font-size: 25px;">👎</span>'
                            st.write(f"##### `Review:` {sentiment.capitalize()} {emoji_html}", unsafe_allow_html=True)
                        st.write("-" * 40)
                        
                    all_reviews_shown = True
                
        

        # Hide the button if all reviews have been shown
        if all_reviews_shown:
            st.button("Show Less Reviews", key="hide_button")
                    



    

    st.write("#### Recommendations:")
    
    num_cols = 5  # Adjust the number of columns as needed
    cols = st.columns(num_cols)
    
    image_size = (135, 220)  # Adjusted image size
    

    for i in range(len(names)):
        with cols[i % num_cols]:
            # Create a clickable button overlaying the image using HTML/CSS
            button_html = f"""
                <div style="position: relative; padding-button: 20px; width: {image_size[0]}px; height: {image_size[1]}px;">
                <img  src="{posters[i]}" alt="{names[i]}" style="width: 100%; height: 100%; object-fit: cover;">{names[i]}
                    <button style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: transparent; border: none; cursor: pointer;" onclick="selectMovie('{names[i]}')"></button>
                </div>
            """
            st.markdown(button_html, unsafe_allow_html=True)
            st.markdown(" <br><br><br><br> ", unsafe_allow_html=True)


# Footer
st.markdown('''
--------------------------------------------------------------
🎬 Movie Recommendation & Sentiment Analysis 🍿

Explore, Analyze, and Discover Movies with Streamlit!

🌟Machine Learning and Natural Language Processing 🤖

Created by [Mukesh Mushyakhwo]

Contact: [mukesh@mukeshmushyakhwo.com.np]

GitHub: [https://github.com/MukeshMushyakhwo]

📧 Feel free to reach out for questions, feedback, or collaboration opportunities.

Happy Movie Watching! 🎥🍿
--------------------------------------------------------------
''')


