#!/usr/bin/env python3
"""Sync i18n locale files to the canonical key set and bootstrap Romansh."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LOCALES = ("de", "fr", "it", "rm")

# Rumantsch Grischun overlays for high-visibility UI copy.
RM_OVERLAYS: dict[str, str] = {
    "Über uns": "Davart nus",
    "News": "Novitads",
    "Mitmachen": "Participar",
    "Kontakt": "Contact",
    "Mitglieder-Login": "Login dals commembers",
    "Become a member": "Daventar commember",
    "Team": "Team",
    "Zitatwand": "Muret da citaziuns",
    "Wer wir sind": "Tge che nus essan",
    "Verwaltung": "Administraziun",
    "Die Verwaltung wird von den Genossenschafter:innen gewählt.": "L'administraziun vegn elegida dals commembers da la cooperativa.",
    "Gründungsteam": "Equipa fundativa",
    "Statuten": "Statuts",
    "Terms & Conditions": "Cundiziuns generalas",
    "Privacy Notice": "Decleraziun da protecziun da datas",
    "Legal notice": "Impressum",
    "Research & development fund": "Fonds da retschertga e svilup",
    "Chat": "Chat",
    "API docs": "Documentaziun API",
    "Hugging Face": "Hugging Face",
    "Source of this website": "Codest source da questa pagina",
    "Toggle navigation menu": "Alternar il menu da navigaziun",
    "Close menu": "Serrar il menu",
    "Join the dialogue": "Participar al dialog",
    "In Zusammenarbeit mit:": "En collavuraziun cun:",
    "Partner des Schweizer Nationalen KI-Dialogs": "Partenaris dal dialog naziunal svizzer da l'IA",
    "Im Schweizer Nationalen KI-Dialog mitreden": "Sa far tgirar en il dialog naziunal svizzer da l'IA",
    "Public AI Switzerland veranstaltet einen nationalen Dialog zur KI-Politik und -Infrastruktur der Schweiz. Mach mit und hilf mitzugestalten, wie KI der Öffentlichkeit dient.": "Public AI Switzerland organisa in dialog naziunal davart la politica e l'infrastructura d'IA da la Svizra. Participescha e gidai a definir co l'IA serva al public.",
    "Öffentliche KI für die Schweiz — genossenschaftlich, auf Schweizer Infrastruktur.": "IA publica per la Svizra — cooperativa, sin infrastructura svizra.",
    "Public AI Switzerland ist eine kundeneigene Genossenschaft. Wir helfen Menschen in der Schweiz, Schweizer KI zu nutzen, zu besitzen und mitzugestalten.": "Public AI Switzerland è ina cooperativa da commembers. Nus gidain persunas en Svizra ad acceder, posseder e co-definir l'IA svizra.",
    "Unsere Mission: öffentliche KI in der Schweiz aufbauen und unterstützen.": "Nossa missiun: construir e sustegnir l'IA publica en Svizra.",
    "Public AI Switzerland ist das Schweizer Kapitel der grösseren Bewegung für öffentliche KI (auch «Public AI», grossgeschrieben). Wie viele in dieser Bewegung sind wir überzeugt, dass KI eine Form öffentlicher Infrastruktur sein sollte — wie Parks, Züge oder Strom.": "Public AI Switzerland è il chapital svizzer dal pli grond moviment per l'IA publica (er «Public AI», cun maiuscla). sco blers en quest moviment essan nus convints che l'IA duess esser ina furma d'infrastructura publica sco parcs, trens u electricitad.",
    "Wenn du neugierig bist, wirf einen Blick auf unsere Schwesterprojekte — darunter die <a href=\"https://publicai.co\" target=\"_blank\" rel=\"noopener noreferrer\">Public AI Inference Utilty</a>, ein gemeinnütziges Open-Source-Projekt, das die technische Infrastruktur baut, und das <a href=\"https://publicai.network\" target=\"_blank\" rel=\"noopener noreferrer\">Public AI Network</a>, ein Treffpunkt für die Bewegung.": "Sche ti es incuriös, guarda noss projects siro — tranter auters la <a href=\"https://publicai.co\" target=\"_blank\" rel=\"noopener noreferrer\">Public AI Inference Utilty</a>, in project open source senza finamira da lucrativ che construescha l'infrastructura tecnica, e il <a href=\"https://publicai.network\" target=\"_blank\" rel=\"noopener noreferrer\">Public AI Network</a>, in lieu da reunir per il moviment.",
    "Public AI Switzerland ist eine Genossenschaft, die Schweizer KI zugänglich macht und in die Hände ihrer Genossenschafter:innen legt.": "Public AI Switzerland è ina cooperativa che renda l'IA svizra accessibla e la metta en manas da ses commembers.",
    "Die weltweit erste Genossenschaft für KI": "La emprima cooperativa dal mund per l'IA",
    "Genossenschaftsanteil zeichnen →": "Scriver in'acziun da cooperativa →",
    "Apertus kostenlos nutzen": "Utilisar Apertus gratuitamain",
    "(Neu) Dem Schweizer Nationalen KI-Dialog beitreten": "(Nov) Participar al dialog naziunal svizzer da l'IA",
    "Apertus-Deployer weltweit": "Deployer d'Apertus en il mund",
    "registrierte Nutzer:innen": "utilisaturs registrads",
    "Für Privatpersonen": "Per persunas privatas",
    "Für Unternehmen und Entwickler:innen": "Per interpresas e sviluppaders",
    "Chat öffnen": "Avrir il chat",
    "Zur Dokumentation": "A la documentaziun",
    "Der massgebliche Wortlaut der Statuten ist Deutsch.": "Il text legal decisiv dals statuts è tudestg.",
    "Copyright © Public AI Switzerland 2026. All rights reserved.": "Copyright © Public AI Switzerland 2026. Tut ils dretgs reservads.",
    "Photo: Joshua Tan (CC BY 4.0)": "Foto: Joshua Tan (CC BY 4.0)",
    "Über Public AI Switzerland": "Davart Public AI Switzerland",
}


def load_locale(locale: str) -> dict[str, str]:
    path = ROOT / f"i18n_{locale}.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def save_locale(locale: str, data: dict[str, str]) -> None:
    path = ROOT / f"i18n_{locale}.json"
    path.write_text(
        json.dumps(dict(sorted(data.items())), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    canonical = load_locale("en")
    de = load_locale("de")

    for locale in LOCALES:
        current = load_locale(locale)
        merged = dict(current)

        for key in canonical:
            if key not in merged:
                if locale == "de":
                    merged[key] = key
                elif locale == "rm":
                    merged[key] = RM_OVERLAYS.get(key, de.get(key, canonical[key]))
                else:
                    merged[key] = current.get(key, canonical[key])

        if locale == "rm":
            for key, value in RM_OVERLAYS.items():
                if key in canonical:
                    merged[key] = value

        save_locale(locale, merged)
        print(f"Synced i18n_{locale}.json ({len(merged)} keys)")


if __name__ == "__main__":
    main()
