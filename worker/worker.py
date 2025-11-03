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
                # Trigger a scan for the site
                scan_resp = requests.post(SCAN_ENDPOINT, json={"url": site_url})
                scan_resp.raise_for_status()
                result = scan_resp.json()
                score = result.get("score")
                recommendations = result.get("recommendations")
                details = result.get("details")
                print(f"Scanned {site_url}: Score {score}")
                if details:
                    print(f"Details: {details}")
                if recommendations:
                    print(f"Recommendations: {recommendations}\n")
            except Exception as e:
                print(f"Scan failed for {site_url}: {e}")
        time.sleep(3600)

if __name__ == "__main__":
    run_monitor()
