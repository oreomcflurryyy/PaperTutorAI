def get_answer_settings(length: str):

    if length == "Short":
        return {
            "max_tokens": 350,
            "instruction": """
Give a concise answer.

Rules:
- Maximum 2 short paragraphs.
- No tables.
- Maximum 3 bullet points.
- Skip the Evidence section unless specifically asked.
- Keep Sources to one line.
"""
        }

    elif length == "Medium":
        return {
            "max_tokens": 800,
            "instruction": """
Give a balanced explanation.

Rules:
- 3-5 paragraphs.
- Use a few bullet points.
- Include a brief Evidence section.
"""
        }

    elif length == "Detailed":
        return {
            "max_tokens": 1800,
            "instruction": """
Explain thoroughly.

Rules:
- Use headings.
- Explain important concepts.
- Include Key Takeaways.
- Include Evidence.
"""
        }

    else:   # Very Detailed
        return {
            "max_tokens": 3500,
            "instruction": """
Teach like a university professor.

Rules:
- Comprehensive explanation.
- Use headings.
- Use bullet points.
- Include examples.
- Include Evidence.
- Include Sources.
"""
        }