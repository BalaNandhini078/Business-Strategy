#!/bin/bash

# AI-Powered Business Idea Generator - Run Script

echo "🚀 Starting AI-Powered Business Idea Generator..."
echo ""

# Check if GOOGLE_API_KEY is set
if [ -z "$GOOGLE_API_KEY" ]; then
    echo "⚠️  Warning: GOOGLE_API_KEY environment variable is not set!"
    echo "Please set it using:"
    echo "  export GOOGLE_API_KEY='your-api-key-here'"
    echo ""
    read -p "Do you want to continue anyway? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check if requirements are installed
if ! python -c "import streamlit" 2>/dev/null; then
    echo "📦 Installing requirements..."
    pip install -r requirements.txt
fi

echo ""
echo "✅ Starting Streamlit application..."
echo "🌐 The app will open in your browser automatically"
echo ""

# Run the Streamlit app
streamlit run app.py
