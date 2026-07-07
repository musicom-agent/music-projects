---
name: web-research
description: "Web search without web_search tool, browser, or pip — Google News RSS + DuckDuckGo Lite + curl + Python html.parser in constrained Docker sandboxes."
tags: [web-search, curl, docker, sandbox, duckduckgo, google-news, research]
---

# web-research

When the `web_search` tool doesn't exist, Chrome isn't installed, and pip is unavailable — still get web results via **Google News RSS** (primary) or **DuckDuckGo Lite** (secondary) + curl + Python's built-in `html.parser`.

## Prerequisites

- `curl` available (almost always)
- Python 3 with `html.parser` (built-in, always available)
- Internet access (curl must reach the target)

## Quick Decision Guide

| Task type | Method | Why |
|-----------|--------|-----|
| **News research / daily digests** | **Google News RSS** (first choice) | Stable XML, 50–200 results, regex-friendly, no fragile HTML parsing. Proven: 102 results vs DDG returning empty on first pass (May 2026). |
| **General web search** | **DDG Lite** | Better for non-news topics, product searches, documentation lookups. |
| **Both fail** | Try the other + SearXNG fallback | `curl -s 'https://searx.be/search?q=QUERY&format=json'` |

## Method 1: Google News RSS (Primary — Use First for News)

More reliable than DDG Lite — stable XML, no HTML parsing fragility, richer results.

```bash
curl -s --max-time 15 "https://news.google.com/rss/search?q=YOUR+SEARCH+QUERY&hl=en-US&gl=US&ceid=US:en" \
  -H "User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36" \
  -o /tmp/gnews_results.xml
```

Parse with Python regex:

```python
import re

xml = open('/tmp/gnews_results.xml').read()
titles = re.findall(r'<title>([^<]+)</title>', xml)
links = re.findall(r'<link>([^<]+)</link>', xml)

for t, l in zip(titles, links):
    # Strip source suffixes like " - Blog Name"
    clean_title = re.sub(r'\s*-\s*.+$', '', t).strip()
    print(f"{clean_title[:200]}")
    print(f"  {l[:200]}")
    print()
```

**Parameters:**
- `hl` — language (en-US, de-DE, etc.)
- `gl` — country (US, GB, DE, etc.)
- `ceid` — combined `country:language` (US:en, DE:de)
- Remove all three for global results (but less relevant)

**Pitfalls:**
- **XML can be large** (100KB+ for popular queries) — parse efficiently, don't `cat` it
- **Returns many irrelevant results** — always filter by keywords in post-processing
- **Empty results for obscure queries** — fall back to DDG Lite
- **Links use Google News format** — the `<link>` field is a Google News redirect URL. Extract the real URL with: `url = link.split('?')[0].replace('/articles/', '/rss/articles/')` or follow the redirect
- **Source noise** — some titles end with `"[23 images]"` or `" - Source Name"` — clean them with regex: `re.sub(r'\s*-\s*.+$', '', title)`
- **Deduplication** — the same article often appears under multiple sources. Deduplicate by title or article ID prefix

### Deduplication Pattern

```python
# Deduplicate by normalized title
seen = set()
unique = []
for t, l in zip(titles, links):
    norm = re.sub(r'\s+', ' ', t.lower()).strip()
    if norm not in seen and norm:
        seen.add(norm)
        unique.append((t, l))
```

## Method 2: DuckDuckGo Lite (Secondary — General Search)

Use for non-news topics or when Google News RSS is empty.

### 1. Fetch

```bash
curl -s --max-time 15 'https://lite.duckduckgo.com/lite/' \
  -d 'q=YOUR+SEARCH+QUERY' \
  -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36' \
  -o /tmp/ddg_results.html
```

**Important:** DuckDuckGo Lite uses POST for search, NOT GET. The query goes in `-d 'q=...'`.

### 2. Parse with Python's `html.parser`

