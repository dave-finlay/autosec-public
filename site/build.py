"""Builds securomatic.dev from this repository into site/dist, for
Cloudflare Pages: each Markdown page as HTML (so the basis record's
predicate type, https://securomatic.dev/basis/v1, is its
specification), and the keys and the avatar as they are.

    pip install -r site/requirements.txt && python3 site/build.py
"""

import html
import re
import shutil
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "site" / "dist"
GITHUB = "https://github.com/securomatic/public"

# Source page: where it's served (Pages serves a.html at /a).
PAGES = {
    "README.md": "index.html",
    "basis/v1.md": "basis/v1.html",
    "keys/README.md": "keys/index.html",
}
FILES = ["keys/*.pem", "brand/*.png"]

TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="icon" href="/brand/securomatic-avatar.png">
<style>
:root {{ --bg: #fbfaf7; --fg: #1b2422; --muted: #5b6663; --line: #e2ded6;
  --code: #f1eee8; --accent: #b4561b; }}
@media (prefers-color-scheme: dark) {{
  :root {{ --bg: #12201d; --fg: #e8e4dc; --muted: #9aa6a2; --line: #2a3a36;
    --code: #1a2b27; --accent: #f5a04b; }}
}}
body {{ margin: 0; background: var(--bg); color: var(--fg);
  font: 16px/1.6 system-ui, -apple-system, sans-serif; }}
main {{ max-width: 46rem; margin: 0 auto; padding: 1.5rem 16px 4rem; }}
header {{ display: flex; align-items: center; gap: .75rem;
  padding-bottom: 1rem; border-bottom: 1px solid var(--line); }}
header img {{ width: 40px; height: 40px; border-radius: 8px; }}
header a {{ color: var(--fg); font-weight: 600; text-decoration: none; }}
a {{ color: var(--accent); }}
code, pre {{ font: 14px/1.5 ui-monospace, SFMono-Regular, Menlo, monospace;
  background: var(--code); border-radius: 4px; }}
code {{ padding: .1em .3em; overflow-wrap: anywhere; }}
pre {{ padding: .75rem 1rem; overflow-x: auto; }}
pre code {{ padding: 0; background: none; }}
table {{ border-collapse: collapse; display: block; overflow-x: auto; }}
th, td {{ border: 1px solid var(--line); padding: .35rem .6rem;
  text-align: left; vertical-align: top; }}
</style>
</head>
<body>
<main>
<header><img src="/brand/securomatic-avatar.png" alt=""><a href="/">Securomatic</a></header>
{body}
</main>
</body>
</html>
"""


def build():
    if DIST.exists():
        shutil.rmtree(DIST)
    served = {source: out for source, out in PAGES.items()}
    for pattern in FILES:
        for path in sorted(ROOT.glob(pattern)):
            name = path.relative_to(ROOT).as_posix()
            served[name] = name
            (DIST / name).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(path, DIST / name)
    for source, out in PAGES.items():
        text = (ROOT / source).read_text()
        body = markdown.markdown(text, extensions=["tables", "fenced_code"])
        body = _links(body, source, served)
        heading = re.search(r"^# (.+)$", text, re.M)
        title = heading.group(1) if heading else "Securomatic"
        (DIST / out).parent.mkdir(parents=True, exist_ok=True)
        (DIST / out).write_text(TEMPLATE.format(title=html.escape(title), body=body))
    (DIST / "_headers").write_text(
        "/keys/*.pem\n  Content-Type: text/plain; charset=utf-8\n"
    )


def _links(body: str, source: str, served: dict[str, str]) -> str:
    """Relative links to what the site serves become links on the site;
    the rest go to the file on GitHub."""
    here = Path(source).parent

    def fix(match):
        href = match.group(1)
        if re.match(r"[a-z]+:|#|/", href):
            return match.group(0)
        parts = []  # the path from the repository's root, ".." resolved
        for part in (here / href).as_posix().split("/"):
            if part == "..":
                parts.pop()
            elif part not in ("", "."):
                parts.append(part)
        target = "/".join(parts)
        page = served.get(target) or served.get(f"{target}/README.md")
        if page:
            url = "/" + re.sub(r"(index)?\.html$", "", page)
            return f'href="{url}"'
        kind = "tree" if href.endswith("/") else "blob"
        return f'href="{GITHUB}/{kind}/main/{target}"'

    return re.sub(r'href="([^"]+)"', fix, body)


if __name__ == "__main__":
    build()
