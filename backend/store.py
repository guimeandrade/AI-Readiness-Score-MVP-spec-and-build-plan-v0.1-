from typing import Dict, List, Optional
from pydantic import BaseModel
from threading import Lock
import time

class SiteEntry(BaseModel):
    url: str
    last_scan: float = 0.0
    score: float = 0.0
    recommendations: List[str] = []
    details: Optional[Dict[str, float]] | None = None

class SiteStore:
    def __init__(self):
        self.sites: Dict[str, SiteEntry] = {}
        self.lock = Lock()

    def add_site(self, url: str) -> SiteEntry:
        with self.lock:
            if url not in self.sites:
                entry = SiteEntry(url=url)
                self.sites[url] = entry
            return self.sites[url]

    def update_site(self, url: str, score: float, recommendations: List[str], details: Dict[str, float]):
        with self.lock:
            if url in self.sites:
                entry = self.sites[url]
                entry.last_scan = time.time()
                entry.score = score
                entry.recommendations = recommendations
                entry.details = details
            else:
                entry = SiteEntry(url=url, last_scan=time.time(), score=score, recommendations=recommendations, details=details)
                self.sites[url] = entry
