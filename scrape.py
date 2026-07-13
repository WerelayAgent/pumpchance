import os, requests, re, urllib.parse
from concurrent.futures import ThreadPoolExecutor

BASE_URL = "https://chancecoin.now"
OUT_DIR = r"c:\Tools\project crypto\pumpchance"
PUBLIC_DIR = os.path.join(OUT_DIR, "public")

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
})

def download_file(url, local_path):
    try:
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        if os.path.exists(local_path):
            return
        res = session.get(url, timeout=10)
        if res.status_code == 200:
            with open(local_path, "wb") as f:
                f.write(res.content)
            print(f"Downloaded: {url}")
        else:
            print(f"Failed {res.status_code}: {url}")
    except Exception as e:
        print(f"Error {url}: {e}")

def main():
    os.makedirs(PUBLIC_DIR, exist_ok=True)
    
    print(f"Fetching index.html from {BASE_URL}...")
    r = session.get(BASE_URL + "/")
    html = r.text

    # Extract assets FIRST
    assets = set()
    assets.update(re.findall(r'/(?:_next/static|static|assets|images)/[a-zA-Z0-9_/\.-]+\.(?:css|js|png|jpg|jpeg|svg|webp|gif|woff2|woff|ttf)', html))
    assets.update(re.findall(r'href="(/[^"]+\.(?:png|jpg|ico))"', html))
    assets.update(re.findall(r'src="(/[^"]+\.(?:png|jpg|svg|webp))"', html))
    # Open Graph Images
    assets.update(re.findall(r'content="https://chancecoin.now(/[^"]+\.(?:png|jpg|jpeg))"', html))
    
    print(f"Found {len(assets)} assets.")
    
    urls_to_download = []
    for asset in assets:
        clean_asset = asset.split('?')[0]
        url = urllib.parse.urljoin(BASE_URL, clean_asset)
        local_path = os.path.join(PUBLIC_DIR, clean_asset.lstrip("/"))
        urls_to_download.append((url, local_path))
        
    with ThreadPoolExecutor(max_workers=20) as executor:
        for url, local in urls_to_download:
            executor.submit(download_file, url, local)

    # Rebranding Replacements
    html = html.replace("CHANCECOIN", "PUMPCHANCE")
    html = html.replace("Chancecoin", "Pumpchance")
    html = html.replace("chancecoin", "pumpchance")
    
    html = html.replace("CHANCE COIN", "PUMP CHANCE")
    html = html.replace("Chance Coin", "Pump Chance")
    html = html.replace("Chance coin", "Pump chance")
    html = html.replace("chance coin", "pump chance")
    
    html = html.replace("CHANCE", "PUMPCHANCE")
    html = html.replace("Chance", "Pumpchance")
    
    html = html.replace("pumpchance.now", "pumpchance.com") # Just in case it's there
    
    # Twitter replacement
    html = re.sub(r'x\.com/[a-zA-Z0-9_]+', 'x.com/pumpchance', html)
    html = re.sub(r'twitter\.com/[a-zA-Z0-9_]+', 'twitter.com/pumpchance', html)
    
    # Contract Address replacement
    html = html.replace("JCKwsT8UAbygnFkZ7u3amDUM7BXRtwUhCsHQv2khpump", "coming soon on pump.fun")
    
    # Strip asset query params in HTML
    html = re.sub(r'\?[a-f0-9]{8,16}', '', html)
    html = re.sub(r'\?dpl=[a-zA-Z0-9_-]+', '', html)

    index_path = os.path.join(PUBLIC_DIR, "index.html")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(html)
    print("Saved rebranded index.html")

if __name__ == "__main__":
    main()
