import json, html, os, datetime, base64, io
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d = json.load(open(os.path.join(ROOT, "data/posts.json")))
DAYS = ["Lun","Mar","Mié","Jue","Vie","Sáb","Dom"]
MES = ['','ene','feb','mar','abr','may','jun','jul','ago','sep','oct','nov','dic']
def fmt(ds):
    dt = datetime.date.fromisoformat(ds); return f"{DAYS[dt.weekday()]} {dt.day} {MES[dt.month]}"
def b64(path, box):
    im = Image.open(path); im.thumbnail(box); b = io.BytesIO(); im.convert("RGB").save(b, "JPEG", quality=72)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()
def thumb(i):
    f = os.path.join(ROOT, "media", i.replace(".mp4", "-cover.png") if i.endswith(".mp4") else i + ".jpg")
    return b64(f, (440, 780))
def view(i):
    if i.startswith("new/"): return "https://github.com/javo-jpg/sensalabsocialmedia/blob/main/media/" + (i if i.endswith(".mp4") else i + ".jpg")
    return f"https://drive.google.com/file/d/{i}/view"
esc = html.escape
posts = sorted(d["posts"], key=lambda p: (p["date"], p["time"]))

# calendar md
md = ["# Parrilla Sensa Lab — noviembre 2026\n", "| ID | Fecha | Hora CDMX | Pieza | Formato | Pilar | Estado |", "|---|---|---|---|---|---|---|"]
for p in posts:
    md.append(f"| {p['id']} | {fmt(p['date'])} | {p['time']} | {p['title']} | {p['format']} | {p.get('pillar','')} | {p.get('status','')} |")
md.append("\n## Copies y briefs\n")
for p in posts:
    md += [f"### {p['id']} · {p['title']} ({fmt(p['date'])})", "", p["copy"], "", p.get("hashtags", "")]
    if p.get("brief"): md += ["", "**Brief:** " + p["brief"]]
    if p["media"]: md += ["", "Media: " + " ".join(view(m) for m in p["media"])]
    md.append("")
open(os.path.join(ROOT, "calendar/2026-11.md"), "w").write("\n".join(md))

STATUS = {"programado": "s-prog", "listo": "s-ok", "por producir": "s-todo"}
cards = []
for p in posts:
    imgs = "".join(f'<a href="{view(m)}" target="_blank" rel="noopener" class="{"vid" if m.endswith(".mp4") else ""}"><img loading="lazy" src="{thumb(m)}" alt="{esc(p["title"])} {n+1}"></a>' for n, m in enumerate(p["media"]))
    st = "".join(f'<a href="{view(m)}" target="_blank" rel="noopener"><img loading="lazy" class="story" src="{thumb(m)}" alt="story"></a>' for m in p.get("story", []))
    nets = "".join(f'<span class="net">{esc(n)}</span>' for n in p["networks"])
    media = f'<div class="strip">{imgs}</div>' if imgs else f'<div class="brief"><b>Por producir.</b> {esc(p.get("brief",""))}</div>'
    stories = f'<div class="lbl">Stories</div><div class="strip">{st}</div>' if st else ""
    note = f'<p class="note">{esc(p["note"])}</p>' if p.get("note") else ""
    s = p.get("status", "")
    cards.append(f'''<article class="card" data-id="{p['id']}" data-pillar="{esc(p.get('pillar',''))}">
<header><span class="num">{p['id']}</span><div><div class="date">{fmt(p['date'])} · {p['time']} CDMX</div><h2>{esc(p['title'])}</h2></div><span class="badge {STATUS.get(s,'')}">{esc(s)}</span></header>
<div class="meta"><span class="fmt">{esc(p['format'])}</span><span class="pil">{esc(p.get('pillar',''))}</span>{nets}</div>
{media}{stories}
<pre class="copy">{esc(p['copy'])}</pre><p class="tags">{esc(p.get('hashtags',''))}</p>{note}
<div class="actions"><button class="ok" data-v="ok">Aprobar</button><button class="ch" data-v="ch">Cambios</button><input placeholder="Nota (opcional)"></div>
</article>''')
hl = "".join(f'<figure><img src="{b64(os.path.join(ROOT,"media/highlights",n.replace(" ","")+".jpg"),(240,420))}" alt="{esc(n)}"><figcaption><b>{esc(n)}</b><span>{esc(t)}</span></figcaption></figure>' for n, t in d["highlights"])
stories_plan = "".join(f"<li>{esc(s)}</li>" for s in d["stories"])
back = "".join(f'<li>{esc(b["title"])} · ' + " ".join(f'<a href="{view(m)}" target="_blank" rel="noopener">ver</a>' for m in b["media"]) + '</li>' for b in d["backlog"])
pillars = sorted({p.get("pillar","") for p in posts})
filters = '<button class="f on" data-p="">Todos</button>' + "".join(f'<button class="f" data-p="{esc(x)}">{esc(x)}</button>' for x in pillars)
tpl = open(os.path.join(ROOT, "scripts/template.html")).read()
out = (tpl.replace("{{CARDS}}", "\n".join(cards)).replace("{{BACKLOG}}", back).replace("{{N}}", str(len(posts)))
       .replace("{{READY}}", str(sum(1 for p in posts if p["media"]))).replace("{{TODO}}", str(sum(1 for p in posts if not p["media"])))
       .replace("{{HIGHLIGHTS}}", hl).replace("{{STORIES}}", stories_plan).replace("{{FILTERS}}", filters))
os.makedirs(os.path.join(ROOT, "preview"), exist_ok=True)
open(os.path.join(ROOT, "preview/index.html"), "w").write(out)
print("ok", len(posts))
