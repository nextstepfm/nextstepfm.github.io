---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

layout: default
starring: [7gano,k_katsumi,sonson_twit]
---

<div class="home">
  {%- if page.title -%}
    <h1 class="page-heading">{{ page.title }}</h1>
  {%- endif -%}

  <!-- {{ content }} -->

<!-- 
  {% if site.paginate %}
    {% assign posts = paginator.posts %}
  {% else %}
    {% assign posts = site.posts %}
  {% endif %} -->

  {%- for name in page.starring -%}
    <a href="https://twitter.com/{{name}}"><img class="twitter" src="{{site.baseurl}}/images/{{name}}.jpg" style="margin-left:10px;"/></a>
  {%- endfor -%}


  <p style="margin-top:20px">{{ site.description }}</p>

  {%- if posts.size > 0 -%}
    {%- if page.list_title -%}
      <h2 class="post-list-heading">{{ page.list_title }}</h2>
    {%- endif -%}
    <ul class="post-list">
      {%- assign date_format = site.minima.date_format | default: "%b %-d, %Y" -%}
      {%- for post in posts -%}
      <li>
          {%- if post.type == "podcast" -%}
            <img src="{{site.baseurl}}/images/mic-24px.svg" alt="" width="24" height="24">
          {%- else %}
            <img src="{{site.baseurl}}/images/article-24px.svg" alt="" width="24" height="24">
          {%- endif -%}
        <span class="post-meta" style="margin-left:10px;">{{ post.date | date: date_format }} - Episode {{ post.episode }}</span>
        <h3>
          <a class="post-link" href="{{ post.url | relative_url }}">
            {{ post.title }}
          </a>
        </h3>
        {%- if site.show_excerpts -%}
          {{ post.excerpt }}
        {%- endif -%}
      </li>
      {%- endfor -%}
    </ul>

  {%- endif -%}

</div>