# Development Notes

## Project Journey

### Initial Challenges
- Started with Logistic Regression but accuracy was around 75%
- Class imbalance (2172 ham vs 433 spam) was causing poor spam detection
- Realized I needed better preprocessing and class balancing

### Key Learnings

#### Model Selection
After experimenting with different approaches:
1. **Logistic Regression** - Good baseline (75% accuracy)
2. **Ensemble (Voting Classifier)** - Too complex, overfitting issues
3. **MultinomialNB** - Final choice! Best for spam detection with TF-IDF
   - Achieved 99.88% training accuracy
   - Works well with text classification
   - Faster inference than ensemble

#### Preprocessing Decisions
- Used NLTK PorterStemmer for word normalization
- TF-IDF with bigrams (1-2 grams) captures phrase patterns
- Text truncation to 5000 chars prevents memory issues
- Kept numbers and '$' in text (important for spam patterns)

#### UI/UX Evolution
- Started with simple rotating PNG icon
- Upgraded to animated SVG for modern look
- Changed labels from "ham"/"spam" to "Not Spam"/"Spam" for clarity
- Added multi-layer detection (whitelist, financial domains, keywords, ML)

### Technical Decisions

**Why 50% threshold?**
- Lower threshold (0.75) gave too many false negatives
- 50% provides better balance for real-world use
- Combined with rule-based checks (whitelist, financial domains)

**Why MultinomialNB over others?**
- Native probability estimates (good for confidence scores)
- Works well with TF-IDF features
- Computationally efficient
- Proven effective for spam classification

### Future Improvements
- [ ] Add user feedback loop to retrain model
- [ ] Implement API rate limiting
- [ ] Add batch prediction endpoint
- [ ] Create Firefox extension version
- [ ] Add email signature detection

### Resources Used
- scikit-learn documentation
- NLTK stemming guide
- FastAPI best practices
- Chrome Extension Manifest V3 docs

---

**Note:** This project taught me the importance of:
1. Proper class balancing in ML
2. Iterative model selection
3. Combining rule-based and ML approaches
4. User-friendly UI design
