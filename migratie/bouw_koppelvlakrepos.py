"""Bouw per koppelvlak een Git-repository met alle releases van de Verzuimstandaard.

Elk publicatiejaar wordt één versie in de geschiedenis, met als label het
jaartal. Daardoor kan iedereen twee willekeurige releases met elkaar
vergelijken. Per versie staan in Git:

    xsd/<Bericht>.xsd       het schema, zonder jaartal in de naam
    berichten/<Bericht>.md  de berichtstructuur, afgeleid van de XSD

De officiële bestanden (PDF, XLS, XSD, ZIP) gaan niet in Git maar worden
klaargezet als bijlagen bij de GitHub-release van dat jaar. maak_releases.py
zet ze daarna online.

Gebruik:
    python bouw_koppelvlakrepos.py <cachemap> <werkmap> [eigenaar]
"""
import collections
import datetime
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

from xsd_naar_markdown import markdown

KOPPELVLAKKEN = {
    "werkgevers-arbodiensten": "Werkgevers ↔ Arbodiensten",
    "werkgevers-verzekeraars": "Werkgevers ↔ Verzekeraars",
    "arbodiensten-verzekeraars": "Arbodiensten ↔ Verzekeraars",
}
CENTRAAL = "sim-verzuim-standaard"
AANTAL_ACTUEEL = 3
MAANDEN = {m: i + 1 for i, m in enumerate(
    "januari februari maart april mei juni juli augustus september oktober november december".split())}
EXTENSIE = {"application/pdf": ".pdf", "application/zip": ".zip"}


def repo_naam(kv):
    return f"sim-verzuim-{kv}"


def publicatiedatum(teksten, jaar):
    """'Publicatie juli 2020 (update november)' -> de laatst genoemde maand van dat jaar."""
    maanden = [MAANDEN[w] for t in teksten for w in re.findall(r"[a-z]+", t.lower()) if w in MAANDEN]
    return datetime.datetime(int(jaar), max(maanden, default=7), 1, 12, 0, 0)


def basisnaam(xsdnaam):
    """Dienstverbanden2026.xsd -> Dienstverbanden"""
    return re.sub(r"20[12]\d$", "", Path(xsdnaam).stem)


def leesbare_naam(titel):
    return re.sub(r"\s*\((xsd|pdf)\)\s*$", "", titel, flags=re.I).strip()


def git(map_, *args, datum=None):
    omgeving = dict(os.environ)
    if datum:
        stempel = datum.strftime("%Y-%m-%dT%H:%M:%S+02:00")
        omgeving.update(GIT_AUTHOR_DATE=stempel, GIT_COMMITTER_DATE=stempel)
    return subprocess.run(["git", "-C", str(map_), *args], check=True, capture_output=True,
                          text=True, encoding="utf-8", env=omgeving).stdout


def verzamel_jaar(cache, regels):
    """Lees alle bestanden van één koppelvlak-jaar.

    Geeft (xsds, bijlagen): xsds is {bestandsnaam: bytes}, bijlagen is een lijst
    (naam_voor_release, bron_bytes, titel).
    """
    xsds, bijlagen, gezien = {}, [], set()
    for r in regels:
        if r["sha256"] in gezien:
            continue
        gezien.add(r["sha256"])
        pad = cache / r["koppelvlak"] / r["jaar"] / r["bestand"]
        inhoud = pad.read_bytes()
        soort = r["content_type"].split(";")[0]
        if soort == "application/zip":
            with zipfile.ZipFile(pad) as z:
                namen = [n for n in z.namelist() if not n.endswith("/")]
                for n in namen:
                    if n.lower().endswith(".xsd"):
                        xsds.setdefault(Path(n).name, z.read(n))
                if len(namen) == 1 and namen[0].lower().endswith(".xsd"):
                    # Losse XSD die sivi.org als zip aanbiedt: als .xsd bijvoegen.
                    bijlagen.append((Path(namen[0]).name, z.read(namen[0]), r["titel"]))
                    continue
        ext = EXTENSIE.get(soort, ".xlsx" if "spreadsheet" in soort else "")
        bijlagen.append((r["bestand"] + ext, inhoud, r["titel"]))
    return xsds, bijlagen


def zoek_funhie(cache, kv, jaar, basis, regels):
    sleutel = f"{basis.lower()}{jaar}_funhie"
    for r in regels:
        b = r["bestand"].lower()
        if b.endswith(sleutel) or re.search(rf"\d\d-{re.escape(sleutel)}$", b):
            return cache / kv / jaar / r["bestand"]
    return None


def schrijf_lf(pad, inhoud):
    """Schrijf met LF-regeleinden, zodat een vergelijking niet op regeleinden struikelt."""
    pad.write_bytes(inhoud.replace(b"\r\n", b"\n").replace(b"\r", b"\n"))


