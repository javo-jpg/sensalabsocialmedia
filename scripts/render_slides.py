"""Render the new carousels/cards (no footage needed) as 1080x1350 JPGs with the Sensa Lab visual system."""
import os, json, asyncio, html
from playwright.async_api import async_playwright
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
M = lambda i: f"file://{ROOT}/media/{i}.jpg"
FONT = "/usr/share/fonts/opentype/inter"
CSS = f"""
@font-face{{font-family:ID;src:url(file://{FONT}/InterDisplay-SemiBold.otf);font-weight:600}}
@font-face{{font-family:ID;src:url(file://{FONT}/InterDisplay-Bold.otf);font-weight:800}}
@font-face{{font-family:ID;src:url(file://{FONT}/InterDisplay-Medium.otf);font-weight:500}}
*{{margin:0;box-sizing:border-box}}
body{{width:1080px;height:1350px;font-family:ID;color:#1c1466;overflow:hidden;position:relative;
 background:radial-gradient(900px 700px at 15% 10%,#ffffff 0%,transparent 60%),radial-gradient(900px 900px at 90% 85%,#8d7bff 0%,transparent 60%),radial-gradient(700px 700px at 20% 90%,#c9b8ff 0%,transparent 70%),#ece6ff}}
body.dark{{color:#fff;background:radial-gradient(900px 800px at 85% 15%,#3b2bff 0%,transparent 60%),radial-gradient(800px 800px at 10% 90%,#7a3cff 0%,transparent 60%),#0b0a1f}}
.pad{{position:absolute;inset:72px}}
.kicker{{font-weight:600;font-size:26px;letter-spacing:.12em;text-transform:uppercase;color:#3b2bff}}
body.dark .kicker{{color:#bdb3ff}}
h1{{font-weight:800;font-size:112px;line-height:.95;letter-spacing:-.04em;margin-top:28px}}
h2{{font-weight:800;font-size:84px;line-height:1;letter-spacing:-.035em;margin-top:24px}}
p.lead{{font-weight:500;font-size:38px;line-height:1.3;margin-top:28px;max-width:880px;opacity:.85}}
.card{{border-radius:36px;background-size:cover;background-position:center 45%;box-shadow:0 30px 80px rgba(28,20,102,.25)}}
.foot{{position:absolute;left:72px;right:72px;bottom:56px;display:flex;justify-content:space-between;align-items:center;font-weight:600;font-size:28px}}
.pill{{border:2px solid currentColor;border-radius:99px;padding:6px 18px;font-size:20px;letter-spacing:.06em}}
.steps{{margin-top:48px;display:flex;flex-direction:column;gap:26px}}
.step{{display:flex;gap:28px;align-items:flex-start;background:rgba(255,255,255,.55);backdrop-filter:blur(10px);border-radius:28px;padding:30px 34px}}
body.dark .step{{background:rgba(255,255,255,.08)}}
.step b{{font-size:44px;font-weight:800;color:#3b2bff;min-width:70px}}body.dark .step b{{color:#bdb3ff}}
.step div{{font-size:36px;font-weight:600;line-height:1.2}}.step small{{display:block;font-size:26px;font-weight:500;opacity:.75;margin-top:8px}}
.big{{font-weight:800;font-size:260px;letter-spacing:-.06em;line-height:.9;color:#3b2bff}}body.dark .big{{color:#fff}}
.src{{font-size:20px;opacity:.6;font-weight:500}}
.cta{{display:inline-block;margin-top:44px;background:#3b2bff;color:#fff;border-radius:99px;padding:22px 40px;font-size:36px;font-weight:600}}
.x{{color:#c2410c}}.ok{{color:#0f8a4b}}body.dark .ok{{color:#5eead4}}body.dark .x{{color:#fdba74}}
"""
def foot(n, total, dark=False):
    return f'<div class="foot"><span>SensaLab</span><span class="pill">{n:02d} / {total:02d}</span><span class="pill">SENSALAB.IO</span></div>'

def steps(items):
    return '<div class="steps">' + "".join(f'<div class="step"><b>{i+1:02d}</b><div>{html.escape(t)}<small>{html.escape(s)}</small></div></div>' for i, (t, s) in enumerate(items)) + "</div>"

