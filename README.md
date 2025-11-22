# Spam Email Detection - Chrome Extension

AI-powered spam detection system for Gmail with a modern, animated Chrome extension and Python backend.

## Features

- **Modern UI:** Vibrant neon colors, breathing animations, floating particles
- **Single Input:** Paste any email for instant analysis
- **4-Layer Detection:** Whitelist, financial domains, spam keywords, ML model
- **75% Accuracy Threshold:** Balanced spam detection
- **Real-time Gmail Integration:** Auto-scan opened emails
- **Transactional Email Recognition:** Detects legitimate financial services

## Tech Stack

### Frontend (Chrome Extension)
- Manifest V3
- Modern CSS animations (50+ keyframes)
- Glassmorphism design
- Responsive UI

### Backend (Python)
- FastAPI
- scikit-learn (Logistic Regression)
- NLTK for text processing
- TF-IDF vectorization

## Installation

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Train the model:
```bash
python model/train_model.py
```

5. Start the server:
```bash
python app.py
```

Server will run on `http://127.0.0.1:8000`

### Extension Setup

1. Open Chrome and go to `chrome://extensions/`
2. Enable "Developer mode"
3. Click "Load unpacked"
4. Select the `extension` folder
5. Pin the extension to your toolbar

## Usage

1. **Manual Analysis:**
   - Click extension icon
   - Paste complete email text
   - Click "Analyze"

2. **Gmail Integration:**
   - Open any email in Gmail
   - Click "Get from Gmail" in extension
   - Click "Analyze"

3. **Auto-Detection:**
   - Content script automatically scans opened emails
   - Red banner appears if spam detected

## Project Structure

```
spam-extension-project/
├── backend/
│   ├── data/
│   │   ├── spam.csv           # Training dataset
│   │   └── trusted_domains.csv # Whitelist
│   ├── model/
│   │   ├── train_model.py     # ML model training
│   │   ├── spam_model.pkl     # Trained model
│   │   └── vectorizer.pkl     # TF-IDF vectorizer
│   ├── app.py                 # FastAPI server
│   ├── requirements.txt       # Python dependencies
│   └── verify_model.py        # Model testing
├── extension/
│   ├── assets/                # Icons
│   ├── manifest.json          # Extension config
│   ├── popup.html            # Popup UI
│   ├── popup.css             # Styles & animations
│   ├── popup.js              # Popup logic
│   ├── content.js            # Gmail integration
│   └── background.js         # Service worker
└── README.md
```

## Detection Layers

1. **Whitelist Check:** Custom trusted domains
2. **Financial Domain Verification:** 30+ known services (SBI, Amazon Pay, etc.)
3. **Spam Keyword Detection:** 15+ spam indicators
4. **ML Model:** 75% confidence threshold

## Customization

### Add Trusted Domains
Edit `backend/data/trusted_domains.csv` - one domain per line

### Adjust Threshold
In `backend/app.py`, change `spam_threshold` value (currently 0.75)

### Retrain Model
Add emails to `backend/data/spam.csv` and run:
```bash
python model/train_model.py
```

## Performance

- **99.6% Training Accuracy**
- **75% Production Threshold** (optimized for real-world use)
- **Multi-layer filtering** reduces false positives
- **Recognizes 30+ financial services**

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## License

MIT License - feel free to use and modify!

## Author

Built with ❤️ for secure email management
