import pandas as pd
import pickle
import re
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import os

# Download NLTK data
nltk.download('stopwords')
STOPWORDS = set(stopwords.words('english'))

def preprocess_text(text):
    if not isinstance(text, str):
        return ""
    # Truncate to 1000 chars to speed up processing
    text = text[:1000]
    
    ps = PorterStemmer()
    text = re.sub('[^a-zA-Z]', ' ', text)
    text = text.lower()
    text = text.split()
    text = [ps.stem(word) for word in text if not word in STOPWORDS]
    text = ' '.join(text)
    return text

def train():
    print("DEBUG: Running updated train_model.py with global STOPWORDS")
    # Get script directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, '..', 'data', 'spam.csv')
    model_path = os.path.join(base_dir, 'spam_model.pkl')
    vectorizer_path = os.path.join(base_dir, 'vectorizer.pkl')

    print(f"Loading dataset from {data_path}...")
    try:
        df = pd.read_csv(data_path, encoding='latin-1')
    except FileNotFoundError:
        print(f"Error: spam.csv not found at {data_path}")
        return

    # Keep only necessary columns and rename
    # The new dataset has 'Body' and 'Label' columns.
    # Label is already 0 or 1.
    df = df[['Body', 'Label']]
    df.columns = ['message', 'label']

    print("Preprocessing data...")
    # Drop NaNs just in case
    df.dropna(inplace=True)
    df['message'] = df['message'].apply(preprocess_text)

    # Labels are already numeric (0/1), but let's ensure they are integers
    df['label'] = df['label'].astype(int)

    X = df['message']
    y = df['label']

    # Vectorization
    print("Vectorizing text...")
    cv = TfidfVectorizer(max_features=2500)
    X = cv.fit_transform(X).toarray()

    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=0)

    # Train
    print("Training model...")
    model = LogisticRegression(class_weight='balanced')
    model.fit(X_train, y_train)

    # Evaluate
    y_pred = model.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print(classification_report(y_test, y_pred))

    # Save
    print(f"Saving model to {model_path}...")
    pickle.dump(model, open(model_path, 'wb'))
    pickle.dump(cv, open(vectorizer_path, 'wb'))
    print("Done!")

if __name__ == "__main__":
    train()
