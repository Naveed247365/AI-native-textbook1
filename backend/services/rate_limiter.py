"""
Rate limiter service for translation endpoints
Implements in-memory sliding window algorithm (10 requests per user per hour)
"""
import time
from collections import defaultdict
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)


class RateLimiter:
    """
    In-memory rate limiter using sliding window algorithm

    Limits: 10 translations per user per hour (3600 seconds)

    Note: This is a simple in-memory implementation suitable for single-instance deployments.
    For multi-instance/production deployments, consider using Redis for distributed rate limiting.
    """

    def __init__(self, max_requests: int = 10, window_seconds: int = 3600):
        """
        Initialize rate limiter

        Args:
            max_requests: Maximum number of requests allowed per window
            window_seconds: Time window in seconds (default: 3600 = 1 hour)
        """
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        # Store: {user_id: [timestamp1, timestamp2, ...]}
        self.request_history: Dict[str, List[float]] = defaultdict(list)
        logger.info(f"RateLimiter initialized: {max_requests} requests per {window_seconds}s")

    def check_rate_limit(self, user_id: str) -> tuple[bool, int]:
        """
        Check if user has exceeded rate limit

        Args:
            user_id: User identifier (UUID string)

        Returns:
            tuple[bool, int]: (is_allowed, retry_after_seconds)
            - is_allowed: True if request is allowed, False if rate limit exceeded
            - retry_after_seconds: Seconds until rate limit resets (0 if allowed)
        """
        current_time = time.time()
        cutoff_time = current_time - self.window_seconds

        # Get user's request history
        user_requests = self.request_history[user_id]

        # Remove timestamps outside the sliding window
        user_requests = [ts for ts in user_requests if ts > cutoff_time]
        self.request_history[user_id] = user_requests

        # Check if user has exceeded limit
        if len(user_requests) >= self.max_requests:
            # Calculate retry_after: time until oldest request expires
            oldest_timestamp = user_requests[0]
            retry_after = int(oldest_timestamp + self.window_seconds - current_time)

            logger.warning(
                f"Rate limit exceeded for user {user_id}: "
                f"{len(user_requests)}/{self.max_requests} requests in last {self.window_seconds}s. "
                f"Retry after {retry_after}s"
            )
            return False, retry_after

        # Record this request
        user_requests.append(current_time)
        self.request_history[user_id] = user_requests

        logger.debug(
            f"Rate limit check passed for user {user_id}: "
            f"{len(user_requests)}/{self.max_requests} requests in window"
        )
        return True, 0

    def reset_user(self, user_id: str) -> None:
        """
        Reset rate limit for a specific user (admin function)

        Args:
            user_id: User identifier to reset
        """
        if user_id in self.request_history:
            del self.request_history[user_id]
            logger.info(f"Rate limit reset for user {user_id}")

    def get_remaining_requests(self, user_id: str) -> int:
        """
        Get number of remaining requests for user in current window

        Args:
            user_id: User identifier

        Returns:
            int: Number of requests remaining
        """
        current_time = time.time()
        cutoff_time = current_time - self.window_seconds

        user_requests = self.request_history.get(user_id, [])
        user_requests = [ts for ts in user_requests if ts > cutoff_time]

        remaining = max(0, self.max_requests - len(user_requests))
        return remaining


# Global rate limiter instance (singleton)
# 10 translations per user per hour
translation_rate_limiter = RateLimiter(max_requests=10, window_seconds=3600)
