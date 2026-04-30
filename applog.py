import streamlit as st
from google import genai
import os
from dotenv import load_dotenv
import difflib
import re
import hashlib
import json
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
import io

load_dotenv()

st.set_page_config(
    page_title="AI Business Idea and Strategy Generator",
    page_icon="💡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================== AUTHENTICATION FUNCTIONS ====================

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    """Load users from JSON file"""
    if os.path.exists('users.json'):
        with open('users.json', 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    """Save users to JSON file"""
    with open('users.json', 'w') as f:
        json.dump(users, f, indent=4)

def load_history():
    """Load search history from JSON file"""
    if os.path.exists('search_history.json'):
        with open('search_history.json', 'r') as f:
            return json.load(f)
    return {}

def save_history(history):
    """Save search history to JSON file"""
    with open('search_history.json', 'w') as f:
        json.dump(history, f, indent=4)

def add_to_history(username, user_data, ideas, selected_idea=None, strategy=None):
    """Add a search to user history"""
    history = load_history()
    
    if username not in history:
        history[username] = []
    
    # Convert ideas to proper format for history
    formatted_ideas = []
    for idea in ideas:
        formatted_ideas.append({
            'title': idea.get('name', idea.get('title', 'Untitled')),
            'description': idea.get('tagline', idea.get('description', 'No description'))
        })
    
    entry = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'user_inputs': user_data,
        'generated_ideas': formatted_ideas,
        'selected_idea': selected_idea,
        'strategy': strategy
    }
    
    history[username].insert(0, entry)
    
    if len(history[username]) > 20:
        history[username] = history[username][:20]
    
    save_history(history)

def get_user_history(username):
    """Get search history for a specific user"""
    history = load_history()
    return history.get(username, [])

def clear_user_history(username):
    """Clear all history for a specific user"""
    history = load_history()
    if username in history:
        history[username] = []
        save_history(history)

def signup_page():
    """User registration page"""
    st.markdown("""
        <div style='text-align: center; padding: 2rem;'>
            <h1 style='background: linear-gradient(120deg, #667eea 0%, #764ba2 100%);
                       -webkit-background-clip: text;
                       -webkit-text-fill-color: transparent;
                       font-size: 3rem;'>
                💡 AI Business Generator
            </h1>
            <p style='font-size: 1.2rem; color: #718096;'>Create your account to get started</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
            <div style='background: white; padding: 2rem; border-radius: 15px; 
                        box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
        """, unsafe_allow_html=True)
        
        st.markdown("### 📝 Sign Up")
        
        new_username = st.text_input("Username", placeholder="Choose a username", key="signup_username")
        new_password = st.text_input("Password", type="password", placeholder="Choose a password", key="signup_password")
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter password", key="confirm_password")
        
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            if st.button("✅ Create Account", use_container_width=True):
                if not new_username or not new_password:
                    st.error("❌ Please fill all fields!")
                elif new_password != confirm_password:
                    st.error("❌ Passwords do not match!")
                elif len(new_password) < 6:
                    st.error("❌ Password must be at least 6 characters!")
                else:
                    users = load_users()
                    if new_username in users:
                        st.error("❌ Username already exists!")
                    else:
                        hashed_password = hash_password(new_password)
                        users[new_username] = hashed_password
                        save_users(users)
                        st.success("✅ Account created successfully! Please login.")
                        st.balloons()
        
        with col_btn2:
            if st.button("🔙 Back to Login", use_container_width=True):
                st.session_state['auth_page'] = 'login'
                st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)

def login_page():
    """User login page"""
    st.markdown("""
        <div style='text-align: center; padding: 2rem;'>
            <h1 style='background: linear-gradient(120deg, #667eea 0%, #764ba2 100%);
                       -webkit-background-clip: text;
                       -webkit-text-fill-color: transparent;
                       font-size: 3rem;'>
                💡 AI Business Generator
            </h1>
            <p style='font-size: 1.2rem; color: #718096;'>Get 5 personalized business ideas in seconds</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
            <div style='background: white; padding: 2rem; border-radius: 15px; 
                        box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
        """, unsafe_allow_html=True)
        
        st.markdown("### 🔐 Login")
        
        username = st.text_input("Username", placeholder="Enter your username", key="login_username")
        password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_password")
        
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            if st.button("🚀 Login", use_container_width=True):
                if not username or not password:
                    st.error("❌ Please fill all fields!")
                else:
                    users = load_users()
                    if username in users:
                        hashed_password = hash_password(password)
                        if users[username] == hashed_password:
                            st.session_state['authenticated'] = True
                            st.session_state['username'] = username
                            st.success(f"✅ Welcome back, {username}!")
                            st.rerun()
                        else:
                            st.error("❌ Incorrect password!")
                    else:
                        st.error("❌ Username not found!")
        
        with col_btn2:
            if st.button("📝 Sign Up", use_container_width=True):
                st.session_state['auth_page'] = 'signup'
                st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
        st.info("💡 **First time?** Click 'Sign Up' to create an account!")

