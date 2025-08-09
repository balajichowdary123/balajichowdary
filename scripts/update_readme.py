#!/usr/bin/env python3
import os, sys, json, requests, datetime
from jinja2 import Environment, FileSystemLoader
from base64 import b64encode

ROOT = os.path.dirname(os.path.dirname(__file__))
TEMPLATES = os.path.join(ROOT, "scripts", "templates")
OUT = os.path.join(ROOT, "README.md")
ASSETS = os.path.join(ROOT, "assets")
OUTPUT = os.path.join(ROOT, "output")

env = Environment(loader=FileSystemLoader(TEMPLATES), trim_blocks=True, lstrip_blocks=True)

def fetch_spotify_now_playing():
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    if not client_id or not client_secret:
        return None
    # Get token
    token_url = "https://accounts.spotify.com/api/token"
    auth = b64encode(f"{client_id}:{client_secret}".encode()).decode()
    headers = {"Authorization": f"Basic {auth}"}
    data = {"grant_type": "client_credentials"}
    resp = requests.post(token_url, headers=headers, data=data, timeout=15)
    if resp.status_code != 200:
        return None
    token = resp.json().get("access_token")
    # NOTE: client-credentials cannot get user currently-playing; requires user auth.
    # We'll just return None and let README show a static placeholder.
    return None

def fetch_leetcode_stats():
    username = os.getenv("LEETCODE_USERNAME")
    if not username:
        return None
    url = "https://leetcode.com/graphql"
    query = '''
    query userProfileProfileUserStatus($username: String!) {
      allQuestionsCount {
        difficulty
        count
      }
      matchedUser(username: $username) {
        username
        submitStats {
          acSubmissionNum {
            difficulty
            count
            submissions
          }
        }
        profile {
          reputation
          ranking
        }
      }
    }
    '''
    json_data = {"query": query, "variables": {"username": username}}
    try:
        r = requests.post(url, json=json_data, timeout=15)
        if r.status_code == 200:
            j = r.json()
            return j.get("data", {})
    except Exception:
        return None
    return None

def render_skill_bar(skill, pct, color="#00F7FF", width=300, height=18):
    # A small SVG generator for skill bars (animated)
    pct = max(0, min(100, int(pct)))
    svg = f'''<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="g{skill}" x1="0" x2="1">
      <stop offset="0%" stop-color="{color}" stop-opacity="1"/>
      <stop offset="100%" stop-color="#8a2be2" stop-opacity="1"/>
    </linearGradient>
  </defs>
  <rect x="0" y="0" rx="8" ry="8" width="{width}" height="{height}" fill="#111827" opacity="0.25"/>
  <rect x="0" y="0" rx="8" ry="8" width="{int(width * pct/100)}" height="{height}" fill="url(#g{skill})">
    <animate attributeName="width" from="0" to="{int(width * pct/100)}" dur="1.2s" fill="freeze"/>
  </rect>
  <text x="{width-6}" y="{height-4}" font-size="11" font-family="Inter, Arial" fill="#e6edf3" text-anchor="end">{pct}%</text>
  <text x="8" y="{height-4}" font-size="11" font-family="Inter, Arial" fill="#e6edf3">{skill}</text>
</svg>'''
    return svg

def recolor_snake(svg_path, color="#00F7FF"):
    if not os.path.exists(svg_path):
        return
    s = open(svg_path,'r',encoding='utf8').read()
    # Replace fill/stroke colors heuristically (this is simple; adjust regex for robust usage)
    s = s.replace('#6cc644', color)  # common green -- replace with theme color
    outp = svg_path
    open(outp,'w',encoding='utf8').write(s)

def main():
    # load template
    tmpl = env.get_template("dynamic_readme_template.md")
    now = datetime.datetime.utcnow().isoformat()
    lc = fetch_leetcode_stats() or {}
    spotify = fetch_spotify_now_playing() or {}
    # sample skills (you will change these values later)
    skills = {
        "Python": 90,
        "JavaScript": 82,
        "AI/ML": 75,
        "React": 85
    }
    # generate skill bar svgs into assets/skillbars/
    os.makedirs(os.path.join(ASSETS, "skillbars"), exist_ok=True)
    skill_svgs = {}
    for name, pct in skills.items():
        svg = render_skill_bar(name, pct)
        fname = f"{name.replace(' ','_').lower()}.svg"
        path = os.path.join(ASSETS, "skillbars", fname)
        open(path, "w", encoding="utf8").write(svg)
        skill_svgs[name] = path.replace(ROOT + "/", "")

    # recolor snake if exists
    snake_path = os.path.join(OUTPUT, "github-contribution-grid-snake.svg")
    if os.path.exists(snake_path):
        recolor_snake(snake_path, color="#00F7FF")

    # render README
    rendered = tmpl.render(
        username="balajichowdary123",
        now=now,
        leetcode=lc,
        spotify=spotify,
        skill_svgs=skill_svgs
    )
    with open(OUT, "w", encoding="utf8") as f:
        f.write(rendered)
    print("Rendered README.md")

if __name__ == "__main__":
    main()
