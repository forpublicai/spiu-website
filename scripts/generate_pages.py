#!/usr/bin/env python3
"""Generate static pages for all locales using shared site CSS classes."""

from __future__ import annotations

import html
import json
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS_DIR))

from components.layout import subpage_header  # noqa: E402
from components.renderers import (  # noqa: E402
    render_about,
    render_contact,
    render_fonds,
    render_impressum,
    render_join,
    render_news,
    render_privacy,
    render_terms,
)
from content.loaders import (  # noqa: E402
    load_about,
    load_contact,
    load_fonds,
    load_impressum,
    load_join,
    load_news,
    load_privacy,
    load_community_photos,
    load_terms,
)

ROOT = Path(__file__).resolve().parents[1]
STATS = json.loads((ROOT / "assets" / "stats.json").read_text(encoding="utf-8"))

OPEN_COLLECTIVE = (
    "https://opencollective.com/datalets/projects/public-ai-switzerland/"
    "contribute/founding-membership-99202/checkout?interval=year&amount=100&contributeAs=me"
)

SITE = "https://publicai.ch"
LOCALES = ("en", "de", "fr", "it", "rm")
LANG_ATTR = {
    "en": "en",
    "de": "de-CH",
    "fr": "fr-CH",
    "it": "it-CH",
    "rm": "rm-CH",
}
LOGO_BY_LOCALE = {
    "en": "logo-switzerland-en.png",
    "de": "logo-switzerland-de.png",
    "fr": "logo-switzerland-fr.png",
    "it": "logo-switzerland-it.png",
    "rm": "logo-switzerland-rm.png",
}

I18N: dict[str, str] = {}
CURRENT_LOCALE = "en"
CURRENT_PREFIX = ""


def load_i18n(locale: str) -> dict[str, str]:
    path = ROOT / "scripts" / f"i18n_{locale}.json"
    return json.loads(path.read_text(encoding="utf-8"))


def set_locale(locale: str) -> None:
    global I18N, CURRENT_LOCALE, CURRENT_PREFIX
    CURRENT_LOCALE = locale
    CURRENT_PREFIX = "" if locale == "en" else locale
    I18N = load_i18n(locale)


SITE = "https://publicai.ch"


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def t(de: str) -> str:
    return I18N.get(de, de)


def t_format(de: str, **kwargs: str) -> str:
    return I18N.get(de, de).format(**kwargs)


def fmt_stat(value: int | float | None) -> str:
    if value is None:
        return "—"
    return f"{int(value):,}".replace(",", "'")


def fmt_tokens_billions(value: int | float | None) -> str:
    if value is None:
        return "—"
    return f"{value / 1_000_000_000:.2f}B"


def asset_prefix(prefix: str = "") -> str:
    return "../" if prefix else ""


def locale_href(locale: str, page: str) -> str:
    if page == "index.html":
        return f"{SITE}/" if locale == "en" else f"{SITE}/{locale}/"
    return f"{SITE}/{page}" if locale == "en" else f"{SITE}/{locale}/{page}"


def head(title: str, description: str, page: str, prefix: str = "") -> str:
    locale = CURRENT_LOCALE
    lang = LANG_ATTR[locale]
    assets = asset_prefix(prefix)
    canonical = locale_href(locale, page)
    x_default = locale_href("en", page)
    hreflang_lines = "\n".join(
        f'  <link rel="alternate" hreflang="{LANG_ATTR[loc]}" href="{locale_href(loc, page)}">'
        for loc in LOCALES
    )
    return f"""  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(description)}">
  <link rel="canonical" href="{canonical}">
{hreflang_lines}
  <link rel="alternate" hreflang="x-default" href="{x_default}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@500;600&family=Overpass+Mono&family=Overpass:wght@700&family=Public+Sans:wght@300;400;600&family=Roboto+Flex:wght@500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{assets}assets/fonts/nb-international.css">
  <link href="{assets}assets/style.css" rel="stylesheet" type="text/css">
  <link rel="icon" href="/favicon.ico">"""


