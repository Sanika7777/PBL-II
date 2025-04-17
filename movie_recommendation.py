import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# Load the dataset
data = pd.read_csv(r'C:\Users\Madhavi\OneDrive\Desktop\ML-Workshop-master\pbl-II\dataset.csv')

# Preprocess the data
# Assuming the dataset has columns 'movie_title', 'genre', 'emotion', 'rating', 'lead_actors', 'release_year'
data = data.dropna(subset=['genre', 'emotion'])

# Split the data into training and testing sets
X = data['genre']  # Assuming 'genre' is used as the description
y = data['emotion']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Convert text data to numerical features using TF-IDF
vectorizer = TfidfVectorizer(max_features=5000)
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# Train a Random Forest Classifier
model = RandomForestClassifier(random_state=42)
model.fit(X_train_tfidf, y_train)

# Evaluate the model
y_pred = model.predict(X_test_tfidf)

# Enhance debugging and preprocessing in recommend_movies

def recommend_movies(user_mood):
    # Preprocess the input mood
    user_mood_tfidf = vectorizer.transform([user_mood])

    # Predict the mood category and log probabilities
    mood_probabilities = model.predict_proba(user_mood_tfidf)
    mood_category = model.predict(user_mood_tfidf)[0]
    print(f"Predicted Mood Category: {mood_category}")
    print(f"Prediction Probabilities: {mood_probabilities}")  # Debugging statement

    # Recommend movies matching the predicted mood
    recommended_movies = data[data['emotion'] == mood_category]
    print(f"Number of Movies Found: {len(recommended_movies)}")  # Debugging statement

    recommended_movies = recommended_movies.head(10)

    # Prepare the movie details with a short plot
    movie_details = []
    for _, row in recommended_movies.iterrows():
        plot = f"A {row['genre']} movie starring {row['lead_actors']} released in {row['release_year']} with a rating of {row['rating']}."
        movie_details.append({
            'Title': row['movie_title'],
            'Genre': row['genre'],
            'Rating': row['rating'],
            'Lead Actors': row['lead_actors'],
            'Release Year': row['release_year'],
            'Plot': plot
        })

    return movie_details

# Example usage
user_mood = input("Enter your current mood: ")
recommended_movies = recommend_movies(user_mood)
print("Recommended Movies:")
for movie in recommended_movies:
    print(f"Title: {movie['Title']}, Genre: {movie['Genre']}, Rating: {movie['Rating']}, Lead Actors: {movie['Lead Actors']}, Release Year: {movie['Release Year']}, Plot: {movie['Plot']}")