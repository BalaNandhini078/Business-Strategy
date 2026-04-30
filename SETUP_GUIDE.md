# 🚀 Quick Setup Guide - Google Gemini API

## Step 1: Get Your Google API Key

1. Visit **Google AI Studio**: https://aistudio.google.com/app/apikey
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Choose **"Create API key in new project"** or select an existing project
5. Copy your API key (it will look like: `AIza...`)

⚠️ **Important**: Keep your API key secure and never share it publicly!

## Step 2: Set Up Environment Variable

### On Linux/Mac (Terminal):
```bash
export GOOGLE_API_KEY='your-api-key-here'
```

To make it permanent, add to `~/.bashrc` or `~/.zshrc`:
```bash
echo 'export GOOGLE_API_KEY="your-api-key-here"' >> ~/.bashrc
source ~/.bashrc
```

### On Windows (Command Prompt):
```cmd
set GOOGLE_API_KEY=your-api-key-here
```

### On Windows (PowerShell):
```powershell
$env:GOOGLE_API_KEY='your-api-key-here'
```

To make it permanent on Windows:
1. Search for "Environment Variables" in Windows search
2. Click "Edit the system environment variables"
3. Click "Environment Variables" button
4. Under "User variables", click "New"
5. Variable name: `GOOGLE_API_KEY`
6. Variable value: your API key
7. Click OK

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 4: Run the Application

### On Linux/Mac:
```bash
./run.sh
```

### On Windows:
```cmd
run.bat
```

### Or manually:
```bash
streamlit run app.py
```

## Step 5: Start Creating Business Ideas! 🎉

The app will automatically open in your browser at `http://localhost:8501`

---

## Free Tier Limits (Google Gemini API)

- **Gemini 1.5 Pro**: 2 requests per minute (free tier)
- **Gemini 1.5 Flash**: 15 requests per minute (free tier)
- More than enough for personal use!

For higher limits, you can upgrade to a paid plan.

---

## Troubleshooting

### "Please make sure your GOOGLE_API_KEY is set correctly"
- Double-check your API key is correct
- Make sure environment variable is set in the same terminal/session
- Try restarting your terminal after setting the variable

### "Module not found" errors
- Run: `pip install -r requirements.txt`
- Make sure you're using Python 3.8 or higher

### "Streamlit command not found"
- Run: `pip install streamlit`
- Or: `python -m pip install streamlit`

---

## Need Help?

- **Google AI Documentation**: https://ai.google.dev/docs
- **Streamlit Documentation**: https://docs.streamlit.io
- **Check API Key**: https://aistudio.google.com/app/apikey

Happy Business Planning! 💼✨
