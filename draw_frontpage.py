#!/usr/bin/env python3
"""Draw the news-image-20261119 front page: 'The World in One Page'.

Thursday 19 November 2026 - 40 stories, 6 continents, one page.
Lead: the ICJ rules 9-6 that Myanmar committed genocide against the
Rohingya in 2017 - the first state ever found guilty of genocide.
Second story: the first-ever Trump-Xi-Putin trilateral in Shenzhen ends
with a four-point peace declaration but no deal on Ukraine or Iran.
Third: GTA VI launches worldwide after a 13-year wait.
Verified against Reuters, AP, BBC, The Hindu, NDTV, FT and UN reporting
for 18-19 Nov 2026. Hero: generated illustration of the Peace Palace.
Output: 1024x1024 PNG, deterministic (no randomness, no network, no clock).
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (250, 246, 236)
INK = (17, 17, 17)
GREY = (90, 90, 90)
WHITE = (255, 255, 255)

F = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = os.path.join(F, "DejaVuSerif-Bold.ttf")
SERIF = os.path.join(F, "DejaVuSerif.ttf")
SANS = os.path.join(F, "DejaVuSans.ttf")
SANS_B = os.path.join(F, "DejaVuSans-Bold.ttf")
HERE = os.path.dirname(os.path.abspath(__file__))
HERO = os.path.join(HERE, "media-generation-news19-hero-peace-palace-0-2dc38f24-f64b-49c2-9988-0a5bcb7ad4ef.webp")

COL = {
    "ASIA": (0, 87, 183), "EUROPE": (15, 118, 110), "AFRICA": (166, 90, 0),
    "AMERICAS": (166, 25, 46), "OCEANIA": (109, 40, 217), "WORLD": (120, 90, 0),
    "SPORT": (51, 65, 85),
}


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def trunc(draw, text, fnt, max_w):
    if draw.textlength(text, font=fnt) <= max_w:
        return text
    while text and draw.textlength(text + "...", font=fnt) > max_w:
        text = text.rsplit(" ", 1)[0] if " " in text else text[:-1]
    return text + "..."


def hero_crop(box_w, box_h):
    im = Image.open(HERO).convert("RGB")
    w, h = im.size
    target = box_w / box_h
    ch = int(w / target)
    ch = min(ch, h)
    im = im.crop((0, 0, w, ch))
    return im.resize((box_w, box_h), Image.LANCZOS)


# (region, headline, deck) - 37 grid stories; lead + 2 strips make 40.
ITEMS = [
    ("ASIA", "Cyclone Akvan bears down on Odisha", "Landfall due Friday near Gopalpur; 72,000 evacuated."),
    ("ASIA", "Modi meets William and Kate", "UK-India ties top the agenda."),
    ("ASIA", "India, Japan review defence ties", "Ministers meet in Tokyo."),
    ("ASIA", "Iran widens Gulf attacks", "Kuwait base hit; Bahrain struck again."),
    ("ASIA", "China extends US tariff truce", "24% tariff suspended to 10 Jan 2027."),
    ("ASIA", "Canada adjusts China ties", "Carney seeks the right deal with US."),
    ("ASIA", "Saudi alerts lifted", "Danger passed in three southern cities."),
    ("ASIA", "APEC closes in Shenzhen", "21 leaders wrap the summit."),
    ("ASIA", "Quad leaders wrap Manila talks", "Trump flew on to Shenzhen after Manila."),
    ("ASIA", "AI 171 crash report nearly done", "Centre tells top court probe at fag end."),
    ("ASIA", "Indian journalists hit back", "'We are journalists, not reel makers.'"),
    ("ASIA", "Taiwan drafts repression crime", "Bill targets transnational repression."),
    ("ASIA", "50 pupils ill after tar-plant fumes", "Suspected pollution hospitalises children."),
    ("ASIA", "Railways brace for Cyclone Akvan", "Minister reviews storm preparedness."),
    ("EUROPE", "EU proposes EUR 45bn Ukraine loan", "Covers Kyiv's EUR 70bn shortfall."),
    ("EUROPE", "Melenchon 'could win' French presidency", "Justice minister's warning."),
    ("EUROPE", "Tanker sunk off Bulgaria 'hit by projectiles'", "Officials confirm the strike."),
    ("EUROPE", "Deutsche Bank's $582m Epstein deals", "FT reports the 2013-2018 flows."),
    ("AFRICA", "Somalia accuses UAE of secret bases", "Mogadishu alleges unauthorised sites."),
    ("AFRICA", "Libya seizes cocaine, millions of pills", "Haul found in the east, officials say."),
    ("AMERICAS", "Jeffries nominated for Speaker, 251-11", "First Black Speaker if elected in Jan."),
    ("AMERICAS", "Peltola wins Alaska Senate race", "Democrats hold the Alaska seat."),
    ("AMERICAS", "Senators warn AI cyber threats grow", "White House urged to act."),
    ("AMERICAS", "Fed minutes point to more rate hikes", "Most officials back further rises."),
    ("AMERICAS", "Liu Yunping elected caucus chair", "First Taiwanese American in the post."),
    ("AMERICAS", "US proposes tougher green-card rules", "Longer hiring process ahead."),
    ("AMERICAS", "Mexico publishes Banxico minutes", "November 5 cut to 6.25% explained."),
    ("AMERICAS", "Trump 'unhappy' Vance balked at Iran war", "Report says president praised Rubio."),
    ("OCEANIA", "Australia sanctions Israeli settlers", "Over West Bank expansion."),
    ("OCEANIA", "New Zealand first to play GTA VI", "Midnight launch begins the rollout."),
    ("WORLD", "Voyager 1 nears one light-day", "NASA to confirm the milestone today."),
    ("WORLD", "Pew: Islam largest faith by 2035", "Report projects the crossover."),
    ("WORLD", "Earth 'lost' a billion years of history", "Scientists may have found why."),
    ("WORLD", "Oil slides as Gulf tension rises", "Markets rattled by the Middle East."),
    ("WORLD", "Nvidia halts H-series chips to China", "Chipmaker cites export rules."),
    ("SPORT", "India forms panel for pro leagues", "14-member body to shape leagues."),
    ("SPORT", "Duckett 133 puts England on top", "England on top in the third ODI."),
]


def main():
    assert len(ITEMS) == 37, len(ITEMS)
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 26
    # ---- masthead ----
    d.text((W // 2, 14), "THE WORLD", font=font(SERIF_B, 64), fill=INK, anchor="ma")
    d.text((W // 2, 92), "THURSDAY 19 NOVEMBER 2026  \u2022  40 STORIES  \u2022  6 CONTINENTS  \u2022  ONE PAGE",
           font=font(SANS_B, 15), fill=INK, anchor="ma")
    d.line([(M, 120), (W - M, 120)], fill=INK, width=4)
    d.line([(M, 126), (W - M, 126)], fill=INK, width=1)

    # ---- lead: ICJ judgment, hero right ----
    d.text((M, 136), "THE HAGUE  \u2022  WORLD COURT", font=font(SANS_B, 14), fill=COL["EUROPE"])
    d.text((M, 156), "MYANMAR GUILTY", font=font(SERIF_B, 33), fill=INK)
    d.text((M, 194), "OF GENOCIDE", font=font(SERIF_B, 33), fill=INK)
    deck = ("The world court rules 9-6: Myanmar committed genocide "
            "against the Rohingya in 2017 - the first state ever "
            "found guilty of genocide.")
    y = 236
    for ln in wrap(d, deck, font(SERIF, 16), 560):
        d.text((M, y), ln, font=font(SERIF, 16), fill=INK)
        y += 21
    hx, hy, hw, hh = 600, 136, 398, 170
    img.paste(hero_crop(hw, hh), (hx, hy))
    d.rectangle([hx, hy, hx + hw, hy + hh], outline=INK, width=2)
    d.rectangle([hx, hy + hh - 26, hx + hw, hy + hh], fill=(15, 118, 110))
    d.text((hx + hw // 2, hy + hh - 22), "PEACE PALACE  \u2022  9-6 VERDICT",
           font=font(SANS_B, 13), fill=WHITE, anchor="ma")

    # ---- strip 1: trilateral ----
    ty = 318
    d.rectangle([M, ty, W - M, ty + 40], fill=INK)
    d.text((M + 14, ty + 4), "TRUMP, XI, PUTIN: PEACE DECLARATION, NO DEAL  \u2022  ",
           font=font(SANS_B, 15), fill=(255, 213, 79))
    d.text((M + 14, ty + 22), "Four-point pact on nuclear talks, oil and the UN - but nothing on Ukraine or Iran",
           font=font(SANS, 14), fill=WHITE)
    d.text((W - M - 14, ty + 4), "ASIA", font=font(SANS_B, 15), fill=(255, 213, 79), anchor="ra")

    # ---- strip 2: GTA VI ----
    gy = 364
    d.rectangle([M, gy, W - M, gy + 40], fill=(24, 24, 64))
    d.text((M + 14, gy + 4), "GTA VI IS OUT  \u2022  ",
           font=font(SANS_B, 15), fill=(255, 213, 79))
    d.text((M + 14, gy + 22), "Rockstar's epic launches worldwide after a 13-year wait; preorders top $1.5bn",
           font=font(SANS, 14), fill=WHITE)
    d.text((W - M - 14, gy + 4), "WORLD", font=font(SANS_B, 15), fill=(255, 213, 79), anchor="ra")

    # ---- 37-item grid: 3 cols x 13 rows ----
    gx, gy2 = M, 416
    cw = (W - 2 * M - 24) // 3
    chh = 42
    for i, (reg, head, deck) in enumerate(ITEMS):
        x = gx + (i % 3) * (cw + 12)
        y = gy2 + (i // 3) * chh
        col = COL[reg]
        d.line([(x, y + 3), (x, y + chh - 7)], fill=col, width=4)
        d.text((x + 10, y), reg, font=font(SANS_B, 9), fill=col)
        d.text((x + 10, y + 11), trunc(d, head, font(SERIF_B, 12), cw - 12),
               font=font(SERIF_B, 12), fill=INK)
        d.text((x + 10, y + 27), trunc(d, deck, font(SANS, 10), cw - 12),
               font=font(SANS, 10), fill=(60, 60, 60))

    # ---- footer ----
    d.text((W // 2, 984), "Sources: Reuters, AP, BBC, The Hindu, NDTV, FT, UN  \u2022  19 November 2026",
           font=font(SANS, 11), fill=GREY, anchor="ma")
    out = os.path.join(HERE, "news.png")
    img.save(out, optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
