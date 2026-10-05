"""Bouw de pagina's van het Verzuim-portaal uit de drie koppelvlakrepositories.

De koppelvlakrepositories zijn de bron. Dit script haalt per koppelvlak de
berichtbeschrijvingen van de nieuwste release op, maakt een overzicht van
alle releases (met downloadtellingen als er een GitHub-token is) en schrijft
mkdocs.gen.yml met de navigatie. Daarna bouwt mkdocs de site.

Gebruik:
    python bouw_portaal.py <map met gekloonde koppelvlakrepos> <portaalmap>
"""
import json
import os
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

KOPPELVLAKKEN = {
    "werkgevers-arbodiensten": "Werkgevers ↔ Arbodiensten",
    "werkgevers-verzekeraars": "Werkgevers ↔ Verzekeraars",
    "arbodiensten-verzekeraars": "Arbodiensten ↔ Verzekeraars",
}
CENTRAAL = "sim-verzuim-standaard"
AANTAL_ACTUEEL = 3


def git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True,
                          text=True, encoding="utf-8").stdout


def releases_via_api(repo):
    """Haal releases en downloadtellingen op. Zonder token: geen tellingen."""
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        return {}
    verzoek = urllib.request.Request(
        f"https://api.github.com/repos/{repo}/releases?per_page=100",
        headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"})
    try:
        with urllib.request.urlopen(verzoek, timeout=30) as antwoord:
            return {r["tag_name"]: r for r in json.load(antwoord)}
    except OSError as fout:
        print(f"Let op: downloadtellingen voor {repo} niet opgehaald ({fout})")
        return {}


def koppelvlak_paginas(kv, titel, repo_map, docs, eigenaar):
    naam = f"sim-verzuim-{kv}"
    repo = f"{eigenaar}/{naam}"
    basis = f"https://github.com/{repo}"
    centraal = f"https://github.com/{eigenaar}/{CENTRAAL}"
    jaren = [t for t in git(repo_map, "tag", "--sort=version:refname").split() if re.fullmatch(r"20\d\d", t)]
    nieuwste = jaren[-1]
    uit = docs / kv
    (uit / "berichten").mkdir(parents=True, exist_ok=True)

    # Berichtpagina's van de nieuwste release, met schema-links naar GitHub.
    berichten = []
    for pad in git(repo_map, "ls-tree", "--name-only", nieuwste, "berichten/").split():
        tekst = git(repo_map, "show", f"{nieuwste}:{pad}")
        tekst = re.sub(r"\(\.\./xsd/([^)]+)\)", rf"({basis}/blob/{nieuwste}/xsd/\1)", tekst)
        bestand = Path(pad).name
        if bestand == "README.md":
            bestand = "index.md"
        else:
            kop = re.search(r"^# (.+)$", tekst, re.M)
            berichten.append((bestand, kop.group(1) if kop else bestand[:-3]))
        (uit / "berichten" / bestand).write_text(tekst, encoding="utf-8")

    api = releases_via_api(repo)
    actueel = set(jaren[-AANTAL_ACTUEEL:])
    regels = [
        f"# {titel}",
        "",
        f"De Verzuimstandaard {titel}: berichten, releases en downloads.",
        f"De bron staat in de repository [{naam}]({basis}).",
        "",
        "## Releases",
        "",
        f"De {AANTAL_ACTUEEL} meest recente releases zijn actueel. Oudere releases blijven beschikbaar.",
        "",
        "| Release | Status | Wat is er veranderd? | Downloads |",
        "|---|---|---|---|",
    ]
    for i, jaar in reversed(list(enumerate(jaren))):
        status = "**actueel**" if jaar in actueel else "archief"
        vergelijk = (f"[{jaren[i - 1]} → {jaar}]({basis}/compare/{jaren[i - 1]}...{jaar})" if i else "eerste release")
        downloads = "–"
        if jaar in api:
            downloads = str(sum(a["download_count"] for a in api[jaar]["assets"]))
        regels.append(f"| [{jaar}]({basis}/releases/tag/{jaar}) | {status} | {vergelijk} | {downloads} |")
    regels += [
        "",
        f"Alles sinds {jaren[0]} in één overzicht: [{jaren[0]} → {nieuwste}]({basis}/compare/{jaren[0]}...{nieuwste}).",
        "",
    ]
    if nieuwste in api:
        regels += [f'??? note "Downloads per bestand, release {nieuwste}"', "",
                   "    | Bestand | Downloads |", "    |---|---|"]
        for a in sorted(api[nieuwste]["assets"], key=lambda a: -a["download_count"]):
            regels.append(f"    | [{a['name']}]({a['browser_download_url']}) | {a['download_count']} |")
        regels.append("")
    regels += [
        f"## Berichten in release {nieuwste}",
        "",
        "| Bericht | |",
        "|---|---|",
    ]
    for bestand, kop in berichten:
        regels.append(f"| [{kop}](berichten/{bestand}) | [schema]({basis}/blob/{nieuwste}/xsd/{bestand[:-3]}.xsd) |")
    regels += [
        "",
        "## Vragen en wijzigingen",
        "",
        f"- [Stel een vraag over {titel}]({centraal}/issues/new?template=vraag.yml)",
        f"- [Dien een wijzigingsverzoek in]({centraal}/issues/new?template=wijzigingsverzoek.yml)",
        f"- [Lopende vragen en verzoeken voor dit koppelvlak]({centraal}/issues?q=is%3Aissue+label%3A%22{titel.replace(' ', '+').replace('↔', '%E2%86%94')}%22)",
        "",
    ]
    (uit / "index.md").write_text("\n".join(regels), encoding="utf-8")
    return [{titel: [{"Overzicht en releases": f"{kv}/index.md"},
                     {"Berichten": [{"Alle berichten": f"{kv}/berichten/index.md"}] +
                      [{kop: f"{kv}/berichten/{bestand}"} for bestand, kop in berichten]}]}]


def main(kv_map, portaal):
    kv_map, portaal = Path(kv_map), Path(portaal)
    eigenaar = os.environ.get("EIGENAAR", "DucoSivi")
    docs = portaal / "docs"
    nav = [{"Ingang": "index.md"}, {"Werkwijze": "werkwijze.md"}]
    for kv, titel in KOPPELVLAKKEN.items():
        nav += koppelvlak_paginas(kv, titel, kv_map / f"sim-verzuim-{kv}", docs, eigenaar)

    def yaml_nav(items, inspring=0):
        regels = []
        for item in items:
            for sleutel, waarde in item.items():
                if isinstance(waarde, list):
                    regels.append(" " * inspring + f'- "{sleutel}":')
                    regels += yaml_nav(waarde, inspring + 4)
                else:
                    regels.append(" " * inspring + f'- "{sleutel}": {waarde}')
        return regels

    (portaal / "mkdocs.gen.yml").write_text(
        "INHERIT: mkdocs.yml\nnav:\n" + "\n".join(yaml_nav(nav, 2)) + "\n", encoding="utf-8")
    print("Portaalpagina's gemaakt voor", ", ".join(KOPPELVLAKKEN))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