def nav(overlay: bool = False, prefix: str = "") -> str:
    nav_class = "site-nav site-nav--overlay" if overlay else "site-nav site-nav--solid"
    root = f"/{prefix}/" if prefix else "/"
    p = f"/{prefix}/" if prefix else "/"
    assets = asset_prefix(prefix)
    logo = LOGO_BY_LOCALE.get(CURRENT_LOCALE, LOGO_BY_LOCALE["en"])
    return f"""  <nav class="{nav_class}" aria-label="Main">
    <a class="site-nav__brand" href="{root}" title="Public AI Switzerland">
      <img src="{assets}assets/{logo}" alt="Public AI Switzerland" class="site-nav__logo">
    </a>
    <div class="site-nav__cluster">
      <div class="site-nav__lang" data-lang-switcher></div>
      <button class="site-nav__toggle" type="button" aria-label="{esc(t('Toggle navigation menu'))}" aria-expanded="false" aria-controls="site-menu">
        <span></span><span></span><span></span>
      </button>
      <button class="site-nav__backdrop" type="button" aria-label="{esc(t('Close menu'))}" tabindex="-1"></button>
      <div class="site-nav__links" id="site-menu">
        <a href="{p}about.html" class="site-nav__link">{t('Über uns')}</a>
        <a href="{p}news.html" class="site-nav__link">{t('News')}</a>
        <a href="{p}contact.html" class="site-nav__link">{t('Kontakt')}</a>
        <a href="#" class="site-nav__link is-disabled" tabindex="-1" aria-disabled="true">{t('Mitglieder-Login')}</a>
        <a href="{p}join.html" class="site-nav__cta button button--primary js-join-link">{t('Anteil zeichnen')}</a>
      </div>
    </div>
  </nav>"""


def footer(prefix: str = "") -> str:
    p = f"/{prefix}/" if prefix else "/"
    assets = asset_prefix(prefix)
    return f"""  <footer class="site-footer" id="resources">
    <div class="site-footer__content">
      <div class="site-footer__links">
        <a href="{p}news.html">{t('News')}</a>
        <a href="{p}about.html">{t('Über uns')}</a>
        <a href="{p}join.html" class="js-join-link">{t('Become a member')}</a>
        <a href="{p}contact.html">{t('Kontakt')}</a>
        <a href="https://www.apertus-ai.org/" target="_blank" rel="noopener noreferrer">Apertus</a>
        <a href="https://chat.publicai.co/" target="_blank" rel="noopener noreferrer">{t('Chat')}</a>
        <a href="https://platform.publicai.co/docs" target="_blank" rel="noopener noreferrer">{t('API docs')}</a>
        <a href="https://huggingface.co/blog/inference-providers-publicai" target="_blank" rel="noopener noreferrer">{t('Hugging Face')}</a>
        <a href="https://github.com/forpublicai/publicai.ch" target="_blank" rel="noopener noreferrer">{t('Source of this website')}</a>
      </div>
      <p>{t('Photo: Joshua Tan (CC BY 4.0)')}</p>
      <div class="site-footer__legal">
        <a href="{p}statuten.html">{t('Statutes')}</a>
        <a href="{p}fonds.html">{t('Research & development fund')}</a>
        <a href="{p}terms.html">{t('Terms & Conditions')}</a>
        <a href="{p}privacy.html">{t('Privacy Notice')}</a>
        <a href="{p}impressum.html">{t('Legal notice')}</a>
        <a href="{p}about.html">{t('Über uns')}</a>
      </div>
      <p>{t('Copyright © Public AI Switzerland 2026. All rights reserved.')}</p>
    </div>
  </footer>
  <script src="{assets}assets/lang-switcher.js"></script>
  <script src="{assets}assets/site-nav.js"></script>
  <script src="{assets}assets/join.js"></script>"""


