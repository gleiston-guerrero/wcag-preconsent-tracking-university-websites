# Ecuadorian series from Telconet, 7 September 2026

*Versión en español: [READ_ME_ES.md](READ_ME_ES.md)*

Three passes over the 126 sites of the census, from an Ecuadorian residential
connection of Telconet S.A (AS27947, Guayaquil / Samborondón).

Purpose: an operator control. The campaign reported in the article measured the
Ecuadorian vantage point from ETAPA EP (AS27668, Cuenca). This series checks
whether the Ecuadorian result depends on the network operator.

It is NOT a second measurement occasion and it is not part of the four-vantage
replication. It must not be mixed with data/raw/tracking/ or with
data/raw/tracking_extended/.

Instrument: the same audit_multivantage.js as the reported campaign, unmodified.
axe-core 4.13.0, Playwright 1.62.1, Node v24.12.0; the August campaign used
Node v24.18.1.

It records the state of the cookie jar, not the network requests.

Measurement conditions: same machine and same security configuration as in
August. Microsoft Defender inactive, McAfee installed with no web-protection or
anti-tracking services running. Chromium is launched with a clean profile and no
extensions.
