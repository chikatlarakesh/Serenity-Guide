import base64
import streamlit as st
import plotly.express as px
import pandas as pd
import requests
import random
import os
import datetime
from dotenv import load_dotenv
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu
import anthropic

# Load environment variables from .env file
load_dotenv()
# Retrieve the API key
claude_api_key = os.getenv("CLAUDE_API_KEY")

client = anthropic.Client(api_key=claude_api_key)

def anxiety_management_guide(mood, feeling_description, current_stress_level, recent_events):
    # Construct the message for ClaudeAI
    message = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=250,
        temperature=0.2,
        system=f"You are a helpful mental health assistant that helps users manage their anxiety based on their mood, feelings, stress level, and recent events. Provide recommendations for exercises and techniques to reduce anxiety based on the user's mood, {mood}, their feelings described as: {feeling_description}, their current stress level of {current_stress_level}, and recent events: {recent_events}.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"Task: Help me manage my anxiety. I'm feeling {mood}. Here's what I'm experiencing: {feeling_description}. My current stress level is {current_stress_level}, and these are some recent events that might have contributed: {recent_events}\n\nConsiderations:\nProvide tailored anxiety-reduction exercises.\nConsider the user's mood, stress level, feelings, and recent events.\nOffer practical and effective techniques.\nEnsure the suggestions are easy to follow."
                    }
                ]
            }
        ]
    )
    return message  # Return the message or response from ClaudeAI

# Set page config (must be the first Streamlit command)
st.set_page_config(page_title="Anxiety Relief App", page_icon=":relieved:", layout="centered")

# Data for mental health (sampled)
data = {
    'Activity': ['Meditation', 'Yoga', 'Breathing', 'Journaling', 'Music'],
    'Calmness_Level': [85, 78, 90, 75, 88]
}

