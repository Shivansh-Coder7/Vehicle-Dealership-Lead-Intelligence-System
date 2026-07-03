from ddgs import DDGS
import pandas as pd
from urllib.parse import urlparse
import time

data = pd.read_csv("businesses.csv")
names = data["name"].dropna().astype(str).str.strip().tolist()
names = [name for name in names if name]

DIR_DOMAINS = {
    "google.com", "facebook.com", "instagram.com",
    "justdial.com", "indiamart.com", "cardekho.com",
    "carwale.com", "cars24.com", "olx.in",
    "reddit.com", "wikipedia.org", "yellowpages.in",
    "sulekha.com", "tradeindia.com", "youtube.com",
    "twitter.com", "linkedin.com", "magicpin.in",
    "bikewale.com", "bikedekho.com", "zigwheels.com",
    "team-bhp.com", "91wheels.com", "drivespark.com",
}

def clean_domain(url):
    host = urlparse(url).netloc.lower()
    if host.startswith("www."):
        host = host[4:]
    return host

def classify_link(url):
    domain = clean_domain(url)
    if domain in DIR_DOMAINS:
        return "referral"
    return "official_or_other"

rows = []

print(f"Checking online presence for {len(names)} businesses...")
print("-" * 50)

with DDGS() as ddgs:
    for i, name in enumerate(names):
        query = f"{name} Indore vehicle showroom dealer"
        print(f"[{i+1}/{len(names)}] Searching: {name}")

        try:
            search_results = list(ddgs.text(query, max_results=5))
            time.sleep(1)
        except Exception as e:
            print(f"  Error: {e}")
            search_results = []

        seen = set()
        official_link = None
        relevant_links = []

        for r in search_results:
            url = r.get("href") or r.get("url")
            title = (r.get("title") or "").strip()
            body = (r.get("body") or "").strip()

            if not url or url in seen:
                continue
            seen.add(url)

            domain = clean_domain(url)
            link_row = {
                "name": name,
                "title": title,
                "url": url,
                "domain": domain,
                "snippet": body,
                "type": classify_link(url),
            }

            if official_link is None and domain not in DIR_DOMAINS:
                official_link = link_row
                continue

            if len(relevant_links) < 4:
                relevant_links.append(link_row)

        rows.append({
            "name": name,
            "has_website": official_link is not None,
            "official_url": official_link["url"] if official_link else "",
            "official_title": official_link["title"] if official_link else "",
            "relevant_links": relevant_links,
        })

        print(f"  Website: {'YES - ' + official_link['url'] if official_link else 'NO'}")

results_df = pd.DataFrame(rows)
results_df.to_csv("car_showroom_online_presence.csv", index=False)

print("\n" + "=" * 50)
print(f"Done! Saved {len(results_df)} records")
print(f"  Has website: {results_df['has_website'].sum()}")
print(f"  No website:  {(~results_df['has_website']).sum()}")
