#!/usr/bin/env python
"""Build a static public deployment from the private Orum Learning Lab source."""
from __future__ import annotations

import html
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import quote

import markdown
import yaml

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT / "_public_site"
BASE = ""
SITE_TITLE = "교육채널 오름"
SITE_DESC = "뇌과학·학습과학·자기조절학습을 교육 현장의 언어로 번역합니다."
CATEGORIES = [
    ("학습과학", "learning-science", "기억과 전략을 실제 공부의 언어로."),
    ("자기조절학습", "self-regulated-learning", "계획, 점검, 실행, 회고의 기술."),
    ("뇌파·뉴로피드백", "eeg-neurofeedback", "교육적 활용과 과학적 경계."),
    ("학습상담", "learning-consulting", "생각·정서·행동·환경을 함께 읽기."),
    ("교육채널오름서비스", "orum-services", "오름의 통합 학습설계와 상담 방식."),
]


def url(path: str) -> str:
    return BASE + "/" + quote(path.lstrip("/"), safe="/%:#?=&-_.")


def read_markdown(path: Path):
    raw = path.read_text(encoding="utf-8")
    if raw.startswith("---\n"):
        _, front, body = raw.split("---\n", 2)
        return yaml.safe_load(front) or {}, body.strip()
    return {}, raw


def render_md(text: str) -> str:
    return markdown.markdown(text, extensions=["extra", "sane_lists", "nl2br"])


def nav() -> str:
    links = "".join(
        f'<a href="{url("categories/" + slug + "/")}">{html.escape(label if label != "교육채널오름서비스" else "오름 서비스")}</a>'
        for label, slug, _ in CATEGORIES
    )
    return f'''<header class="site-header"><nav class="site-nav">
<a class="wordmark" href="{url('')}" aria-label="교육채널 오름 홈"><span class="wordmark-mark">O</span><span>교육채널 오름</span></a>
<div class="nav-links" aria-label="블로그 카테고리">{links}<a class="nav-cta" href="https://www.orumedu.com/" rel="noopener">오름 에듀</a></div>
</nav></header>'''


def shell(title: str, content: str, description: str = SITE_DESC) -> str:
    return f'''<!doctype html><html lang="ko-KR"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{html.escape(description)}"><title>{html.escape(title)} | {SITE_TITLE}</title>
<link rel="stylesheet" href="{url('assets/css/style.css')}"></head><body>{nav()}<main>{content}</main>
<footer class="site-footer"><p>© {datetime.now().year} 교육채널 오름 · 연구 근거와 교육 현장의 적용 가능성을 함께 다룹니다.</p><p><a href="{url('about/')}">소개</a> · <a href="{url('methodology/')}">운영 원칙</a> · <a href="{url('categories/')}">전체 카테고리</a></p></footer></body></html>'''


def post_url(post: dict) -> str:
    dt = post["date"]
    if isinstance(dt, datetime):
        day = dt
    else:
        day = datetime.fromisoformat(str(dt).replace(" +0900", "+09:00"))
    cats = "/".join(post.get("categories", []))
    slug = post["slug"]
    return f"{cats}/{day:%Y/%m/%d}/{slug}.html"


def post_card(post: dict) -> str:
    return f'''<article class="post-card"><p class="post-meta">{post["date"]:%Y. %m. %d} · {html.escape(" · ".join(post.get("categories", [])))}</p>
<h2><a href="{url(post_url(post))}">{html.escape(post["title"])}</a></h2><p>{html.escape(post.get("description", ""))}</p>
<a class="text-link" href="{url(post_url(post))}">읽어보기 <span aria-hidden="true">›</span></a></article>'''


