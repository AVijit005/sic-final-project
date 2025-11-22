from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import pickle
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import os

# Initialize App
app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, including chrome-extension://
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Model & Vectorizer
model_path = "model/spam_model.pkl"
vectorizer_path = "model/vectorizer.pkl"
whitelist_path = "data/trusted_domains.csv"

model = None
vectorizer = None
trusted_domains = set()

# Ensure NLTK data is downloaded
nltk.download('stopwords')
ps = PorterStemmer()

def load_resources():
    global model, vectorizer, trusted_domains
    if os.path.exists(model_path) and os.path.exists(vectorizer_path):
        model = pickle.load(open(model_path, "rb"))
        vectorizer = pickle.load(open(vectorizer_path, "rb"))
    else:
        print("Model or vectorizer not found. Please train the model first.")
    
    if os.path.exists(whitelist_path):
        # Read CSV with no header, assuming first column is domain
        df = pd.read_csv(whitelist_path, header=None)
        if not df.empty:
            trusted_domains = set(df[0].astype(str).str.lower().values)
    else:
        print("Trusted domains file not found.")

print("DEBUG: Calling load_resources...")
load_resources()
print("DEBUG: load_resources finished.")

class EmailRequest(BaseModel):
    sender: str
    subject: str
    body: str

STOPWORDS = set(stopwords.words('english'))

def preprocess_text(text):
    text = re.sub('[^a-zA-Z]', ' ', text)
    text = text.lower()
    text = text.split()
    text = [ps.stem(word) for word in text if not word in STOPWORDS]
    text = ' '.join(text)
    return text

def check_whitelist(sender):
    if not trusted_domains:
        return False
    
    sender = sender.lower()
    domain = sender.split('@')[-1]
    
    if domain in trusted_domains:
        return True
    return False

def is_financial_or_transactional(sender, subject, body):
    """
    Check if email is from legitimate financial/transactional services.
    ONLY checks sender domain - keywords alone are not enough!
    """
    sender = sender.lower()
    
    # Known legitimate financial and service domains
    trusted_financial_domains = [
        'sbi.co.in', 'icicibank.com', 'hdfcbank.com', 'axisbank.com',
        'amazonpay.in', 'paytm.com', 'phonepe.com', 'googlepay.com',
        'paypal.com', 'razorpay.com', 'instamojo.com',
        'amazon.in', 'amazon.com', 'flipkart.com',
        'swiggy.com', 'zomato.com', 'uber.com', 'ola.com',
        'irctc.co.in', 'makemytrip.com', 'goibibo.com',
        'netflix.com', 'spotify.com', 'hotstar.com',
        'google.com', 'microsoft.com', 'apple.com'
    ]
    
    # ONLY check sender domain - don't trust keywords alone
    domain = sender.split('@')[-1] if '@' in sender else ''
    for trusted_domain in trusted_financial_domains:
        if trusted_domain in domain:
            return True
    
    return False

def has_spam_indicators(subject, body):
    """
    Check for strong spam indicators that should override other checks.
    Returns True if email has obvious spam characteristics.
    """
    text = f"{subject} {body}".lower()
    
    # Strong spam indicators
    spam_keywords = [
        'winner', 'won', 'lottery', 'prize', 'claim now', 'urgent act',
        'limited time', 'click here now', 'congratulations!!!',
        'free money', 'million dollars', 'bitcoin', 'cryptocurrency',
        'act now', 'expire soon', 'verify your account immediately',
        'suspended account', 'confirm identity', 'wire transfer'
    ]
    
    # Count spam indicators
    spam_count = sum(1 for keyword in spam_keywords if keyword in text)
    
    # If 2+ strong spam indicators, definitely spam
    return spam_count >= 2

@app.post("/predict")
def predict_spam(email: EmailRequest):
    if model is None or vectorizer is None:
        raise HTTPException(status_code=500, detail="Model not loaded")

    # Layer 1: Check Whitelist (CSV-based trusted domains)
    if check_whitelist(email.sender):
        return {
            "label": "whitelisted",
            "confidence": 1.0,
            "reason": "Sender is in the whitelist"
        }
    
    # Layer 2: Check for known financial/transactional services
    if is_financial_or_transactional(email.sender, email.subject, email.body):
        return {
            "label": "ham",
            "confidence": 0.95,
            "reason": "Recognized as legitimate financial or transactional email"
        }
    
    # Layer 2.5: Check for obvious spam indicators (override ML if found)
    if has_spam_indicators(email.subject, email.body):
        return {
            "label": "spam",
            "confidence": 0.95,
            "reason": "Contains multiple spam indicators"
        }

    # Layer 3: ML Model Prediction with Balanced Threshold
    full_text = f"{email.subject} {email.body}"
    processed_text = preprocess_text(full_text)
    vectorized_text = vectorizer.transform([processed_text]).toarray()
    
    prediction = model.predict(vectorized_text)[0]
    proba = model.predict_proba(vectorized_text)[0]
    
    # Balanced threshold: 75% for optimal accuracy
    # Not too strict (80% missed spam), not too loose (70% too many false positives)
    spam_threshold = 0.75  # Sweet spot between precision and recall
    spam_probability = float(proba[1])  # Probability of spam (class 1)
    ham_probability = float(proba[0])   # Probability of ham (class 0)
    
    if spam_probability >= spam_threshold:
        label = "spam"
        confidence = spam_probability
    else:
        label = "ham"
        confidence = ham_probability
    
    reason = "Contains suspicious keywords and patterns" if label == "spam" else "Appears to be legitimate"

    return {
        "label": label,
        "confidence": round(confidence, 2),
        "reason": reason
    }

@app.get("/")
def read_root():
    return {"message": "Spam Detection API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
