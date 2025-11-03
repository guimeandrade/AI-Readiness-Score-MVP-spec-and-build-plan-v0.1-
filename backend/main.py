from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import requests
from bs4 import BeautifulSoup

# Import the site store singleton to track monitored sites and their scores
from store import site_store, SiteEntry

app = FastAPI(title="AI Readiness Score API")


class ScanRequest(BaseModel):
    url: str


class ScanResult(BaseModel):
    url: str
    score: float
    recommendations: List[str]


class AddSiteRequest(BaseModel):
    url: str


@app.post("/sites", response_model=SiteEntry)
def add_site(req: AddSiteRequest):
    """Add a site to be monitored for AI readiness."""
    return site_store.add_site(req.url)


@app.get("/sites", response_model=List[SiteEntry])
def list_sites():
    """List all monitored sites with their latest scores and recommendations."""
    return site_store.list_sites()


def compute_score(html: str) -> tuple[float, List[str]]:
    """Compute a simple AI readiness score based on page structure and metadata."""
    soup = BeautifulSoup(html, "html.parser")
    score = 0.0
    max_score = 100.0
    recommendations: List[str] = []

    # Check for meta tags like description and title
    meta_tags = soup.find_all("meta")
    if meta_tags:
        score += 20
    else:
        recommendations.append("Add meta tags such as <meta name='description'> and proper <title> tags.")

    # Check for semantic HTML tags
    semantic_tags = ["header", "nav", "main", "article", "section", "footer"]
    semantic_found = any(soup.find(tag) for tag in semantic_tags)
    if semantic_found:
        score += 30
    else:
        recommendations.append("Use semantic HTML tags like <header>, <nav>, <main>, <article>, <section>, <footer>.")

    # Evaluate content length
    text_length = len(soup.get_text(strip=True))
    if text_length > 300:
        score += 20
    else:
        recommendations.append("Increase meaningful text content on the page.")

    # Check for structured data (basic check for JSON-LD script)
    structured_data = soup.find("script", type="application/ld+json")
    if structured_data:
        score += 20
    else:
        recommendations.append("Add structured data using JSON-LD to help AI understand your content.")

    # Normalize score to 0-100
    if score > max_score:
        score = max_score

    return score, recommendations


@app.post("/scan", response_model=ScanResult)
def scan(req: ScanRequest):
    """Fetch the URL, compute its AI readiness score, update the store, and return results."""
    try:
        response = requests.get(req.url, timeout=10)
        response.raise_for_status()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch URL: {e}")

    score, recommendations = compute_score(response.text)
    # Update the store with the scanned result
    site_store.add_site(req.url)
    site_store.update_site(req.url, score, recommendations)

    return ScanResult(url=req.url, score=score, recommendations=recommendations)