```python
from html.parser import HTMLParser

class DDGLiteParser(HTMLParser):
    """Parse DuckDuckGo Lite results.
    
    DDG Lite structure: each result spans multiple <tr> rows.
    States: in_link (URL) → in_result_link (title) → in_snippet (desc)
    Result complete when </span> closes (in_link state).
    """
    def __init__(self):
        super().__init__()
        self.results = []
        self.current_result = None
        self.state = 'idle'
        self.buffer = ''
        
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        cls = attrs.get('class', '')
        
        if tag == 'span' and 'link-text' in cls:
            self.current_result = {'url': '', 'title': '', 'snippet': ''}
            self.state = 'in_link'
            self.buffer = ''
        elif tag == 'a' and 'result-link' in cls:
            self.state = 'in_result_link'
            self.buffer = ''
        elif tag == 'td' and 'result-snippet' in cls:
            self.state = 'in_snippet'
            self.buffer = ''
            
    def handle_data(self, data):
        if self.current_result is None:
            return
        if self.state == 'in_link':
            self.current_result['url'] = data.strip()
        elif self.state == 'in_result_link':
            self.buffer += data
        elif self.state == 'in_snippet':
            self.buffer += data
            
    def handle_endtag(self, tag):
        if tag == 'span' and self.state == 'in_link' and self.current_result:
            self.state = 'idle'
            self.results.append(self.current_result)
            self.current_result = None
        elif tag == 'a' and self.state == 'in_result_link' and self.current_result:
            self.current_result['title'] = self.buffer.strip()
            self.state = 'idle'
            self.buffer = ''
        elif tag == 'td' and self.state == 'in_snippet' and self.current_result:
            self.current_result['snippet'] = self.buffer.strip()
            self.state = 'idle'
            self.buffer = ''
            
    def handle_entityref(self, name):
        entities = {'nbsp': ' ', 'amp': '&', 'lt': '<', 'gt': '>',
                    'quot': '"', 'apos': "'", 'ndash': '-', 'mdash': '—'}
        self.buffer += entities.get(name, name)
        
    def handle_charref(self, name):
        if name.startswith('x'):
            try: self.buffer += chr(int(name[1:], 16))
            except ValueError: pass
        else:
            try: self.buffer += chr(int(name))
            except ValueError: pass

# Usage
import subprocess
result = subprocess.run(
    ['curl', '-s', '--max-time', '15', 'https://lite.duckduckgo.com/lite/',
     '-d', 'q=YOUR+QUERY',
     '-H', 'User-Agent: Mozilla/5.0 (X11; Linux x86_64)'],
    capture_output=True, text=True, timeout=15
)
parser = DDGLiteParser()
parser.feed(result.stdout)
for r in parser.results:
    title = r['title'] or r['url'].split('/')[-1][:50]
    print(f"[{title}]")
    print(f"  {r['url']}")
    if r['snippet']:
        print(f"  {r['snippet'][:200]}")
    print()
```

**Key detail:** The `handle_endtag` for `</span>` appends the result to the list. The result is only complete when `</span>` closes — this was the fix that made parsing work reliably in May 2026.

### 3. Debug Tips

If results are empty:
1. Check that curl succeeded: `curl -sI https://lite.duckduckgo.com/lite/`
2. Write raw HTML to `/tmp/ddg_debug.html` and inspect for `link-text` and `result-link` classes
3. DDG Lite sometimes returns results with empty `<a class='result-link'>` tags — fall back to any `<a>` tag
4. If still empty, **switch to Google News RSS immediately** — DDG Lite can silently fail with certain query patterns or IP ranges

## Alternative Search Engines

If both DDG Lite and Google News RSS fail:
- **SearXNG instances**: `curl -s 'https://searx.be/search?q=QUERY&format=json'` — returns JSON if instance supports it (varies by instance)
- **Startpage / Brave**: Require JS rendering — won't work here without a browser

## Pitfalls

- **DDG Lite can silently fail**: Returns empty results even when curl succeeds. **Always verify** that your parser returned non-empty results. If empty, switch to Google News RSS immediately.
- **POST not GET**: DuckDuckGo Lite requires `-d 'q=...'` (POST), not GET parameters. GET returns the search form, not results.
- **Empty titles (DDG)**: DDG Lite sometimes returns results with empty `<a class='result-link'>` tags. Use the URL slug or snippet as fallback title.
- **User-Agent required (both)**: Without a real User-Agent header, DDG may return empty/malformed results AND Google News RSS may redirect oddly. Always use: `'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'`
- **Timeout**: Add `--max-time 10` to curl in case of slow network.
- **HTML entities (DDG)**: DDG Lite uses entities like `&nbsp;`, `&amp;`, `&#x27;` — decode them in your parser.
- **Google News RSS XML size**: Can be 100KB+ for popular queries — parse efficiently, don't dump to terminal.
- **Google News RSS deduplication**: Same articles appear under multiple sources — always deduplicate.
