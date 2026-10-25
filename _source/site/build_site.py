"""Generates the Spanish page and the SEO files from index.html.

Run from the repo root after any change to index.html:
    python3 _source/site/build_site.py

What it does:
  1. Sets the site address (SITE) everywhere in index.html (canonical, hreflang, og:*, JSON-LD).
  2. Writes es/index.html: the same page with a Spanish <head>, a Spanish no-JavaScript
     version and asset paths pointing one folder up. The page itself opens in Spanish
     because of data-page-lang="es" (a visitor's manual EN/ES choice still wins).
  3. Writes sitemap.xml (both languages, with hreflang) and robots.txt.

To move to your own domain, change SITE below and run the script again.
"""
import re
from datetime import date
from pathlib import Path

SITE = "https://portfolio-six-flax-48.vercel.app"  # no trailing slash

ROOT = Path(__file__).resolve().parents[2]

ES_HEAD = {
    "title": "Santiago Lopez Viñao — Programador en formación",
    "description": "Portfolio de Santiago Lopez Viñao, programador en formación en Barcelona. Proyectos, trayectoria y buzón de ideas.",
    "og_title": "Santiago Lopez Viñao — Programador en formación",
    "og_description": "Programador en formación en Barcelona: estudio Desarrollo de Aplicaciones Multiplataforma y Web (DAM/DAW). Disponible para trabajar.",
    "job_title": "Programador en formación",
}

ES_NOSCRIPT = """<noscript>
<main style="max-width:720px;margin:0 auto;padding:48px 20px;font-family:Inter,system-ui,sans-serif;color:#f5f5f7;line-height:1.5">
<h1>Santiago Lopez Viñao</h1>
<p>Programador en formación · Barcelona, España · Disponible para trabajar</p>
<h2>Sobre mí</h2>
<p>La curiosidad me define. Soy versátil y he aprendido a adaptarme a cada giro que han dado la vida y el trabajo. Busco crecer, y no solo en tecnología. Con experiencia en atención al cliente, creación de contenido y liderazgo de equipos pequeños, me mueve la mejora continua. Sobre todo, quiero dejar huella y saber que lo que hago ayuda a alguien.</p>
<h2>Proyectos</h2>
<ul>
<li><strong><a href="https://aquaterra-beta.vercel.app" style="color:#f5f5f7">Aquaterra</a></strong> — Web inmobiliaria para invertir en Paraguay desde España: proyectos, comparador, chat con IA y panel de leads (JavaScript, Supabase, Vercel).</li>
<li><strong><a href="https://finanzas-personales-eight-lac.vercel.app" style="color:#f5f5f7">Mis Cuentas</a></strong> — App de finanzas personales con demo pública: importa extractos del banco, clasifica gastos y planifica el ahorro mensual (React, TypeScript, Supabase).</li>
</ul>
<h2>Experiencia y formación</h2>
<ul>
<li><strong>Estudiante de DAM/DAW</strong> — Universae, Barcelona (Ahora — 2028). Desarrollo de Aplicaciones Multiplataforma y Web.</li>
<li><strong>Front Office Agent</strong> — ME Sitges Terramar, Barcelona (2026 — Actualidad)</li>
<li><strong>Camarero &amp; Guest Experience Trainee</strong> — ME Sitges Terramar, Barcelona (2025 — 2026)</li>
<li><strong>Encargado</strong> — Happy Park, Mallorca (2024 — 2025)</li>
<li><strong>Encargado de bar</strong> — Three Monkeys Bar, Buenos Aires (2022 — 2023)</li>
<li><strong>Administrativo</strong> — ByC Gastronomía, Buenos Aires (2021 — 2022)</li>
</ul>
<h2>Contacto</h2>
<p><a href="mailto:lopezvinaoes@gmail.com" style="color:#f5f5f7">lopezvinaoes@gmail.com</a> · <a href="https://www.linkedin.com/in/santiago-lopez-vi%C3%B1ao/" style="color:#f5f5f7">LinkedIn</a> · <a href="https://github.com/lopezvinaoes-tech" style="color:#f5f5f7">GitHub</a> · CV: <a href="../assets/cv/Santiago-Lopez-CV-ES.pdf" style="color:#f5f5f7">Español</a> / <a href="../assets/cv/Santiago-Lopez-CV-EN.pdf" style="color:#f5f5f7">English</a></p>
</main>
</noscript>"""


