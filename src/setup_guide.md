# Setup Guide

## 1. Get Your Google Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your API key

## 2. Create Environment File

Create a `.env` file in the `src/` directory with the following content:

```
GOOGLE_API_KEY=your_actual_api_key_here
MEMORY_FILE=agent_memory.json
LOG_LEVEL=INFO
```

## 3. Install Dependencies

```bash
cd src
pip install -r requirements.txt
```

## 4. Run the Application

```bash
python main.py
```

## 5. Test the System

Try these example inputs:
- "Search for information about artificial intelligence"
- "Analyze the benefits of renewable energy"
- "Recommend books about machine learning" 