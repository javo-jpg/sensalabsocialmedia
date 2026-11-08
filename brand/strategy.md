# Estrategia de redes Sensa Lab — noviembre 2026

## Objetivo
Posicionar a Sensa Lab como **el lab de tech experiencial con base en LA** al que las agencias y las marcas llaman para la capa interactiva, y generar conversaciones de venta (DMs, llamadas) con agencias en EE. UU. Las redes son una fan page de tech, IA y experiencias interactivas, y venden 3 productos concretos: Mirror, Arcade y Playboard.

## Lo que dicen los datos (2025–2026)
- **Instagram:** los carruseles tienen el engagement más alto (~0.50–0.55%) y más vistas en todos los tamaños de cuenta; los Reels generan más comentarios; las imágenes sueltas son lo más débil (~0.35–0.37%) y van a la baja. Las marcas suben a ~8 Reels y 5 carruseles al mes. (Socialinsider)
- **LinkedIn:** los documentos nativos (carruseles en PDF) lideran el engagement (~7%); las encuestas ganan impresiones; las vistas de video bajaron. (Socialinsider)
- **LA 2028:** el CEO de USOPP espera ~10x más activaciones de marca que en Milano Cortina 2026, y las marcas están armando su plan después del Mundial. (Adweek) Las marcas que no son patrocinadoras no pueden usar marcas del COI (aros, etc.). (BizBash)

## Implicaciones
1. Menos posts de imagen suelta; más **carruseles** (guardables) y **Reels** (alcance + comentarios).
2. En LinkedIn, todos los carruseles se suben como **documento PDF**.
3. **Perfiles personales de Jon y Javier** en LinkedIn: es donde está el alcance en B2B; la página de la empresa amplifica.
4. Contenido **propio y real** (BTS, demos) por encima de lo genérico: es lo que diferencia un lab de una agencia más.
5. **LA 2028** como serie fija mensual, sin usar marcas olímpicas.

## Pilares
| Pilar | Qué es | Formato | % |
|---|---|---|---|
| Lab / BTS | Pruebas, montajes, proyecciones, oficina | Reels, stories | 25% |
| Experiencias | Sensa Mirror, Arcade, Playboard | Carrusel + Reel demo | 25% |
| Fan page / insights | Breakdowns de activaciones top, tendencias de IA | Carruseles (material de Audrey) | 30% |
| LA 2028 | Serie "Road to LA 2028" | Carrusel / Documento | 10% |
| Agencias | White label, cómo trabajamos | Post + highlight | 10% |

## Cadencia
- **Feed IG/FB:** L/Mi/V carrusel o post + Ma/Ju Reel (cuando haya footage).
- **LinkedIn página:** mismos días; carruseles como PDF; 1 encuesta al mes.
- **LinkedIn personal:** Jon 1/semana, Javier 1/semana; el otro comenta en la primera hora.
- **Stories:** diarias, con encuestas/quiz los lunes; todo se archiva en highlights.

## Perfil
- **Bio IG (propuesta):** "Creative tech lab · Los Angeles / AI mirrors, arcade games & interactive booths for brands + agencies / Book a demo ↓"
- **Highlights:** LAB · MIRROR · ARCADE · PLAYBOARD · AGENCIES · LA 2028 · CONTACT (portadas en `media/highlights/`).
- Fijar los 3 posts: relanzamiento, Sensa Mirror y White label.

## Métricas a revisar cada lunes en la junta
Alcance, guardados y compartidos por post, DMs recibidos, visitas a la web desde las redes, seguidores de agencias en LinkedIn.

## Producción sin footage
Todo se genera desde el sistema visual de Audrey: `scripts/render_slides.py` (carruseles y tarjetas 1080x1350) y `scripts/render_reels.py` (reels 1080x1920, sin audio; el audio se elige de la librería nativa de IG al publicar). Pendiente: corregir el título del slide 7 de "Top AI booths".

Fuentes: Socialinsider Instagram Benchmarks 2026; Socialinsider LinkedIn Engagement Benchmarks 2026; Adweek, "After World Cup, Brands Look to LA28"; BizBash, "Los Angeles Olympics: What Event Producers Need to Know".
