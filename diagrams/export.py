"""Exporta diagrams/out/*.drawio a SVG para la web y deja los íconos dentro del archivo.

El CLI de draw.io escribe los íconos de Azure como rutas file:// de su propia
instalación; aquí se reemplazan por data URIs leídos de diagrams/icons/azure2.

    python3 diagrams/export.py              # todos
    python3 diagrams/export.py red png      # uno, también en PNG para revisarlo
"""
import base64
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / 'out'
DEST = HERE.parent / 'public' / 'img' / 'diagrams'
CLI = ['flatpak', 'run', 'com.jgraph.drawio.desktop', '--disable-gpu', '-x']


def export(name, fmt='svg'):
    src = OUT / f'{name}.drawio'
    dst = OUT / f'{name}.{fmt}'
    args = CLI + ['-f', fmt, '-b', '16', '-o', str(dst), str(src)]
    if fmt == 'png':
        args[5:5] = ['-s', '1.5']
    subprocess.run(args, check=True, capture_output=True, timeout=180)
    return dst


def inline(svg_path):
    text = svg_path.read_text()

    def swap(m):
        rel = m.group(1)
        f = HERE / 'icons' / rel
        data = base64.b64encode(f.read_bytes()).decode()
        return f'xlink:href="data:image/svg+xml;base64,{data}"'

    text, n = re.subn(r'xlink:href="file:///[^"]*?/img/lib/(azure2/[^"]+\.svg)"', swap, text)
    # draw.io agrega una imagen PNG de respaldo por cada etiqueta HTML; el navegador usa el texto
    text = re.sub(r'(</foreignObject>)<image [^>]*?xlink:href="data:image/png;base64,[^"]*"[^>]*?/>', r'\1', text)
    # colores adaptables al modo oscuro: la página es clara, se fija el color claro
    text = re.sub(r'light-dark\(\s*((?:[^(),]|\([^()]*\))+?)\s*,\s*(?:[^()]|\([^()]*\))+\)', r'\1', text)
    text = text.replace('color-scheme: light dark;', 'color-scheme: light;')
    left = re.findall(r'xlink:href="file:[^"]*"', text)
    if left:
        raise SystemExit(f'{svg_path.name}: unresolved images {left[:3]}')
    DEST.mkdir(parents=True, exist_ok=True)
    (DEST / svg_path.name).write_text(text)
    return n


def main():
    names = [sys.argv[1]] if len(sys.argv) > 1 else sorted(p.stem for p in OUT.glob('*.drawio'))
    fmt = sys.argv[2] if len(sys.argv) > 2 else 'svg'
    for name in names:
        dst = export(name, fmt)
        if fmt == 'svg':
            print(name, 'icons inlined:', inline(dst), f'{(DEST / dst.name).stat().st_size // 1024} KB')
        else:
            print(name, '->', dst)


if __name__ == '__main__':
    main()
