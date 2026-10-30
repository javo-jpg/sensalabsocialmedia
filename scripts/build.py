import json, html, os, datetime
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d = json.load(open(os.path.join(ROOT, "data/posts.json")))
DAYS = ["Lun","Mar","Mié","Jue","Vie","Sáb","Dom"]
def fmt(ds):
    dt = datetime.date.fromisoformat(ds); return f"{DAYS[dt.weekday()]} {dt.day} {['','ene','feb','mar','abr','may','jun','jul','ago','sep','oct','nov','dic'][dt.month]}"
def thumb(i): return f"https://drive.google.com/thumbnail?id={i}&sz=w800"
def view(i): return f"https://drive.google.com/file/d/{i}/view"
# calendar md
os.makedirs(os.path.join(ROOT,"calendar"), exist_ok=True)
md = ["# Parrilla Sensa Lab — 30 oct a 27 nov 2026\n", "| # | Fecha | Hora CDMX | Pieza | Formato | Redes |","|---|---|---|---|---|---|"]
for p in d["posts"]:
    md.append(f"| {p['id']} | {fmt(p['date'])} | {p['time']} | {p['title']} | {p['format']} | {', '.join(p['networks'])} |")
md.append("\n## Copies\n")
for p in d["posts"]:
    md += [f"### {p['id']} · {p['title']} ({fmt(p['date'])})", "", p["copy"], "", p["hashtags"], "", "Media: " + " ".join(view(m) for m in p["media"]), ""]
open(os.path.join(ROOT,"calendar/2026-11.md"),"w").write("\n".join(md))
# preview html
cards=[]
for p in d["posts"]:
    imgs = "".join(f'<a href="{view(m)}" target="_blank" rel="noopener"><img loading="lazy" src="{thumb(m)}" alt="{html.escape(p["title"])} {n+1}"></a>' for n,m in enumerate(p["media"]))
    st = "".join(f'<a href="{view(m)}" target="_blank" rel="noopener"><img loading="lazy" class="story" src="{thumb(m)}" alt="story"></a>' for m in p.get("story",[]))
    nets = "".join(f'<span class="net">{n}</span>' for n in p["networks"])
    note = f'<p class="note">{html.escape(p["note"])}</p>' if p.get("note") else ""
    stories = f'<div class="lbl">Stories</div><div class="strip">{st}</div>' if st else ""
    cards.append(f'''<article class="card" data-id="{p['id']}">
<header><span class="num">{p['id']}</span><div><div class="date">{fmt(p['date'])} · {p['time']} CDMX</div><h2>{html.escape(p['title'])}</h2></div></header>
<div class="meta"><span class="fmt">{html.escape(p['format'])}</span>{nets}</div>
<div class="strip">{imgs}</div>{stories}
<pre class="copy">{html.escape(p['copy'])}</pre><p class="tags">{html.escape(p['hashtags'])}</p>{note}
<div class="actions"><button class="ok" data-v="ok">Aprobar</button><button class="ch" data-v="ch">Cambios</button><input placeholder="Nota (opcional)"></div>
</article>''')
back = "".join(f'<li>{html.escape(b["title"])} · ' + " ".join(f'<a href="{view(m)}" target="_blank" rel="noopener">ver</a>' for m in b["media"]) + '</li>' for b in d["backlog"])
tpl = open(os.path.join(ROOT,"scripts/template.html")).read()
os.makedirs(os.path.join(ROOT,"preview"), exist_ok=True)
open(os.path.join(ROOT,"preview/index.html"),"w").write(tpl.replace("{{CARDS}}","\n".join(cards)).replace("{{BACKLOG}}",back).replace("{{N}}",str(len(d["posts"]))))
print("ok")
