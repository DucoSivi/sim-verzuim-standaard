"""Haal alle gepubliceerde bestanden van de Verzuimstandaard op van sivi.org.

Leest per koppelvlak de downloadpagina, verzamelt per jaar de links naar
pdf, xsd, xls en zip, en downloadt ze naar een lokale cachemap.

Een bestand hoort bij het jaar dat in zijn eigen adres staat, niet bij het
kopje waaronder het op de pagina staat. Op sivi.org staan meerdere links
onder het verkeerde jaar; die worden zo vanzelf goed ingedeeld en in het
manifest als afwijking vastgelegd.

Gebruik:
    python haal_sivi_bestanden.py <cachemap>
"""
import concurrent.futures
import hashlib
import json
import re
import sys
import time
from pathlib import Path
from urllib.parse import unquote

import bs4
import requests

BASIS = "https://www.sivi.org"
KOPPELVLAKKEN = [
    "werkgevers-arbodiensten",
    "werkgevers-verzekeraars",
    "arbodiensten-verzekeraars",
]
SOORT = re.compile(r"\((pdf|xsd|xls|xlsx|zip)[^)]*\)", re.I)
JAAR_IN_ADRES = re.compile(r"(?<!\d)(20[12]\d)(?!\d)")


def pagina_adres(koppelvlak):
    return f"{BASIS}/verzuim/verzuimstandaard-{koppelvlak}/downloads-verzuimstandaard-{koppelvlak}/"


def lees_links(html):
    """Geef [(kopjesjaar, publicatietekst, linktekst, href)] in paginavolgorde."""
    soup = bs4.BeautifulSoup(html, "lxml")
    hoofd = soup.find("main") or soup
    jaar, publicatie, links = None, "", []
    for el in hoofd.find_all(["h2", "h3", "h4", "h5", "a"]):
        tekst = el.get_text(" ", strip=True)
        if el.name in ("h2", "h3", "h4"):
            m = re.search(r"(Documentatie|XML[- ]schema).*?(20\d\d)", tekst)
            if m:
                jaar = m.group(2)
        elif el.name == "h5":
            if tekst:
                publicatie = tekst
        elif el.name == "a" and jaar:
            href = el.get("href", "")
            if (href.startswith("/") or "sivi.org" in href) and SOORT.search(tekst):
                links.append((jaar, publicatie, tekst, href))
    return links


def bestandsnaam(antwoord, href):
    cd = antwoord.headers.get("content-disposition", "")
    m = re.search(r"filename\*=UTF-8''([^;]+)", cd) or re.search(r'filename="?([^";]+)"?', cd)
    if m:
        return unquote(m.group(1)).strip()
    return href.strip("/").split("/")[-1]


def download(sessie, href, doelmap):
    adres = href if href.startswith("http") else BASIS + href
    for poging in range(4):
        try:
            r = sessie.get(adres, timeout=120)
            r.raise_for_status()
            break
        except requests.RequestException:
            if poging == 3:
                raise
            time.sleep(2 * (poging + 1))
    naam = bestandsnaam(r, href)
    doelmap.mkdir(parents=True, exist_ok=True)
    pad = doelmap / naam
    pad.write_bytes(r.content)
    return naam, len(r.content), hashlib.sha256(r.content).hexdigest(), r.headers.get("content-type", "")


def main(cachemap):
    cache = Path(cachemap)
    sessie = requests.Session()
    sessie.headers["User-Agent"] = "SIVI-verzuim-migratie/1.0"
    manifest = []
    for kv in KOPPELVLAKKEN:
        html = sessie.get(pagina_adres(kv), timeout=60).text
        gezien = set()
        for kopjesjaar, publicatie, tekst, href in lees_links(html):
            jaren = JAAR_IN_ADRES.findall(href)
            jaar = jaren[0] if jaren else kopjesjaar
            if (kv, jaar, href) in gezien:
                continue
            gezien.add((kv, jaar, href))
            manifest.append({
                "koppelvlak": kv,
                "jaar": jaar,
                "kopjesjaar": kopjesjaar,
                "publicatie": publicatie if jaar == kopjesjaar else "",
                "titel": tekst,
                "href": href,
                "afwijking": jaar != kopjesjaar,
            })

    def haal(regel):
        doel = cache / regel["koppelvlak"] / regel["jaar"]
        naam, grootte, sha, soort = download(sessie, regel["href"], doel)
        regel.update(bestand=naam, grootte=grootte, sha256=sha, content_type=soort)
        return regel

    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        resultaat = list(pool.map(haal, manifest))

    (cache / "manifest.json").write_text(json.dumps(resultaat, ensure_ascii=False, indent=1), encoding="utf-8")
    afwijkingen = [r for r in resultaat if r["afwijking"]]
    print(f"{len(resultaat)} bestanden opgehaald, {len(afwijkingen)} stonden onder een ander jaar")
    for r in afwijkingen:
        print(f"  {r['koppelvlak']}: '{r['titel']}' staat onder {r['kopjesjaar']}, adres zegt {r['jaar']}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "cache")
