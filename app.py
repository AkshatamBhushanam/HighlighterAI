

import os
import streamlit as st

# Get the API key from Streamlit Cloud secrets
# if it isn't already available as an environment variable.
if not os.getenv("GEMINI_API_KEY"):
    try:
        os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"]
    except Exception:
        st.error("Gemini API key is not configured.")
        st.stop()

from highlight_engine import get_highlights
from highlighter import find_highlight_ranges, create_highlighted_html


# Page configuration
st.set_page_config(
    page_title="HighlightAI",
    page_icon="✨",
    layout="centered"
)

st.markdown("""
<style>

/* Main highlight button */
div.stButton > button {
    background-color: #6b1599;
    color: white;
    border: white;
    border-radius: 10px;
    padding: 0.6rem 1rem;
    font-weight: 600;
    transition: 0.2s;
}

/* Button hover effect */
div.stButton > button:hover {
    background-color: #541178;
    color: white;
    border: white;
}

/* Button when clicked/focused */
div.stButton > button:focus {
    color: white;
    border: white;
}

</style>
""", unsafe_allow_html=True)



# Application heading
st.title("✨ HighlightAI")

st.caption("AI-powered contextual text highlighting")

st.divider()


# Mode selection
mode_options = {
    "📚 Study": "study",
    "📰 News": "news",
    "🌐 General": "general",
    "📖 Definitions": "definitions"
}

selected_mode = st.selectbox(
    "Choose your highlighting mode:",
    options=list(mode_options.keys())
)

mode = mode_options[selected_mode]


# Text input
original_text = st.text_area(
    "Paste your text here:",
    height=250,
    placeholder="Enter an article, textbook passage, notes, or any other text..."
)


# Highlight button
if st.button("✨ Highlight important text", use_container_width=True):

    if not original_text.strip():
        st.warning("Please enter some text first.")

    else:
        try:
            with st.spinner("AI is analyzing your text..."):

                # Ask Gemini to select important passages
                highlights = get_highlights(original_text, mode)

                # Find their positions in the original text
                positions = find_highlight_ranges(
                    original_text,
                    highlights
                )

                # Generate highlighted HTML
                highlighted_html = create_highlighted_html(
                    original_text,
                    positions
                )

            st.success(f"Found {len(positions)} important passages!")

            st.subheader("Your highlighted text")

            st.markdown(
                highlighted_html,
                unsafe_allow_html=True
            )

        except Exception as error:
            st.error("Something went wrong while processing your text.")
            st.caption(str(error))
