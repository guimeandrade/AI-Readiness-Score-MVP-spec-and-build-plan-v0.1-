from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Import the site store singleton to track monitored sites and their scores
from store import site_store, SiteEntry

app = FastAPI(title="AI Readiness Score API")

class ScanRequest(BaseModel):
    url: str

class ScanResult(BaseModel):
    url: str
    score: float
    recommendations: List[str]
    details: Dict[str, float]

class AddSiteRequest(BaseModel):
    url: str

@app.post("/sites", response_model=SiteEntry)
def add_site(req: AddSiteRequest):
    """Add a new site to be monitored"""
    return site_store.add_site(req.url)

@app.get("/sites", response_model=List[SiteEntry])
def list_sites():
    """List all monitored sites with their latest scores"""
    return site_store.list_sites()

def compute_score(html: str) -> (float, List[str], Dict[str, float]):
    """Compute AI readiness score for a page and provide category breakdown and recommendations"""
    soup = BeautifulSoup(html, "html.parser")
    recommendations: List[str] = []
    details: Dict[str, float] = {}

    # Define weights for each category (sum to 1.0)
    weights = {
        "content_structure": 0.2,
        "metadata_quality": 0.2,
        "performance": 0.2,
        "crawlability": 0.2,
        "ai_friendliness": 0.2,
    }

    total_score = 0.0

    # Content structure score
    content_score = 0.0
    semantic_tags = ["header", "nav", "main", "article", "section", "footer"]
    if any(soup.find(tag) for tag in semantic_tags):
        content_score += 0.5
    else:
        recommendations.append("Use semantic HTML tags like <header>, <nav>, <main>, <article>, <section>, <footer>.")
    text_length = len(soup.get_text(strip=True))
    if text_length > 500:
        content_score += 0.5
    else:
        recommendations.append("Increase meaningful text content on the page.")
    details["content_structure"] = content_score * 100 * weights["content_structure"]

    # Metadata quality score
    meta_score = 0.0
    if soup.find("title") and soup.title and soup.title.string:
        meta_score += 0.3
    else:
        recommendations.append("Add a descriptive <title> tag.")
    if soup.find("meta", attrs={"name": "description"}):
        meta_score += 0.3
    else:
        recommendations.append("Add a meta description tag.")
    if soup.find("meta", attrs={"property": "og:title"}) and soup.find("meta", attrs={"property": "og:description"}):
        meta_score += 0.4
    else:
        recommendations.append("Add Open Graph tags (og:title, og:description) for better AI/LLM presentation.")
    details["metadata_quality"] = meta_score * 100 * weights["metadata_quality"]

    # Performance score (approximate by HTML size)
    perf_score = 0.0
    if len(html) < 50000:
        perf_score = 1.0
    else:
        perf_score = 0.5
        recommendations.append("Optimize page size for faster performance.")
    details["performance"] = perf_score * 100 * weights["performance"]

    # Crawlability score (robots meta and canonical tag)
    crawl_score = 0.0
    robots_meta = soup.find("meta", attrs={"name": "robots"})
    if robots_meta and "noindex" in (robots_meta.get("content") or "").lower():
        recommendations.append("Remove 'noindex' robots meta tag to allow indexing.")
    else:
        crawl_score += 0.5
    if soup.find("link", attrs={"rel": "canonical"}):
        crawl_score += 0.5
    else:
        recommendations.append("Add a canonical link tag.")
    details["crawlability"] = crawl_score * 100 * weights["crawlability"]

    # AI friendliness score (structured data and headings)
    ai_score = 0.0
    if soup.find("script", type="application/ld+json"):
        ai_score += 0.6
    else:
        recommendations.append("Add structured data using JSON-LD to help AI understand your content.")
    headings = soup.find_all(["h1", "h2"])
    if headings:
        ai_score += 0.4
    else:
        recommendations.append("Add heading tags (<h1>, <h2>) to structure your content.")
    details["ai_friendliness"] = ai_score * 100 * weights["ai_friendliness"]

    # Sum up the weighted category scores
    total_score = sum(details.values())
    if total_score > 100:
        total_score = 100
    return total_score, recommendations, details

@app.post("/scan", response_model=ScanResult)
def scan(req: ScanRequest):
    """Fetch the URL, compute its AI readiness score, update the store, and return results"""
    try:
        response = requests.get(req.url, timeout=10)
        response.raise_for_status()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch URL: {e}")
    score, recommendations, details = compute_score(response.text)
    # update the store with score, recommendations, and details
    site_store.update_site(req.url, score, recommendations, details)
    return ScanResult(url=req.url, score=score, recommendations=recommendations, details=details)
