"""Zet per koppelvlak de GitHub-releases online met de officiële bestanden als bijlage.

Leest releases.json die bouw_koppelvlakrepos.py per repository heeft gemaakt.
Kan veilig opnieuw draaien: een bestaande release wordt aangevuld met de
bijlagen die nog ontbreken.

Gebruik:
    python maak_releases.py <werkmap>
"""
import json
import subprocess
import sys
from pathlib import Path


def gh(*args, invoer=None):
    return subprocess.run(["gh", *args], check=True, capture_output=True, text=True,
                          encoding="utf-8", input=invoer).stdout


def toelichting(info, r):
    repo = info["repo"]
    basis = f"https://github.com/{repo}"
    publicatie = ", ".join(r["publicatie"]) or f"juli {r['jaar']}"
    status = ("**actueel**, een van de drie meest recente releases" if r["status"] == "actueel"
              else "archief, blijft beschikbaar")
    regels = [f"{publicatie} · {status}", "", "### Wat is er veranderd?", ""]
    if r["vorige"]:
        regels.append(f"- [Vergelijk {r['vorige']} → {r['jaar']}]({basis}/compare/{r['vorige']}...{r['jaar']}):"
                      " alle wijzigingen per bericht en per element")
    else:
        regels.append("- Eerste release in deze repository.")
    namen = {b["basis"]: b["naam"] for b in r["berichten"]}
    for b in r["nieuw"]:
        regels.append(f"- Nieuw bericht: {namen.get(b, b)}")
    for b in r["vervallen"]:
        regels.append(f"- Vervallen bericht: {b}")
    if any("release-note" in a["bestand"] for a in r["bijlagen"]):
        regels.append("- De release notes staan als PDF bij de bestanden hieronder.")
    regels += ["", "### Berichten", "", "| Bericht | Elementen |", "|---|---|"]
    for b in r["berichten"]:
        regels.append(f"| [{b['naam']}]({basis}/blob/{r['jaar']}/berichten/{b['basis']}.md) | {b['elementen']} |")
    regels += [
        "",
        "### Bestanden",
        "",
        "De officiële publicatie zoals op sivi.org: de toelichting en de functionele beschrijvingen per bericht (PDF),"
        " de XML-schema's (XSD), waar van toepassing de verzuimcontrolecodes (XLS) en de zips.",
    ]
    if any("revisie" in a["bestand"] for a in r["bijlagen"]):
        regels.append("De bestanden *met revisie* zijn de huidige revisiedocumenten."
                      " De vergelijking hierboven laat dezelfde wijzigingen zien, rechtstreeks uit de schema's.")
    if r["afwijkingen"]:
        regels += ["", "### Bij de import", ""]
        for a in r["afwijkingen"]:
            regels.append(f"- Op sivi.org stond '{a['titel']}' onder {a['kopjesjaar']}; het bestand hoort bij {a['jaar']}.")
    regels += ["", "---", "*Simulatie: geïmporteerd van sivi.org op 5 oktober 2026.*", ""]
    return "\n".join(regels)


def maak(werkmap):
    for releasefile in sorted(Path(werkmap, "releases").glob("*/releases.json")):
        info = json.loads(releasefile.read_text(encoding="utf-8"))
        repo = info["repo"]
        bestaand = {r["tagName"] for r in json.loads(
            gh("release", "list", "-R", repo, "--limit", "100", "--json", "tagName"))}
        for r in info["releases"]:
            map_jaar = releasefile.parent / r["jaar"]
            bestanden = [str(map_jaar / a["bestand"]) for a in r["bijlagen"]]
            titel = f"{r['jaar']} ({r['status']})"
            notities = map_jaar.parent / f"notities-{r['jaar']}.md"
            notities.write_text(toelichting(info, r), encoding="utf-8")
            if r["jaar"] not in bestaand:
                gh("release", "create", r["jaar"], "-R", repo, "--verify-tag", "--title", titel,
                   "--notes-file", str(notities), f"--latest={'true' if r['nieuwste'] else 'false'}", *bestanden)
                print(f"{repo} {r['jaar']}: aangemaakt met {len(bestanden)} bestanden", flush=True)
            else:
                online = {a["name"] for a in json.loads(
                    gh("release", "view", r["jaar"], "-R", repo, "--json", "assets"))["assets"]}
                ontbreekt = [b for b in bestanden if Path(b).name not in online]
                gh("release", "edit", r["jaar"], "-R", repo, "--title", titel, "--notes-file", str(notities))
                if ontbreekt:
                    gh("release", "upload", r["jaar"], "-R", repo, *ontbreekt)
                print(f"{repo} {r['jaar']}: bijgewerkt, {len(ontbreekt)} bestanden aangevuld", flush=True)


if __name__ == "__main__":
    maak(sys.argv[1])