def page_shell(
    title: str,
    description: str,
    page: str,
    body: str,
    overlay: bool | None = None,
    prefix: str = "",
    extra_scripts: str = "",
    subpage_title: str | None = None,
    hero_image: str | None = None,
) -> str:
    use_overlay = overlay if overlay is not None else subpage_title is not None
    if subpage_title:
        body = (
            subpage_header(
                subpage_title,
                prefix,
                hero_image,
                asset_prefix,
            )
            + "\n"
            + body
        )
    lang = LANG_ATTR[CURRENT_LOCALE]
    body_attr = ' style="margin: 0; padding: 0;"'
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
{head(title, description, page, prefix)}
</head>
<body{body_attr}>
{nav(use_overlay, prefix)}
<main>
{body}
</main>
{footer(prefix)}
{extra_scripts}</body>
</html>
"""


def timeline_section() -> str:
    logo = LOGO_BY_LOCALE.get(CURRENT_LOCALE, LOGO_BY_LOCALE["en"])
    return f"""    <section class="flex one" id="timeline">
      <div class="content">
        <h2>{t('Eine Schweizer Tradition, fortgesetzt')}</h2>
        <div class="timeline-layout">
          <div class="timeline-sidebar">
            <p>{t('In jeder Epoche des industriellen Wandels hat die Schweiz gleich reagiert: mit Genossenschaften. Fahre mit der Maus über jede Epoche, um mehr zu erfahren.')}</p>
          </div>
          <div class="timeline">
            <div class="timeline__item">
              <div class="timeline__marker"><span class="timeline__year">1899</span></div>
              <div class="timeline__body">
                <img src="/assets/logo-raiffeisen.png" alt="Raiffeisen" class="timeline__logo">
                <p class="timeline__era">{t('Banking für die Bevölkerung')}</p>
                <p class="timeline__detail">{t('Als Banken Städte, aber nicht Bauern bedienten, legten Schweizer Gemeinden ihr Erspartes zusammen und steuerten ihre eigene Kreditversorgung.')}</p>
              </div>
            </div>
            <div class="timeline__item">
              <div class="timeline__marker"><span class="timeline__year">1925</span></div>
              <div class="timeline__body">
                <img src="/assets/logo-migros.png" alt="Migros" class="timeline__logo">
                <p class="timeline__era">{t('Faire Zugang zu Grundbedürfnissen')}</p>
                <p class="timeline__detail">{t('Als Zwischenhändler die Lebensmittelpreise in die Höhe trieben, fuhr Gottlieb Duttweiler mit einem Lastwagen zu den Menschen. Heute ist Migros der grösste Detailhändler der Schweiz — immer noch eine Genossenschaft.')}</p>
              </div>
            </div>
            <div class="timeline__item">
              <div class="timeline__marker"><span class="timeline__year">1941</span></div>
              <div class="timeline__body">
                <img src="/assets/logo-coop.png" alt="Coop" class="timeline__logo">
                <p class="timeline__era">{t('Solidarität der Konsument:innen')}</p>
                <p class="timeline__detail">{t('Als der Krieg Knappheit bedrohte, fusionierten Konsumentenkooperativen zu einer nationalen Kraft und gaben die Kaufkraft zurück in die Hände der Mitglieder.')}</p>
              </div>
            </div>
            <div class="timeline__item">
              <div class="timeline__marker"><span class="timeline__year">1997</span></div>
              <div class="timeline__body">
                <img src="/assets/logo-mobility.png" alt="Mobility" class="timeline__logo">
                <p class="timeline__era">{t('Geteilte Infrastruktur')}</p>
                <p class="timeline__detail">{t("Als privater Autobesitz verschwenderisch wirkte, hat die Schweiz das Genossenschafts-Carsharing vorangetrieben — heute mit 230'000 Mitgliedern.")}</p>
              </div>
            </div>
            <div class="timeline__item timeline__item--highlight">
              <div class="timeline__marker"><span class="timeline__year">2025</span></div>
              <div class="timeline__body">
                <img src="/assets/{logo}" alt="Public AI Switzerland" class="timeline__logo">
                <p class="timeline__era">{t('Kollektive Intelligenz')}</p>
                <p class="timeline__detail">{t('Als KI zu kritischer Infrastruktur wurde, die von wenigen ausländischen Konzernen kontrolliert wird, hat die Schweiz getan, was sie immer tut: eine Genossenschaft gegründet.')}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>"""


def legacy_join_section() -> str:
    disclaimer = t(
        'Hinweis: Public AI Switzerland wird noch aufgebaut und die Vorteile können sich ändern. Bis dahin werden Gründungsmitgliedsbeiträge treuhänderisch von <a href="https://datalets.ch" target="_blank" rel="noopener noreferrer">Datalets.ch</a>, einem Schweizer gemeinnützigen Verein, verwaltet. Der Kauf berechtigt zu zwei Anteilscheinen à je CHF 50 in der Genossenschaft. Zahlung via TWINT und RaiseNow folgt in Kürze.'
    )
    return f"""    <section class="founding-member-cta" id="join-legacy">
      <div class="content">
        <h2>{t('Unser Plan: KI im Besitz der Bevölkerung')}</h2>
        <p class="cta-subtitle">{t('KI verändert unsere Arbeit, unsere Wirtschaft und unsere Gesellschaft. Wir haben einen Plan, KI um lokale Kontrolle, gemeinsamen Nutzen und demokratische Governance zu organisieren. Werde noch heute Gründungsmitglied und mach mit.')}</p>
        <div class="cta-membership-tiers">
          <h3>{t('GRÜNDUNGSMITGLIED WERDEN:')}</h3>
          <div class="membership-tiers">
            <div class="membership-card">
              <div class="membership-price">CHF 100</div>
              <p>{t('Gründungsmitgliedschaft bei Public AI Switzerland')}</p>
              <a href="#" class="button js-join-link">{t('MITMACHEN UND MITGLIED WERDEN')}</a>
              <p class="cta-disclaimer">{disclaimer}</p>
            </div>
          </div>
        </div>
        <div class="cta-benefits">
          <h3>{t('VORTEILE FÜR GRÜNDUNGSMITGLIEDER')}</h3>
          <div class="benefits-grid">
            <div class="benefit-item"><div class="benefit-title">{t('Verbessertes Chat-Erlebnis')}</div><div class="benefit-desc">{t('Grössere Kontextfenster, Datei- und Bild-Uploads sowie Gruppenchats in einem erweiterten Apertus-Erlebnis.')}</div></div>
            <div class="benefit-item"><div class="benefit-title">{t('Am Puls der Zeit bleiben')}</div><div class="benefit-desc">{t('Jeden Monat neue KI-Tools aus unserer Community und von Technologiepartnern.')}</div></div>
            <div class="benefit-item"><div class="benefit-title">{t('Limitierte physische Zine')}</div><div class="benefit-desc">{t('Eine limitierte physische Ausgabe des Own Our Own (O3) Plans plus ein Mitgliedschaftszertifikat.')}</div></div>
          </div>
        </div>
      </div>
    </section>"""


def legacy_compare_section() -> str:
    logo = LOGO_BY_LOCALE.get(CURRENT_LOCALE, LOGO_BY_LOCALE["en"])
    return f"""    <section class="flex one" id="compare">
      <div class="content">
        <h2>{t('So vergleichen wir uns')}</h2>
        <div class="compare-grid">
          <div class="compare-card compare-card--ours">
            <h3><img src="/assets/{logo}" alt="Public AI Switzerland" class="compare-logo"></h3>
            <div class="compare-row"><span class="compare-label">{t('Kosten')}</span><span class="compare-value">CHF 100{t('/ Jahr')}</span></div>
            <div class="compare-row"><span class="compare-label">{t('Datenresidenz')}</span><span class="compare-value">{t('Schweiz')}</span></div>
            <div class="compare-row"><span class="compare-label">{t('Eigentum')}</span><span class="compare-value">{t('Genossenschaft, du bist Miteigentümer:in')}</span></div>
            <div class="compare-row"><span class="compare-label">{t('Governance')}</span><span class="compare-value">{t('Eine Person, eine Stimme')}</span></div>
            <div class="compare-row"><span class="compare-label">{t('Überschüsse')}</span><span class="compare-value">{t('Für Mitglieder reinvestiert')}</span></div>
            <div class="compare-row"><span class="compare-label">{t('Quellcode')}</span><span class="compare-value">{t('Open Source')}</span></div>
            <div class="compare-row"><span class="compare-label">{t('Modell')}</span><span class="compare-value">{t('Apertus (in der Schweiz entwickelt, offen)')}</span></div>
          </div>
          <div class="compare-card compare-card--theirs">
            <h3>ChatGPT (OpenAI)</h3>
            <div class="compare-row"><span class="compare-label">{t('Kosten')}</span><span class="compare-value">CHF 240{t('/ Jahr')}</span></div>
            <div class="compare-row"><span class="compare-label">{t('Datenresidenz')}</span><span class="compare-value">{t('Vereinigte Staaten')}</span></div>
            <div class="compare-row"><span class="compare-label">{t('Eigentum')}</span><span class="compare-value">{t('Aktiengesellschaft, Aktionär:innen besitzen es')}</span></div>
            <div class="compare-row"><span class="compare-label">{t('Governance')}</span><span class="compare-value">{t('Verwaltungsrat')}</span></div>
            <div class="compare-row"><span class="compare-label">{t('Überschüsse')}</span><span class="compare-value">{t('Aktionärsdividenden')}</span></div>
            <div class="compare-row"><span class="compare-label">{t('Quellcode')}</span><span class="compare-value">{t('Geschlossen')}</span></div>
            <div class="compare-row"><span class="compare-label">{t('Modell')}</span><span class="compare-value">{t('GPT (proprietär)')}</span></div>
          </div>
        </div>
      </div>
    </section>"""


def dialogue_section(prefix: str = "") -> str:
    assets = asset_prefix(prefix)
    partners = [
        ("public-ai.png", "Public AI"),
        ("change-org.svg", "Change.org"),
        ("eth-ai-center.png", "ETH AI Center"),
        ("epfl-ai-center.png", "EPFL AI Center"),
        ("apertus.png", "Apertus"),
        ("collective-intelligence-project.png", "Collective Intelligence Project"),
        ("swiss-ai-weeks.png", "Swiss {ai} Weeks"),
        ("metagov.png", "Metagov"),
    ]
    logos = "\n".join(
        f'          <img src="{assets}assets/partners/{filename}" alt="{esc(alt)}" class="dialogue-partners__logo" loading="lazy">'
        for filename, alt in partners
    )
    return f"""    <section class="flex one distribution-cta" id="dialogue">
      <div class="content">
        <h2>{t('Im Schweizer Nationalen KI-Dialog mitreden')}</h2>
        <p class="larger">{t('Public AI Switzerland veranstaltet einen nationalen Dialog zur KI-Politik und -Infrastruktur der Schweiz. Mach mit und hilf mitzugestalten, wie KI der Öffentlichkeit dient.')}</p>
        <p class="distribution-cta__actions"><a href="https://dialogue.publicai.ch" class="button" target="_blank" rel="noopener noreferrer">{t('Join the dialogue')}</a></p>
        <div class="dialogue-partners" aria-label="{esc(t('Partner des Schweizer Nationalen KI-Dialogs'))}">
          <p class="dialogue-partners__label">{t('In Zusammenarbeit mit:')}</p>
          <div class="dialogue-partners__logos">
{logos}
          </div>
        </div>
      </div>
    </section>"""


def legacy_faq_section() -> str:
    return f"""    <section class="flex one" id="faq">
      <div class="content">
        <h2>{t('Häufige Fragen')}</h2>
        <div class="faq-list">
          <details class="faq-item"><summary>{t('Wie funktioniert die Mitgliedschaft?')}</summary><p>{t('Mitgliedschaft bei Public AI Switzerland bedeutet, dass du Miteigentümer:in mit Stimmrecht bist. Um Mitglied zu werden, kaufst du zuerst zwei Genossenschaftsanteile à je CHF 50 (insgesamt CHF 100). Diese berechtigen dich zum Stimmen. Ab dem zweiten Jahr beträgt der jährliche Mitgliedsbeitrag CHF 50.')}</p><p>{t('Stimmrechte sind von Gebühren für Mitgliederleistungen getrennt. Der erste Mitgliedsbeitrag beinhaltet ein einjähriges kostenloses Abo für Mitgliederleistungen. Die Nutzung von Apertus ist separat; der Chat ist kostenlos, die API wird separat abgerechnet. Überschüsse werden reinvestiert, nicht ausgeschüttet.')}</p></details>
          <details class="faq-item"><summary>{t('Warum eine Genossenschaft gründen?')}</summary><p>{t('Die Schweiz verlässt sich zunehmend auf ausländische KI-Plattformen, die aus Silicon Valley oder Shenzhen gesteuert werden. Es ist Zeit für ein neues Modell — eines, das wir gemeinsam besitzen und kontrollieren.')}</p></details>
          <details class="faq-item"><summary>{t('Was ist eine Genossenschaft?')}</summary><p>{t('Eine Genossenschaft ist ein Unternehmen im Besitz und unter demokratischer Kontrolle ihrer Mitglieder. Denk an Migros, Coop, Raiffeisen oder Mobility.')}</p></details>
          <details class="faq-item"><summary>{t('Wie unterscheidet sich das von ChatGPT/OpenAI?')}</summary><p>{t('Statt CHF 240 pro Jahr für ChatGPT zu zahlen, zahlen Mitglieder CHF 100 und besitzen einen Teil ihrer eigenen KI.')}</p></details>
          <details class="faq-item"><summary>{t('Ist die Plattform bereits live?')}</summary><p>{t('Ja! Probiere es auf <a href="https://chat.publicai.co" target="_blank" rel="noopener noreferrer">chat.publicai.co</a> oder die API unter <a href="https://platform.publicai.co/docs" target="_blank" rel="noopener noreferrer">platform.publicai.co/docs</a>.')}</p></details>
        </div>
      </div>
    </section>"""


def index_body(prefix: str = "") -> str:
    users = fmt_stat(STATS.get("registeredUsers"))
    developers = fmt_stat(STATS.get("developers"))
    tokens = fmt_tokens_billions(STATS.get("tokensProcessed"))
    hero_stats = t_format(
        "Schliesse dich {users} registrierten Nutzer:innen und {developers} Entwickler:innen an, die Schweizer KI nutzen",
        users=f"<strong>{users}</strong>",
        developers=f"<strong>{developers}</strong>",
    )
    return f"""    <header class="hero">
      <div class="hero__media" aria-hidden="true"></div>
      <div class="content">
        <h1>{t('Die weltweit erste Genossenschaft für KI')}</h1>
        <p class="dynamic-numbers">{hero_stats}</p>
        <div class="hero-cta">
          <a href="join.html" class="button button--primary js-join-link">{t('Genossenschaftsanteil zeichnen →')}</a>
          <a href="https://chat.publicai.co/" class="button button--hero-outline" target="_blank" rel="noopener noreferrer">{t('Apertus kostenlos nutzen')}</a>
          <a href="https://dialogue.publicai.ch" class="button button--hero-olive hero-cta__dialogue" target="_blank" rel="noopener noreferrer">{t('(Neu) Dem Schweizer Nationalen KI-Dialog beitreten')}</a>
        </div>
      </div>
      <a href="#intro" class="hero-scroll-cue" aria-label="{esc(t('Nach unten scrollen'))}">&#8964;</a>
    </header>

    <section class="flex one intro-section" id="intro">
      <div class="content">
        <p class="larger">{t('Public AI Switzerland ist eine kundeneigene Genossenschaft, die in der Schweiz entwickelte KI, insbesondere Apertus, für Schweizer Einwohner:innen und Unternehmen zugänglich macht.')}</p>
        <div class="stat-strip stat-strip--panel" id="stats">
          <div class="stat-strip__item">
            <span class="stat-strip__value stat-strip__value--accent">#1</span>
            <span class="stat-strip__label">{t('Apertus-Deployer weltweit')}</span>
          </div>
          <div class="stat-strip__item">
            <span class="stat-strip__value">{users}</span>
            <span class="stat-strip__label">{t('registrierte Nutzer:innen')}</span>
          </div>
          <div class="stat-strip__item">
            <span class="stat-strip__value">{developers}</span>
            <span class="stat-strip__label">{t('Entwickler:innen, die unsere API nutzen')}</span>
          </div>
          <div class="stat-strip__item">
            <span class="stat-strip__value">{tokens}</span>
            <span class="stat-strip__label">{t('Tokens verarbeitet')}</span>
          </div>
        </div>
      </div>
    </section>

