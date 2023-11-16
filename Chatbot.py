import wikipedia
import streamlit as st
import time  # Import time for the loading simulation
import pywhatkit  # Import the pywhatkit library for playing music
from datetime import datetime  # Import datetime to get the current time
import pyjokes  # Import pyjokes for jokes

st.title("💬 Hound ResearchBot")
st.caption("🚀 from HoundAi")

# Add an "About" section in the Streamlit menu
st.sidebar.title("About")
st.sidebar.info(
    "This chatbot was created by Louis Wesamoyo to assist with research. "
    "Feel free to ask questions or request information."
)

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    if msg["role"] == "assistant":
        st.chat_message("Hound").write(msg["content"])
    else:
        st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Initialize response with a default value
    response = ""

    # Check if the user asked about the creator
    if "who created you" in prompt.lower() or "who made you" in prompt.lower():
        response = "I was created by Louis Wesamoyo. And he told me to tell you I am still under development."

    # Check if the user wants to know the current time
    elif "current time" in prompt.lower() or "time now" in prompt.lower():
        current_time = datetime.now().strftime("%H:%M:%S")
        response = f"The current time is {current_time}."

    # Check if the user wants to play music on YouTube
    elif "play music" in prompt.lower():
        # Assuming the prompt contains the song name
        song_name = prompt.replace("play music", "").strip()
        pywhatkit.playonyt(song_name)
        response = f"Playing music on YouTube: {song_name}."

    # Check if the user wants to hear a joke
    elif "tell me a joke" in prompt.lower() or "joke" in prompt.lower():
        joke = pyjokes.get_joke()
        response = f"Sure, here's a joke for you: {joke}."

    else:
        # Use a spinner for loading animation
        with st.spinner("Fetching information..."):
            try:
                # Simulate a delay (replace with actual API call)
                time.sleep(2)

                # Use Wikipedia library to get information
                page = wikipedia.page(prompt)
                content = page.content

                # Display the content using st.markdown()
                st.markdown(content, unsafe_allow_html=True)
                st.session_state.messages.append({"role": "assistant", "content": content})
            except wikipedia.exceptions.DisambiguationError as e:
                content = f"Ambiguous query. Please be more specific. Options: {', '.join(e.options)}"
                st.markdown(content)
                st.session_state.messages.append({"role": "assistant", "content": content})
            except wikipedia.exceptions.PageError:
                content = "Sorry, I couldn't find information on that topic."
                st.markdown(content)
                st.session_state.messages.append({"role": "assistant", "content": content})

    # Add the bot's response to the conversation
    st.markdown(response, unsafe_allow_html=True)
    st.session_state.messages.append({"role": "assistant", "content": response})

# Conditionally add a button to scroll to the top using JavaScript
if "content" in locals() and st.button("↑ Scroll to Top"):
    st.markdown("""
    <script>
        document.getElementById('root').scrollIntoView({ behavior: 'smooth' });
    </script>
    """, unsafe_allow_html=True)
