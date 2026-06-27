def needs_web_search(results):
    """
    Decide whether web search is needed.
    """

    if len(results) < 3:
        return True

    text = " ".join(chunk["text"] for chunk in results)

    # Very little retrieved text
    if len(text) < 1000:
        return True

    return False