import time
import requests

# List of websites to monitor. In a real application, this might come from a database.
WEBSITES = [
    "https://example.com",
    "https://another-site.com"
]

# Backend endpoint for scanning websites
BACKEND_URL = "http://localhost:8000/scan"

def run_monitor():
    """Periodically scan each website and print the AI-readiness score."""
    while True:
        for site_url in WEBSITES:
            try:
                response = requests.post(BACKEND_URL, json={"url": site_url})
                if response.status_code == 200:
                    data = response.json()
                    score = data.get("score")
                    recommendations = data.get("recommendations")
                    print(f"Scanned {site_url}: score={score}, recommendations={recommendations}")
                else:
                    print(f"Failed to scan {site_url}: HTTP {response.status_code}")
            except Exception as exc:
                print(f"Error scanning {site_url}: {exc}")
        # Wait for an hour before scanning again
        time.sleep(3600)

if __name__ == "__main__":
    run_monitor()
