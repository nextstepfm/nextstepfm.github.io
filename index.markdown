---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

layout: default
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

  <img src="{{site.baseurl}}/images/logo.jpg" alt="" width="128" height="128">
  <p style="margin-top:20px">k_katsumi, sonson_twit がiOSを中心にお話しするポッドキャスト．ハッシュタグ #nextstepfm でお便り募集しています．オリジナルメンバーは，_katsumi, 7gano, sonson_twitの3人でお話ししていました．</p>

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