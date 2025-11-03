from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup

app = FastAPI(title="AI Readiness Score API")

class ScanRequest(BaseModel):
    url: str

class ScanResult(BaseModel):
    url: str
    score: float
    recommendations: list[str]

def compute_score(html: str) -> tuple[float, list[str]]:
    """Compute a simple AI readiness score based on page structure and metadata."""
    soup = BeautifulSoup(html, "html.parser")
    score = 0.0
    max_score = 100.0
    recommendations: list[str] = []
    # Check for meta tags like description and title
    meta_tags = soup.find_all("meta")
    if meta_tags:
        score += 20
    else:
        recommendations.append("Add meta tags such as <meta name='description'> and proper <title> tags.")
    # Check for semantic HTML tags usage
    semantic_tags = ['header', 'nav', 'main', 'article', 'section', 'footer']
    used_semantic = sum(1 for tag in semantic_tags if soup.find(tag) is not None)
    score += used_semantic * 10  # up to 60 points
    if used_semantic < len(semantic_tags):
        recommendations.append("Use semantic HTML tags like <header>, <nav>, <main>, <article>, <section>, <footer> for better structure.")
    # Check content length for meaningful information
    if len(html) > 1000:
        score += 20
    else:
        recommendations.append("Increase the amount of meaningful content on the page.")
    # Ensure score doesn't exceed maximum
    final_score = min(score, max_score)
    return final_score, recommendations

@app.post("/scan", response_model=ScanResult)
def scan(request: ScanRequest) -> ScanResult:
    """Fetch the page at the given URL and return an AI readiness score and recommendations."""
    try:
        response = requests.get(request.url, timeout=10)
        response.raise_for_status()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    score, recommendations = compute_score(response.text)
    return ScanResult(url=request.url, score=score, recommendations=recommendations)
