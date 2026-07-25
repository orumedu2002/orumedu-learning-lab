from pathlib import Path

html = (Path(__file__).parents[1] / "tools" / "multiple-intelligences-garden" / "index.html").read_text(encoding="utf-8")

assert "const APP_VERSION = 'v0.2'" in html, "v0.2 version marker is missing"
assert "<title>다중지능 검사</title>" in html, "browser title has not been renamed"
assert "<h1 class=\"title\">다중지능 검사</h1>" in html, "intro title has not been renamed"
assert "@media (max-width:560px)" in html, "mobile-specific breakpoint is missing"
assert "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">" in html, "mobile viewport meta tag is missing"
assert "v${APP_VERSION}" not in html, "version text must not accidentally be prefixed twice"
print("v0.2 static checks passed")
