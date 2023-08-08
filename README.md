# Movie Recommendation with Sentiment Analysis System
The "Movie Recommendation with Sentiment Analysis System" is an innovative project that combines the power of content-based movie recommendation with sentiment analysis of reviews. The system enhances the movie exploration process by analyzing reviews related to the selected movie. It employs a pre-trained sentiment analysis model to determine whether the reviews are positive or negative in nature. This sentiment analysis provides users with insights into the overall reception of the movie by the audience. The sentiment analysis aspect of the system leverages a pre-trained model from the GitHub repository *[Mukesh Mushyakhwo](https://github.com/MukeshMushyakhwo/Review-Sentiment-Analysis.)*. This integration enhances the accuracy and reliability of sentiment classification.

## Dataset
* Dataset was downoaded from kaggle *[TMDB 5000 Movie Dataset]("https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata")*
* Poster of movies was fetched from TMDB API



## Features

- Content-based movie recommendations based on user input.
- Detailed movie information, including cast, genre, and release date.
- Sentiment analysis of movie reviews to determine positive/negative sentiments.
- User-friendly interface for seamless interaction.
- Personalization and learning to improve recommendations over time.

## Getting Started

1. Clone this repository: `git clone https://github.com/your_username/movie-recommendation-system.git`
2. Install required dependencies: `pip install requirements.txt`

## Usage

1. Run the Streamlit app: `streamlit run app.py`
2. Input your movie preferences or search for a specific movie title.
3. Explore recommended movies and review sentiment analysis.

## Text Preprocessing

Text preprocessing is performed to clean and normalize review text before sentiment analysis. It involves:
- Converting text to lowercase.
- Removing links, HTML tags, punctuation, and numbers.
- Removing extra spaces.

## Cosine Similarity

Cosine similarity is used to measure the similarity between movies based on their feature vectors. It helps in suggesting movies that are similar to the user's preferences.

## Dependencies

- [Streamlit](https://streamlit.io/)
- [joblib](https://joblib.readthedocs.io/)
- [pandas](https://pandas.pydata.org/)
- [requests](https://docs.python-requests.org/en/latest/)
- [scikit-learn](https://scikit-learn.org)

---

## 🎬 Movie Recommendation & Sentiment Analysis 🍿

Explore, Analyze, and Discover Movies 

🌟Machine Learning and Natural Language Processing 🤖


Created by **Mukesh Mushyakhwo**

Contact: mukesh@mukeshmushyakhwo.com.np

GitHub: https://github.com/MukeshMushyakhwo

📧 Feel free to reach out for questions, feedback, or collaboration opportunities.

Happy Movie Watching! 🎥🍿
