from typing import List, Dict
from pydantic import BaseModel
from threading import Lock
import time


class SiteEntry(BaseModel):
    url: str
    last_scan: float = 0.0
    score: float = 0.0
    recommendations: List[str] = []


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

    def update_site(self, url: str, score: float, recommendations: List[str]):
        with self.lock:
            if url in self.sites:
                entry = self.sites[url]
                entry.score = score
                entry.recommendations = recommendations
                entry.last_scan = time.time()

    def list_sites(self) -> List[SiteEntry]:
        with self.lock:
            return list(self.sites.values())


# Singleton instance to be used across the application
site_store = SiteStore()
