---
layout: page
title: 카테고리
permalink: /categories/
---

<p class="category-intro">교육채널 오름의 글을 주제별로 모았습니다. 연구의 언어와 학습 현장의 질문이 만나는 지점을 찾아보세요.</p>

<div class="category-index">
{% assign sorted_categories = site.categories | sort %}
{% for category in sorted_categories %}
  {% assign category_name = category[0] %}
  {% assign posts = category[1] %}
  <section class="category-group" id="{{ category_name | slugify }}">
    <div class="category-group-title">
      <h2>{{ category_name }}</h2>
      <span>{{ posts.size }}개 글</span>
    </div>
    <div class="category-posts">
      {% for post in posts %}
        <article>
          <p>{{ post.date | date: "%Y. %m. %d" }}</p>
          <h3><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h3>
          <a class="text-link" href="{{ post.url | relative_url }}">읽어보기 <span aria-hidden="true">›</span></a>
        </article>
      {% endfor %}
    </div>
  </section>
{% endfor %}
</div>
