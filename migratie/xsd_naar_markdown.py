"""Zet een berichtschema (XSD) van de Verzuimstandaard om naar een leesbare Markdown-pagina.

De structuur, het voorkomen, het formaat en de toegestane waarden komen uit de
XSD. De Nederlandse namen komen uit de functionele hiërarchie (de FunHie-PDF)
als die er is; die PDF koppelt elke xml-tag aan een naam.

Eén regel per element, zodat een vergelijking tussen twee releases per element
laat zien wat er veranderd is.
"""
import re
from pathlib import Path

from lxml import etree

XS = "{http://www.w3.org/2001/XMLSchema}"
MAX_WAARDEN = 12


def namen_uit_funhie(pdfpad):
    """Lees uit een FunHie-PDF per xml-tag de naam en of hij verplicht (V) of facultatief (F) is."""
    if not pdfpad:
        return {}
    import fitz

    regels = []
    with fitz.open(pdfpad) as pdf:
        for pagina in pdf:
            regels += [r.strip() for r in pagina.get_text().splitlines()]
    namen = {}
    for i, regel in enumerate(regels):
        m = re.match(r"xml tag:\s*(\S+)", regel)
        if not m or m.group(1) in namen:
            continue
        tag = m.group(1)
        if i >= 3 and regels[i - 2] in ("V", "F"):
            naam = regels[i - 3]
        else:
            naam = regels[i - 1] if i >= 1 else ""
        # Groepen heten in de PDF "werkgever - COMMUNICATIE"; alleen het laatste deel is de naam.
        naam = re.sub(r"^.* - (?=[A-Z][A-Z /-]+$)", "", naam)
        if naam.isupper():
            naam = naam.capitalize()
        namen[tag] = naam
    return namen


class Schema:
    def __init__(self, pad):
        self.boom = etree.parse(str(pad))
        self.wortel = self.boom.getroot()
        self.namespace = self.wortel.get("targetNamespace", "")
        self.versie = self.wortel.get("version", "")
        self.simpel = {t.get("name"): t for t in self.wortel.findall(f"{XS}simpleType")}
        self.complex = {t.get("name"): t for t in self.wortel.findall(f"{XS}complexType")}

    @staticmethod
    def lokaal(naam):
        return naam.split(":")[-1] if naam else naam

    def formaat(self, restrictie):
        """Beschrijf een xs:restriction in de notatie van de SIVI-documentatie (an..35, n..9,2, ...)."""
        basis = self.lokaal(restrictie.get("base", ""))
        facetten = {}
        waarden = []
        for f in restrictie:
            if not isinstance(f.tag, str):
                continue
            soort = f.tag.replace(XS, "")
            if soort == "enumeration":
                waarden.append(f.get("value"))
            else:
                facetten[soort] = f.get("value")
        if basis in self.simpel:
            onder_formaat, onder_waarden = self.simpel_formaat(self.simpel[basis])
            return onder_formaat, waarden or onder_waarden
        if basis in ("decimal", "integer", "int", "long", "nonNegativeInteger", "positiveInteger"):
            cijfers = facetten.get("totalDigits", "")
            decimalen = facetten.get("fractionDigits")
            tekst = f"n..{cijfers}" if cijfers else "n"
            if decimalen and decimalen != "0":
                tekst += f",{decimalen}"
            return tekst, waarden
        if basis == "date":
            return "datum", waarden
        if basis == "time":
            return "tijd", waarden
        if basis == "base64Binary":
            return "binair (base64)", waarden
        if "length" in facetten:
            return f"an{facetten['length']}", waarden
        if "maxLength" in facetten:
            return f"an..{facetten['maxLength']}", waarden
        return basis or "tekst", waarden

    def simpel_formaat(self, simpletype):
        restrictie = simpletype.find(f"{XS}restriction")
        if restrictie is None:
            return "tekst", []
        return self.formaat(restrictie)

    def type_van(self, element):
        """Geef (formaat, waarden, kinderen) voor een element."""
        typenaam = self.lokaal(element.get("type"))
        complextype = element.find(f"{XS}complexType")
        simpletype = element.find(f"{XS}simpleType")
        if complextype is None and typenaam in self.complex:
            complextype = self.complex[typenaam]
        if complextype is not None:
            return "groep", [], self.kinderen(complextype)
        if simpletype is not None:
            formaat, waarden = self.simpel_formaat(simpletype)
            return formaat, waarden, []
        if typenaam in self.simpel:
            formaat, waarden = self.simpel_formaat(self.simpel[typenaam])
            return formaat, waarden, []
        if typenaam:
            return {"date": "datum", "time": "tijd", "string": "tekst"}.get(typenaam, typenaam), [], []
        return "", [], []

    def kinderen(self, complextype):
        uit = []
        for houder in complextype.iter(f"{XS}sequence", f"{XS}choice", f"{XS}all"):
            for kind in houder:
                if kind.tag == f"{XS}element" and kind.getparent() is houder:
                    uit.append(kind)
            break
        return uit

    def regels(self, element, niveau=0):
        minimum = element.get("minOccurs", "1")
        maximum = element.get("maxOccurs", "1")
        maximum = "*" if maximum == "unbounded" else maximum
        formaat, waarden, kinderen = self.type_van(element)
        yield niveau, element.get("name") or self.lokaal(element.get("ref")), f"{minimum}..{maximum}", formaat, waarden
        for kind in kinderen:
            yield from self.regels(kind, niveau + 1)


def markdown(xsdpad, bericht, koppelvlak_titel, jaar, funhie_pdf=None):
    schema = Schema(xsdpad)
    namen = namen_uit_funhie(funhie_pdf)
    wortels = schema.wortel.findall(f"{XS}element")
    regels = []
    for wortel in wortels:
        regels += list(schema.regels(wortel))

    uit = [
        f"# {bericht}",
        "",
        f"Verzuimstandaard {koppelvlak_titel}, release {jaar}.",
        "",
        "| | |",
        "|---|---|",
        f"| Schema | [`xsd/{Path(xsdpad).name}`](../xsd/{Path(xsdpad).name}) |",
        f"| Namespace | `{schema.namespace}` |",
        f"| Versie | {schema.versie or '-'} |",
        f"| Elementen | {len(regels)} |",
        "",
        "Deze pagina is afgeleid van de XSD. De namen komen uit de functionele hiërarchie;"
        " de volledige toelichting per element staat in de PDF bij de release.",
        "",
        "## Berichtstructuur",
        "",
        "| XML-tag | Naam | Voorkomen | Formaat | Toegestane waarden |",
        "|---|---|---|---|---|",
    ]
    for niveau, tag, voorkomen, formaat, waarden in regels:
        inspringing = "&emsp;" * niveau
        if len(waarden) > MAX_WAARDEN:
            waardetekst = f"{len(waarden)} waarden, o.a. " + ", ".join(waarden[:5]) + " …"
        else:
            waardetekst = ", ".join(waarden)
        naam = namen.get(tag, "").replace("|", "/")
        if formaat == "groep":
            tagtekst = f"{inspringing}**`{tag}`**"
        else:
            tagtekst = f"{inspringing}`{tag}`"
        uit.append(f"| {tagtekst} | {naam} | {voorkomen} | {formaat} | {waardetekst} |")
    uit.append("")
    return "\n".join(uit), len(regels)
