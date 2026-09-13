from my_agent.tools.resilience import TokenBucket, with_exponential_backoff
import threading

# Throttle to strictly 1 request every 2 seconds, no bursts
search_bucket = TokenBucket(rate_per_second=0.5, capacity=1)
# Max 2 concurrent requests
search_semaphore = threading.Semaphore(2)

@with_exponential_backoff(
    max_attempts=5,
    initial_delay=1,
    max_delay=20,
)
def _search(query: str) -> str:
    from duckduckgo_search import DDGS
    with DDGS() as ddgs:
        results = [r for r in ddgs.text(query, max_results=5)]
        if not results:
            return "No results found."
        
        formatted_results = "\n\n".join([
            f"Title: {r['title']}\nSnippet: {r['body']}\nURL: {r['href']}" 
            for r in results
        ])
        return formatted_results

def google_search(query: str) -> str:
    """Search the web for real-world problems, complaints, and information.
    
    Args:
        query: The search query (e.g., 'site:reddit.com "I hate manually"').
    """
    search_bucket.acquire()
    with search_semaphore:
        try:
            return _search(query)
        except Exception as e:
            return f"Search failed after retries: {e}"
