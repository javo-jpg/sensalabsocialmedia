# Sensa Lab — Social Media

Centro de operación de las redes de Sensa Lab (Instagram `@sensa.lab`, Facebook, LinkedIn) vía Metricool (brand id `7566765`).

## Estructura
- `data/posts.json` — fuente única de la parrilla (fechas, copies, media en Drive, redes, estado).
- `calendar/` — parrilla legible por mes (se genera desde el JSON).
- `brand/voice.md` — tono y reglas de copy.
- `brand/strategy.md` — estrategia, pilares, cadencia, perfil y highlights.
- `media/highlights/` — portadas de highlights de IG.
- `scripts/build.py` — genera `calendar/*.md` y `preview/index.html` desde el JSON.
- `preview/` — página de revisión para aprobar contenido.

## Flujo
1. Editar `data/posts.json`.
2. `python3 scripts/build.py`.
3. Revisión/aprobación (Javier / Jon) en la preview.
4. Programar aprobados en Metricool (IG + FB + LinkedIn). Horario base: L/M/V 11:00 CDMX (9:00 LA).

## Origen
Material diseñado por Audrey (Sheet "PARRILLA SENSA LAB", pestañas *Sin publicar IG* / *Sin publicar LinkedIn*), reordenado y con copies reescritos en oct 2026.
