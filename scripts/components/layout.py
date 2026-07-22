"""Shared layout and section HTML components."""

from __future__ import annotations

import html
from typing import Callable


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def subpage_header(
    title: str,
    subtitle: str = "",
    prefix: str = "",
    image: str | None = None,
    asset_prefix: Callable[[str], str] | None = None,
) -> str:
    style_attr = ""
    extra_class = ""
    if image:
        img_path = image.removeprefix("assets/")
        style_attr = f' style="--hero-background-image: url(\'/assets/{img_path}\');"'
        if "community-photos" in image:
            extra_class = " hero--custom-bg"
    subtitle_html = (
        f'\n        <p class="dynamic-numbers">{esc(subtitle)}</p>' if subtitle else ""
    )
    return f"""    <header class="hero hero--subpage{extra_class}"{style_attr}>
      <div class="hero__media" aria-hidden="true"></div>
      <div class="content">
        <h1>{esc(title)}</h1>{subtitle_html}
      </div>
    </header>"""


def page_section(
    inner: str,
    *,
    section_id: str = "",
    intro: bool = False,
    extra_class: str = "",
) -> str:
    classes = ["flex", "one", "page-section"]
    if intro:
        classes.append("intro-section")
    if extra_class:
        classes.append(extra_class)
    id_attr = f' id="{section_id}"' if section_id else ""
    return f"""    <section class="{' '.join(classes)}"{id_attr}>
      <div class="content">
{inner}
      </div>
    </section>"""


def pillar_grid(items: list[tuple[str, str, str]]) -> str:
    cards = []
    for label, title, desc in items:
        cards.append(
            f"""          <article class="pillar-card">
            <span class="pillar-card__label">{esc(label)}</span>
            <h3 class="pillar-card__title">{esc(title)}</h3>
            <p class="pillar-card__desc">{esc(desc)}</p>
          </article>"""
        )
    return f"""        <div class="pillar-grid">
{chr(10).join(cards)}
        </div>"""


def team_grid(members: list[dict[str, str]], assets: str) -> str:
    cards = []
    for member in members:
        photo = member["photo"]
        name = member["name"]
        alt = member.get("alt", name)
        role_html = ""
        if member.get("role"):
            role_html = f'\n            <p class="team-card__role">{esc(member["role"])}</p>'
        cards.append(
            f"""          <article class="team-card">
            <img class="team-card__photo" src="{assets}{photo}" alt="{esc(alt)}" loading="lazy">
            <h3 class="team-card__name">{esc(name)}</h3>{role_html}
          </article>"""
        )
    return f"""        <div class="team-grid">
{chr(10).join(cards)}
        </div>"""


def quote_wall(quotes: list[dict[str, str]]) -> str:
    items = []
    for quote in quotes:
        items.append(
            f"""          <blockquote class="quote-wall__item">
            <p class="quote-wall__text">{esc(quote["text"])}</p>
            <footer class="quote-wall__author">— {esc(quote["author"])}</footer>
          </blockquote>"""
        )
    return f"""        <div class="quote-wall">
{chr(10).join(items)}
        </div>"""


def news_list(items: list[dict[str, str]]) -> str:
    articles = []
    for item in items:
        link = item.get("link")
        link_html = ""
        if link:
            if link.startswith("http"):
                link_html = (
                    f'\n            <p><a href="{esc(link)}" class="button" '
                    f'target="_blank" rel="noopener noreferrer">{esc(item["link_label"])}</a></p>'
                )
            else:
                link_html = (
                    f'\n            <p><a href="{esc(link)}" class="button">'
                    f'{esc(item["link_label"])}</a></p>'
                )
        articles.append(
            f"""          <article class="news-list__item">
            <time class="news-list__date" datetime="{esc(item["date"])}">{esc(item["date_display"])}</time>
            <h3 class="news-list__title">{esc(item["title"])}</h3>
            <p class="news-list__summary">{esc(item["summary"])}</p>{link_html}
          </article>"""
        )
    return f"""        <div class="news-list">
{chr(10).join(articles)}
        </div>"""


