# Example: Feature Design Using the Reasoning Framework

This example demonstrates how to apply the 5-Phase Reasoning Model to design and implement a new feature: a rate limiter for an API.

## The Request

"We need to add rate limiting to our API to prevent abuse. Users should be limited to 100 requests per minute."

---

## Phase 1: Comprehension

### Problem Analysis

**What exactly is being asked?**
- Implement rate limiting for API requests
- Limit: 100 requests per minute per user
- Purpose: Prevent API abuse

**Explicit Requirements:**
- [ ] Track request counts per user
- [ ] Limit to 100 requests per minute
- [ ] Block requests that exceed the limit

**Implicit Requirements:**
- [ ] Minimal performance impact
- [ ] Clear feedback when rate limited
- [ ] Thread-safe implementation
- [ ] Easy to configure limits

**Constraints:**
- Must integrate with existing API framework
- Should not significantly increase latency
- Must handle concurrent requests

**Questions to Clarify:**
- How should we identify users? (API key, IP address, user ID)
- What response should blocked requests receive?
- Should limits be configurable per user tier?

**Assumption**: We'll use API keys to identify users and return HTTP 429 for blocked requests.

---

## Phase 2: Strategy

### Possible Approaches

#### Approach A: Fixed Window Counter
```
- Divide time into fixed windows (e.g., each minute)
- Count requests in current window
- Reset count at window boundary
```
- **Pros**: Simple to implement, low memory
- **Cons**: Burst traffic at window boundaries

#### Approach B: Sliding Window Log
```
- Store timestamp of each request
- Count requests in last N seconds
- Remove expired timestamps
```
- **Pros**: Accurate, no boundary issues
- **Cons**: High memory usage, O(n) lookup

#### Approach C: Token Bucket
```
- Each user has a bucket with tokens
- Requests consume tokens
- Tokens regenerate over time
```
- **Pros**: Allows controlled bursts, smooth limiting
- **Cons**: More complex implementation

#### Approach D: Sliding Window Counter (Hybrid)
```
- Use fixed windows but interpolate between them
- Weighted average of current and previous window
```
- **Pros**: Low memory, no hard boundaries
- **Cons**: Slightly more complex than fixed window

### Decision

**Chosen Approach**: Token Bucket (Approach C)

**Reasoning**:
- Allows legitimate burst traffic while maintaining limits
- Industry standard for API rate limiting
- Good balance of accuracy and performance
- Well-understood algorithm

**Trade-offs Accepted**:
- Slightly more complex than fixed window
- Requires tracking tokens and last refill time

---

## Phase 3: Execution

### Architecture Design

```
┌─────────────────────────────────────────────────────┐
│                   API Request                        │
└─────────────────────┬───────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────┐
│              Rate Limiter Middleware                 │
│  ┌─────────────────────────────────────────────┐    │
│  │  1. Extract API key from request            │    │
│  │  2. Get/create token bucket for user        │    │
│  │  3. Try to consume token                    │    │
│  │  4. Allow or reject request                 │    │
│  └─────────────────────────────────────────────┘    │
└─────────────────────┬───────────────────────────────┘
                      │
          ┌───────────┴───────────┐
          │                       │
          ▼                       ▼
    ┌───────────┐          ┌───────────────┐
    │  Allowed  │          │   Rejected    │
    │  (200 OK) │          │  (429 Error)  │
    └───────────┘          └───────────────┘
```

### Implementation

#### Step 1: Token Bucket Class

```python
import time
from threading import Lock
from dataclasses import dataclass


@dataclass
class TokenBucket:
    """Token bucket for rate limiting."""

    capacity: int           # Maximum tokens
    tokens: float          # Current tokens
    refill_rate: float     # Tokens per second
    last_refill: float     # Last refill timestamp
    lock: Lock             # Thread safety

    @classmethod
    def create(cls, requests_per_minute: int):
        """Create a bucket with specified rate limit."""
        return cls(
            capacity=requests_per_minute,
            tokens=requests_per_minute,
            refill_rate=requests_per_minute / 60.0,
            last_refill=time.time(),
            lock=Lock()
        )

    def consume(self) -> bool:
        """Try to consume a token. Returns True if allowed."""
        with self.lock:
            self._refill()
            if self.tokens >= 1:
                self.tokens -= 1
                return True
            return False

    def _refill(self):
        """Refill tokens based on elapsed time."""
        now = time.time()
        elapsed = now - self.last_refill
        tokens_to_add = elapsed * self.refill_rate
        self.tokens = min(self.capacity, self.tokens + tokens_to_add)
        self.last_refill = now
```

#### Step 2: Rate Limiter Manager

```python
from typing import Dict
from threading import Lock


class RateLimiter:
    """Manages rate limiting across multiple users."""

    def __init__(self, requests_per_minute: int = 100):
        self.requests_per_minute = requests_per_minute
        self.buckets: Dict[str, TokenBucket] = {}
        self.lock = Lock()

    def is_allowed(self, user_id: str) -> bool:
        """Check if request is allowed for user."""
        bucket = self._get_or_create_bucket(user_id)
        return bucket.consume()

    def _get_or_create_bucket(self, user_id: str) -> TokenBucket:
        """Get existing bucket or create new one for user."""
        with self.lock:
            if user_id not in self.buckets:
                self.buckets[user_id] = TokenBucket.create(
                    self.requests_per_minute
                )
            return self.buckets[user_id]
```

