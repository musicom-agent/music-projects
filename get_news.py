import urllib.request
import xml.etree.ElementTree as ET
import re
import json
from bs4 import BeautifulSoup

def fetch_url(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.read()
    except Exception as e:
        return None

def parse_rss(data):
    items = []
    if not data: return items
    try:
        root = ET.fromstring(data)
        for item in root.findall(".//item"):
            title = item.find("title")
            link = item.find("link")
            desc = item.find("description")
            pub_date = item.find("pubDate")
            
            t_txt = title.text if title is not None else ""
            l_txt = link.text if link is not None else ""
            d_txt = desc.text if desc is not None else ""
            d_clean = re.sub("<[^<]+?>", "", d_txt) if d_txt else ""
            d_clean = re.sub(r"\s+", " ", d_clean).strip()
            
            items.append({
                "title": t_txt.strip(),
                "link": l_txt.strip(),
                "desc": d_clean[:400],
                "date": pub_date.text.strip() if pub_date is not None else ""
            })
    except Exception as e:
        pass
    return items

def scrape_sos():
    html = fetch_url("https://www.soundonsound.com/news")
    items = []
    if not html: return items
    try:
        soup = BeautifulSoup(html, "html.parser")
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if href.startswith("/news/") and len(a.get_text(strip=True)) > 20:
                title = a.get_text(strip=True)
                full_url = f"https://www.soundonsound.com{href}"
                desc_text = ""
                p = a.find_parent("div", class_="views-row") or a.find_parent("div")
                if p:
                    all_text = p.get_text(separator=" ", strip=True)
                    if title in all_text:
                        desc_text = all_text.replace(title, "", 1).strip()
                if not desc_text:
                    ns = a.find_next_sibling()
                    if ns:
                        desc_text = ns.get_text(strip=True)
                desc_text = re.sub(r"\s+", " ", desc_text).strip()
                items.append({
                    "title": title,
                    "link": full_url,
                    "desc": desc_text[:400],
                    "date": ""
                })
        seen = set()
        dedup = []
        for i in items:
            if i["link"] not in seen:
                seen.add(i["link"])
                dedup.append(i)
        return dedup[:12]
    except Exception as e:
        return []

synth = parse_rss(fetch_url("https://www.synthtopia.com/feed/"))
mt = parse_rss(fetch_url("https://musictech.com/feed/"))
sos = scrape_sos()

res = {"synthtopia": synth[:12], "musictech": mt[:12], "sos": sos}
print(json.dumps(res))
