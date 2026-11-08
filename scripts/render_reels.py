"""Build vertical reels (1080x1920, silent; audio is added natively in IG at scheduling) from generated scenes."""
import os, asyncio, subprocess, json
from playwright.async_api import async_playwright
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT = "/usr/share/fonts/opentype/inter"
M = lambda i: f"file://{ROOT}/media/{i}.jpg"
CSS = f"""
@font-face{{font-family:ID;src:url(file://{FONT}/InterDisplay-Bold.otf);font-weight:800}}
@font-face{{font-family:ID;src:url(file://{FONT}/InterDisplay-Medium.otf);font-weight:500}}
*{{margin:0;box-sizing:border-box}}
body{{width:1080px;height:1920px;overflow:hidden;font-family:ID;color:#fff;position:relative;
background:radial-gradient(900px 900px at 85% 10%,#3b2bff 0%,transparent 60%),radial-gradient(900px 900px at 10% 95%,#7a3cff 0%,transparent 60%),#0b0a1f}}
body.light{{color:#1c1466;background:radial-gradient(900px 800px at 15% 10%,#fff 0%,transparent 60%),radial-gradient(1000px 1000px at 90% 90%,#8d7bff 0%,transparent 60%),#ece6ff}}
.img{{position:absolute;left:60px;right:60px;top:640px;height:760px;border-radius:44px;background-size:cover;box-shadow:0 40px 100px rgba(0,0,0,.45)}}
.t{{position:absolute;left:80px;right:80px;top:200px;font-weight:800;font-size:150px;line-height:.95;letter-spacing:-.045em}}
.t.mid{{top:auto;bottom:auto;top:50%;transform:translateY(-50%)}}
.s{{font-weight:500;font-size:46px;letter-spacing:0;margin-top:30px;opacity:.85;line-height:1.25}}
.k{{position:absolute;left:80px;top:120px;font-weight:500;font-size:34px;letter-spacing:.14em;color:#bdb3ff}}
.f{{position:absolute;left:80px;right:80px;bottom:110px;display:flex;justify-content:space-between;font-weight:500;font-size:34px}}
.pill{{border:2px solid currentColor;border-radius:99px;padding:6px 20px;font-size:28px}}
"""
def sc(text, img=None, pos="12%", kicker="", sub="", light=False, mid=False):
    i = f'<div class="img" style="background-image:url({M(img)});background-position:center {pos}"></div>' if img else ""
    s = f'<div class="s">{sub}</div>' if sub else ""
    k = f'<div class="k">{kicker}</div>' if kicker else ""
    return ("light" if light else "", f'{k}<div class="t{" mid" if mid else ""}">{text}{s}</div>{i}<div class="f"><span>SensaLab</span><span class="pill">SENSALAB.IO</span></div>')

REELS = {
 "N1-lab": [(1.6, sc("Not a studio.", mid=True)),
            (1.6, sc("A lab.", "11P1W7KT0Bxej6cDzY7rOIcV7L6o5afM_", "2%", "SENSA LAB")),
            (1.8, sc("Mirrors that restyle you.", "1X1YSGm8G7HswgTgo_4cZTw_rsWAU1tyW")),
            (1.8, sc("Games that sell for you.", "1uo7IBU4jwBAJKNdAOhZvF1NyTGWv00J2")),
            (1.8, sc("Avatars that wave back.", "1KZTBuZ5E3p2JoF0QJYCCr7oPTc05AbJk", "8%")),
            (2.4, sc("Things people<br>actually touch.", sub="Interactive experiences for brands + agencies. Los Angeles.", light=True, mid=True))],
 "N5-arcade": [(1.4, sc("Press start.", "1uo7IBU4jwBAJKNdAOhZvF1NyTGWv00J2", kicker="SENSA ARCADE")),
               (1.8, sc("Your brand, as a game.", "10Ojfh6BTAqn9aS6XQcb4UajY8X9srxuR")),
               (1.8, sc("Move. Tap. Play.", "1dsaFdpVDQxg-bRl7Q49nmsfcWboc6JVh")),
               (1.8, sc("Live leaderboard.", "11ZhJx582VnYCIlFPCDRlbuY8B-U1ZrvO")),
               (1.8, sc("Every round is a lead.", mid=True)),
               (2.4, sc("Sensa Arcade.", sub="Ready in 3 weeks.<br>DM “ARCADE” for the deck.", light=True, mid=True))],
 "N9-recap": [(1.6, sc("November<br>in the lab.", mid=True, kicker="RECAP"))] +
             [(0.7, sc("", m, "12%")) for m in ["13UwjaE12fn_H2RXW3s03gmS5i_RwDB8U", "1ggL9_llGWwkKGW15LRcAADrcWO7b9aZI", "1KZTBuZ5E3p2JoF0QJYCCr7oPTc05AbJk", "1WXG4E6f_a6INkLimEpE9AH_WlhQsFB6l", "1FmTxuFvgFLUKpdT07gB2KyXvn7r93fHF", "1-WM8vtrYEmKHCR9OLmgeKBxj1V7tRcfZ", "19YrIkX0THY0IIuZc-7o7QepcwHN2w1p6", "14H4knetR-f51wdZqsf281FbmAnh4yW7p", "1XIRPaB8oFdYEQ2QHZMte2dJoQT0B0kwu", "1sSi-H-9DpMIscLg8dZeZtUs7bxT9Yyru"]] +
             [(2.4, sc("December’s loading.", sub="Want in? DMs open.", light=True, mid=True))],
}

async def render():
    d = f"{ROOT}/build/reels"; os.makedirs(d, exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1080, "height": 1920})
        for k, scenes in REELS.items():
            for i, (dur, (cls, body)) in enumerate(scenes):
                f = f"{d}/{k}-{i:02d}.html"
                open(f, "w").write(f'<html><head><meta charset="utf-8"><style>{CSS}</style></head><body class="{cls}">{body}</body></html>')
                await pg.goto("file://" + f); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(150)
                await pg.screenshot(path=f"{d}/{k}-{i:02d}.png")
        await b.close()

def encode():
    d = f"{ROOT}/build/reels"; os.makedirs(f"{ROOT}/media/new", exist_ok=True)
    for k, scenes in REELS.items():
        parts = []
        for i, (dur, _) in enumerate(scenes):
            out = f"{d}/{k}-{i:02d}.mp4"; n = int(dur * 30)
            # slow push-in for life
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-i", f"{d}/{k}-{i:02d}.png", "-vf",
                f"scale=1188:2112,zoompan=z='min(1+0.0016*on,1.1)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={n}:s=1080x1920:fps=30,format=yuv420p",
                "-frames:v", str(n), "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", out], check=True)
            parts.append(out)
        lst = f"{d}/{k}.txt"; open(lst, "w").write("".join(f"file '{x}'\n" for x in parts))
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
                        "-shortest", "-c:v", "copy", "-c:a", "aac", "-movflags", "+faststart", f"{ROOT}/media/new/{k}.mp4"], check=True)
        subprocess.run(["cp", f"{d}/{k}-00.png", f"{ROOT}/media/new/{k}-cover.png"])
        print(k)

asyncio.run(render()); encode()