def bouw(cachemap, werkmap, eigenaar):
    cache, werk = Path(cachemap), Path(werkmap)
    manifest = json.loads((cache / "manifest.json").read_text(encoding="utf-8"))
    per_jaar = collections.defaultdict(list)
    for r in manifest:
        per_jaar[(r["koppelvlak"], r["jaar"])].append(r)

    for kv, titel in KOPPELVLAKKEN.items():
        naam = repo_naam(kv)
        repo = werk / "kv" / naam
        releasemap = werk / "releases" / naam
        for m in (repo, releasemap):
            if m.exists():
                shutil.rmtree(m)
            m.mkdir(parents=True)
        git(repo, "init", "-q", "-b", "main")
        git(repo, "config", "core.autocrlf", "false")
        (repo / ".gitattributes").write_text("* text=auto eol=lf\n*.xsd text eol=lf\n", encoding="utf-8")

        jaren = sorted(j for (k, j) in per_jaar if k == kv)
        # Berichtnamen zoals sivi.org ze noemt, van de nieuwste publicatie.
        berichtnamen = {}
        for jaar in jaren:
            for r in per_jaar[(kv, jaar)]:
                m = re.search(r"/([a-z0-9-]+?)(20[12]\d)(-2)?/?$", r["href"])
                if "(xsd)" in r["titel"].lower() and m:
                    berichtnamen[m.group(1)] = leesbare_naam(r["titel"])

        releases, vorige = [], None
        for jaar in jaren:
            regels = per_jaar[(kv, jaar)]
            xsds, bijlagen = verzamel_jaar(cache, regels)
            datum = publicatiedatum([r["publicatie"] for r in regels if r["publicatie"]], jaar)

            for oud in list((repo / "xsd").glob("*.xsd")) + list((repo / "berichten").glob("*.md")):
                oud.unlink()
            (repo / "xsd").mkdir(exist_ok=True)
            (repo / "berichten").mkdir(exist_ok=True)

            berichten = []
            for xsdnaam, inhoud in sorted(xsds.items()):
                basis = basisnaam(xsdnaam)
                doel = repo / "xsd" / f"{basis}.xsd"
                schrijf_lf(doel, inhoud)
                weergave = berichtnamen.get(basis.lower(), basis)
                funhie = zoek_funhie(cache, kv, jaar, basis, regels)
                md, aantal = markdown(doel, weergave, titel, jaar, funhie)
                (repo / "berichten" / f"{basis}.md").write_text(md, encoding="utf-8")
                berichten.append((basis, weergave, aantal, funhie is not None))

            overzicht = [f"# Berichten {titel} {jaar}", "",
                         "| Bericht | Schema | Elementen |", "|---|---|---|"]
            for basis, weergave, aantal, _ in berichten:
                overzicht.append(f"| [{weergave}]({basis}.md) | [`{basis}.xsd`](../xsd/{basis}.xsd) | {aantal} |")
            (repo / "berichten" / "README.md").write_text("\n".join(overzicht) + "\n", encoding="utf-8")

            git(repo, "add", "-A")
            git(repo, "commit", "-q", "-m", f"Release {jaar}: Verzuimstandaard {titel}",
                "-m", f"Gepubliceerd op sivi.org ({', '.join(sorted(set(r['publicatie'] for r in regels if r['publicatie'])))}).",
                datum=datum)
            git(repo, "tag", "-a", jaar, "-m", f"Verzuimstandaard {titel} {jaar}", datum=datum)

            map_jaar = releasemap / jaar
            map_jaar.mkdir(parents=True)
            namen_gebruikt = set()
            bijlage_lijst = []
            for bnaam, inhoud, btitel in bijlagen:
                if bnaam in namen_gebruikt:
                    continue
                namen_gebruikt.add(bnaam)
                (map_jaar / bnaam).write_bytes(inhoud)
                bijlage_lijst.append({"bestand": bnaam, "titel": btitel})

            nu = {b[0] for b in berichten}
            releases.append({
                "jaar": jaar,
                "datum": datum.date().isoformat(),
                "publicatie": sorted(set(r["publicatie"] for r in regels if r["publicatie"])),
                "vorige": vorige["jaar"] if vorige else None,
                "nieuw": sorted(nu - vorige["berichten"]) if vorige else [],
                "vervallen": sorted(vorige["berichten"] - nu) if vorige else [],
                "berichten": [{"basis": b[0], "naam": b[1], "elementen": b[2]} for b in berichten],
                "bijlagen": bijlage_lijst,
                "afwijkingen": [
                    {"titel": r["titel"], "kopjesjaar": r["kopjesjaar"], "jaar": r["jaar"]}
                    for r in manifest
                    if r["koppelvlak"] == kv and r["afwijking"] and jaar in (r["jaar"], r["kopjesjaar"])
                ],
            })
            vorige = {"jaar": jaar, "berichten": nu}

        actueel = {r["jaar"] for r in releases[-AANTAL_ACTUEEL:]}
        for r in releases:
            r["status"] = "actueel" if r["jaar"] in actueel else "archief"
            r["nieuwste"] = r is releases[-1]
        (releasemap / "releases.json").write_text(json.dumps(
            {"koppelvlak": kv, "titel": titel, "repo": f"{eigenaar}/{naam}", "releases": releases},
            ensure_ascii=False, indent=1), encoding="utf-8")

        (repo / "README.md").write_text(readme(kv, titel, eigenaar, releases), encoding="utf-8")
        git(repo, "add", "-A")
        git(repo, "commit", "-q", "-m", "Inrichting repository: README met releases en verwijzing naar de centrale ingang",
            datum=datetime.datetime.now())
        print(f"{naam}: {len(releases)} releases ({', '.join(r['jaar'] for r in releases)})")