#### Step 3: Middleware Integration

```python
from functools import wraps
from flask import request, jsonify


# Global rate limiter instance
rate_limiter = RateLimiter(requests_per_minute=100)


def rate_limit(f):
    """Decorator to apply rate limiting to endpoints."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Extract user identifier
        api_key = request.headers.get('X-API-Key')
        if not api_key:
            return jsonify({'error': 'API key required'}), 401

        # Check rate limit
        if not rate_limiter.is_allowed(api_key):
            return jsonify({
                'error': 'Rate limit exceeded',
                'message': 'Too many requests. Please retry later.',
                'retry_after': 60
            }), 429

        return f(*args, **kwargs)
    return decorated_function


# Usage example
@app.route('/api/data')
@rate_limit
def get_data():
    return jsonify({'data': 'your data here'})
```

---

## Phase 4: Review

### Requirements Verification

| Requirement | Status | Notes |
|-------------|--------|-------|
| Track request counts per user | ✅ | Via TokenBucket per API key |
| Limit to 100 requests/minute | ✅ | Configurable via constructor |
| Block requests exceeding limit | ✅ | Returns HTTP 429 |
| Minimal performance impact | ✅ | O(1) operations |
| Clear feedback when limited | ✅ | JSON error with retry_after |
| Thread-safe implementation | ✅ | Locks on bucket operations |

### Edge Case Coverage

- [x] **First request**: Bucket created with full tokens ✅
- [x] **Exactly at limit**: 100th request succeeds, 101st blocked ✅
- [x] **After waiting**: Tokens refill based on elapsed time ✅
- [x] **Concurrent requests**: Thread locks prevent race conditions ✅
- [x] **Missing API key**: Returns 401 before rate check ✅

### Code Quality Check

- [x] Code is readable and well-formatted
- [x] Clear separation of concerns (bucket vs limiter vs middleware)
- [x] Thread-safe with proper locking
- [x] Follows Python conventions (dataclass, type hints)
- [x] No hardcoded values (configurable limit)

### Security Review

- [x] No injection vulnerabilities (uses dictionary keys)
- [x] Input validation (checks for API key presence)
- [x] No sensitive data exposed in responses
- [x] Rate limiting itself is a security feature ✅

### Self-Critique

**What could be improved?**
1. Memory: Old buckets should be cleaned up periodically
2. Persistence: State lost on restart
3. Distribution: Won't work across multiple servers

---

## Phase 5: Refinement

### Improvement 1: Bucket Cleanup

Add periodic cleanup of inactive buckets:

```python
import time
from threading import Thread


class RateLimiter:
    def __init__(self, requests_per_minute: int = 100, cleanup_interval: int = 300):
        self.requests_per_minute = requests_per_minute
        self.buckets: Dict[str, TokenBucket] = {}
        self.lock = Lock()
        self._start_cleanup_thread(cleanup_interval)

    def _start_cleanup_thread(self, interval: int):
        """Start background thread to clean up old buckets."""
        def cleanup():
            while True:
                time.sleep(interval)
                self._cleanup_old_buckets()

        thread = Thread(target=cleanup, daemon=True)
        thread.start()

    def _cleanup_old_buckets(self):
        """Remove buckets that haven't been used recently."""
        now = time.time()
        with self.lock:
            old_keys = [
                key for key, bucket in self.buckets.items()
                if now - bucket.last_refill > 300  # 5 minutes inactive
            ]
            for key in old_keys:
                del self.buckets[key]
```

### Improvement 2: Rate Limit Headers

Add informative headers to responses:

```python
def rate_limit(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if not api_key:
            return jsonify({'error': 'API key required'}), 401

        bucket = rate_limiter._get_or_create_bucket(api_key)

        if not bucket.consume():
            response = jsonify({
                'error': 'Rate limit exceeded',
                'message': 'Too many requests. Please retry later.',
            })
            response.status_code = 429
            response.headers['X-RateLimit-Limit'] = str(rate_limiter.requests_per_minute)
            response.headers['X-RateLimit-Remaining'] = '0'
            response.headers['Retry-After'] = '60'
            return response

        # Execute endpoint
        result = f(*args, **kwargs)

        # Add rate limit info to successful responses
        if hasattr(result, 'headers'):
            result.headers['X-RateLimit-Limit'] = str(rate_limiter.requests_per_minute)
            result.headers['X-RateLimit-Remaining'] = str(int(bucket.tokens))

        return result
    return decorated_function
```

---

## Final Solution Summary

### Components Delivered

1. **TokenBucket**: Thread-safe token bucket implementation
2. **RateLimiter**: Manages buckets per user with automatic cleanup
3. **Middleware**: Flask decorator for easy endpoint protection
4. **Headers**: Standard rate limit headers for client feedback

### Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| Token Bucket algorithm | Allows bursts while maintaining limits |
| Per-API-key tracking | Standard user identification |
| Thread locks | Safe for concurrent requests |
| Background cleanup | Prevents memory growth |
| Standard headers | Client-friendly feedback |

### Future Considerations

- **Distributed rate limiting**: Use Redis for multi-server deployments
- **Tiered limits**: Different limits for different user tiers
- **Endpoint-specific limits**: Different limits for different API endpoints
- **Monitoring**: Add metrics for rate limit hits and violations
