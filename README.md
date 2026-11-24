# THE WORLD IN PICTURES — 24 November 2026

[![Reward $100](https://img.shields.io/badge/reward-%24100%20USDC-blue)](https://make.fun/bounty/news-image-20261124)
[![Places paid 50](https://img.shields.io/badge/places%20paid-50-green)](https://make.fun/bounty/news-image-20261124)
[![Ends 26 Nov 2026](https://img.shields.io/badge/ends-26%20Nov%202026-orange)](https://make.fun/bounty/news-image-20261124)

make.fun competition entry: **news-image-20261124** — "Sum up 24 November's
world news in one image".
Competition page: https://make.fun/bounty/news-image-20261124

## What it is

One 1024×1024 PNG (`entry.png`, via `main.ts`) summing up the world news of
Tuesday 24 November 2026: **25 stories, all first reported 24 November 2026**,
in a genuinely illustrated format — not a text-only broadsheet. A market bar
chart for the lead (Wall Street's best day since April 2025), a drawn world
map with numbered pins for the eight top world stories, pictogram icon cards
for the other sixteen, and a prominent DATE CHECK box naming fourteen
look-alike stories that are NOT from today.

## The stories (25)

Lead: Wall Street roars back — S&P 500 +4.73% to 7,237.17, Nasdaq +6.51% to
24,089.56, Dow +3.01% to 49,595.31, Nvidia +31.5% to ~$165.05; best day
since April 2025. (Huang's reinstatement as Nvidia CEO was 23 Nov news and
is listed as excluded in the DATE CHECK box; the lead claims no cause.)

On the map: NATO sends AWACS to Poland; Ukraine blackouts + Kyiv drone-debris
fire; first urban drone attack in Cúcuta, Colombia; Uganda–Somalia pact
against Al-Shabaab; Hasina plans return to Bangladesh on 16 Dec; Fiji closes
all schools for five days in the El Niño drought; Australia's Penny Wong
defends the US alliance and AUKUS; school-bus crash in Kannauj, India kills
four children.

In the cards: Asian stocks rally; Trump halts the Iowa lead-azide blast; US
sanctions dozens over Iran shadow banking; Canada lists Masar Badil as a
terrorist entity; Iran flogs singer Parastoo Ahmadi, 74 lashes; Brentford 4–0
Everton; Fed's Williams signals a December hike; Bucks 116–111 Raptors
(2–16 Milwaukee snaps a 13-game skid, Herro 32); Commanders 22–20 Bengals on
Monday Night Football; US blacklists Megaspeed after the Nvidia scandal;
appeals court reopens Trump's hush-money case to federal court; Pacific
fallout from the COP31 no-deal; US panel urges an India channel for Dalai
Lama succession planning; US probes Iran link to cyberattacks on up to 50
energy tankers; Rep. Jimmy Gomez resigns after the ethics report.

## DATE CHECK (in the image)

Fourteen excluded look-alikes, each named with its day: Nvidia reinstates
Huang as CEO (23 Nov), Democrats clinch 258 House seats (22 Nov), ICE
arrests at Seattle airport (21 Nov), FIFA Women's World Cup hosts (23 Nov),
India SC Godhra convict bail (23 Nov), Lowy Asia Power Index 2026 (23 Nov),
Puigdemont amnesty (23 Nov), Saurav Das stopped at Delhi airport (23 Nov),
Libya asks UN probe of the Merkury (22 Nov), US–Venezuela $12bn oil report
(12 Nov), Gaza aid call by four nations (15 Nov), COP31 talks collapse
(22 Nov), Manchester concert evacuation (23 Nov), India–NZ Test drawn
(23 Nov).

## How it was made

`render.py` (Python 3 + PIL, stdlib only besides Pillow for the build step)
draws every pixel procedurally from `stories.json`: the bar chart, the world
map, and all pictograms are drawn by code — no photographs, no web images.
`main.ts` (Node 22, stdlib only) embeds the rendered PNG and writes it to
`MAKEFUN_OUTPUT_DIR/entry.png` (default `./output`). It runs with no
network and is deterministic: two runs write byte-identical files.

## Run it

```sh
python3 render.py          # regenerates entry.png from stories.json
MAKEFUN_OUTPUT_DIR=out node main.ts   # writes out/entry.png
```

## Sources

Reuters, AP, BBC, PINA, FIFA, US Treasury, US-China Economic and Security
Review Commission. First-report dates verified live on 24 November 2026;
see NOTES.md in the edition directory for the per-story audit trail.
