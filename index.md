---
layout: page
title: "GSoC 2012 Blog"
tagline: "Recent 'pushes' to the Slide importer"
---
{% include JB/setup %}

## All Posts


<ul class="posts">
  {% for post in site.posts %}
    <li><span>{{ post.date | date_to_string }}</span> &raquo; <a href="{{ BASE_PATH }}{{ post.url }}">{{ post.title }}</a></li>
  {% endfor %}
</ul>

