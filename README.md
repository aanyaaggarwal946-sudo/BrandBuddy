# BrandBuddy – Gemini Knowledge-Based Streamlit Chatbot

## Files
- `app.py`: Streamlit interface and Gemini integration.
- `knowledge_base.py`: BrandBuddy digital-marketing knowledge manual.
- `.streamlit/secrets.toml`: API key configuration.
- `requirements.txt`: required packages.

## Setup (Windows PowerShell)
1. Extract this ZIP.
2. Open PowerShell inside the extracted `brandbuddy_streamlit` folder.
3. Open `.streamlit/secrets.toml` and replace the placeholder with your NEW Gemini API key:

```toml
GEMINI_API_KEY = "YOUR_NEW_GEMINI_API_KEY"
```

Keep this file private. Do not upload it to GitHub or share screenshots containing the key.

4. Install packages:

```powershell
py -m pip install -r requirements.txt
```

If `py` is unavailable but `python` works:

```powershell
python -m pip install -r requirements.txt
```

5. Start the app:

```powershell
py -m streamlit run app.py
```

Or:

```powershell
python -m streamlit run app.py
```

Streamlit normally opens at http://localhost:8501.

## Notes
- The app uses the `google-genai` SDK and `gemini-2.5-flash` model identifier.
- Model availability depends on your API project and region. If unavailable, change the model identifier in `app.py` to a Gemini Flash model available to your API key.
- Conversation history remains in Streamlit session state and is not permanently stored.
- This is a knowledge-guided chatbot: the manual is sent with each request. It is not a retrieval-augmented generation (RAG) system.
