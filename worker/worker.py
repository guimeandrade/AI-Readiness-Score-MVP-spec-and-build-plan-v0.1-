import time
import requests

# Backend API base URL
BACKEND_BASE_URL = "http://localhost:8000"
SITES_ENDPOINT = f"{BACKEND_BASE_URL}/sites"
SCAN_ENDPOINT = f"{BACKEND_BASE_URL}/scan"


def run_monitor():
    """Periodically fetch monitored sites from the backend and trigger scans."""
    while True:
        # Retrieve list of sites to monitor from the backend
        try:
            resp = requests.get(SITES_ENDPOINT)
            resp.raise_for_status()
            sites = resp.json()
        except Exception as e:
            print(f"Failed to fetch site list: {e}")
            sites = []

        for site in sites:
            site_url = site.get("url")
            if not site_url:
                continue
            try:
                response = requests.post(SCAN_ENDPOINT, json={"url": site_url})
                if response.status_code == 200:
                    data = response.json()
                    score = data.get("score")
                    recommendations = data.get("recommendations")
                    print(f"Scanned {site_url}: score={score}, recommendations={recommendations}")
                else:
                    print(f"Failed to scan {site_url}: HTTP {response.status_code}")
            except Exception as exc:
                print(f"Error scanning {site_url}: {exc}")

        # Wait an hour before next monitoring cycle
        time.sleep(3600)


if __name__ == "__main__":
    run_monitor()
