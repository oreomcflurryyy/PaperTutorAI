"""
summary.py

Generate a structured summary of the uploaded paper.
"""

from rag.llm import summarize_paper


def generate_summary(context):

    summary_settings = {
        "max_tokens": 4000
    }

    return summarize_paper(
        context,
        summary_settings
    )