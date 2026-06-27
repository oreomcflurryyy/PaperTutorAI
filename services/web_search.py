from ddgs import DDGS


def search_web(query, max_results=10):
    """
    Search the web and return the top results.
    """

    results = []

    with DDGS() as ddgs:

        for result in ddgs.text(
            query,
            max_results=max_results
        ):

            results.append(
                {
                    "title": result.get("title", ""),
                    "body": result.get("body", ""),
                    "url": result.get("href", "")
                }
            )

    return results