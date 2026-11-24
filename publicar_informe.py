#!/usr/bin/env python3
"""Publica un informe Markdown en informes/ y actualiza automáticamente README.md + git push."""
from __future__ import annotations

import datetime
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent
DIR_INF = REPO / 'informes'


def slugify(txt: str) -> str:
    s = re.sub(r'[^a-zA-Z0-9_-]+', '_', txt.strip().lower()).strip('_')
    return (s or 'informe')[:60]


def extraer_titulo(md: str, fallback: str) -> str:
    for line in md.splitlines():
        l = line.strip()
        if l.startswith('#'):
            return l.lstrip('#').strip()
    return fallback


def publicar(slug: str, contenido_md: str, commit_msg: str | None = None) -> Path:
    DIR_INF.mkdir(parents=True, exist_ok=True)
    ahora = datetime.datetime.now(datetime.timezone.utc)
    ts = ahora.strftime('%Y-%m-%d_%H%M')
    fecha_hum = ahora.strftime('%Y-%m-%d %H:%M UTC')
    fname = f'{ts}_{slugify(slug)}.md'
    destino = DIR_INF / fname

    cuerpo = contenido_md.strip() + '\n'
    destino.write_text(cuerpo, encoding='utf-8')

    # Construir índice cronológico inverso de todos los informes
    archivos = sorted(DIR_INF.glob('*.md'), reverse=True)
    lineas_idx = []
    for p in archivos:
        tit = extraer_titulo(p.read_text(encoding='utf-8'), p.stem)
        lineas_idx.append(f'- [`{p.name}`](informes/{p.name}) — {tit}')

    readme = (
        f'<!-- AUTO-ACTUALIZADO: último informe publicado el {fecha_hum} -->\n'
        f'> **Último informe:** [`informes/{fname}`](informes/{fname}) · *Actualizado: {fecha_hum}*\n\n'
        f'{cuerpo}\n'
        f'---\n\n'
        f'## Historial de informes\n\n'
        + '\n'.join(lineas_idx)
        + '\n'
    )
    (REPO / 'README.md').write_text(readme, encoding='utf-8')

    msg = commit_msg or f'informe: {fname}'
    subprocess.run(['git', '-C', str(REPO), 'add', 'README.md', f'informes/{fname}', 'publicar_informe.py'], check=True)
    subprocess.run(['git', '-C', str(REPO), 'commit', '-m', msg], check=True)
    subprocess.run(['git', '-C', str(REPO), 'push', '-u', 'origin', 'main'], check=True)
    print(f'PUBLICADO_OK: informes/{fname}')
    return destino


def main() -> int:
    if len(sys.argv) < 2:
        print('Uso: publicar_informe.py <slug> [ruta_md_o_stdin]', file=sys.stderr)
        return 2
    slug = sys.argv[1]
    if len(sys.argv) >= 3 and sys.argv[2] != '-':
        contenido = Path(sys.argv[2]).read_text(encoding='utf-8')
    else:
        contenido = sys.stdin.read()
    if not contenido.strip():
        print('Error: contenido vacío', file=sys.stderr)
        return 1
    publicar(slug, contenido)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
