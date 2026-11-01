
import json
from google import genai
from google.genai import types

def normalize_text(text):
    return " ".join(text.split())

# -----------------------------------------
# GEMINI CONFIGURATION
# -----------------------------------------

client = genai.Client()

MODEL = "gemini-3.5-flash-lite"


# -----------------------------------------
# HIGHLIGHTING MODES
# -----------------------------------------

MODES = {
    "study": """
    Identify important academic information:
    - Definitions
    - Important concepts
    - Scientific facts
    - Key explanations
    - Important relationships between concepts
    """,

    "news": """
    Identify important information in the news:
    - Major events
    - Important people and organizations
    - Causes and consequences
    - Important developments
    - Significant facts and figures
    """,

    "general": """
    Identify the central information in the text:
    - Main ideas
    - Important statements
    - Key facts
    - Significant arguments
    - Important conclusions
    """,

    "definitions": """
    Focus specifically on:
    - Definitions of terms
    - Explanations of concepts
    - Technical terminology
    - Characteristics and properties
    """
}


# -----------------------------------------
# MAIN HIGHLIGHTING FUNCTION
# -----------------------------------------

def get_highlights(original_text, mode="study"):

    # Check input
    if not original_text.strip():
        return []

    # Check selected mode
    if mode not in MODES:
        raise ValueError("Invalid highlighting mode!")

    # Create prompt
    prompt = f"""
    You are an intelligent contextual text-highlighting system.

    Your job is to identify important passages in the
    provided text according to the selected mode.

    SELECTED MODE: {mode}

    MODE INSTRUCTIONS:
    {MODES[mode]}

    IMPORTANT RULES:

    1. Understand the meaning and context of the entire text.
    2. Select genuinely important words, phrases or sentences.
    3. Prioritize useful information over ordinary sentences.
    4. Return the EXACT original wording.
    5. Never rewrite, paraphrase or correct the source text.
    6. Every selected passage must appear exactly in the original text.
    7. Avoid highlighting too much text.
    8. Do not invent information.
    9. Provide a short reason for every selection.
    10. Return an empty highlights array if nothing is important.

    Return JSON in this structure:

    {{
        "highlights": [
            {{
                "text": "exact passage copied from original text",
                "reason": "why this passage is important"
            }}
        ]
    }}

    ORIGINAL TEXT:

    {original_text}
    """

    # Send request to Gemini
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json"
        )
    )

    # Parse JSON response
    result = json.loads("" if response.text==None else response.text)

    # -------------------------------------
    # VALIDATE AI OUTPUT
    # -------------------------------------

    valid_highlights = []

    for item in result.get("highlights", []):

        passage = item.get("text", "")
        reason = item.get("reason", "")

        # Ensure correct data types
        if not isinstance(passage, str):
            continue

        if not isinstance(reason, str):
            continue

        # Ensure passage exists in original text
        if passage and normalize_text(passage) in normalize_text(original_text):

            valid_highlights.append({
                "text": passage,
                "reason": reason
            })

        else:
            print("Rejected invalid passage:", passage)

    return valid_highlights


# -----------------------------------------
# TEST PROGRAM
# -----------------------------------------

if __name__ == "__main__":

    sample_text = """
    Artificial Intelligence is transforming the world.

    Machine learning is a subset of AI that enables computers
    to learn from data without being explicitly programmed.

    Deep learning uses neural networks with multiple layers.
    """

    print("Testing HighlightAI...\n")

    highlights = get_highlights(
        sample_text,
        mode="news"
    )

    if not highlights:
        print("No important passages found.")

    for item in highlights:

        print("\nImportant passage:")
        print(item["text"])

        print("Reason:")
        print(item["reason"])

        print("-" * 40)