def product(name, key, hook, sub, img, how, gets, specs, word, pos="25%"):
    T = 5
    return [
        ("", f'<div class="pad"><div class="kicker">Signature Experience · {key}</div><h1>{hook}</h1><p class="lead">{sub}</p><div class="card" style="height:560px;margin-top:56px;background-image:url({M(img)});background-position:center {pos}"></div></div>{foot(1,T)}'),
        ("", f'<div class="pad"><div class="kicker">{name} · How it works</div><h2>Three steps.<br>Zero training.</h2>{steps(how)}</div>{foot(2,T)}'),
        ("dark", f'<div class="pad"><div class="kicker">{name} · What your brand gets</div><h2>More than<br>a cool moment.</h2>{steps(gets)}</div>{foot(3,T)}'),
        ("", f'<div class="pad"><div class="kicker">{name} · The package</div><div class="big" style="margin-top:40px">3</div><h2 style="margin-top:0">weeks from<br>yes to live.</h2>{steps([(s, "") for s in specs])}</div>{foot(4,T)}'),
        ("dark", f'<div class="pad" style="display:flex;flex-direction:column;justify-content:center"><div class="kicker">{name}</div><h1>Want it at your next event?</h1><p class="lead">Send us a DM with the word <b>{word}</b> and we\'ll send the deck, pricing and dates.</p><span class="cta">DM “{word}”</span></div>{foot(5,T)}'),
    ]