{legacy_join_section()}

    <section class="flex one" id="audiences">
      <div class="content">
        <div class="product-comparison">
          <div class="product-card">
            <h3>{t('Für Privatpersonen')}</h3>
            <p class="product-desc">{t('Eine freundliche Chat-Oberfläche fürs Schreiben, Recherchieren und den Alltag, ganz ohne technisches Wissen.')}</p>
            <div class="audience-actions">
              <a class="button button--dark" href="https://chat.publicai.co/" target="_blank" rel="noopener noreferrer">{t('Chat öffnen')}</a>
            </div>
          </div>
          <div class="product-card">
            <h3>{t('Für Unternehmen und Entwickler:innen')}</h3>
            <p class="product-desc">{t('Eine vollständige API für Textgenerierung, Embeddings und Retrieval.')}</p>
            <div class="audience-actions">
              <a class="button button--dark" href="https://platform.publicai.co/docs" target="_blank" rel="noopener noreferrer">{t('Zur Dokumentation')}</a>
            </div>
          </div>
        </div>
      </div>
    </section>

{timeline_section()}

{legacy_compare_section()}

{dialogue_section(prefix)}

{legacy_faq_section()}"""


def intro_page(title: str, subtitle: str, sections: str) -> str:
    return f"""    <section class="flex one intro-section">
      <div class="content">
        <h2>{esc(title)}</h2>
        <p class="larger">{esc(subtitle)}</p>
      </div>
    </section>
{sections}"""


STATUTEN_BODY = (Path(__file__).resolve().parent / "statuten_body.html").read_text(
    encoding="utf-8"
)


def statuten_section() -> str:
    note = ""
    if CURRENT_LOCALE != "de":
        note = f"""    <section class="flex one intro-section">
      <div class="content">
        <p class="statutes-doc__locale-note">{esc(t('Der massgebliche Wortlaut der Statuten ist Deutsch.'))}</p>
      </div>
    </section>
