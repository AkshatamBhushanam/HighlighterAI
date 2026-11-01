
import re

def find_highlight_ranges(original_text, highlights):
    ranges = []

    for item in highlights:
        passage = item["text"]
        reason = item["reason"]

        # Allow spaces, tabs and line breaks to match each other
        words = passage.split()
        pattern = r"\s+".join(re.escape(word) for word in words)

        match = re.search(pattern, original_text)

        if match:
            ranges.append({
                "start": match.start(),
                "end": match.end(),
                "text": original_text[match.start():match.end()],
                "reason": reason
            })
        else:
            print("Could not locate passage:", passage)

    # Sort passages according to their position in the original text
    ranges.sort(key=lambda item: item["start"])

    return ranges



from html import escape


def create_highlighted_html(original_text, ranges):
    result = []
    previous_end = 0

    for item in ranges:
        start = item["start"]
        end = item["end"]

        # Avoid processing overlapping highlights
        if start < previous_end:
            continue

        # Preserve and safely escape the original text
        result.append(escape(original_text[previous_end:start]))

        highlighted_text = escape(original_text[start:end])
        safe_reason = escape(item["reason"], quote=True)

        result.append(
            f'<mark title="{safe_reason}" '
            f'style="background-color: #fff176; '
            f'padding: 2px; border-radius: 3px;">'
            f'{highlighted_text}</mark>'
        )

        previous_end = end

    result.append(escape(original_text[previous_end:]))

    # Preserve original spaces and line breaks when displayed
    return (
        '<div style="white-space: pre-wrap; line-height: 1.6;">'
        + "".join(result)
        + '</div>'
    )

if __name__ == "__main__":
    from highlight_engine import get_highlights

    sample_text = """
    Artificial Intelligence is transforming the world.

    Machine learning is a subset of AI that enables computers
    to learn from data without being explicitly programmed.

    Deep learning uses neural networks with multiple layers.
    """

    highlights = get_highlights(sample_text, mode="study")

    positions = find_highlight_ranges(sample_text, highlights)

    
    html = create_highlighted_html(sample_text, positions)

    print("\n\nHighlighted HTML:\n")
    print(html)
