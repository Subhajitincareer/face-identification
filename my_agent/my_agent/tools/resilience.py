import random
import time
import threading
import logging
from functools import wraps

# Setup basic logging for observability
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%H:%M:%S')
logger = logging.getLogger(__name__)

class TokenBucket:
    def __init__(self, rate_per_second: float, capacity: int):
        self.rate = rate_per_second
        self.capacity = capacity
        self.tokens = float(capacity)
        self.updated_at = time.monotonic()
        self.lock = threading.Lock()

    def acquire(self, tokens: int = 1):
        while True:
            with self.lock:
                now = time.monotonic()
                elapsed = now - self.updated_at

                self.tokens = min(
                    self.capacity,
                    self.tokens + elapsed * self.rate
                )
                self.updated_at = now

                if self.tokens >= tokens:
                    self.tokens -= tokens
                    return

                missing = tokens - self.tokens
                wait_time = missing / self.rate

            logger.info(f"[TokenBucket] Bucket empty. Waiting {wait_time:.2f}s to refill...")
            time.sleep(wait_time)

def with_exponential_backoff(
    max_attempts=5,
    initial_delay=1.0,
    max_delay=30.0,
    retry_exceptions=(Exception,),
):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            delay = initial_delay
            tool_name = func.__name__

            for attempt in range(1, max_attempts + 1):
                try:
                    start_time = time.time()
                    result = func(*args, **kwargs)
                    exec_time = time.time() - start_time
                    logger.info(f"[SUCCESS] Tool '{tool_name}' executed on attempt {attempt} in {exec_time:.2f}s")
                    return result

                except retry_exceptions as e:
                    if attempt == max_attempts:
                        logger.error(f"[FAILURE] Tool '{tool_name}' permanently failed after {max_attempts} attempts. Final Error: {e}")
                        raise e

                    jitter = random.uniform(0, delay * 0.25)
                    wait_time = min(delay + jitter, max_delay)
                    
                    logger.warning(f"[RETRY] Tool '{tool_name}' failed on attempt {attempt} ({e}). Retrying in {wait_time:.2f}s...")
                    time.sleep(wait_time)

                    delay = min(delay * 2, max_delay)

        return wrapper

    return decorator
