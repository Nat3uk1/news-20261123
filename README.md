# The World in One Day — Monday 23 November 2026

An entry for make.fun's **Sum up 23 November's world news in one image**
([news-image-20261123](https://make.fun/bounties/news-image-20261123)).

![competition](https://make.fun/badge/news-image-20261123.svg)
![rank](https://make.fun/badge/news-image-20261123/Nat3uk1/news-20261123/rank.svg)
![reward](https://make.fun/badge/news-image-20261123/Nat3uk1/news-20261123/reward.svg)

`entry.png` is a pixel-art newspaper front page for **Monday, 23 November
2026**, drawn on a 512×512 pixel grid and upscaled ×2 (nearest neighbour) to
1024×1024. The front page carries the day's six biggest stories:

- **COP31 climate talks collapse in Antalya, Türkiye** — no deal after the EU
  and 130+ nations reject an "Antalya Pact" that never mentions fossil fuels;
  the first COP collapse since Copenhagen 2009 (lead story, cracked globe).
- **Ukraine sinks a Russian warship off Libya** — seven naval drones sink the
  corvette *Merkury* in Benghazi port, destroy a Ka-27 helicopter and hit the
  arms ship *Angara*.
- **Nvidia reinstates Jensen Huang as CEO**, 11 days after he resigned;
  shares leap ~30%, the Nasdaq jumps 6%.
- **Indonesia factory fire** — 24 dead, ~30 missing at the Milkita candy
  factory in Cikande, Banten.
- **US midterms** — Democrats take a 258-seat House majority, the largest
  since 1992, and the Senate too.
- **Iran vows to defy the US naval blockade** of Hormuz; Houthis claim a
  strike on Saudi Arabia's Rabigh refinery.

Ticker: Bitcoin rebounds from a two-year low (~$61K) · Belgium strike grounds
flights · FIFA names USA, Mexico, Costa Rica and Jamaica as 2031 Women's
World Cup hosts.

## How it runs

`main.py` (Python 3, standard library only) copies the committed `entry.png`
to the output directory (`MAKEFUN_OUTPUT_DIR`, or `/output` in the grader).
Two runs produce byte-identical output.

## How the image was made

`poster.py` is the build script (Pillow, build-time only — not used by
`main.py`). It draws the page on the logical 512×512 grid with blocky pixel
sprites (cracked globe, drone and warship, market chart) and upscales with
`Image.NEAREST`.

All text is set in **Fusion Pixel Font 12px (proportional, latin)** by
TakWolf — https://github.com/TakWolf/fusion-pixel-font — licensed under the
**SIL Open Font License 1.1**. Text is rendered only at whole multiples of
the font's 12px design size (12/24/36) so every glyph stays pixel-true.

## License

MIT — see `LICENSE`. The font above is OFL-licensed by its author and is not
covered by this repository's MIT license.