def show_history_page():
    """Display user search history"""
    # Back button
    if st.button("⬅️ Back to Generate Ideas"):
        st.session_state['page'] = 'input'
        st.rerun()
    
    st.markdown("""
        <div class='app-header'>
            <div class='app-title'>📜 Your Search History</div>
            <p style='font-size: 1.2rem; color: #718096; margin-top: 1rem;'>
                View your past business idea searches
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    username = st.session_state['username']
    history = get_user_history(username)
    
    if not history:
        st.info("📭 No search history yet. Generate some business ideas to see them here!")
        if st.button("🚀 Generate New Ideas"):
            st.session_state['page'] = 'input'
            st.rerun()
        return
    
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("🗑️ Clear History", use_container_width=True):
            clear_user_history(username)
            st.success("✅ History cleared!")
            st.rerun()
    with col2:
        if st.button("➕ New Search", use_container_width=True):
            st.session_state['page'] = 'input'
            st.rerun()
    
    st.markdown(f"### 📊 Total Searches: {len(history)}")
    st.markdown("---")
    
    for idx, entry in enumerate(history):
        with st.expander(f"🔍 Search {idx + 1} - {entry['timestamp']}", expanded=(idx == 0)):
            
            st.markdown("#### 📝 Your Inputs:")
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**Interests:** {entry['user_inputs'].get('interests', 'N/A')}")
                skills = entry['user_inputs'].get('skills', [])
                if isinstance(skills, list):
                    st.markdown(f"**Skills:** {', '.join(skills)}")
                else:
                    st.markdown(f"**Skills:** {skills}")
                st.markdown(f"**Budget:** ₹{entry['user_inputs'].get('budget', 'N/A')}")
                st.markdown(f"**City:** {entry['user_inputs'].get('city', 'N/A')}")
            
            with col2:
                st.markdown(f"**Risk Tolerance:** {entry['user_inputs'].get('risk_tolerance', 'N/A')}")
                st.markdown(f"**Time Commitment:** {entry['user_inputs'].get('time_commitment', 'N/A')}")
                st.markdown(f"**Income Goal:** ₹{entry['user_inputs'].get('income_goal', 'N/A')}/month")
                st.markdown(f"**Business Type:** {entry['user_inputs'].get('business_type', 'N/A')}")
            
            st.markdown("---")
            
            st.markdown("#### 💡 Generated Ideas:")
            for i, idea in enumerate(entry['generated_ideas'], 1):
                col_idea, col_btn = st.columns([4, 1])
                with col_idea:
                    st.markdown(f"**{i}. {idea.get('title', 'Untitled')}**")
                    st.markdown(f"{idea.get('description', 'No description')}")
                with col_btn:
                    # Show View button for ALL ideas, but only functional for the one with strategy
                    is_selected = entry.get('selected_idea') == idea.get('title')
                    has_strategy = entry.get('strategy') is not None
                    
                    if is_selected and has_strategy:
                        # This idea has a strategy - blue button
                        if st.button("👁️ View", key=f"view_idea_{idx}_{i}", help="View full strategy", type="primary"):
                            # Set up session state to view this strategy
                            st.session_state['view_from_history'] = {
                                'idea': {'name': idea.get('title'), 'tagline': idea.get('description')},
                                'strategy': entry.get('strategy'),
                                'user_data': entry.get('user_inputs')
                            }
                            st.session_state['page'] = 'strategy'
                            st.session_state['previous_page'] = 'history'
                            st.rerun()
                    else:
                        # No strategy for this idea - disabled button
                        st.button("👁️ View", key=f"view_idea_{idx}_{i}", disabled=True, help="No strategy generated for this idea")
                st.markdown("")
            
            if entry.get('selected_idea'):
                st.markdown("---")
                st.markdown("#### ⭐ Selected Idea:")
                st.info(f"**{entry['selected_idea']}**")
                
                if entry.get('strategy'):
                    st.markdown("#### 📋 Full Strategy Generated:")
                    st.success("✅ Strategy was created for this idea")
                    
                    # Show preview of strategy
                    st.text_area("Strategy Preview:", entry['strategy'], height=200, key=f"preview_{idx}", disabled=True)

# ==================== SESSION STATE INITIALIZATION ====================

if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = ''
if 'auth_page' not in st.session_state:
    st.session_state['auth_page'] = 'login'
if 'page' not in st.session_state:
    st.session_state.page = 'input'
if 'business_ideas' not in st.session_state:
    st.session_state.business_ideas = []
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}
if 'show_error' not in st.session_state:
    st.session_state.show_error = False
if 'error_messages' not in st.session_state:
    st.session_state.error_messages = []
if 'previous_page' not in st.session_state:
    st.session_state.previous_page = None

# ==================== CHECK AUTHENTICATION ====================

if not st.session_state['authenticated']:
    if st.session_state['auth_page'] == 'login':
        login_page()
    else:
        signup_page()
    st.stop()

# ==================== SIDEBAR NAVIGATION ====================
with st.sidebar:
    st.markdown(f"### 👤 {st.session_state['username']}")
    
    st.markdown("### 🧭 Navigation")
    if st.button("🏠 Generate Ideas", use_container_width=True):
        st.session_state['page'] = 'input'
        st.rerun()
    
    if st.button("📜 View History", use_container_width=True):
        st.session_state['previous_page'] = st.session_state.get('page', 'input')
        st.session_state['page'] = 'history'
        st.rerun()
    
    st.markdown("---")
    
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state['authenticated'] = False
        st.session_state['username'] = ''
        st.session_state['page'] = 'input'
        st.session_state['business_ideas'] = []
        st.session_state['user_data'] = {}
        st.rerun()

# Show history page if selected
if st.session_state['page'] == 'history':
    show_history_page()
    st.stop()

# Custom CSS with enhanced styling
st.markdown("""
    <style>
    .main { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }
    
    .app-header {
        text-align: center;
        padding: 2rem;
        background: white;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .app-title {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(120deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Required field indicator */
    .required-star {
        color: #e53e3e;
        font-size: 1.2rem;
        font-weight: bold;
        margin-left: 0.2rem;
    }
    
    /* Custom label styling */
    .stTextInput label, .stTextArea label, .stMultiSelect label, .stSelectbox label {
        font-weight: 600 !important;
        color: #2d3748 !important;
    }
    
    /* Blue styling for selected skills */
    .stMultiSelect [data-baseweb="tag"] {
        background-color: #667eea !important;
        border: 2px solid #5568d3 !important;
    }
    
    .stMultiSelect [data-baseweb="tag"] span {
        color: white !important;
    }
    
    /* Character counter */
    .char-counter {
        font-size: 0.85rem;
        color: #718096;
        margin-top: -0.5rem;
        margin-bottom: 1rem;
        text-align: right;
    }
    
    .char-counter.warning {
        color: #d69e2e;
        font-weight: bold;
    }
    
    .char-counter.error {
        color: #e53e3e;
        font-weight: bold;
    }
    
    /* Error popup styling */
    .error-popup {
        position: fixed;
        top: 20px;
        right: 20px;
        background: white;
        border-left: 5px solid #e53e3e;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        z-index: 9999;
        max-width: 400px;
        animation: slideIn 0.3s ease-out;
    }
    
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    .error-popup-title {
        color: #e53e3e;
        font-weight: bold;
        font-size: 1.2rem;
        margin-bottom: 0.5rem;
    }
    
    .error-popup-message {
        color: #2d3748;
        font-size: 0.95rem;
        line-height: 1.5;
    }
    
    /* Input field styling */
    .stTextInput input, .stTextArea textarea {
        border: 2px solid #e2e8f0 !important;
        border-radius: 8px !important;
    }
    
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 1px #667eea !important;
    }
    
    /* Disable submit button styling */
    .stButton button:disabled {
        background: #cbd5e0 !important;
        color: #a0aec0 !important;
        cursor: not-allowed !important;
    }
    
    .idea-card {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: transform 0.3s;
        border-left: 5px solid #667eea;
        height: 100%;
        display: flex;
        flex-direction: column;
    }
    
    .idea-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .idea-content {
        flex: 1;
        display: flex;
        flex-direction: column;
    }
    
    .idea-header {
        display: flex;
        align-items: flex-start;
        margin-bottom: 1rem;
    }
    
    .idea-description {
        flex: 1;
        line-height: 1.6;
        color: #4a5568;
        margin-bottom: 1.5rem;
    }
    
    .idea-footer {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        gap: 1rem;
        margin-top: auto;
    }
    
    .idea-stat {
        text-align: center;
        padding: 0.75rem;
        background: #f7fafc;
        border-radius: 8px;
    }
    
    .idea-stat-label {
        font-size: 0.75rem;
        color: #718096;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .idea-stat-value {
        font-size: 1rem;
        color: #2d3748;
        font-weight: 600;
        margin-top: 0.25rem;
    }
    
    .idea-number {
        display: inline-block;
        background: linear-gradient(120deg, #667eea 0%, #764ba2 100%);
        color: white;
        width: 45px;
        height: 45px;
        border-radius: 50%;
        text-align: center;
        line-height: 45px;
        font-weight: bold;
        font-size: 1.3rem;
    }
    
    .idea-title {
        font-size: 1.8rem;
        font-weight: bold;
        color: #2d3748;
        margin: 1rem 0;
    }
    
    .highlight-box {
        background: #f7fafc;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
    }
    
    .highlight-label {
        font-weight: bold;
        color: #667eea;
        font-size: 0.9rem;
    }
    
    .highlight-value {
        color: #2d3748;
        font-size: 1.1rem;
        margin-top: 0.5rem;
    }
    
    .stButton>button {
        background: linear-gradient(120deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: bold;
        padding: 0.75rem 2rem;
        border-radius: 25px;
        border: none;
        font-size: 1.1rem;
        width: 100%;
    }
    
    .stButton>button:hover:not(:disabled) {
        background: linear-gradient(120deg, #764ba2 0%, #667eea 100%);
        transform: scale(1.02);
    }
    
    .strategy-box {
        background: white;
        padding: 2.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Comprehensive list of valid Indian cities
VALID_INDIAN_CITIES = [
    "Mumbai", "Delhi", "Bangalore", "Bengaluru", "Hyderabad", "Chennai", "Kolkata", "Calcutta",
    "Pune", "Ahmedabad", "Surat", "Jaipur", "Lucknow", "Kanpur", "Nagpur", "Indore",
    "Thiruvananthapuram", "Trivandrum", "Bhopal", "Patna", "Raipur", "Ranchi", "Gandhinagar",
    "Shimla", "Jammu", "Srinagar", "Chandigarh", "Dehradun", "Panaji", "Guwahati", "Imphal",
    "Shillong", "Aizawl", "Kohima", "Agartala", "Itanagar", "Dispur", "Gangtok", "Port Blair",
    "Thane", "Visakhapatnam", "Vizag", "Vadodara", "Baroda", "Ghaziabad", "Ludhiana", "Agra",
    "Nashik", "Faridabad", "Meerut", "Rajkot", "Varanasi", "Banaras", "Aurangabad", "Dhanbad",
    "Amritsar", "Navi Mumbai", "Allahabad", "Prayagraj", "Howrah", "Coimbatore", "Jabalpur",
    "Gwalior", "Vijayawada", "Jodhpur", "Madurai", "Kota", "Solapur", "Hubli", "Dharwad",
    "Mysore", "Mysuru", "Tiruchirappalli", "Trichy", "Bareilly", "Aligarh", "Tiruppur",
    "Moradabad", "Jalandhar", "Bhubaneswar", "Salem", "Warangal", "Guntur", "Bhiwandi",
    "Saharanpur", "Gorakhpur", "Bikaner", "Amravati", "Noida", "Jamshedpur", "Bhilai",
    "Cuttack", "Firozabad", "Kochi", "Cochin", "Nellore", "Bhavnagar", "Durgapur", "Asansol",
    "Rourkela", "Nanded", "Kolhapur", "Ajmer", "Akola", "Gulbarga", "Kalaburagi", "Jamnagar",
    "Ujjain", "Loni", "Siliguri", "Jhansi", "Ulhasnagar", "Sangli", "Mangalore", "Mangaluru",
    "Erode", "Belgaum", "Belagavi", "Ambattur", "Tirunelveli", "Malegaon", "Gaya", "Jalgaon",
    "Udaipur", "Maheshtala", "Davanagere", "Kozhikode", "Calicut", "Kurnool", "Rajahmundry",
    "Bokaro", "South Dumdum", "Bellary", "Patiala", "Gopalpur", "Bhagalpur", "Muzaffarnagar",
    "Bhatpara", "Panihati", "Latur", "Dhule", "Tirupati", "Rohtak", "Korba", "Bhilwara",
    "Berhampur", "Muzaffarpur", "Ahmednagar", "Mathura", "Kollam", "Avadi", "Kadapa",
    "Kamarhati", "Sambalpur", "Bilaspur", "Shahjahanpur", "Satara", "Bijapur", "Rampur",
    "Shivamogga", "Shimoga", "Chandrapur", "Junagadh", "Thrissur", "Alwar", "Bardhaman",
    "Kulti", "Kakinada", "Nizamabad", "Parbhani", "Tumkur", "Khammam", "Ozhukarai",
    "Bihar Sharif", "Panipat", "Darbhanga", "Bally", "Dewas", "Ichalkaranji", "Karnal",
    "Bathinda", "Jalna", "Eluru", "Barasat", "Purnia", "Satna", "Mau", "Sonipat",
    "Farrukhabad", "Sagar", "Durg", "Ratlam", "Hapur", "Arrah", "Karimnagar", "Anantapur",
    "Etawah", "Ambernath", "North Dumdum", "Bharatpur", "Begusarai", "New Delhi", "Gandhidham",
    "Baranagar", "Tiruvottiyur", "Puducherry", "Pondicherry", "Sikar", "Thoothukudi",
    "Tuticorin", "Rewa", "Mirzapur", "Raichur", "Pali", "Ramagundam", "Haridwar", "Hardwar",
    "Vijapur", "Katihar", "Naihati", "Nadiad", "Yamunanagar", "English Bazar", "Unnao",
    "Surendranagar", "Hugli", "Hooghly", "Alappuzha", "Alleppey", "Kottayam", "Machilipatnam",
    "Adoni", "Udupi", "Kaithal", "Vizianagaram", "Nagercoil", "Nagarcoil", "Thanjavur",
    "Tanjore", "Murwara", "Katni", "Kharagpur", "Dindigul", "Vellore", "Ernakulam",
    "Palakkad", "Palghat", "Bidar", "Munger", "Panchkula", "Burhanpur", "Hospet",
    "Nangloi Jat", "Malda", "Ongole", "Deoghar", "Chapra", "Haldia", "Khandwa",
    "Nandurbar", "Morena", "Amroha", "Anand", "Bhusawal", "Orai", "Bahraich", "Vapi",
    "Chirala", "Chittoor", "Bhuj", "Dibrugarh", "Silchar", "Khanna", "Greater Noida",
    "Gurgaon", "Gurugram", "Vasai", "Virar", "Kalyan", "Dombivli", "Ulwe", "Kharghar"
]

CITIES_LOWER = [city.lower() for city in VALID_INDIAN_CITIES]

# Valid interest keywords (for validation)
VALID_INTEREST_KEYWORDS = [
    "technology", "tech", "coding", "programming", "software", "computer", "ai", "ml",
    "cooking", "food", "baking", "culinary", "recipe", "chef", "restaurant",
    "fitness", "gym", "health", "wellness", "yoga", "sports", "exercise", "nutrition",
    "education", "teaching", "training", "learning", "coaching", "tutor", "mentor",
    "art", "design", "creative", "photography", "painting", "drawing", "graphic",
    "music", "singing", "instrument", "dance", "performance", "entertainment",
    "business", "entrepreneur", "startup", "finance", "marketing", "sales",
    "fashion", "style", "clothing", "apparel", "boutique", "retail",
    "travel", "tourism", "adventure", "hospitality", "hotel",
    "writing", "content", "blogging", "journalism", "copywriting",
    "social", "media", "digital", "online", "internet", "web",
    "beauty", "cosmetics", "skincare", "salon", "makeup", "spa",
    "automotive", "car", "vehicle", "mechanic", "repair",
    "real estate", "property", "housing", "construction", "architecture",
    "consulting", "advisory", "strategy", "management", "leadership",
    "agriculture", "farming", "organic", "gardening", "plants",
    "handicraft", "handmade", "craft", "artisan", "diy",
    "electronics", "gadgets", "mobile", "hardware", "iot",
    "gaming", "esports", "video games", "streaming",
    "pets", "animals", "veterinary", "grooming",
    "events", "planning", "wedding", "party", "celebration"
]

def find_closest_city(input_city, max_matches=3):
    """Find closest matching cities using fuzzy matching"""
    input_lower = input_city.lower().strip()
    
    if input_lower in CITIES_LOWER:
        idx = CITIES_LOWER.index(input_lower)
        return True, VALID_INDIAN_CITIES[idx], []
    
    matches = difflib.get_close_matches(input_lower, CITIES_LOWER, n=max_matches, cutoff=0.6)
    
    if matches:
        suggestions = [VALID_INDIAN_CITIES[CITIES_LOWER.index(m)] for m in matches]
        return False, None, suggestions
    
    return False, None, []

def validate_city(city):
    """Validate city with spell checking"""
    if not city or not city.strip():
        return False, "Please enter a city name", []
    
    found, correct_city, suggestions = find_closest_city(city)
    
    if found:
        return True, correct_city, []
    elif suggestions:
        return False, f"Did you mean: {', '.join(suggestions)}?", suggestions
    else:
        return False, "Please enter a valid Indian city", []

def validate_interests(text):
    """Validate interests field"""
    if not text or not text.strip():
        return False, "Field of Interest is required"
    
    text = text.strip()
    
    if len(text) > 50:
        return False, f"Maximum 50 characters allowed (current: {len(text)})"
    
    if len(text) < 5:
        return False, "Please enter at least 5 characters"
    
    if not any(c.isalpha() for c in text):
        return False, "Interest must contain letters"
    
    # Check if interest is relevant
    text_lower = text.lower()
    is_relevant = any(keyword in text_lower for keyword in VALID_INTEREST_KEYWORDS)
    
    if not is_relevant:
        return False, "Please enter relevant business interests (e.g., Technology, Cooking, Fitness, Education, etc.)"
    
    return True, text

def validate_numeric_input(value, field_name):
    """Validate numeric inputs (budget/income)"""
    if not value or not value.strip():
        return False, 0, f"{field_name} is required"
    
    # Remove common currency symbols but keep numbers
    cleaned = value.strip().replace(',', '').replace('₹', '').replace('Rs', '').replace('rs', '')
    
    # Check if it contains only numbers and decimal point
    if not re.match(r'^\d+\.?\d*$', cleaned):
        return False, 0, f"{field_name} must contain only numbers"
    
    try:
        amount = float(cleaned)
        if amount <= 0:
            return False, 0, f"{field_name} must be greater than 0"
        return True, amount, f"₹{amount:,.2f}"
    except:
        return False, 0, f"Invalid {field_name}"

def show_error_popup(errors):
    """Display error messages in a popup"""
    if errors:
        error_html = '<div class="error-popup">'
        error_html += '<div class="error-popup-title">⚠️ Please Fix These Errors</div>'
        for error in errors:
            error_html += f'<div class="error-popup-message">• {error}</div>'
        error_html += '</div>'
        st.markdown(error_html, unsafe_allow_html=True)

def generate_top_5_ideas(interests, skills, budget, location, risk_level, time_commitment, income_goal, business_type):
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        return None
    
    client = genai.Client(api_key=api_key)
    
    prompt = f"""Generate EXACTLY 5 business ideas for:
Interests: {interests}
Skills: {', '.join(skills)}
Budget: ₹{budget:,.2f}
Location: {location}, India
Risk: {risk_level}
Time: {time_commitment}
Income Goal: ₹{income_goal:,.2f}
Type: {business_type}

Format each idea EXACTLY like this:

IDEA 1
NAME: [Creative business name]
TAGLINE: [One catchy sentence]
DESCRIPTION: [2-3 sentences explaining the concept]
INVESTMENT: [Amount needed]
TIMELINE: [Launch time]
INCOME: [Monthly potential]

(Repeat for IDEA 2, 3, 4, 5)

Make each unique and specific to {location}."""

    try:
        response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
        return response.text
    except Exception as e:
        st.error(f"Error: {e}")
        return None

def parse_ideas(text):
    ideas = []
    current = {}
    
    for line in text.split('\n'):
        line = line.strip()
        
        if 'IDEA' in line and any(c.isdigit() for c in line):
            if current:
                ideas.append(current)
            num = ''.join(c for c in line if c.isdigit())[:1]
            current = {'number': num}
        
        for field in ['NAME', 'TAGLINE', 'DESCRIPTION', 'INVESTMENT', 'TIMELINE', 'INCOME']:
            if line.startswith(field + ':') or line.startswith('**' + field):
                value = line.split(':', 1)[1] if ':' in line else line
                current[field.lower()] = value.strip().replace('**', '').replace('*', '')
    
    if current:
        ideas.append(current)
    
    return ideas[:5]

def generate_strategy(idea, user_data):
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        return "Error: API key missing"
    
    client = genai.Client(api_key=api_key)
    
    prompt = f"""Create detailed business strategy for:
**{idea.get('name', 'Business')}**
{idea.get('description', '')}

Context:
Budget: {user_data['budget']}
Location: {user_data['location']}
Skills: {', '.join(user_data['skills'])}
Time: {user_data['time_commitment']}
Goal: {user_data['income_goal']}

Provide comprehensive strategy with:

## 1. Executive Summary

## 2. Market Analysis
- Target market
- Competition
- Trends

## 3. Business Model
- Revenue streams
- Pricing
- Costs

## 4. Investment Breakdown
[Detailed budget]

## 5. Launch Timeline
[Month by month]

## 6. Marketing Strategy
- Channels
- Budget
- Tactics

## 7. Operations
- Daily operations
- Team needed
- Tools

## 8. Financial Projections
- Year 1 revenue
- Break-even
- Growth

## 9. Risks & Mitigation

## 10. Action Steps
[Numbered immediate steps]"""

    try:
        response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
        return response.text
    except Exception as e:
        return f"Error: {e}"

# PAGE 1: INPUT
def show_input_page():
    st.markdown("""
        <div class="app-header">
            <h1 class="app-title">💡 AI Powered Business Idea and Strategy Generator</h1>
            <p style="color: #666; font-size: 1.2rem;">Get 5 personalized business ideas in seconds</p>
        </div>
    """, unsafe_allow_html=True)
    
    with st.form("form", clear_on_submit=False):
        st.markdown("### 📝 Your Profile")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Personal Info")
            
            # Field of Interest with character counter and red star
            st.markdown('<label>Field of Interest <span class="required-star">*</span></label>', unsafe_allow_html=True)
            interests = st.text_area("", max_chars=50, placeholder="Technology, Cooking, Fitness...", 
                                    help="Enter your main interests (max 50 characters)", key="interests", label_visibility="collapsed")
            char_count = len(interests) if interests else 0
            char_class = "error" if char_count > 50 else ("warning" if char_count > 40 else "")
            st.markdown(f'<div class="char-counter {char_class}">{char_count}/50 characters</div>', unsafe_allow_html=True)
            
            # Skills with red star
            st.markdown('<label>Skills <span class="required-star">*</span></label>', unsafe_allow_html=True)
            skills = st.multiselect("", [
                "Programming/Coding", "Digital Marketing", "Graphic Design",
                "Content Writing", "Teaching/Training", "Sales",
                "Photography", "Social Media", "Data Analysis", "Other"
            ], help="Select your key skills", key="skills", label_visibility="collapsed")
            
            # City with red star
            st.markdown('<label>City <span class="required-star">*</span></label>', unsafe_allow_html=True)
            location = st.text_input("", placeholder="Mumbai, Bangalore, Delhi...",
                                    help="Enter your Indian city", key="location", label_visibility="collapsed")
            
            # Budget with red star - numeric only
            st.markdown('<label>Budget (₹) <span class="required-star">*</span></label>', unsafe_allow_html=True)
            budget = st.text_input("", placeholder="50000",
                                  help="Enter numbers only", key="budget", label_visibility="collapsed")
        
        with col2:
            st.markdown("#### Preferences")
            
            risk_level = st.select_slider("Risk Tolerance",
                options=["Very Low", "Low", "Moderate", "High", "Very High"], value="Moderate")
            
            time_commitment = st.selectbox("Time Commitment", [
                "Part-time (10-20 hrs/week)", "Full-time (40+ hrs/week)",
                "Weekends only", "Flexible"
            ])
            
            # Income Goal with red star - numeric only
            st.markdown('<label>Income Goal (₹/month) <span class="required-star">*</span></label>', unsafe_allow_html=True)
            income_goal = st.text_input("", placeholder="50000",
                                       help="Enter numbers only", key="income_goal", label_visibility="collapsed")
            
            business_type = st.selectbox("Business Type", [
                "Online/E-commerce", "Service-based", "Product-based",
                "Consulting", "Freelancing", "Food & Beverage",
                "Technology/SaaS", "Education", "No Preference"
            ])
        
        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("🚀 Generate Top 5 Ideas")
    
    if submitted:
        errors = []
        
        # Validate interests
        interest_valid, interest_result = validate_interests(interests)
        if not interest_valid:
            errors.append(f"Field of Interest: {interest_result}")
        else:
            interests = interest_result
        
        # Validate skills
        if not skills:
            errors.append("Skills: Please select at least one skill")
        
        # Validate city
        city_valid, city_result, suggestions = validate_city(location)
        if not city_valid:
            error_msg = f"City: {city_result}"
            if suggestions:
                error_msg += f" Suggestions: {', '.join(suggestions)}"
            errors.append(error_msg)
        else:
            location = city_result
        
        # Validate budget (numeric only)
        budget_valid, budget_amt, budget_msg = validate_numeric_input(budget, "Budget")
        if not budget_valid:
            errors.append(f"Budget: {budget_msg}")
        
        # Validate income goal (numeric only)
        income_valid, income_amt, income_msg = validate_numeric_input(income_goal, "Income Goal")
        if not income_valid:
            errors.append(f"Income Goal: {income_msg}")
        
        if errors:
            # Show error popup
            show_error_popup(errors)
        else:
            st.session_state.user_data = {
                'interests': interests, 'skills': skills, 'budget': budget_msg,
                'budget_amount': budget_amt, 'location': location,
                'risk_level': risk_level, 'time_commitment': time_commitment,
                'income_goal': income_msg, 'income_amount': income_amt,
                'business_type': business_type
            }
            
            with st.spinner("🤖 AI is analyzing your profile and generating 5 personalized ideas..."):
                response = generate_top_5_ideas(
                    interests, skills, budget_amt, location,
                    risk_level, time_commitment, income_amt, business_type
                )
                
                if response:
                    ideas = parse_ideas(response)
                    if len(ideas) >= 3:
                        st.session_state.business_ideas = ideas
                        # Save ideas to history
                        add_to_history(
                            st.session_state['username'],
                            st.session_state['user_data'],
                            ideas
                        )
                        st.session_state.page = 'ideas'
                        st.rerun()
                    else:
                        st.error("Could not generate enough ideas. Please try again.")

# PAGE 2: IDEAS
def show_ideas_page():
    st.markdown("""
        <div class="app-header">
            <h1 class="app-title">🎉 Your Top 5 Business Ideas</h1>
            <p style="color: #666; font-size: 1.1rem;">Click "Explore Strategy" to see the full plan</p>
        </div>
    """, unsafe_allow_html=True)
    
    user_data = st.session_state.user_data
    st.info(f"📍 {user_data['location']} | 💰 Budget: {user_data['budget']} | 🎯 Goal: {user_data['income_goal']}/mo")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    for idx, idea in enumerate(st.session_state.business_ideas):
        st.markdown(f"""
            <div class="idea-card">
                <div class="idea-header">
                    <span class="idea-number">{idea.get('number', idx+1)}</span>
                </div>
                <div class="idea-content">
                    <h2 class="idea-title">{idea.get('name', f'Idea {idx+1}')}</h2>
                    <p style="color: #667eea; font-style: italic; font-size: 1.1rem; margin-bottom: 1rem;">
                        {idea.get('tagline', '')}
                    </p>
                    <div class="idea-description">
                        {idea.get('description', '')}
                    </div>
                    <div class="idea-footer">
                        <div class="idea-stat">
                            <div class="idea-stat-label">💰 Investment</div>
                            <div class="idea-stat-value">{idea.get('investment', 'N/A')}</div>
                        </div>
                        <div class="idea-stat">
                            <div class="idea-stat-label">⏱️ Timeline</div>
                            <div class="idea-stat-value">{idea.get('timeline', 'N/A')}</div>
                        </div>
                        <div class="idea-stat">
                            <div class="idea-stat-label">📊 Income</div>
                            <div class="idea-stat-value">{idea.get('income', 'N/A')}</div>
                        </div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Explore button below the card
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
        with col_btn2:
            if st.button(f"🔍 Explore Full Strategy", key=f"btn_{idx}"):
                st.session_state.selected_idea = idea
                st.session_state.page = 'strategy'
                st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("← Start Over"):
        st.session_state.page = 'input'
        st.rerun()

# PAGE 3: STRATEGY
def show_strategy_page():
    # Check if viewing from history or from normal flow
    if 'view_from_history' in st.session_state and st.session_state.get('view_from_history'):
        history_data = st.session_state['view_from_history']
        idea = history_data['idea']
        strategy_text = history_data['strategy']
        # Set it in session state for the page to use
        st.session_state.strategy = strategy_text
        st.session_state.strategy_for = idea.get('name')
    else:
        idea = st.session_state.selected_idea
    
    st.markdown(f"""
        <div style="background: linear-gradient(120deg, #667eea 0%, #764ba2 100%); 
                    color: white; padding: 2.5rem; border-radius: 15px; margin-bottom: 2rem;">
            <h1 style="margin: 0; font-size: 2.5rem;">📊 Complete Strategy</h1>
            <h2 style="margin-top: 1rem; font-weight: normal;">{idea.get('name', '')}</h2>
            <p style="font-style: italic; opacity: 0.9;">{idea.get('tagline', '')}</p>
        </div>
    """, unsafe_allow_html=True)
    
    if 'strategy' not in st.session_state or st.session_state.get('strategy_for') != idea.get('name'):
        with st.spinner("🤖 Creating detailed strategy..."):
            strategy = generate_strategy(idea, st.session_state.user_data)
            st.session_state.strategy = strategy
            st.session_state.strategy_for = idea.get('name')
            # Save strategy to history
            add_to_history(
                st.session_state['username'],
                st.session_state['user_data'],
                st.session_state['business_ideas'],
                idea.get('name', 'Untitled'),
                strategy
            )
    
    st.markdown(f'<div class="strategy-box">{st.session_state.strategy}</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Check if viewing from history
        if st.session_state.get('previous_page') == 'history':
            # From history: show "Ideas" button
            if st.button("💡 Ideas", use_container_width=True, help="Go to all ideas"):
                if 'view_from_history' in st.session_state:
                    del st.session_state['view_from_history']
                st.session_state['page'] = 'ideas'
                st.session_state['previous_page'] = None
                st.rerun()
        else:
            # Normal flow: show "Back to Ideas"
            if st.button("← Back to Ideas", use_container_width=True):
                st.session_state.page = 'ideas'
                st.rerun()
    
    with col2:
        # Generate New Ideas button
        if st.button("🔄 Generate New Ideas", use_container_width=True):
            if 'view_from_history' in st.session_state:
                del st.session_state['view_from_history']
            st.session_state.page = 'input'
            st.session_state.business_ideas = []
            st.session_state['previous_page'] = None
            st.rerun()
    
    with col3:
        # Create PDF for strategy download
        try:
            from reportlab.lib.enums import TA_CENTER
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch)
            styles = getSampleStyleSheet()
            story = []
            
            # Title
            title_style = styles['Heading1']
            title_style.alignment = TA_CENTER
            story.append(Paragraph(f"Business Strategy: {idea.get('name', 'Untitled')}", title_style))
            story.append(Spacer(1, 0.3*inch))
            
            # Timestamp
            from datetime import datetime
            story.append(Paragraph(f"<i>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</i>", styles['Normal']))
            story.append(Spacer(1, 0.3*inch))
            
            # Strategy content
            for line_text in st.session_state.strategy.split('\n'):
                if line_text.strip():
                    clean_text = line_text.strip().replace('<', '&lt;').replace('>', '&gt;')
                    
                    if clean_text.startswith('#') or clean_text.startswith('**') or (len(clean_text) < 50 and clean_text.isupper()):
                        clean_text = clean_text.replace('#', '').replace('**', '').strip()
                        story.append(Paragraph(clean_text, styles['Heading2']))
                        story.append(Spacer(1, 0.15*inch))
                    elif clean_text.startswith('•') or clean_text.startswith('-'):
                        story.append(Paragraph(f"&nbsp;&nbsp;&nbsp;{clean_text}", styles['Normal']))
                        story.append(Spacer(1, 0.08*inch))
                    else:
                        story.append(Paragraph(clean_text, styles['Normal']))
                        story.append(Spacer(1, 0.12*inch))
            
            doc.build(story)
            pdf_data = buffer.getvalue()
            
            # Clean filename
            import re
            clean_name = re.sub(r'[^a-zA-Z0-9_-]', '_', idea.get('name', 'strategy'))
            clean_name = clean_name[:50]
            
            st.download_button("📥 Download PDF", pdf_data,
                              file_name=f"{clean_name}_strategy.pdf",
                              mime="application/pdf")
        except Exception as e:
            # Fallback to TXT
            st.download_button("📥 Download TXT", st.session_state.strategy,
                              file_name=f"{idea.get('name', 'strategy')}.txt")


# ROUTER
def main():
    page = st.session_state.page
    
    if page == 'input':
        show_input_page()
    elif page == 'ideas':
        show_ideas_page()
    elif page == 'strategy':
        show_strategy_page()

if __name__ == "__main__":
    main()