@st.cache_data
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Animated background
page_bg_img = f"""
<style>
/* Animated background gradient */
[data-testid="stAppViewContainer"] > .main {{
background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
background-size: 400% 400%;
animation: gradientBG 15s ease infinite;
}}

[data-testid="stSidebar"] > div:first-child {{
background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
background-size: 400% 400%;
animation: gradientBG 15s ease infinite;
}}

[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
}}

[data-testid="stToolbar"] {{
right: 2rem;
}}

.main .block-container {{
    max-width: 900px;  /* Increase the width of the centered section */
    padding: 2rem 1rem;  /* Adjust padding for a more spacious look */
}}

@keyframes gradientBG {{
    0% {{
        background-position: 0% 50%;
    }}
    50% {{
        background-position: 100% 50%;
    }}
    100% {{
        background-position: 0% 50%;
    }}
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

def load_lottie_url(url: str):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

# Main function to control page navigation
def main():
    selected = option_menu(
        menu_title=None,
        options=["Home", "Calm Space", "About & Feedback"],
        icons=["house-door-fill", "cloud-sun-fill", "chat-dots-fill"],
        menu_icon="sun",
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "#333", "border-radius": "10px", "box-shadow": "0 4px 6px rgba(0, 0, 0, 0.1)"},
            "nav-link": {
                "font-size": "18px",
                "text-align": "center",
                "margin": "0px",
                "--hover-color": "#ddd",
                "border-radius": "10px",
                "color": "#fff",
                "background-color": "rgba(0, 0, 0, 0.8)",  # More opaque background
                "transition": "background-color 0.3s ease, transform 0.2s"
            },
            "nav-link-selected": {"background-color": "#04AA6D", "color": "#fff", "transform": "scale(1.1)"}
        }
    )

    if selected == "Home":
        show_main_page()
    elif selected == "Calm Space":
        soothing_sounds()
    elif selected == "About & Feedback":
        show_about_and_feedback()

def show_main_page():
    st.markdown(
    """
    <style>
    .centered-title {
        text-align: center;
        font-size: 2.5rem;
        font-weight: bold;
    }
    </style>
    <h1 class="centered-title">Welcome to SereniFi</h1>
    """, unsafe_allow_html=True
    )

    st.markdown('<h3 class="pulse" style="text-align: center;">Feel Calm, Centered, and Peaceful</h3>', unsafe_allow_html=True)

    st.image("https://images.pexels.com/photos/185801/pexels-photo-185801.jpeg?auto=compress&cs=tinysrgb&w=600", caption="Breathe and Relax", use_column_width=True)

    st.write("---")

    # Interactive content
    st.markdown("""
    ### Welcome to Your Oasis of Calm

    Imagine a sanctuary where you can escape the hustle and bustle of everyday life—this is your space to recharge and rejuvenate. Embracing mental health is not just about addressing issues; it's about nurturing your inner self and fostering a sense of tranquility.

    **Discover Your Path to Peace:**
    - **Mindful Breathing:** Click below to start a guided breathing exercise that helps calm your mind instantly.
    - **Relaxation Techniques:** Explore various methods to integrate relaxation into your daily routine.
    - **Personalized Tips:** Answer a quick survey to receive tailored advice for enhancing your well-being.

    **Engage with Us:**
    - Share your favorite relaxation techniques or feedback on how our platform helps you.

    Your path to a serene and fulfilling life starts here. Let’s embark on this journey together—take the first step today!
    """)

    # Interactive Widgets
    if st.button('Start Guided Breathing'):
        st.balloons()
        st.write("**Guided Breathing Exercise:** Inhale deeply through your nose for 4 seconds, hold for 4 seconds, and exhale slowly through your mouth. Repeat this process a few times to feel the calming effect.")

    st.write("---")

    # Survey for Personalized Tips
    st.subheader("Personalized Tips for You")
    with st.form(key='personalized_tips_form'):
        mood = st.radio("What's your current anxiety level?", ["Low", "Moderate", "High", "Overwhelmed"])
        submit_button = st.form_submit_button("Get Tips")
        if submit_button:
            tips = {
                "Low": "Keep up the great work! Stay consistent with mindfulness techniques.",
                "Moderate": "Take a moment to practice deep breathing.",
                "High": "Pause and try a guided meditation.",
                "Overwhelmed": "It's important to step away and take a break."
            }
            st.write(f"**Tip:** {tips[mood]}")

    st.write("---")

    st.markdown("""
    ### Embrace Your Journey to Wellness

    Taking care of your mental health is an ongoing journey that requires attention and effort. It's essential to recognize the value of setting aside time for yourself amidst your busy schedule. Activities such as mindfulness, relaxation exercises, and engaging in hobbies can significantly improve your overall well-being. 

    Remember, mental health is not just the absence of mental illness but a state of complete emotional, psychological, and social well-being. Incorporating small, positive changes into your daily routine can lead to a more balanced and fulfilling life. Embrace these practices with an open heart and notice the positive impact they have on your day-to-day life. 
    """)

    st.video("https://www.youtube.com/watch?v=inpok4MKVLM", start_time=10)

    st.write("---")

    st.markdown('<h4 style="text-align: center;">The Importance of Mental Health</h4>', unsafe_allow_html=True)

    st.write("Mental health is just as important as physical health, but often overlooked. It affects how we think, feel, and act in our daily lives. Prioritizing mental well-being can help us manage stress, connect with others, and make informed decisions. Let's work together to break the stigma and support each other on this journey.")
    
    # Graph of Calmness Levels
    df = pd.DataFrame(data)
    fig = px.bar(df, x='Activity', y='Calmness_Level', title='Calmness Level by Activity', color='Calmness_Level', color_continuous_scale='Viridis')
    st.plotly_chart(fig)

def soothing_sounds():
    st.title("Soothing Sounds")
    st.markdown("**Choose a soothing sound to help you relax:**")

    sounds = {
        "Rain Sounds": "https://www.youtube.com/watch?v=mnW1n8eG7yI",
        "Ocean Waves": "https://www.youtube.com/watch?v=WjHc_EvJlOw",
        "Forest Ambience": "https://www.youtube.com/watch?v=7yO9B6SmbN8",
        "Soft Piano": "https://www.youtube.com/watch?v=O8S8Hn_3mYk"
    }
    
    selected_sound = st.selectbox("Select a Sound:", list(sounds.keys()))
    st.video(sounds[selected_sound])

def show_about_and_feedback():
    st.title("About & Feedback")
    st.markdown("This application aims to provide a supportive space for individuals seeking to manage their anxiety and promote mental wellness.")

    st.subheader("Feedback")
    with st.form(key='feedback_form'):
        feedback = st.text_area("Your Feedback:")
        submit_feedback = st.form_submit_button("Submit Feedback")
        if submit_feedback:
            st.success("Thank you for your feedback! We appreciate your input.")

if __name__ == "__main__":
    main()
