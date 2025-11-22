import pickle
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import os

# Ensure NLTK data
nltk.download('stopwords')
ps = PorterStemmer()

STOPWORDS = set(stopwords.words('english'))

def preprocess_text(text):
    text = re.sub('[^a-zA-Z]', ' ', text)
    text = text.lower()
    text = text.split()
    text = [ps.stem(word) for word in text if not word in STOPWORDS]
    text = ' '.join(text)
    return text

def verify():
    print("Loading model...")
    if not os.path.exists('model/spam_model.pkl'):
        print("Model file not found!")
        return
    
    model = pickle.load(open('model/spam_model.pkl', 'rb'))
    vectorizer = pickle.load(open('model/vectorizer.pkl', 'rb'))
    
    test_email = "WINNER!! As a valued network customer you have been selected to receive a £900 prize reward!"
    print(f"Testing with: {test_email}")
    
    processed = preprocess_text(test_email)
    vectorized = vectorizer.transform([processed]).toarray()
    prediction = model.predict(vectorized)[0]
    
    if prediction == 1:
        print("Result: SPAM (Correct)")
    else:
        print("Result: HAM (Incorrect)")

if __name__ == "__main__":
    verify()