"""
    return note + STATUTEN_BODY


def legal_blocks(blocks: list[tuple[str, str]]) -> str:
    parts = []
    for heading, body in blocks:
        parts.append(f"""    <section class="flex one intro-section">
      <div class="content">
        <h3>{esc(heading)}</h3>
        <p>{body}</p>
      </div>
    </section>""")
    return "\n".join(parts)


def redirect_page(target: str, title: str, label: str, locale: str = "en") -> str:
    lang = LANG_ATTR[locale]
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="refresh" content="0; url={target}">
  <link rel="canonical" href="{target}">
  <title>{esc(title)}</title>
</head>
<body>
  <p><a href="{target}">{esc(label)}</a></p>
</body>
</html>"""


def build_pages(prefix: str = "") -> dict[str, str]:
    pages: dict[str, str] = {}
    p = f"/{prefix}/" if prefix else "/"
    rel = f"{prefix}/" if prefix else ""
    hero_backgrounds = load_community_photos()

    pages["index.html"] = page_shell(
        "Public AI Switzerland",
        t("Public AI Switzerland ist eine Genossenschaft, die Schweizer KI zugänglich macht und in die Hände ihrer Genossenschafter:innen legt."),
        "index.html",
        index_body(prefix),
        overlay=True,
        prefix=prefix,
    )

    pages["mission.html"] = redirect_page(
        f"{rel}about.html",
        "Redirecting to About, Public AI Switzerland",
        "Mission",
        CURRENT_LOCALE,
    )

    pages["join.html"] = page_shell(
        "Public AI Switzerland, Become a member",
        "Buy a cooperative share at Public AI Switzerland.",
        "join.html",
        render_join(t),
        prefix=prefix,
        subpage_title=t(load_join()["hero_title"]),
        hero_image=hero_backgrounds.get("join.html"),
    )

    pages["usage.html"] = redirect_page(
        "https://platform.publicai.co/docs",
        "Redirecting to API docs, Public AI Switzerland",
        t("API docs"),
        CURRENT_LOCALE,
    )

    pages["apertus.html"] = redirect_page(
        "https://www.apertus-ai.org/",
        "Redirecting to Apertus",
        "Apertus",
        CURRENT_LOCALE,
    )

    pages["team.html"] = redirect_page(
        f"{rel}about.html#team",
        "Redirecting to About, Public AI Switzerland",
        t("Gründungsteam"),
        CURRENT_LOCALE,
    )

    pages["community.html"] = redirect_page(
        f"{rel}about.html",
        "Redirecting to About, Public AI Switzerland",
        t("Community"),
        CURRENT_LOCALE,
    )

    news_data = load_news()
    pages["news.html"] = page_shell(
        "Public AI Switzerland, News",
        "News from the cooperative.",
        "news.html",
        render_news(t, CURRENT_LOCALE),
        prefix=prefix,
        subpage_title=t(news_data["hero_title"]),
        hero_image=hero_backgrounds.get("news.html"),
    )

    contact_data = load_contact()
    pages["contact.html"] = page_shell(
        "Public AI Switzerland, Contact",
        "Get in touch with Public AI Switzerland.",
        "contact.html",
        render_contact(t),
        prefix=prefix,
        subpage_title=t(contact_data["hero_title"]),
        hero_image=hero_backgrounds.get("contact.html"),
    )

    terms_data = load_terms()
    pages["terms.html"] = page_shell(
        "Public AI Switzerland, Terms and conditions",
        "Terms and conditions for Public AI Switzerland.",
        "terms.html",
        render_terms(t),
        prefix=prefix,
        subpage_title=t(terms_data["hero_title"]),
    )

    privacy_data = load_privacy()
    pages["privacy.html"] = page_shell(
        "Public AI Switzerland, Privacy policy",
        "Privacy policy for Public AI Switzerland.",
        "privacy.html",
        render_privacy(t),
        prefix=prefix,
        subpage_title=t(privacy_data["hero_title"]),
    )

    pages["statuten.html"] = page_shell(
        "Public AI Switzerland, Statutes",
        "Statutes of Public AI Switzerland.",
        "statuten.html",
        statuten_section(),
        prefix=prefix,
        subpage_title=t("Statuten"),
    )

    fonds_data = load_fonds()
    pages["fonds.html"] = page_shell(
        "Public AI Switzerland, Research and development fund",
        "Research and development fund of Public AI Switzerland.",
        "fonds.html",
        render_fonds(t),
        prefix=prefix,
        subpage_title=t(fonds_data["hero_title"]),
    )

    impressum_data = load_impressum()
    pages["impressum.html"] = page_shell(
        "Public AI Switzerland, Legal notice",
        "Legal notice for Public AI Switzerland.",
        "impressum.html",
        render_impressum(t),
        prefix=prefix,
        subpage_title=t(impressum_data["hero_title"]),
    )

    about_data = load_about()
    pages["about.html"] = page_shell(
        "About, Public AI Switzerland",
        "About Public AI Switzerland.",
        "about.html",
        render_about(t, prefix, asset_prefix),
        prefix=prefix,
        subpage_title=t(about_data["hero_title"]),
        hero_image="assets/IMG_2517.jpg",
    )

    return pages


REMOVED_PAGES = ("worldwide.html",)


def main() -> None:
    for locale in LOCALES:
        set_locale(locale)
        prefix = "" if locale == "en" else locale
        pages = build_pages(prefix)
        out_dir = ROOT if locale == "en" else ROOT / locale
        out_dir.mkdir(parents=True, exist_ok=True)
        for name, content in pages.items():
            path = out_dir / name
            path.write_text(content, encoding="utf-8")
            print(f"Wrote {path}")
        for name in REMOVED_PAGES:
            path = out_dir / name
            if path.exists():
                path.unlink()
                print(f"Removed {path}")


if __name__ == "__main__":
    main()
