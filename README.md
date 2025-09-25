
```
 ▓░▒█████   ▒█████   ████████     ▒█████   █████  ████████ 
▓░▒██    ██ ██    ██    ██        ██   ██ ██   ██    ██    
▒░▒██    ██ ██    ██    ██        ███████ ██   ██    ██    
░▒ ██    ██ ██    ██    ██        ██   ██ ██   ██    ██    
 ░  █████    █████      ██        ██████   █████     ██    


```

# Welcome to the Cognitive Behavioral Therapy Bot

A Cognitive Behavioral Therapy chatbot that helps identify cognitive distortions in user input using spaCy's NLP capabilities.

## Features

- **Cognitive Distortion Detection**: Identifies 8 common CBT distortions using both exact phrase matching and semantic similarity
- **CBT Responses**: Provides thoughtful CBT reflections for each detected distortion
- **Interactive Chat Interface**: Clean, user-friendly console interface
- **Modular Architecture**: Well-organized code structure with separate modules for data, detection, and UI

## Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   python -m spacy download en_core_web_md
   ```
3. Run the chatbot:
   ```bash
   python app.py
   ```

## Project Structure

- `app.py` - Main entry point
- `cbt_data.py` - Cognitive distortion phrases and CBT responses
- `cbt_detector.py` - Core detection logic using spaCy
- `chatbot.py` - Interactive chat interface
- `requirements.txt` - Python dependencies

## Future Enhancements

- Add sentiment analysis
- Implement more cognitive distortions
- Add conversation history tracking
- Create web interface