def readme(kv, titel, eigenaar, releases):
    naam = repo_naam(kv)
    basis = f"https://github.com/{eigenaar}/{naam}"
    centraal = f"https://github.com/{eigenaar}/{CENTRAAL}"
    portaal = f"https://{eigenaar.lower()}.github.io/{CENTRAAL}/{kv}/"
    nieuwste = releases[-1]["jaar"]
    oudste = releases[0]["jaar"]
    regels = [
        f"# Verzuimstandaard {titel}",
        "",
        "> **Simulatie.** Zo zou dit koppelvlak er op GitHub uitzien in de voorgestelde inrichting:"
        f" één centrale ingang ([{CENTRAAL}]({centraal})) en per koppelvlak een eigen repository met de releases."
        " De bestanden zijn de officiële publicaties van sivi.org, op 5 oktober 2026 geïmporteerd.",
        "",
        f"Deze repository bevat alle releases van de Verzuimstandaard {titel}."
        f" Vragen, wijzigingsverzoeken en discussies lopen via de [centrale ingang]({centraal}).",
        "",
        "## Releases",
        "",
        f"De {AANTAL_ACTUEEL} meest recente releases zijn actueel. Oudere releases blijven beschikbaar.",
        "",
        "| Release | Status | Berichten | Wat is er veranderd? |",
        "|---|---|---|---|",
    ]
    for r in reversed(releases):
        vergelijk = (f"[{r['vorige']} → {r['jaar']}]({basis}/compare/{r['vorige']}...{r['jaar']})"
                     if r["vorige"] else "eerste release in deze repository")
        status = f"**{r['status']}**" if r["status"] == "actueel" else r["status"]
        regels.append(f"| [{r['jaar']}]({basis}/releases/tag/{r['jaar']}) | {status} | {len(r['berichten'])} | {vergelijk} |")
    regels += [
        "",
        "Bij elke release horen de officiële bestanden: de toelichting en de functionele beschrijvingen (PDF),"
        " de XML-schema's (XSD), waar van toepassing de verzuimcontrolecodes (XLS) en de zips.",
        "",
        "## Twee releases vergelijken",
        "",
        "Elke release heeft het jaartal als label. Daarmee kun je elke twee releases naast elkaar leggen, per bericht en per element:",
        "",
        f"- vorige naar huidige: [{releases[-2]['jaar']} → {nieuwste}]({basis}/compare/{releases[-2]['jaar']}...{nieuwste})",
        f"- alles sinds de oudste release: [{oudste} → {nieuwste}]({basis}/compare/{oudste}...{nieuwste})",
        f"- zelf kiezen: `{basis}/compare/<oud>...<nieuw>`",
        "",
        "## Wat staat waar",
        "",
        "| Map | Inhoud |",
        "|---|---|",
        "| [`xsd/`](xsd) | De XML-schema's van de nieuwste release, één bestand per bericht, zonder jaartal in de naam |",
        "| [`berichten/`](berichten) | Per bericht de berichtstructuur in Markdown, afgeleid van de XSD |",
        f"| [Releases]({basis}/releases) | De officiële PDF-, XLS-, XSD- en ZIP-bestanden per jaar |",
        "",
        f"De documentatie om te lezen staat op het [portaal]({portaal}).",
        "",
        "## Vragen of een wijziging voorstellen",
        "",
        f"- [Stel een vraag]({centraal}/issues/new?template=vraag.yml)",
        f"- [Dien een wijzigingsverzoek in]({centraal}/issues/new?template=wijzigingsverzoek.yml)",
        f"- [Discussies]({centraal}/discussions)",
        "",
    ]
    afwijkingen = [a for r in releases for a in r["afwijkingen"]]
    if afwijkingen:
        regels += [
            "## Bevindingen bij de import",
            "",
            "Op de downloadpagina van sivi.org stonden deze bestanden onder het verkeerde jaar."
            " De import heeft ze bij het jaar uit hun eigen adres ingedeeld:",
            "",
        ]
        for a in {(a["titel"], a["kopjesjaar"], a["jaar"]): a for a in afwijkingen}.values():
            regels.append(f"- '{a['titel']}' stond onder {a['kopjesjaar']}, hoort bij {a['jaar']}")
        regels.append("")
    return "\n".join(regels)


if __name__ == "__main__":
    bouw(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "DucoSivi")
