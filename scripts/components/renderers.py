"""Page body renderers using content JSON and layout components."""

from __future__ import annotations

from datetime import datetime
from typing import Callable

from components.layout import (
    contact_channels,
    legal_sections,
    news_list,
    page_section,
    quote_wall,
    team_grid,
)
from content.loaders import (
    load_about,
    load_contact,
    load_fonds,
    load_impressum,
    load_join,
    load_news,
    load_privacy,
    load_team,
    load_terms,
)


def render_about(t: Callable[[str], str], prefix: str, asset_prefix: Callable[[str], str]) -> str:
    data = load_about()
    team_data = load_team()
    assets = asset_prefix(prefix)

    intro_parts = []
    for index, paragraph in enumerate(data["intro_paragraphs"]):
        if isinstance(paragraph, str):
            key = paragraph
        else:
            key = paragraph["text_key"]
        content = t(key)
        if index == 0:
            intro_parts.append(f'        <p class="larger">{content}</p>')
            if data.get("mission_statement"):
                intro_parts.append(
                    f'        <p class="intro-mission">{t(data["mission_statement"])}</p>'
                )
        else:
            intro_parts.append(f'        <p class="larger">{content}</p>')
    intro_paragraphs = "\n".join(intro_parts)
    team_members = [
        {
            "name": m["name"],
            "photo": m["photo"],
            "alt": t(m.get("alt_key", m["name"])),
        }
        for m in sorted(team_data["members"], key=lambda m: m["name"])
    ]
    quotes = [
        {"text": t(q["text_key"]), "author": q["author"]}
        for q in data.get("quotes", [])
    ]

    sections = [
        page_section(intro_paragraphs, intro=True),
        page_section(
            f"""        <h2>{t(data["who_heading"])}</h2>
{team_grid(team_members, assets)}""",
            section_id="team",
        ),
        page_section(
            f"""        <h2>{t(data["board_heading"])}</h2>
        <p>{t(data["board_body"])}</p>""",
        ),
        page_section(
            f"""        <h2>{t(data["quotes_heading"])}</h2>
{quote_wall(quotes)}""",
            extra_class="quote-wall-section",
        ),
    ]
    return "\n".join(sections)


def _format_date(iso_date: str, locale: str) -> str:
    dt = datetime.strptime(iso_date, "%Y-%m-%d")
    if locale == "de":
        months = [
            "Januar", "Februar", "März", "April", "Mai", "Juni",
            "Juli", "August", "September", "Oktober", "November", "Dezember",
        ]
        return f"{dt.day}. {months[dt.month - 1]} {dt.year}"
    return dt.strftime("%d %B %Y")


def render_news(t: Callable[[str], str], locale: str) -> str:
    data = load_news()
    items = sorted(data["items"], key=lambda x: x["date"], reverse=True)
    rendered = []
    for item in items:
        entry = {
            "date": item["date"],
            "date_display": _format_date(item["date"], locale),
            "title": t(item["title_key"]),
            "summary": t(item["summary_key"]),
        }
        if item.get("link"):
            entry["link"] = item["link"]
            entry["link_label"] = t(item["link_label_key"])
        rendered.append(entry)
    return page_section(news_list(rendered))


def render_contact(t: Callable[[str], str]) -> str:
    data = load_contact()
    channels = [
        {
            "title": t(c["title_key"]),
            "desc": t(c["desc_key"]),
            "action": c.get("action", ""),
            "action_label": t(c["action_label_key"]) if c.get("action_label_key") else "",
        }
        for c in data["channels"]
    ]
    quick_links = "\n".join(
        f'          <a href="{link["href"]}" class="button"'
        + (' target="_blank" rel="noopener noreferrer"' if link.get("external") else "")
        + f'>{t(link["label_key"])}</a>'
        for link in data["quick_links"]
    )
    address = "<br>".join(data["address_lines"])
    return "\n".join([
        page_section(contact_channels(channels), intro=True),
        page_section(
            f"""        <h2>{t(data["address_heading"])}</h2>
        <p>{address}</p>
        <p class="contact-note">{t(data["address_note_key"])}</p>""",
        ),
        page_section(
            f"""        <h2>{t(data["quick_links_heading"])}</h2>
        <div class="cta-band__actions">
{quick_links}
        </div>""",
        ),
    ])


