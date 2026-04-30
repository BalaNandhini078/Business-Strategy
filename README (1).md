# 💡 AI-Powered Business Idea & Strategy Generator

An intelligent Streamlit application that generates personalized business ideas using Google Gemini AI based on your skills, interests, budget, and preferences.

## ✨ Features

- **Personalized Business Ideas**: Get AI-generated business ideas tailored to your profile
- **Comprehensive Strategy**: Receive detailed business plans including market analysis, revenue models, and action steps
- **Input Validation**: 
  - Valid Indian city verification
  - Budget amount validation in Indian Rupees (₹)
  - Income goal validation
- **Interactive UI**: Beautiful, user-friendly interface with gradient designs
- **Idea Enhancement**: Option to enhance and refine generated ideas
- **Downloadable Results**: Save your business ideas as text files

## 🚀 Installation

1. **Clone or download this repository**

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Set up your Google API key**:

You need a Google API key to use Gemini AI. Get one from [Google AI Studio](https://aistudio.google.com/app/apikey).

Set the environment variable:

**On Linux/Mac**:
```bash
export GOOGLE_API_KEY='your-api-key-here'
```

**On Windows (Command Prompt)**:
```cmd
set GOOGLE_API_KEY=your-api-key-here
```

**On Windows (PowerShell)**:
```powershell
$env:GOOGLE_API_KEY='your-api-key-here'
```

## 🎯 Usage

1. **Run the application**:
```bash
streamlit run app.py
```

2. **Fill in the form with your details**:
   - **Interests & Passions**: What you're passionate about
   - **Skills**: Select from predefined skills or add your own
   - **Location**: Enter a valid Indian city (validates against a list of major cities)
   - **Budget**: Your available investment in Indian Rupees (₹)
   - **Risk Tolerance**: How much risk you're willing to take
   - **Time Commitment**: How much time you can dedicate
   - **Income Goal**: Desired monthly income in ₹
   - **Business Type**: Your preferred business model

3. **Generate Ideas**:
   - Click "Generate Business Idea" to get AI-powered recommendations
   - View comprehensive business strategy
   - Enhance the idea for variations
   - Download your business plan

## 📋 Input Parameters

### Required Fields:
- **Interests**: Text area for your passions and interests
- **Skills**: Multi-select dropdown with options like:
  - Programming/Coding
  - Digital Marketing
  - Graphic Design
  - Content Writing
  - And many more...
- **Location**: Text input (validates against Indian cities)
- **Budget**: Amount in Indian Rupees (₹)
- **Risk Level**: Slider from Very Low to Very High
- **Time Commitment**: Dropdown with options:
  - Part-time (10-20 hours/week)
  - Full-time (40+ hours/week)
  - Weekends only
  - Flexible/As needed
  - 1-2 hours daily
- **Income Goal**: Monthly target in ₹
- **Business Type Preference**: Dropdown with options:
  - Online/E-commerce
  - Service-based
  - Product-based
  - Consulting/Coaching
  - And more...

## 🔐 Validation Features

1. **City Validation**: 
   - Checks if the entered city is in the list of valid Indian cities
   - Provides suggestions for similar city names if not found
   - Case-insensitive matching

2. **Budget Validation**:
   - Accepts amounts in ₹ (Indian Rupees)
   - Removes currency symbols and commas
   - Validates numeric values
   - Ensures positive amounts

3. **Income Goal Validation**:
   - Same validation as budget
   - Warns if goals seem unrealistic for the given budget

## 📊 What You Get

The AI generates a comprehensive business strategy including:

1. **Business Idea Name** - Creative and catchy name
2. **Executive Summary** - Core concept overview
3. **Why This Idea?** - Personalized matching explanation
4. **Market Opportunity** - Target market analysis
5. **Unique Value Proposition** - What makes it special
6. **Revenue Model** - How to make money
7. **Investment Breakdown** - Detailed budget allocation
8. **Timeline to Launch** - Realistic launch schedule
9. **Risk Assessment** - Risks and mitigation strategies
10. **First Steps** - Actionable tasks to start today
11. **Growth Potential** - Path to income goals
12. **Resources Needed** - Tools, partners, skills

## 🎨 Features

- **Beautiful UI**: Gradient designs and modern interface
- **Responsive Layout**: Works on desktop and mobile
- **Real-time Validation**: Immediate feedback on inputs
- **AI-Powered**: Uses Claude Sonnet 4 for intelligent suggestions
- **Download Option**: Save your business ideas
- **Enhance Feature**: Get variations and improvements

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **AI Engine**: Google Gemini AI (Gemini 1.5 Pro)
- **Language**: Python 3.8+

## 📝 Example Usage

```python
# Sample valid inputs:
Interests: "Technology, Online education, Content creation"
Skills: ["Programming/Coding", "Content Writing", "Digital Marketing"]
Location: "Bangalore"
Budget: "200000" or "₹2,00,000"
Risk Level: "Moderate"
Time Commitment: "Part-time (10-20 hours/week)"
Income Goal: "80000" or "₹80,000"
Business Type: "Online/E-commerce"
```

## ⚠️ Important Notes

1. **API Key Required**: You must have a valid Google API key (free tier available)
2. **Internet Connection**: Required for AI generation
3. **City Names**: Must be valid Indian cities from the predefined list
4. **Currency**: All amounts are in Indian Rupees (₹)

## 🐛 Troubleshooting

**Error: "Please make sure your GOOGLE_API_KEY is set correctly"**
- Solution: Set your environment variable correctly before running the app

**City not found**
- Solution: Check spelling or use the suggested cities from the validation message

**Invalid budget/income goal**
- Solution: Enter numeric values only (commas and ₹ symbol are optional)

## 📄 License

This project is for educational and commercial use.

## 🤝 Contributing

Feel free to fork this project and add your own enhancements!

## 📧 Support

For issues or questions, please open an issue in the repository.

---

**Built with ❤️ using Streamlit and Google Gemini AI**
