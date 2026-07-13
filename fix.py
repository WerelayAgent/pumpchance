import re

def main():
    with open('index.html', 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()
    
    text = text.replace('â€”', '—')
    text = text.replace('â€™', "'")
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', text)
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(text)

if __name__ == "__main__":
    main()