def write(path: str, content: str):
    target = OUT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    shutil.copytree(ROOT / "assets", OUT / "assets")
    scss = (OUT / "assets/css/style.scss").read_text(encoding="utf-8")
    (OUT / "assets/css/style.css").write_text(re.sub(r"^---\s*---\s*", "", scss), encoding="utf-8")
    (OUT / "assets/css/style.scss").unlink()

    posts = []
    for source in sorted((ROOT / "_posts").glob("*.md"), reverse=True):
        front, body = read_markdown(source)
        front["slug"] = source.stem.split("-", 3)[-1]
        front["body"] = body
        if not isinstance(front.get("date"), datetime):
            front["date"] = datetime.fromisoformat(str(front["date"]).replace(" +0900", "+09:00"))
        posts.append(front)
    posts.sort(key=lambda x: x["date"], reverse=True)

    hero = f'''<section class="hero"><div class="hero-copy"><p class="eyebrow eyebrow-light">ORUM LEARNING LAB</p><h1>배움의 변화를<br>더 정확하게<br>이해합니다.</h1><p class="hero-summary">뇌과학과 학습과학의 연구를 학생·학부모·교육자가 실제로 활용할 수 있는 언어로 번역합니다.</p><a class="hero-link" href="{url('categories/')}">읽을거리 살펴보기 <span>›</span></a></div><div class="hero-art"><img src="{url('assets/images/orum-learning-lab-hero.png')}" alt="학습과 뇌의 연결을 상징하는 푸른 파형 이미지"></div></section>'''
    pillars = '''<section class="pillars section-light"><div class="section-label">WHAT WE STUDY</div><div class="pillar-grid"><article><span>01</span><h2>학습과학</h2><p>기억, 인출, 피드백, 메타인지를 실제 학습 전략으로 번역합니다.</p></article><article><span>02</span><h2>자기조절학습</h2><p>계획하고, 점검하고, 조정하는 힘이 학습을 어떻게 바꾸는지 살펴봅니다.</p></article><article><span>03</span><h2>근거와 경계</h2><p>뇌파와 뉴로피드백을 포함한 모든 정보를 과장 없이, 한계와 함께 다룹니다.</p></article></div></section>'''
    latest = "".join(post_card(p) for p in posts[:3])
    write("index.html", shell(SITE_TITLE, hero + pillars + f'<section class="latest"><div class="section-label">LATEST NOTES</div><div class="post-list">{latest}</div></section>'))

    cards = "".join(f'<a href="{url("categories/" + slug + "/")}"><span>{i:02d}</span><h2>{html.escape(label if label != "교육채널오름서비스" else "교육채널 오름 서비스")}</h2><p>{html.escape(desc)}</p><b>›</b></a>' for i, (label, slug, desc) in enumerate(CATEGORIES, 1))
    write("categories/index.html", shell("카테고리", f'<article class="page-shell"><header class="page-header"><p class="eyebrow">EDUCATION CHANNEL ORUM</p><h1>카테고리</h1></header><p class="category-intro">교육채널 오름의 글을 분야별로 읽어보세요. 각 카테고리는 독립된 아카이브 페이지로 운영됩니다.</p><div class="category-cards">{cards}</div></article>'))

    for label, slug, desc in CATEGORIES:
        selected = [p for p in posts if label in p.get("categories", [])]
        cards_html = "".join(post_card(p) for p in selected) or '<p class="empty-category">이 카테고리의 글을 준비하고 있습니다.</p>'
        title = label if label != "교육채널오름서비스" else "교육채널 오름 서비스"
        content = f'<section class="category-hero"><p class="eyebrow">CATEGORY</p><h1>{title}</h1><p>{html.escape(desc)}</p></section><section class="category-archive"><div class="post-list">{cards_html}</div></section>'
        write(f"categories/{slug}/index.html", shell(title, content, desc))

    for post in posts:
        thumbnail = post.get("thumbnail")
        thumb = f'<figure class="article-thumbnail"><img src="{url(thumbnail)}" alt="{html.escape(post["title"])}를 위한 대표 이미지"></figure>' if thumbnail else ""
        body = render_md(post["body"])
        content = f'''<article class="article-shell"><header class="article-header"><p class="eyebrow">{html.escape(" · ".join(post.get("categories", [])))}</p><h1>{html.escape(post["title"])}</h1><p class="article-deck">{html.escape(post.get("description", ""))}</p><div class="article-meta"><span>{html.escape(post.get("author", ""))}</span><time>{post["date"]:%Y년 %m월 %d일}</time></div></header>{thumb}<div class="article-body">{body}</div><footer class="article-footer"><p>교육채널 오름은 연구 근거와 교육 현장의 적용 가능성, 그리고 그 한계를 함께 다룹니다.</p></footer></article>'''
        write(post_url(post), shell(post["title"], content, post.get("description", SITE_DESC)))

    for name in ["about", "methodology", "topics"]:
        front, body = read_markdown(ROOT / f"{name}.md")
        title = front.get("title", name)
        content = f'<article class="page-shell"><header class="page-header"><p class="eyebrow">EDUCATION CHANNEL ORUM</p><h1>{html.escape(title)}</h1></header><div class="page-body">{render_md(body)}</div></article>'
        write(f"{name}/index.html", shell(title, content))

    write(".nojekyll", "")
    write("README.md", "# 교육채널 오름 공개 배포 사이트\n\n이 저장소는 private 소스 저장소에서 생성된 정적 배포 결과물입니다.\n")
    print(f"BUILT={OUT}")
    print(f"POSTS={len(posts)}")


if __name__ == "__main__":
    main()
