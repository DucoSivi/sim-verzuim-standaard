# Bedrijfsprocessen: Arbodiensten ↔ Verzekeraars

Dit document beschrijft de gegevensuitwisseling tussen arbodiensten en verzekeraars met betrekking tot re-integratie en interventies.

---

## 1. Aanvraag Interventie (Schadelastbeheersing)
* **Trigger:** Bedrijfsarts adviseert een gerichte interventie (bijv. psychologische ondersteuning, werkplekaanpassing).
* **Actie arbodienst:** Verzending van `InterventieAanvraag` met doelomschrijving en kostenindicatie.

## 2. Voortgang Re-integratiestatus (Poortwachter)
* **Trigger:** Bereiken van wettelijke mijlpalen (week 6 Probleemanalyse, week 52 Eerstejaarsevaluatie).
* **Actie arbodienst:** Verzending van `ReintegratieStatus` (uitsluitend functionele capaciteiten, GEEN medische diagnose).