def milestone_track(items: list[dict[str, str]]) -> str:
    steps = []
    for index, item in enumerate(items, start=1):
        status = item.get("status", "")
        status_class = f" milestone-step--{status}" if status else ""
        steps.append(
            f"""          <article class="milestone-step{status_class}">
            <span class="milestone-step__index">{index:02d}</span>
            <div class="milestone-step__body">
              <h3 class="milestone-step__title">{esc(item["title"])}</h3>
              <p class="milestone-step__when">{esc(item["when"])}</p>
              <p class="milestone-step__desc">{esc(item["desc"])}</p>
            </div>
          </article>"""
        )
    return f"""        <div class="milestone-track">
{chr(10).join(steps)}
        </div>"""


def ecosystem_grid(items: list[tuple[str, str]]) -> str:
    cards = []
    for title, desc in items:
        cards.append(
            f"""          <article class="ecosystem-card">
            <h3 class="ecosystem-card__title">{esc(title)}</h3>
            <p class="ecosystem-card__desc">{esc(desc)}</p>
          </article>"""
        )
    return f"""        <div class="ecosystem-grid">
{chr(10).join(cards)}
        </div>"""


def cta_band(title: str, body: str, buttons: list[tuple[str, str, bool]]) -> str:
    btn_html = []
    for label, href, external in buttons:
        attrs = ' class="button"'
        if external:
            attrs = ' class="button" target="_blank" rel="noopener noreferrer"'
        btn_html.append(f'          <a href="{esc(href)}"{attrs}>{esc(label)}</a>')
    return f"""    <section class="cta-band">
      <div class="content">
        <h2>{esc(title)}</h2>
        <p class="larger">{esc(body)}</p>
        <div class="cta-band__actions">
{chr(10).join(btn_html)}
        </div>
      </div>
    </section>"""


def contact_channels(channels: list[dict[str, str]]) -> str:
    cards = []
    for channel in channels:
        action = channel.get("action", "")
        action_html = ""
        if action:
            if action.startswith("mailto:"):
                action_html = f'\n            <p><a href="{esc(action)}" class="button">{esc(channel["action_label"])}</a></p>'
            elif action.startswith("http"):
                action_html = (
                    f'\n            <p><a href="{esc(action)}" class="button" '
                    f'target="_blank" rel="noopener noreferrer">{esc(channel["action_label"])}</a></p>'
                )
            else:
                action_html = f'\n            <p><a href="{esc(action)}" class="button">{esc(channel["action_label"])}</a></p>'
        cards.append(
            f"""          <article class="contact-card">
            <h3 class="contact-card__title">{esc(channel["title"])}</h3>
            <p class="contact-card__desc">{esc(channel["desc"])}</p>{action_html}
          </article>"""
        )
    return f"""        <div class="contact-grid">
{chr(10).join(cards)}
        </div>"""


def legal_sections(blocks: list[tuple[str, str]]) -> str:
    parts = []
    for heading, body in blocks:
        parts.append(
            page_section(
                f"""        <h3>{esc(heading)}</h3>
        <p>{body}</p>""",
                intro=True,
                extra_class="legal-doc",
            )
        )
    return "\n".join(parts)


def compare_table(rows: list[tuple[str, str, str]]) -> str:
    table_rows = []
    for feature, member, non_member in rows:
        table_rows.append(
            f"""          <tr>
            <th scope="row">{esc(feature)}</th>
            <td>{esc(member)}</td>
            <td>{esc(non_member)}</td>
          </tr>"""
        )
    return f"""        <table class="member-compare">
          <thead>
            <tr>
              <th scope="col"></th>
              <th scope="col"></th>
              <th scope="col"></th>
            </tr>
          </thead>
          <tbody>
{chr(10).join(table_rows)}
          </tbody>
        </table>"""
