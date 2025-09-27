from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# --- Gemini API Configuration ---
try:
    # Configure the API key from environment variables
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        st.error("🚨 GOOGLE_API_KEY not found. Please set it in your environment variables or a .env file.")
        st.stop()
    genai.configure(api_key=api_key)

    # --- Model Selection ---
    # Switching to 'gemini-pro' which is a standard and globally available model.
    model = genai.GenerativeModel('gemini-2.0-flash')

    # Initialize the chat session in Streamlit's session state
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])

except Exception as e:
    st.error(f"An error occurred during initialization: {e}")
    st.stop()


# --- Function to get Gemini response ---
def get_gemini_response(user_query):
    """
    Sends the user's query to the Gemini model and gets the response.
    """
    try:
        # Use the chat session from the session_state
        response = st.session_state.chat_session.send_message(user_query)
        return response.text
    except Exception as e:
        st.error(f"An error occurred while getting the response: {e}")
        return "Sorry, I encountered an error. Please try again."


# --- Streamlit App UI ---
st.set_page_config(
    page_title="Gemini Chatbot ✨",
    page_icon="🧸",
    layout="centered"
)

# --- Custom CSS for Child-Friendly UI ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;700&display=swap');

    html, body, [class*="st-"] {
        font-family: 'Nunito', sans-serif;
    }

    .stApp {
        background-color: #F0F8FF; /* Light Alice Blue background */
    }

    h1 {
        color: #FF6347; /* Tomato color for the main title */
        text-align: center;
    }
    
    .st-emotion-cache-1y4p8pa {
        padding-top: 2rem; /* Reduce top padding */
    }

    [data-testid="stChatMessage"] {
        background-color: #FFFFFF;
        border-radius: 20px;
        padding: 1rem 1.5rem;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
        border: 2px solid transparent;
        margin-bottom: 1rem;
    }
    
    [data-testid="stChatMessageContent"] p {
        font-size: 1.1rem;
    }

    /* User message styling */
    [data-testid="stChatMessage"]:has(div[data-testid="stAvatarIcon-user"]) {
        background-color: #C1E1C1; /* Pastel Green */
    }

    /* Assistant message styling */
    [data-testid="stChatMessage"]:has(div[data-testid="stAvatarIcon-assistant"]) {
        background-color: #FFDAB9; /* Peach Puff */
    }
    
    [data-testid="stChatInput"] {
        background-color: #FFFFFF;
        border-radius: 15px;
        border: 2px solid #FF6347;
    }
    
    .st-emotion-cache-usj992 { /* Send button styling */
        background-color: #FF6347 !important;
        color: white !important;
        border-radius: 10px;
    }

</style>
""", unsafe_allow_html=True)


st.title("ASK YOUR DOUBTS HERE")
st.write("I am here to help you with your questions!")

# Initialize chat history in session state if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# --- Chat Input and Submission ---
user_input = st.chat_input("What do you want to talk about?")

if user_input:
    # Add user's message to chat history and display it
    st.session_state.chat_history.append({"role": "user", "text": user_input})

    # Get Gemini's response
    with st.spinner("Thinking..."):
        gemini_response = get_gemini_response(user_input)
        st.session_state.chat_history.append({"role": "assistant", "text": gemini_response})

# --- Display Chat History ---
for message in st.session_state.chat_history:
    # Use an emoji for the avatar based on the role
    avatar = "🧑‍💻" if message["role"] == "user" else "🤖"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["text"])

