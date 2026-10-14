# Flash Card

🌐 [English](Home) · **Dansk** · [Bahasa Malaysia](Home-ms)

Et flashkortprogram til at lære de mest almindelige malajiske ord med danske oversættelser. Det er løsningen på dag 31 i Udemys kursus *100 Days of Code: The Complete Python Pro Bootcamp*.

![Forsiden af et kort: det malajiske ord](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/031-flash-card/raw/branch/main/docs/images/screenshot-front.png)
![Bagsiden af kortet efter tre sekunder: den danske oversættelse](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/031-flash-card/raw/branch/main/docs/images/screenshot-back.png)

| Side | Læs den, når du vil |
| --- | --- |
| [Installation](Install-da) | Oprette `.venv`, installere programmet og køre testene |
| [Brug](Usage-da) | Øve kortene, forstå fremgangsfilen og bruge indstillingerne |
| [Arkitektur](Architecture-da) | Se lagene og finde koden til hvert opgavetrin |

## De fire opgavetrin

| Trin | Hvad programmet gør | Milepæl |
| --- | --- | --- |
| 1. Brugerflade | Et vindue med et kort og to knapper | MIL-002 |
| 2. Nye flashkort | Et tilfældigt ord fra ordlisten ved hvert tryk på en knap | MIL-003 |
| 3. Vend kortene | Efter 3 sekunder viser kortet den danske oversættelse | MIL-004 |
| 4. Gem din fremgang | Kendte ord fjernes, og resten gemmes i `words_to_learn.csv` | MIL-005 |
| Ekstra | Det malajiske ord bliver udtalt (valgfrit) | MIL-006 |

## Til kursister

Opgavens funktionsnavne er bevaret: `next_card`, `flip_card`, `is_known` og attributterne `flip_timer` og `current_card`. Data læses med standardbibliotekets `csv`-modul i stedet for `pandas`, så kerneprogrammet ikke har nogen afhængigheder ved kørsel.

Repository: <https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/031-flash-card>
