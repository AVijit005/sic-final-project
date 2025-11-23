# Known Issues & Future Work

## Current Limitations
1. **Model doesn't retrain automatically** - Need to manually run `train_model.py` when adding new data
2. **Port 8000 hardcoded** - Sometimes conflicts with other apps
3. **No API authentication** - Anyone on localhost can access the API
4. **Large emails slow down** - Text truncation helps but not perfect

## Bugs Found (Fixed)
- ~~Case sensitivity in label comparison (content.js)~~ ✅ Fixed
- ~~"ham" vs "Not Spam" label inconsistency~~ ✅ Fixed  
- ~~CSS corruption when trying to add 3D brain icon~~ ✅ Switched to SVG

## Future Enhancements
- [ ] Add user feedback system (thumbs up/down on predictions)
- [ ] Implement caching for frequently scanned emails
- [ ] Add confidence explanation (why email was marked spam)
- [ ] Support for multiple languages (currently English only)
- [ ] Dark/Light theme toggle
- [ ] Export scan history as CSV

## Ideas Considered But Not Implemented
- **Neural network approach** - Overkill for this dataset size
- **Real-time Gmail scanning** - Privacy concerns, needs OAuth
- **Browser notifications** - Could be annoying