SETS = {
 "N3-mirror": product("Sensa Mirror", "01", "Your guests,<br>restyled by AI.", "An interactive mirror that drops people into your brand’s world, then hands them a photo they actually want to post.",
    "1X1YSGm8G7HswgTgo_4cZTw_rsWAU1tyW",
    [("Step in front of the mirror", "Motion sensor wakes it up, no buttons."), ("AI restyles them in your look", "Outfit, setting and lighting, all on-brand."), ("Scan, save, share", "QR to their phone, your logo on every shot.")],
    [("Branded photos people share", "Every post is organic reach."), ("Opt-in lead data", "Email or phone in exchange for the photo."), ("A report after the event", "Sessions, shares, peak hours.")],
    ["Mirror screen, camera and sensors", "Custom AI style for your brand", "On-site tech + analytics report"], "MIRROR"),
 "N7-playboard": product("Sensa Playboard", "03", "Your catalog,<br>turned into<br>a game.", "A touch table where people tap, match and win with your products, and learn your lineup without reading a spec sheet.",
    "1uo7IBU4jwBAJKNdAOhZvF1NyTGWv00J2",
    [("Walk up and tap", "Big touch surface, made for groups."), ("Match, sort, compete", "Your products are the game pieces."), ("Win and get the takeaway", "Prize, coupon or QR to the product page.")],
    [("Product education that sticks", "People remember what they played with."), ("Data on what they touched", "See which products got the most play."), ("Longer dwell time at the booth", "Groups stay, crowds attract crowds.")],
    ["Touch table, calibrated on site", "Game built with your catalog", "Leaderboard + analytics report"], "PLAYBOARD"),
}
SETS["N4-la28-1"] = [
 ("dark", f'<div class="pad"><div class="kicker">Road to LA 2028 · 01</div><h1>Summer 2028 is coming to LA.</h1><p class="lead">And brands are already planning what they’ll build around it.</p><div class="card" style="height:520px;margin-top:60px;background-image:url({M("13UwjaE12fn_H2RXW3s03gmS5i_RwDB8U")});background-position:center 35%"></div></div>{foot(1,5)}'),
 ("", f'<div class="pad"><div class="kicker">The number</div><div class="big" style="margin-top:80px">~10x</div><h2>more brand activations expected than at Milano Cortina 2026.</h2><p class="src" style="margin-top:40px">John Slusher, CEO of U.S. Olympic &amp; Paralympic Properties, via Adweek.</p></div>{foot(2,5)}'),
 ("", f'<div class="pad"><div class="kicker">What it means</div><h2>The calendar is shorter than it looks.</h2>{steps([("Agencies are scoping now", "Concepts get pitched long before budgets close."), ("Good tech partners book early", "Production capacity in LA will be tight."), ("Messaging locks 6–12 months out", "The build window is what’s left after that.")])}</div>{foot(3,5)}'),
 ("dark", f'<div class="pad"><div class="kicker">What brands will build</div><h2>Where interactive tech fits.</h2>{steps([("Fan zones and viewing parties", "Games, leaderboards, crowd-reactive screens."), ("Pop-ups and retail", "AI mirrors, try-ons, photo moments."), ("Hospitality and VIP", "Immersive rooms and projection.")])}</div>{foot(4,5)}'),
 ("", f'<div class="pad" style="display:flex;flex-direction:column;justify-content:center"><div class="kicker">Sensa Lab · Los Angeles</div><h1>Scoping 2028? Talk to us early.</h1><p class="lead">We’re an LA-based creative tech lab building interactive experiences for agencies and brands.</p><span class="cta">DM “LA28”</span></div>{foot(5,5)}'),
]
SETS["N8-la28-2"] = [
 ("dark", f'<div class="pad"><div class="kicker">Road to LA 2028 · 02</div><h1>Not a sponsor?</h1><p class="lead">You can still own LA’s summer of 2028. You just can’t use the rings.</p><div class="card" style="height:520px;margin-top:60px;background-image:url({M("11P1W7KT0Bxej6cDzY7rOIcV7L6o5afM_")});background-position:center 4%"></div></div>{foot(1,5)}'),
 ("", f'<div class="pad"><div class="kicker">Fair game</div><h2><span class="ok">✓</span> What non-sponsors can build</h2>{steps([("Your own fan experiences", "City pop-ups, games, photo moments."), ("Viewing parties", "Screens, crowd interaction, your space."), ("A summer-in-LA theme", "Sport, heat, the city. Not the Games’ marks.")])}</div>{foot(2,5)}'),
 ("", f'<div class="pad"><div class="kicker">Avoid</div><h2><span class="x">✕</span> What gets ideas killed by legal</h2>{steps([("The rings and official marks", "Logos, mascots, protected names and terms."), ("Implying you’re official", "“Official partner” language or look-alikes."), ("Branding inside official venues", "Strict rules set by the organizers.")])}</div>{foot(3,5)}'),
 ("dark", f'<div class="pad"><div class="kicker">The play</div><h2>Win on the experience, not the logo.</h2><p class="lead">The activations people remember are the ones they get to do something in. That works with or without a sponsorship.</p></div>{foot(4,5)}'),
 ("", f'<div class="pad" style="display:flex;flex-direction:column;justify-content:center"><div class="kicker">Sensa Lab · Los Angeles</div><h1>Planning a 2028 activation?</h1><p class="lead">We build the interactive layer. Save this and send it to your legal team.</p><span class="cta">DM “LA28”</span><p class="src" style="margin-top:40px">General information, not legal advice. Source: BizBash.</p></div>{foot(5,5)}'),
]
SETS["N2-jon"] = [("dark", f'<div class="pad" style="display:flex;flex-direction:column;justify-content:center"><div class="kicker">Notes from the lab</div><h1 style="font-size:96px">The tech is never what fails.</h1><p class="lead">It’s the queue, the Wi-Fi, the staff, the screen nobody could see from the aisle.</p></div><div class="foot"><span>Jon · Sensa Lab</span><span class="pill">SENSALAB.IO</span></div>')]
SETS["N6-javier"] = [("", f'<div class="pad" style="display:flex;flex-direction:column;justify-content:center"><div class="kicker">Activation ROI</div><h1 style="font-size:96px">If you can’t measure it, it was decoration.</h1><p class="lead">QR, opt-ins, dwell time, shares. Plan the data before you plan the build.</p></div><div class="foot"><span>Javier · Sensa Lab</span><span class="pill">SENSALAB.IO</span></div>')]

async def main(only=None):
    os.makedirs(f"{ROOT}/media/new", exist_ok=True)
    out = {}
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1080, "height": 1350})
        for k, slides in SETS.items():
            if only and k not in only: continue
            out[k] = []
            for i, (cls, body) in enumerate(slides):
                tmp = f"{ROOT}/media/new/_tmp.html"
                open(tmp, "w").write(f'<html><head><meta charset="utf-8"><style>{CSS}</style></head><body class="{cls}">{body}</body></html>')
                await pg.goto("file://" + tmp, wait_until="load"); await pg.evaluate("document.fonts.ready")
                await pg.wait_for_timeout(200)
                fn = f"new/{k}-{i+1}"; await pg.screenshot(path=f"{ROOT}/media/{fn}.jpg", type="jpeg", quality=90)
                out[k].append(fn)
        await b.close()
    json.dump(out, open(f"{ROOT}/media/new/index.json", "w"), indent=1)
    print(out)
asyncio.run(main())