def render_join(t: Callable[[str], str]) -> str:
    data = load_join()
    compare_rows = [
        (t(r["feature_key"]), t(r["member_key"]), t(r["non_member_key"]))
        for r in data["compare_rows"]
    ]
    headers = data["compare_headers"]
    table_rows = "\n".join(
        f'          <tr><th scope="row">{f}</th><td>{m}</td><td>{n}</td></tr>'
        for f, m, n in compare_rows
    )
    benefits = "\n".join(
        f'          <div class="benefit-item"><div class="benefit-title">{t(b["title_key"])}</div>'
        f'<div class="benefit-desc">{t(b["desc_key"])}</div></div>'
        for b in data["benefits"]
    )
    return "\n".join([
        f"""    <section class="founding-member-cta">
      <div class="content">
        <p class="cta-disclaimer">{t(data["disclaimer_key"])}</p>
        <div class="membership-tiers">
          <div class="membership-card">
            <div class="membership-price">CHF 100.–</div>
            <p>{t("2 Anteilscheine à CHF 50.– · Genossenschaftsmitgliedschaft bei Public AI Switzerland")}</p>
            <p>{t("Ab dem 2. Jahr jährlich mind. CHF 50.– in den Forschungs- und Entwicklungsfonds")}</p>
            <a href="#" class="button js-join-link">{t("Jetzt online zeichnen")}</a>
            <p class="cta-disclaimer">{t("Bezahlen mit TWINT und RaiseNow wird zeitnah freigeschaltet")}</p>
          </div>
        </div>
      </div>
    </section>""",
        page_section(
            f"""        <h2>{t(data["compare_heading"])}</h2>
        <p class="larger">{t(data["compare_intro_key"])}</p>
        <table class="member-compare">
          <thead>
            <tr>
              <th scope="col">{t(headers["feature_key"])}</th>
              <th scope="col">{t(headers["member_key"])}</th>
              <th scope="col">{t(headers["non_member_key"])}</th>
            </tr>
          </thead>
          <tbody>
{table_rows}
          </tbody>
        </table>""",
        ),
        page_section(
            f"""        <h2>{t("Deine Genossenschaftsvorteile")}</h2>
        <div class="benefits-grid">
{benefits}
        </div>""",
        ),
        page_section(
            f"""        <h2>{t("Unsere Statuten")}</h2>
        <p>{t("Die Statuten sind das Fundament der Genossenschaft: Sie regeln Zweck, Mitgliedschaft, Stimmrecht und wie Entscheidungen getroffen werden. Wir legen sie öffentlich offen, damit jede und jeder nachlesen kann, wie Public AI Switzerland funktioniert.")}</p>
        <p><a href="statuten.html" class="button">{t("Statuten öffnen →")}</a> <a href="fonds.html" class="button">{t("Reglement zum Forschungs- und Entwicklungsfonds öffnen →")}</a></p>""",
        ),
    ])


def _render_legal(data: dict, t: Callable[[str], str]) -> str:
    notice = page_section(
        f'        <p class="legal-doc__notice">{t(data["notice_key"])}</p>',
        intro=True,
        extra_class="legal-doc",
    )
    blocks = [(t(s["heading_key"]), t(s["body_key"])) for s in data["sections"]]
    return notice + "\n" + legal_sections(blocks)


def render_terms(t: Callable[[str], str]) -> str:
    return _render_legal(load_terms(), t)


def render_privacy(t: Callable[[str], str]) -> str:
    return _render_legal(load_privacy(), t)


def render_impressum(t: Callable[[str], str]) -> str:
    data = load_impressum()
    blocks = [(t(s["heading_key"]), t(s["body_key"])) for s in data["sections"]]
    return legal_sections(blocks)


def render_fonds(t: Callable[[str], str]) -> str:
    data = load_fonds()
    stats = "\n".join(
        f'          <div class="stat-card"><div class="stat-number">{a["percent"]}</div>'
        f'<div class="stat-label">{t(a["label_key"])}</div></div>'
        for a in data["allocation"]
    )
    principles = "\n".join(
        f'          <div class="benefit-item"><div class="benefit-title">{t(p["title_key"])}</div>'
        f'<div class="benefit-desc">{t(p["desc_key"])}</div></div>'
        for p in data["principles"]
    )
    return "\n".join([
        page_section(
            f"""        <div class="stats-grid">
{stats}
        </div>
        <p>{t(data["allocation_note_key"])}</p>""",
        ),
        page_section(
            f"""        <div class="involve-grid">
{principles}
        </div>
        <p><a href="join.html" class="button js-join-link">{t("Genossenschafter werden →")}</a> <a href="statuten.html" class="button">{t("Statuten ansehen")}</a></p>""",
        ),
    ])