def sub_once(pattern, repl, text, flags=0):
    new, n = re.subn(pattern, repl, text, count=1, flags=flags)
    if n != 1:
        raise SystemExit(f"build_site: pattern not found: {pattern}")
    return new


def set_site(html):
    m = re.search(r'<link rel="canonical" href="(https?://[^"/]+)/">', html)
    if not m:
        raise SystemExit("build_site: canonical link not found in index.html")
    return html.replace(m.group(1), SITE)


def attr_escape(s):
    return s.replace("&", "&amp;").replace('"', "&quot;")


def spanish(html):
    h = html
    h = sub_once(r'<html lang="en" data-page-lang="en" translate="no">', '<html lang="es" data-page-lang="es" translate="no">', h)
    h = sub_once(r"<title>[^<]*</title>", f"<title>{ES_HEAD['title']}</title>", h)
    h = sub_once(r'<meta name="description" content="[^"]*">',
                 f'<meta name="description" content="{attr_escape(ES_HEAD["description"])}">', h)
    h = sub_once(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{SITE}/es/">', h)
    h = sub_once(r'<meta property="og:locale" content="en_GB">', '<meta property="og:locale" content="es_ES">', h)
    h = sub_once(r'<meta property="og:locale:alternate" content="es_ES">',
                 '<meta property="og:locale:alternate" content="en_GB">', h)
    h = sub_once(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{SITE}/es/">', h)
    h = sub_once(r'<meta property="og:title" content="[^"]*">',
                 f'<meta property="og:title" content="{attr_escape(ES_HEAD["og_title"])}">', h)
    h = sub_once(r'<meta property="og:description" content="[^"]*">',
                 f'<meta property="og:description" content="{attr_escape(ES_HEAD["og_description"])}">', h)
    h = sub_once(r'<meta property="og:image" content="[^"]*">',
                 f'<meta property="og:image" content="{SITE}/assets/og-es.jpg">', h)
    # JSON-LD
    h = sub_once(r'"jobTitle":"[^"]*"', f'"jobTitle":"{ES_HEAD["job_title"]}"', h)
    h = sub_once(r'("@type":"Person".*?"url":")[^"]*(")', rf"\g<1>{SITE}/es/\g<2>", h, flags=re.S)
    h = sub_once(r'("@type":"Person".*?"image":")[^"]*(")', rf"\g<1>{SITE}/assets/og-es.jpg\g<2>", h, flags=re.S)
    # No-JavaScript version
    h = sub_once(r"<noscript>.*?</noscript>", lambda _: ES_NOSCRIPT, h, flags=re.S)
    # Relative paths: this page lives one folder down
    h = re.sub(r'(?<![\w/.:-])(assets/|support\.js)', r"../\1", h)
    return h


def sitemap():
    today = date.today().isoformat()
    alts = (f'    <xhtml:link rel="alternate" hreflang="en" href="{SITE}/"/>\n'
            f'    <xhtml:link rel="alternate" hreflang="es" href="{SITE}/es/"/>\n'
            f'    <xhtml:link rel="alternate" hreflang="x-default" href="{SITE}/"/>\n')
    urls = "".join(f"  <url>\n    <loc>{SITE}{p}</loc>\n    <lastmod>{today}</lastmod>\n{alts}  </url>\n"
                   for p in ("/", "/es/"))
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
            'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + urls + "</urlset>\n")


def main():
    index = ROOT / "index.html"
    html = set_site(index.read_text(encoding="utf-8"))
    index.write_text(html, encoding="utf-8")

    es_dir = ROOT / "es"
    es_dir.mkdir(exist_ok=True)
    (es_dir / "index.html").write_text(spanish(html), encoding="utf-8")

    (ROOT / "sitemap.xml").write_text(sitemap(), encoding="utf-8")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")
    print("built: index.html (site address), es/index.html, sitemap.xml, robots.txt")


if __name__ == "__main__":
    main()
