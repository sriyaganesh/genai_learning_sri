from duckduckgo_search import DDGS

def search_web(query, max_results=5):
    results_text = []

    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=max_results)

        for r in results:
            title = r.get("title", "")
            snippet = r.get("body", "")
            link = r.get("href", "")

            results_text.append(
                f"Title: {title}\nSnippet: {snippet}\nURL: {link}\n"
            )

    return "\n".join(results_text)