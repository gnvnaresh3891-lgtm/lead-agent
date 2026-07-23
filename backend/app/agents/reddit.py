import asyncio
import httpx
import logging
import uuid
import time
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class RedditAgent:
    def __init__(self, target_url: str = "http://localhost:8000/api/v1/signals/ingest"):
        self.target_url = target_url
        self.subreddits = ["SaaS", "sales", "Entrepreneur"]
        self.keywords = ["alternative to", "looking for a tool", "how do you solve", "recommendation"]
        self.is_running = False

    async def fetch_recent_posts(self, subreddit: str) -> List[Dict[str, Any]]:
        """Fetch recent posts from a subreddit. Uses mock data if blocked."""
        url = f"https://www.reddit.com/r/{subreddit}/new.json?limit=10"
        headers = {"User-Agent": "LeadAgent/0.1 by gnvnaresh3891"}
        
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(url, headers=headers, timeout=5.0)
                if resp.status_code == 200:
                    data = resp.json()
                    return data.get("data", {}).get("children", [])
                else:
                    logger.warning(f"Reddit API returned {resp.status_code} for r/{subreddit}. Using fallback data.")
                    return self._get_fallback_data(subreddit)
        except Exception as e:
            logger.error(f"Error fetching from Reddit r/{subreddit}: {e}")
            return self._get_fallback_data(subreddit)

    def _get_fallback_data(self, subreddit: str) -> List[Dict[str, Any]]:
        """Mock data generator for reliable demo functionality."""
        return [
            {
                "data": {
                    "id": f"mock_{uuid.uuid4().hex[:6]}",
                    "title": f"Looking for an alternative to Apollo in {subreddit}",
                    "selftext": "We are scaling our SDR team and the current tool is too expensive. Any recommendations?",
                    "author": "growth_hacker_99",
                    "url": f"https://reddit.com/r/{subreddit}/comments/mock",
                    "created_utc": time.time()
                }
            },
            {
                "data": {
                    "id": f"mock_{uuid.uuid4().hex[:6]}",
                    "title": "How do you solve multi-channel outreach?",
                    "selftext": "Just started as a VP of Sales and our tech stack is a mess. Need an all-in-one platform.",
                    "author": "vp_sales_guy",
                    "url": f"https://reddit.com/r/{subreddit}/comments/mock2",
                    "created_utc": time.time()
                }
            }
        ]

    def score_post(self, post_data: Dict[str, Any]) -> float:
        """Calculate intent score based on keywords."""
        text = f"{post_data.get('title', '')} {post_data.get('selftext', '')}".lower()
        score = 0.0
        for kw in self.keywords:
            if kw in text:
                score += 35.0
        
        if "?" in text: # Asking a question increases intent
            score += 15.0
            
        return min(score, 100.0)

    async def ingest_to_backend(self, signal: Dict[str, Any]):
        """Post the signal to our local FastAPI ingest route."""
        # For simplicity, we assume org_id is a fixed demo ID
        demo_org_id = "00000000-0000-0000-0000-000000000001"
        headers = {"X-Org-Id": demo_org_id}
        
        try:
            async with httpx.AsyncClient() as client:
                await client.post(self.target_url, json={"signals": [signal]}, headers=headers)
                logger.info(f"Ingested Reddit signal: {signal['signal_id']}")
        except Exception as e:
            logger.error(f"Failed to ingest signal to backend: {e}")

    async def run_cycle(self):
        """Run one scraping cycle."""
        logger.info("Starting Reddit Lead Agent cycle...")
        for sub in self.subreddits:
            posts = await self.fetch_recent_posts(sub)
            for post in posts:
                data = post.get("data", {})
                score = self.score_post(data)
                
                if score >= 50.0: # High intent threshold
                    signal_payload = {
                        "signal_id": str(uuid.uuid4()),
                        "signal_type": "topic_intent",
                        "score": score,
                        "timestamp": data.get("created_utc", time.time()),
                        "payload": {
                            "source": "reddit",
                            "subreddit": sub,
                            "post_id": data.get("id"),
                            "author": data.get("author"),
                            "title": data.get("title"),
                            "url": data.get("url"),
                            "ai_draft": f"Hi {data.get('author')}, saw you were looking for alternatives. Our platform handles this natively..."
                        }
                    }
                    await self.ingest_to_backend(signal_payload)
            await asyncio.sleep(2) # rate limit prevention

    async def start(self):
        self.is_running = True
        while self.is_running:
            await self.run_cycle()
            await asyncio.sleep(60) # Run every 60 seconds

    def stop(self):
        self.is_running = False
