import re, os, requests

BASE_URL = "https://chancecoin.now"
PUBLIC_DIR = r"c:\Tools\project crypto\pumpchance\public"

def main():
    content = open(os.path.join(PUBLIC_DIR, 'index.html'), 'r', encoding='utf-8').read()
    links = re.findall(r'href="([^"]+)"', content)
    srcs = re.findall(r'src="([^"]+)"', content)
    
    for url in links + srcs:
        if url.startswith('./') or url.startswith('/'):
            clean_url = url.replace('./', '/')
            if '.png' in url or '.webp' in url or '.svg' in url or '.ico' in url or '.jpg' in url:
                print("Missing asset found in HTML:", url)
                dl_url = BASE_URL + clean_url
                local_path = os.path.join(PUBLIC_DIR, clean_url.lstrip('/'))
                try:
                    res = requests.get(dl_url)
                    if res.status_code == 200:
                        os.makedirs(os.path.dirname(local_path), exist_ok=True)
                        with open(local_path, "wb") as f:
                            f.write(res.content)
                        print("Downloaded:", dl_url)
                except Exception as e:
                    print("Failed:", e)

if __name__ == "__main__":
    main()
