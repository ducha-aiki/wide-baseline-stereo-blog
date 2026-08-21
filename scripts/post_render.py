#!/usr/bin/env python3
"""Post-render fixes that Quarto does not do on its own.

1. Alias stubs (the pages that keep the old fastpages URLs alive) are
   JavaScript-only redirects.  Crawlers that do not run JS -- Googlebot on a
   bad day, GPTBot, ClaudeBot, Slack/Twitter unfurlers, curl -- see an empty
   page instead of following the redirect.  We add a <meta http-equiv=refresh>,
   a canonical link to the new URL and a plain <a> for humans.

2. The Jekyll blog served its RSS at /feed.xml, Quarto serves it at /index.xml.
   Copy the feed to the old path so subscribers from before the migration keep
   getting posts.
"""

import os
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(os.environ.get("QUARTO_PROJECT_ROOT", ".")).resolve()
OUT = Path(os.environ.get("QUARTO_PROJECT_OUTPUT_DIR", "docs"))
if not OUT.is_absolute():
    OUT = ROOT / OUT

REDIRECT_MARKER = "var redirects = {"
TARGET_RE = re.compile(r'var redirects = \{(.*?)\};', re.S)
DEFAULT_TARGET_RE = re.compile(r'""\s*:\s*"([^"]+)"')


def site_url():
    text = (ROOT / "_quarto.yml").read_text(encoding="utf-8")
    m = re.search(r'^\s*site-url:\s*["\']?([^"\'\s]+)', text, re.M)
    return m.group(1).rstrip("/") if m else ""


def absolute_target(stub: Path, relative_target: str, base: str) -> str:
    """Resolve a stub-relative redirect target into an absolute site URL."""
    resolved = os.path.normpath(str((stub.parent / relative_target)))
    try:
        path = Path(resolved).relative_to(OUT)
    except ValueError:
        return ""
    return f"{base}/{path.as_posix()}" if base else ""


TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Redirect</title>
<script type="text/javascript">
  var redirects = {{{redirects}}};
  var hash = window.location.hash.startsWith('#') ? window.location.hash.slice(1) : window.location.hash;
  var redirect = redirects[hash] || redirects[""] || "/";
  window.document.title = 'Redirect to  ' +  redirect;
  window.location.replace(redirect);
</script>
<meta http-equiv="refresh" content="0; url={target}">
{canonical}<meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
<p>This page has moved to <a href="{target}">{display}</a>.</p>
</body>
</html>
"""


def rewrite_stubs(base: str) -> int:
    fixed = 0
    for path in OUT.rglob("*.html"):
        try:
            html = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        if REDIRECT_MARKER not in html or "http-equiv=\"refresh\"" in html:
            continue
        redirects = TARGET_RE.search(html)
        default = DEFAULT_TARGET_RE.search(html)
        if not redirects or not default:
            continue
        target = default.group(1)
        absolute = absolute_target(path, target, base)
        canonical = f'<link rel="canonical" href="{absolute}">\n' if absolute else ""
        path.write_text(
            TEMPLATE.format(
                redirects=redirects.group(1).strip(),
                target=target,
                canonical=canonical,
                display=absolute or target,
            ),
            encoding="utf-8",
        )
        fixed += 1
    return fixed


def copy_legacy_feed() -> bool:
    feed = OUT / "index.xml"
    if not feed.exists():
        return False
    shutil.copyfile(feed, OUT / "feed.xml")
    return True


def main():
    if not OUT.is_dir():
        print(f"post_render: output dir {OUT} not found, skipping", file=sys.stderr)
        return
    base = site_url()
    if not base:
        print("post_render: no site-url in _quarto.yml, canonical links skipped", file=sys.stderr)
    print(f"post_render: rewrote {rewrite_stubs(base)} redirect stubs")
    print(f"post_render: legacy feed.xml {'written' if copy_legacy_feed() else 'skipped (no index.xml)'}")


if __name__ == "__main__":
    main()
