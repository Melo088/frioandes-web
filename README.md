# FríoAndes, la plataforma

Sitio local de presentación. Vite + GSAP (ScrollTrigger) + Lenis.

    npm install
    npm run dev       # http://localhost:5173
    npm run build     # genera dist/
    node scripts/images.mjs   # regenera los diagramas en WebP desde el repo planning

Tipografías (Fontsource, locales): Schibsted Grotesk para todo el texto y Newsreader en cursiva para las palabras resaltadas.
Marca: logo, paleta y estados tomados de `planning/docs/design/brand`.

## Diagramas

Los diagramas de la web están en inglés y se publican como SVG en `public/img/diagrams/`.

    python3 diagrams/translate.py   # copia en inglés de firewall, telemetría, observabilidad, Fabric y migración (fuentes en diagrams/src)
    python3 diagrams/build.py       # gobierno, seguridad, plataforma y red, dibujados de nuevo
    python3 diagrams/export.py      # exporta con draw.io (flatpak) e incrusta los íconos de diagrams/icons
